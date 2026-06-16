# Database Design
## AI Resume Analyzer

**Version:** 1.0  
**Database:** PostgreSQL 16  
**ORM:** SQLAlchemy 2.0 (async)

---

## 1. Design Principles

- **Simpel dulu:** Hanya tabel yang benar-benar dibutuhkan v1
- **UUID sebagai primary key:** Aman diekspos ke URL/API, tidak enumerable
- **Soft delete:** Pakai `deleted_at` timestamp, data tidak hilang permanen
- **Timestamp standar:** Semua tabel punya `created_at` dan `updated_at`
- **Tidak ada foreign key kompleks:** Cukup relasi user → analysis

---

## 2. Entity Relationship Diagram

```
┌─────────────────────────┐          ┌──────────────────────────────────┐
│         users           │          │            analyses               │
├─────────────────────────┤          ├──────────────────────────────────┤
│ id (PK, UUID)           │◄────┐    │ id (PK, UUID)                    │
│ email (UNIQUE)          │     └────│ user_id (FK → users.id)          │
│ hashed_password         │          │ label                            │
│ is_active               │          │ resume_text (TEXT)               │
│ created_at              │          │ job_description (TEXT)           │
│ updated_at              │          │ match_score (INTEGER)            │
│ deleted_at              │          │ result_json (JSONB)              │
└─────────────────────────┘          │ created_at                       │
                                     │ updated_at                       │
                                     │ deleted_at                       │
                                     └──────────────────────────────────┘

┌─────────────────────────────────────┐
│         password_reset_tokens        │
├─────────────────────────────────────┤
│ id (PK, UUID)                       │
│ user_id (FK → users.id)             │
│ token (UNIQUE)                      │
│ expires_at                          │
│ used_at                             │
│ created_at                          │
└─────────────────────────────────────┘
```

---

## 3. Table Definitions (SQL)

### 3.1 users

```sql
CREATE TABLE users (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email           VARCHAR(255) NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    is_active       BOOLEAN NOT NULL DEFAULT TRUE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at      TIMESTAMPTZ
);

-- Index untuk login lookup
CREATE INDEX idx_users_email ON users(email) WHERE deleted_at IS NULL;
```

**Keterangan kolom:**
| Kolom | Type | Keterangan |
|---|---|---|
| id | UUID | Primary key, auto-generated |
| email | VARCHAR(255) | Login identifier, harus unik |
| hashed_password | VARCHAR(255) | bcrypt hash, bukan plain text |
| is_active | BOOLEAN | False = akun dinonaktifkan admin |
| deleted_at | TIMESTAMPTZ | NULL = aktif; diisi = soft deleted |

---

### 3.2 analyses

```sql
CREATE TABLE analyses (
    id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id          UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    label            VARCHAR(255),
    resume_text      TEXT NOT NULL,
    job_description  TEXT NOT NULL,
    match_score      INTEGER CHECK (match_score BETWEEN 0 AND 100),
    result_json      JSONB NOT NULL DEFAULT '{}',
    created_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at       TIMESTAMPTZ
);

-- Index untuk list analisis user (query paling sering)
CREATE INDEX idx_analyses_user_id 
    ON analyses(user_id, created_at DESC) 
    WHERE deleted_at IS NULL;

-- Index untuk search di result_json (opsional, tambah jika diperlukan)
-- CREATE INDEX idx_analyses_result_gin ON analyses USING gin(result_json);
```

**Keterangan kolom:**
| Kolom | Type | Keterangan |
|---|---|---|
| user_id | UUID | FK ke users, CASCADE delete |
| label | VARCHAR(255) | Nama custom dari user; nullable, default di app layer |
| resume_text | TEXT | Teks hasil parse dari PDF/DOCX |
| job_description | TEXT | Input JD dari user |
| match_score | INTEGER | 0–100, disimpan terpisah untuk query/filter mudah |
| result_json | JSONB | Full AI response (strengths, weaknesses, suggestions, dll) |
| deleted_at | TIMESTAMPTZ | Soft delete |

**Contoh `result_json`:**
```json
{
  "summary": "Resume kamu cukup relevan untuk posisi Backend Engineer...",
  "strengths": [
    "Pengalaman Python 3+ tahun sesuai requirement",
    "Familiar dengan REST API design"
  ],
  "weaknesses": [
    "Tidak ada pengalaman Docker/containerization",
    "Tidak menyebut pengalaman dengan cloud provider"
  ],
  "suggestions": [
    "Tambahkan proyek yang menggunakan Docker di section projects",
    "Sebutkan pengalaman deploy ke AWS/GCP jika ada"
  ],
  "keyword_analysis": {
    "matched": ["Python", "FastAPI", "PostgreSQL", "REST API"],
    "missing": ["Docker", "Kubernetes", "AWS", "Redis"]
  }
}
```

---

### 3.3 password_reset_tokens

```sql
CREATE TABLE password_reset_tokens (
    id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id    UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token      VARCHAR(255) NOT NULL UNIQUE,
    expires_at TIMESTAMPTZ NOT NULL,
    used_at    TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Index untuk lookup token saat reset password
CREATE INDEX idx_password_reset_tokens_token ON password_reset_tokens(token);

-- Cleanup tokens lama (jalankan via cron job atau scheduled task)
-- DELETE FROM password_reset_tokens WHERE expires_at < NOW() - INTERVAL '7 days';
```

