# System Design
## AI Resume Analyzer

**Version:** 1.0  
**Date:** Juni 2026  
**Prinsip:** Low-cost, Maintainable, No Over-engineering (Solo Dev)

---

## 1. Architecture Overview

```
┌─────────────────────────────────────────────┐
│                   CLIENT                    │
│           Nuxt 3 + TypeScript               │
│              (SSR/SPA Hybrid)               │
│           Tailwind CSS + shadcn-vue         │
└─────────────────┬───────────────────────────┘
                  │ HTTPS (REST API)
┌─────────────────▼───────────────────────────┐
│                  BACKEND                    │
│             Python FastAPI                  │
│         (Single Process, Uvicorn)           │
│                                             │
│  ┌─────────────┐   ┌──────────────────────┐ │
│  │  Auth       │   │  Analysis            │ │
│  │  Router     │   │  Router              │ │
│  └─────────────┘   └──────────────────────┘ │
│  ┌─────────────────────────────────────────┐ │
│  │           Service Layer                 │ │
│  │  auth_service / analysis_service /      │ │
│  │  file_service / ai_service              │ │
│  └─────────────────────────────────────────┘ │
│  ┌──────────────┐  ┌──────────────────────┐  │
│  │  SQLAlchemy  │  │   OpenAI Client      │  │
│  │  (async)     │  │   (httpx)            │  │
│  └──────┬───────┘  └──────────┬───────────┘  │
└─────────┼──────────────────── ┼ ─────────────┘
          │                     │
┌─────────▼──────┐    ┌─────────▼──────────┐
│  PostgreSQL     │    │   OpenAI API       │
│  (local/managed)│    │   GPT-4o-mini      │
└────────────────┘    └────────────────────┘
```

**Pilihan arsitektur ini sengaja flat dan sederhana.** Tidak ada message queue, tidak ada microservice, tidak ada Redis. Semua bisa ditambahkan nanti jika traffic tumbuh.

---

## 2. Tech Stack

### Frontend
| Layer | Tech | Alasan |
|---|---|---|
| Framework | Nuxt 3 + Vue 3 | SSR built-in, ecosystem lengkap |
| Language | TypeScript | Type safety, maintainable |
| Styling | Tailwind CSS | Utility-first, cepat |
| UI Components | shadcn-vue | Accessible, tidak opinionated |
| HTTP Client | ofetch (built-in Nuxt) | Terintegrasi dengan Nuxt composables |
| State Management | Pinia | Simple, Vue 3 native |
| Form | VeeValidate + Zod | Validasi TypeScript-friendly |

### Backend
| Layer | Tech | Alasan |
|---|---|---|
| Framework | FastAPI | Async native, auto docs, type hints |
| Language | Python 3.12 | Ecosystem AI/ML terbaik |
| ORM | SQLAlchemy 2.0 (async) | Mature, type-safe |
| DB Driver | asyncpg | Async PostgreSQL driver |
| Validation | Pydantic v2 | Built-in di FastAPI |
| Auth | python-jose + bcrypt | JWT + password hashing |
| File Parsing | pypdf2 + python-docx | Ringan, cukup untuk teks extraction |
| AI Client | openai (official SDK) | Resmi, stable |
| Server | Uvicorn | ASGI, production-ready |

### Infrastructure (Low-cost)
| Komponen | Pilihan | Estimasi Biaya |
|---|---|---|
| App Hosting | Railway / Render (free tier) atau VPS $5/bulan | $0–$5/bulan |
| Database | Railway PostgreSQL / Supabase free tier | $0–$5/bulan |
| AI API | OpenAI GPT-4o-mini | ~$0.02/analisis |
| Domain (opsional) | Cloudflare | $10/tahun |

**Total estimasi:** < $15/bulan untuk < 100 active users.

---

## 3. Project Structure

### Backend (FastAPI)
```
backend/
├── app/
│   ├── main.py                 # Entry point, app factory
│   ├── config.py               # Settings via pydantic-settings
│   ├── database.py             # DB engine & session
│   ├── dependencies.py         # Shared FastAPI deps (get_db, get_current_user)
│   │
│   ├── models/                 # SQLAlchemy ORM models
│   │   ├── user.py
│   │   └── analysis.py
│   │
│   ├── schemas/                # Pydantic request/response schemas
│   │   ├── auth.py
│   │   └── analysis.py
│   │
│   ├── routers/                # FastAPI routers (thin layer)
│   │   ├── auth.py
│   │   └── analysis.py
│   │
│   ├── services/               # Business logic
│   │   ├── auth_service.py
│   │   ├── analysis_service.py
│   │   ├── file_service.py     # PDF/DOCX parsing
│   │   └── ai_service.py       # OpenAI integration
│   │
│   └── utils/
│       └── security.py         # JWT helpers
│
├── alembic/                    # DB migrations
│   └── versions/
├── tests/
├── .env
├── alembic.ini
└── requirements.txt
```

### Frontend (Nuxt 3)
```
frontend/
├── assets/
├── components/
│   ├── ui/                     # shadcn-vue base components
│   ├── auth/                   # LoginForm, RegisterForm
│   └── analysis/               # ScoreGauge, FeedbackCard, HistoryList
│
├── composables/
│   ├── useAuth.ts
│   └── useAnalysis.ts
│
├── pages/
│   ├── index.vue               # Landing page
│   ├── login.vue
│   ├── register.vue
│   ├── dashboard.vue           # History list
│   ├── analyze.vue             # New analysis form
│   └── analysis/[id].vue       # Detail result
│
├── stores/
│   ├── auth.ts                 # Pinia store
│   └── analysis.ts
│
├── middleware/
│   └── auth.ts                 # Route guard
│
├── server/
│   └── api/                    # Nuxt server routes (opsional, untuk proxy)
│
├── types/
│   └── index.ts                # Shared TypeScript types
│
├── nuxt.config.ts
├── tailwind.config.ts
└── tsconfig.json
```

---

## 4. API Design

Base URL: `/api/v1`

### Auth Endpoints
```
POST   /auth/register          # Register user baru
POST   /auth/login             # Login, return JWT
POST   /auth/logout            # Invalidate token
POST   /auth/forgot-password   # Kirim reset email
POST   /auth/reset-password    # Reset dengan token
GET    /auth/me                # Get current user info
```

### Analysis Endpoints
```
POST   /analysis               # Upload resume + JD → trigger AI analysis
GET    /analysis               # List semua analisis user (paginated)
GET    /analysis/{id}          # Get detail satu analisis
PATCH  /analysis/{id}          # Update label/nama
DELETE /analysis/{id}          # Soft delete
```

### Request/Response Example

**POST /analysis**
```
Content-Type: multipart/form-data

Fields:
  - resume_file: File (PDF/DOCX, max 5MB)
  - job_description: string (text)
  - label: string (optional)
```

**Response 201:**
```json
{
  "id": "uuid",
  "label": "Backend Engineer - Tokopedia",
  "match_score": 78,
  "summary": "...",
  "strengths": ["..."],
  "weaknesses": ["..."],
  "suggestions": ["..."],
  "keyword_analysis": {
    "matched": ["Python", "FastAPI"],
    "missing": ["Docker"]
  },
  "created_at": "2026-06-16T10:00:00Z"
}
```

---

## 5. Core Flows

### 5.1 Authentication Flow
```
Client                    FastAPI                    DB
  │                          │                       │
  │── POST /auth/login ──────►│                       │
  │   {email, password}       │── SELECT user ───────►│
  │                          │◄── user row ───────────│
  │                          │── verify bcrypt hash   │
  │                          │── generate JWT         │
  │◄── {access_token} ────────│                       │
  │   (set httpOnly cookie)   │                       │
```

### 5.2 Analysis Flow
```
Client               FastAPI              OpenAI API          DB
  │                     │                    │                │
  │─ POST /analysis ───►│                    │                │
  │  (file + JD)        │                    │                │
  │                     │─ parse file ───────│                │
  │                     │  (extract text)    │                │
  │                     │                    │                │
  │                     │─ POST chat/completions ────────────►│ (OpenAI)
  │                     │  (resume_text + JD + prompt)        │
  │                     │◄─ structured JSON response ─────────│
  │                     │                    │                │
  │                     │─── INSERT analysis ───────────────►│ (DB)
  │                     │                    │                │
  │◄── 201 {result} ────│                    │                │
```

### 5.3 AI Prompt Strategy
Gunakan **structured output** OpenAI untuk mendapat JSON yang reliable:

```python
# ai_service.py (simplified)
async def analyze_resume(resume_text: str, job_description: str) -> dict:
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"""
                Resume:
                {resume_text}
                
                Job Description:
                {job_description}
                
                Analyze and return JSON with: match_score, summary, 
                strengths, weaknesses, suggestions, keyword_analysis.
            """}
        ],
        max_tokens=1500,
        temperature=0.3   # Low temperature untuk output konsisten
    )
    return json.loads(response.choices[0].message.content)
```

---

## 6. Security

### Authentication
- Password di-hash dengan **bcrypt** (rounds=12)
- JWT disimpan di **httpOnly cookie** (bukan localStorage) untuk mencegah XSS
- JWT expire: 7 hari
- CSRF protection: SameSite=Strict cookie flag

### Input Validation
- File upload: validasi MIME type (tidak hanya ekstensi), max 5MB
- Job description: max 5000 karakter
- Semua input di-sanitize via Pydantic sebelum diproses

### Rate Limiting
- Endpoint `/analysis`: max 10 request/jam per user
- Endpoint `/auth/login`: max 5 attempt/menit per IP
- Implementasi: simple in-memory counter dengan `slowapi` (FastAPI middleware)

### Environment Variables
```env
DATABASE_URL=postgresql+asyncpg://...
SECRET_KEY=...         # JWT signing key
OPENAI_API_KEY=...
ALLOWED_ORIGINS=https://yourdomain.com
```

---

## 7. Error Handling

### Backend
Gunakan custom exception handler di FastAPI:

```python
# Konsisten untuk semua error
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "File size exceeds 5MB limit",
    "details": {}
  }
}
```

| HTTP Status | Situasi |
|---|---|
| 400 | Validasi input gagal |
| 401 | Token tidak ada / expired |
| 403 | Akses resource milik user lain |
| 404 | Resource tidak ditemukan |
| 422 | Pydantic validation error |
| 429 | Rate limit exceeded |
| 500 | Unexpected server error |
| 503 | OpenAI API tidak tersedia |

### Frontend
- Global error handler di Nuxt plugin
- Toast notification untuk error yang perlu user action
- Retry button untuk network/AI timeout errors

---

## 8. Testing Strategy (Solo Dev Pragmatic)

**Prinsip: Test yang penting, skip yang trivial.**

### Backend (pytest + pytest-asyncio)
- **Unit test:** `ai_service.py` (mock OpenAI), `file_service.py`
- **Integration test:** Semua endpoint API (pakai `httpx.AsyncClient`)
- **Skip:** Model layer, schema validation (sudah Pydantic)

### Frontend (Vitest + Vue Test Utils)
- **Unit test:** Composables (`useAuth`, `useAnalysis`)
- **Skip:** UI components detail (overhead terlalu tinggi untuk solo dev)

### Target Coverage
- Backend: ~60% (fokus pada service layer)
- Frontend: ~40% (fokus pada composables)

---

## 9. Deployment

### Simple Deployment (VPS / Railway)

```bash
# Backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 2

# Frontend (generate static atau SSR)
nuxt build
node .output/server/index.mjs
```

### docker-compose.yml (untuk development & self-hosted)
```yaml
version: "3.9"
services:
  backend:
    build: ./backend
    env_file: .env
    ports: ["8000:8000"]
    depends_on: [db]
  
  frontend:
    build: ./frontend
    ports: ["3000:3000"]
    environment:
      - NUXT_PUBLIC_API_BASE=http://backend:8000/api/v1
  
  db:
    image: postgres:16-alpine
    volumes: ["pgdata:/var/lib/postgresql/data"]
    environment:
      POSTGRES_DB: resume_analyzer
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: ${DB_PASSWORD}

volumes:
  pgdata:
```

---

## 10. Scalability Path (Future)

Jika traffic tumbuh, berikut urutan penambahan yang recommended:

1. **Tambah Redis** → untuk caching hasil analisis dan rate limiting yang distributed
2. **Tambah task queue (Celery/ARQ)** → AI analysis jadi async background job
3. **Pisah file storage** → Simpan file asli di S3/R2 jika perlu audit trail
4. **Read replica PostgreSQL** → Jika query history mulai lambat
5. **Horizontal scale backend** → Multiple uvicorn workers di balik load balancer

Semua ini tidak perlu di v1. Arsitektur saat ini sudah bisa handle ratusan user aktif dengan satu server.