**Keterangan kolom:**
| Kolom | Type | Keterangan |
|---|---|---|
| token | VARCHAR(255) | Random secure token (secrets.token_urlsafe(32)) |
| expires_at | TIMESTAMPTZ | 1 jam setelah dibuat |
| used_at | TIMESTAMPTZ | NULL = belum dipakai; diisi = sudah terpakai |

---

## 4. SQLAlchemy Models (Python)

### Base Model
```python
# app/models/base.py
import uuid
from datetime import datetime, timezone
from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

class Base(DeclarativeBase):
    pass

class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        onupdate=func.now(), 
        nullable=False
    )
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), 
        nullable=True
    )
```

### User Model
```python
# app/models/user.py
from sqlalchemy import String, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    analyses: Mapped[list["Analysis"]] = relationship(back_populates="user")
    reset_tokens: Mapped[list["PasswordResetToken"]] = relationship(back_populates="user")
```

### Analysis Model
```python
# app/models/analysis.py
from sqlalchemy import String, Text, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid

class Analysis(Base, TimestampMixin):
    __tablename__ = "analyses"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    label: Mapped[str | None] = mapped_column(String(255), nullable=True)
    resume_text: Mapped[str] = mapped_column(Text, nullable=False)
    job_description: Mapped[str] = mapped_column(Text, nullable=False)
    match_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    result_json: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)

    # Relationships
    user: Mapped["User"] = relationship(back_populates="analyses")
```

### Password Reset Token Model
```python
# app/models/password_reset_token.py
from sqlalchemy import String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid

class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    token: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    used_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    user: Mapped["User"] = relationship(back_populates="reset_tokens")
```

---

## 5. Common Queries

### List analisis user dengan pagination
```python
# app/services/analysis_service.py
async def get_user_analyses(
    db: AsyncSession, 
    user_id: UUID, 
    page: int = 1, 
    per_page: int = 10
) -> tuple[list[Analysis], int]:
    offset = (page - 1) * per_page
    
    # Count total
    count_result = await db.execute(
        select(func.count(Analysis.id))
        .where(Analysis.user_id == user_id, Analysis.deleted_at.is_(None))
    )
    total = count_result.scalar()
    
    # Fetch items
    result = await db.execute(
        select(Analysis)
        .where(Analysis.user_id == user_id, Analysis.deleted_at.is_(None))
        .order_by(Analysis.created_at.desc())
        .offset(offset).limit(per_page)
    )
    return result.scalars().all(), total
```

### Soft delete analisis
```python
async def soft_delete_analysis(
    db: AsyncSession, 
    analysis_id: UUID, 
    user_id: UUID
) -> bool:
    result = await db.execute(
        update(Analysis)
        .where(
            Analysis.id == analysis_id,
            Analysis.user_id == user_id,    # pastikan milik user ini
            Analysis.deleted_at.is_(None)
        )
        .values(deleted_at=datetime.now(timezone.utc))
        .returning(Analysis.id)
    )
    await db.commit()
    return result.fetchone() is not None
```

---

## 6. Migrations (Alembic)

```bash
# Setup
alembic init alembic

# Buat migration pertama
alembic revision --autogenerate -m "initial_schema"

# Apply migration
alembic upgrade head

# Rollback 1 step
alembic downgrade -1
```

**Urutan migration v1.0:**
1. `001_create_users_table.py`
2. `002_create_analyses_table.py`
3. `003_create_password_reset_tokens_table.py`

---

## 7. Database Configuration

### Connection Pool (async)
```python
# app/database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    pool_size=5,          # Cukup untuk solo dev / low traffic
    max_overflow=10,
    pool_pre_ping=True,   # Cek koneksi sebelum dipakai (penting untuk managed DB)
    echo=False,           # Set True untuk debug SQL
)

AsyncSessionLocal = async_sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
```

---

## 8. Data Retention & Privacy

| Data | Retensi | Alasan |
|---|---|---|
| User account | Selamanya (sampai user hapus akun) | Needed for service |
| Resume text | Ikut analisis; hapus jika analisis dihapus | Minimal retention |
| Job description | Ikut analisis | Minimal retention |
| AI result | Ikut analisis | User butuh lihat history |
| Password reset token | Hapus setelah 7 hari | Security hygiene |

**Catatan privasi:** Resume text disimpan di DB (bukan file storage), tidak ada pihak ketiga yang mengaksesnya selain OpenAI saat proses analisis. Ini harus dicantumkan di Privacy Policy.

---

## 9. Indexing Strategy

```sql
-- Indexes yang ada (sudah dibuat di section 3):
-- 1. users.email             → untuk login lookup
-- 2. analyses.user_id + created_at → untuk list analisis (query paling sering)
-- 3. password_reset_tokens.token   → untuk reset password lookup

-- Tambah jika dibutuhkan nanti:
-- Full-text search di label analisis:
-- CREATE INDEX idx_analyses_label_fts ON analyses 
--     USING gin(to_tsvector('english', COALESCE(label, '')));
```

**Prinsip:** Jangan tambah index sebelum ada query yang nyata-nyata lambat. Index berlebihan memperlambat write.
