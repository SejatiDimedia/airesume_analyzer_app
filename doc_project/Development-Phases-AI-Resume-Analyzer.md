# Development Phases
## AI Resume Analyzer

**Version:** 1.0  
**Date:** Juni 2026  
**Target:** Solo Developer  
**Estimasi Total:** ~10–12 minggu (part-time) / ~6–8 minggu (full-time)

---

## Overview Timeline

```
Phase 0 │ Setup & Fondasi          │ 3–4 hari
Phase 1 │ Backend Core             │ 1.5–2 minggu
Phase 2 │ Frontend Core            │ 1.5–2 minggu
Phase 3 │ AI Integration           │ 1 minggu
Phase 4 │ Polish & Security        │ 1 minggu
Phase 5 │ Testing & QA             │ 1 minggu
Phase 6 │ Deployment & Launch      │ 3–4 hari
```

---

## Phase 0 — Setup & Fondasi
**Durasi:** 3–4 hari  
**Goal:** Semua tooling siap, developer tidak perlu setup ulang saat coding

### 0.1 Repository & Project Structure
- [x] Buat monorepo dengan struktur `frontend/` dan `backend/`
- [x] Init git, buat `.gitignore` untuk Python dan Node
- [x] Buat `README.md` dengan instruksi setup lokal
- [ ] Setup branch strategy: `main` (production), `dev` (development)

### 0.2 Backend Setup (FastAPI)
- [x] Buat virtual environment Python 3.12
- [x] Install dependencies awal dan buat `requirements.txt`
  ```
  fastapi, uvicorn[standard], sqlalchemy[asyncio], asyncpg,
  alembic, pydantic-settings, python-jose[cryptography],
  bcrypt, python-multipart, pypdf2, python-docx, openai,
  slowapi, pytest, pytest-asyncio, httpx
  ```
- [x] Setup struktur folder sesuai System Design (`routers/`, `services/`, `models/`, dll)
- [x] Buat `app/config.py` dengan `pydantic-settings` untuk env vars
- [x] Buat `app/main.py` dengan app factory, CORS middleware
- [x] Buat `app/database.py` — async engine + session factory
- [ ] Verifikasi: `uvicorn app.main:app --reload` berjalan, `/docs` terbuka

### 0.3 Database Setup
- [x] Install PostgreSQL lokal (atau pakai Docker)
- [x] Buat database `resume_analyzer_dev`
- [x] Init Alembic (`alembic init alembic`)
- [x] Setup `alembic.ini` dan `env.py` untuk async engine
- [ ] Buat model `User`, `Analysis`, `PasswordResetToken`
- [ ] Generate migration pertama dan `alembic upgrade head`
- [ ] Verifikasi: tabel berhasil dibuat di DB
re_
### 0.4 Frontend Setup (Nuxt 3)
- [x] `npx nuxi init frontend` dengan TypeScript template
- [x] Install dependencies: `@pinia/nuxt`, `@vueuse/nuxt`, `vee-validate`, `zod`
- [x] Install dan setup Tailwind CSS
- [x] Install shadcn-vue dan setup komponen dasar
- [x] Setup `nuxt.config.ts`: runtimeConfig, modules, CORS
- [ ] Setup Pinia stores folder dan TypeScript types
- [ ] Buat `types/index.ts` dengan shared interfaces (User, Analysis, dll)
- [ ] Verifikasi: `npm run dev` berjalan di `localhost:3000`

### 0.5 Dev Environment
- [x] Buat `.env.example` dengan semua env vars yang dibutuhkan
- [x] Buat `docker-compose.yml` untuk PostgreSQL lokal
- [ ] Setup VS Code workspace settings (Python interpreter, ESLint, Prettier)
- [ ] Buat `Makefile` dengan shortcut: `make dev`, `make migrate`, `make test`

**Deliverable Phase 0:** Backend dan frontend jalan secara lokal, DB terkoneksi, struktur folder rapi.

---

## Phase 1 — Backend Core
**Durasi:** 1.5–2 minggu  
**Goal:** Semua API endpoint berjalan dan bisa ditest via Swagger UI

### 1.1 Auth System (3–4 hari)

**Day 1–2: Foundation**
- [x] Buat `utils/security.py`: fungsi `hash_password`, `verify_password`, `create_jwt`, `decode_jwt`
- [x] Buat `schemas/auth.py`: `RegisterRequest`, `LoginRequest`, `TokenResponse`, `UserResponse`
- [x] Buat `services/auth_service.py`:
  - `create_user(db, email, password)` — cek duplikat email, hash password, insert
  - `authenticate_user(db, email, password)` — lookup user, verify hash
  - `get_user_by_id(db, user_id)` — untuk dependency injection
- [x] Buat `routers/auth.py`: `POST /auth/register`, `POST /auth/login`
- [x] Buat `dependencies.py`: `get_current_user` dependency (decode JWT dari cookie/header)

**Day 3–4: Password Reset & Middleware**
- [x] Buat `services/auth_service.py` tambahan:
  - `create_reset_token(db, email)` — generate token, simpan ke DB
  - `reset_password(db, token, new_password)` — validasi token, update password, mark used
- [x] Buat `routers/auth.py` tambahan: `POST /auth/forgot-password`, `POST /auth/reset-password`, `GET /auth/me`, `POST /auth/logout`
- [x] Setup rate limiting dengan `slowapi`: max 5 login attempt/menit per IP
- [x] Test manual via Swagger UI semua endpoint auth

**Checklist akhir 1.1:**
- [x] Register user baru → berhasil, email unik enforce
- [x] Login → dapat JWT token
- [x] Hit endpoint protected tanpa token → 401
- [x] Hit endpoint protected dengan token → 200
- [x] Forgot password → token dibuat di DB
- [x] Reset password dengan token valid → password berubah
- [x] Reset password dengan token expired/used → error

### 1.2 File Parsing Service (1–2 hari)

- [x] Buat `services/file_service.py`:
  ```python
  async def extract_text(file: UploadFile) -> str:
      # Validate MIME type (bukan hanya ekstensi)
      # Dispatch ke _extract_pdf() atau _extract_docx()
      # Return cleaned text string
  ```
- [x] Install library pendukung: `PyMuPDF` (atau `pdfplumber`) untuk PDF, `python-docx` untuk DOCX.
- [x] Buat `routers/upload.py` (opsional untuk test manual, atau langsung digabung ke endpoint AI nanti)
- [x] Tulis unit test untuk PDF dan DOCX text extraction (minimal file valid vs invalid)

**Checklist akhir 1.2:**
- [ ] File > 5MB → 400 error
- [ ] File bukan PDF/DOCX → 400 error
- [ ] PDF scan tanpa teks → error message jelas

### 1.3 Analysis CRUD (2 hari)

- [x] Buat `schemas/analysis.py`: `AnalysisCreateRequest`, `AnalysisResponse`, `AnalysisListResponse`, `AnalysisUpdateRequest`
- [x] Buat `services/analysis_service.py`:
  - `create_analysis(db, user_id, resume_text, jd, label, ai_result)`
  - `get_analysis_by_id(db, id, user_id)` — pastikan ownership
  - `list_user_analyses(db, user_id, page, per_page)`
  - `update_analysis_label(db, id, user_id, label)`
  - `soft_delete_analysis(db, id, user_id)`
- [x] Buat `routers/analysis.py`: semua 5 endpoint CRUD
- [x] Semua endpoint dilindungi `get_current_user` dependency
- [x] Test manual semua endpoint (gunakan hardcoded AI result dulu, tanpa OpenAI)

**Checklist akhir 1.3:**
- [x] Create analysis → 201 dengan data
- [x] List analysis → paginated, hanya milik user yang login
- [x] Get by ID → 404 jika bukan milik user
- [x] Update label → berhasil
- [x] Delete → soft delete (tetap ada di DB, tidak muncul di list)

### 1.4 Error Handling & Validation Global (0.5 hari)

- [x] Buat custom exception classes: `NotFoundError`, `ForbiddenError`, `ValidationError`
- [x] Daftarkan exception handlers di `main.py` → semua return format JSON konsisten
- [x] Test: pastikan semua error return format `{ "error": { "code", "message" } }`

**Deliverable Phase 1:** Semua API endpoint berjalan, bisa ditest via Swagger, termasuk auth, file parsing, dan CRUD analisis.

---

## Phase 2 — Frontend Core
**Durasi:** 1.5–2 minggu  
**Goal:** Semua halaman utama berjalan dengan data mock/real dari API

### 2.1 Foundation & Auth Pages (2–3 hari)

**Setup:**
- [x] Buat `composables/useAuth.ts`:
  - `login(email, password)`, `register(...)`, `logout()`, `fetchMe()`
  - Handle API errors → tampilkan ke user
- [x] Buat Pinia store `stores/auth.ts`: state `user`, `isAuthenticated`
- [x] Buat `middleware/auth.ts`: redirect ke `/login` jika belum login
- [x] Setup `ofetch` base URL dari `runtimeConfig`

**Halaman:**
- [x] `pages/login.vue`:
  - Form email + password dengan VeeValidate + Zod schema
  - Submit → call `useAuth().login()` → redirect ke `/dashboard`
  - Link ke register
- [x] `pages/register.vue`:
  - Form email + password + confirm password
  - Validasi password match di client
  - Submit → auto login setelah register

**Checklist akhir 2.1:**
- [x] Register → login otomatis → redirect dashboard
- [x] Login dengan kredensial salah → error message muncul
- [x] Akses `/dashboard` tanpa login → redirect ke `/login`
- [x] Setelah login, akses `/login` → redirect ke `/dashboard`

### 2.2 Layout & Navigation (1 hari)

- [x] Buat `layouts/default.vue`: navbar dengan link ke Dashboard dan tombol Logout (serta mobile bottom-nav)
- [x] Buat `layouts/auth.vue`: layout simpel untuk halaman login/register (tanpa navbar)
- [x] Buat `components/ui/`: Button, Input, Card, Badge, Alert dari shadcn-vue
- [x] Buat error state dan komponen custom
- [x] Setup UI dasar dan theaming (SaaS aesthetic, Slate/Indigo)

### 2.3 Dashboard — History List (2 hari)

- [x] Buat `composables/useAnalysis.ts`:
  - `fetchAnalyses(page)`, `deleteAnalysis(id)`, `updateLabel(id, label)`
- [x] Buat Pinia store `stores/analysis.ts`: state list, pagination, loading (diganti dengan component state untuk saat ini)
- [x] Buat `pages/dashboard.vue`:
  - Header: "My Analyses" + tombol "New Analysis"
  - List analisis
  - Empty state jika belum ada analisis
  - Pagination sederhana (prev/next)
- [x] Buat UI Card untuk analisis (Responsive Desktop/Mobile)

**Checklist akhir 2.3:**
- [x] Dashboard load list analisis dari API
- [ ] Pagination bekerja
- [ ] Delete analisis → hilang dari list
- [x] Empty state tampil jika belum ada analisis

### 2.4 New Analysis Form (2 hari)

- [x] Buat `pages/analyze.vue`:
  - File upload dropzone (drag & drop + click to browse)
  - Textarea untuk job description
  - Tombol "Analyze Resume"
  - Loading state / UI Feedback
- [x] Buat UI komponen File Upload
- [x] Pemasangan logika submit & redirect ke `/result`

**Checklist akhir 2.4:**
- [x] Upload file PDF → diterima (Integrasi)
- [x] Validasi client-side dasar form UI
- [ ] Upload file > 5MB → error di client sebelum kirim (Logika)
- [x] Submit form tanpa file → validasi gagal
- [x] Submit form tanpa JD → validasi gagal
- [x] Loading state muncul saat menunggu

### 2.5 Analysis Result Page (2 hari)

- [x] Buat `pages/result.vue` (UI visualisasi hasil AI): 
- [x] Buat UI `ScoreGauge` (Gauge melingkar dengan persentase)
- [x] Buat UI Feedback Section (Summary, Strengths, Weaknesses)
- [x] Buat UI Keyword Analysis (Matched & Missing)
- [x] Tombol "Back to Dashboard" dan elemen CTA pendukung

**Checklist akhir 2.5:**
- [x] Result page tampil dengan mockup data lengkap
- [x] Score gauge animasi
- [x] Keyword matched dan missing ditampilkan jelas
- [x] Data Result dimuat dari API backend (Integrasi)

**Deliverable Phase 2:** Semua halaman secara UI berjalan. Full flow bisa dicoba end-to-end.

---

## Phase 3 — AI Integration
**Durasi:** 1 minggu  
**Goal:** AI analysis benar-benar bekerja dengan OpenAI

### 3.1 AI Service (2–3 hari)

- [ ] Setup `OPENAI_API_KEY` di `.env`
- [ ] Buat `services/ai_service.py`:
  ```python
  SYSTEM_PROMPT = """
  You are an expert resume reviewer and career coach.
  Analyze the provided resume against the job description.
  Return ONLY a valid JSON object with this exact structure:
  {
    "match_score": <integer 0-100>,
    "summary": <string, 2-3 sentences>,
    "strengths": [<string>, ...],
    "weaknesses": [<string>, ...],
    "suggestions": [<string>, ...],
    "keyword_analysis": {
      "matched": [<string>, ...],
      "missing": [<string>, ...]
    }
  }
  Be specific and actionable. Do not return markdown or extra text.
  """
  
  async def analyze_resume(resume_text: str, job_description: str) -> dict:
      # Call OpenAI dengan response_format json_object
      # Parse response
      # Validate schema output
      # Return dict
  ```
- [ ] Tambah timeout handling (30 detik max)
- [ ] Tambah retry logic sederhana: jika OpenAI timeout, retry 1x
- [ ] Tambah error handling: jika OpenAI API down → 503 response ke user dengan pesan jelas

### 3.2 Wire Up ke Analysis Endpoint (1 hari)

- [x] Update `routers/analysis.py` `POST /analysis`:
  1. Terima file + JD dari request
  2. Call `file_service.extract_text(file)`
  3. Call `ai_service.analyze_resume(resume_text, job_description)` (Masih Mocking)
  4. Call `analysis_service.create_analysis(...)` dengan result AI
  5. Return response
- [ ] Tambah rate limit: max 10 request/jam per user di endpoint ini

### 3.3 Prompt Tuning (1–2 hari)

- [ ] Test dengan berbagai kombinasi resume + JD:
  - Resume sangat relevan → score seharusnya tinggi (>80)
  - Resume tidak relevan sama sekali → score seharusnya rendah (<30)
  - Resume bahasa Indonesia + JD bahasa Inggris → harus bisa handle
  - Resume dengan format aneh (banyak tabel) → teks masih bisa diekstrak
- [ ] Iterasi prompt jika output tidak konsisten atau tidak akurat
- [ ] Pastikan JSON output selalu valid (tidak ada kasus malformed JSON)
- [ ] Catat estimasi token per request → hitung cost per analisis

**Checklist akhir Phase 3:**
- [x] Full flow end-to-end bekerja: upload PDF → dapat AI result (Mock Data Backend)
- [ ] Score masuk akal untuk resume yang relevan vs tidak relevan
- [ ] Suggestions spesifik dan actionable (bukan generik)
- [ ] Error OpenAI API → user dapat pesan error yang informatif
- [ ] Cost per analisis < $0.02

**Deliverable Phase 3:** Aplikasi fully functional end-to-end.

---

## Phase 4 — Polish & Security
**Durasi:** 1 minggu  
**Goal:** Aplikasi aman, nyaman dipakai, dan siap production

### 4.1 Security Hardening (2 hari)

- [ ] **JWT Cookie:** Pastikan token disimpan di httpOnly cookie, bukan localStorage
- [ ] **CORS:** Set `allow_origins` ke domain spesifik, bukan `*`
- [ ] **Rate Limiting Review:**
  - Login: 5 attempt/menit per IP ✓
  - Register: 3 attempt/menit per IP
  - Analysis: 10 request/jam per user ✓
- [ ] **Input Sanitization:**
  - Truncate resume text jika > 8000 kata (untuk kontrol cost token)
  - Truncate job description jika > 3000 kata
- [ ] **File Validation:** Double check MIME type validation (tidak hanya ekstensi)
- [ ] **Secret Key:** Pastikan `SECRET_KEY` panjang dan random (min 32 karakter)
- [ ] **SQL Injection:** Semua query sudah pakai SQLAlchemy ORM (aman by default)
- [ ] **HTTPS:** Pastikan production berjalan di HTTPS

### 4.2 UX Polish (2 hari)

- [ ] **Loading States:** Semua action async punya loading state yang jelas
- [ ] **Error Messages:** Semua error ditampilkan dengan bahasa yang ramah user (bukan stack trace)
- [ ] **Empty States:** Dashboard kosong, hasil keyword kosong — semua punya state yang bagus
- [ ] **Responsive:** Test di mobile (375px) dan tablet (768px)
- [ ] **Form UX:**
  - Disable tombol submit saat loading
  - Auto-focus field pertama saat halaman load
  - Enter di field JD tidak submit form (textarea)
- [ ] **Favicon dan page title** yang sesuai tiap halaman

### 4.3 Performance Basics (1 hari)

- [ ] **Frontend:**
  - Lazy load halaman result (besar)
  - Optimasi image jika ada (pakai `<NuxtImg>`)
- [ ] **Backend:**
  - Tambah `Connection: keep-alive` pada requests ke OpenAI
  - Cek tidak ada N+1 query di list endpoint
- [ ] **Database:**
  - Verifikasi index sudah ada sesuai Database Design
  - Test query speed dengan data 100+ rows

### 4.4 Logging (0.5 hari)

- [ ] Setup basic logging di FastAPI:
  ```python
  import logging
  logging.basicConfig(level=logging.INFO)
  logger = logging.getLogger(__name__)
  
  # Log setiap analysis request (user_id, duration, match_score)
  # Log setiap error (tanpa expose sensitive data)
  ```
- [ ] Pastikan tidak ada `print()` di production code (ganti ke `logger`)
- [ ] Log OpenAI API errors dengan context yang cukup untuk debug

**Deliverable Phase 4:** Aplikasi aman, responsif, dan nyaman dipakai.

---

## Phase 5 — Testing & QA
**Durasi:** 1 minggu  
**Goal:** Bug utama ditemukan dan diperbaiki sebelum launch

### 5.1 Backend Tests (2–3 hari)

**Setup:**
- [ ] Buat `conftest.py`: test database (SQLite in-memory atau PostgreSQL test DB), test client, fixtures user
- [ ] Buat `.env.test` dengan test credentials

**Auth tests (`tests/test_auth.py`):**
- [ ] Register berhasil → user ada di DB
- [ ] Register email duplikat → 400
- [ ] Login credentials benar → dapat token
- [ ] Login credentials salah → 401
- [ ] Akses protected endpoint tanpa token → 401
- [ ] Akses protected endpoint dengan token expired → 401
- [ ] Reset password flow: request token → reset dengan token → token tidak bisa dipakai lagi

**Analysis tests (`tests/test_analysis.py`):**
- [ ] Create analysis (mock AI service) → 201
- [ ] List analysis → hanya milik user sendiri
- [ ] Get analysis milik orang lain → 404
- [ ] Delete analysis → soft delete
- [ ] Analysis tidak muncul setelah delete

**File service tests (`tests/test_file_service.py`):**
- [ ] Siapkan sample PDF dan DOCX di `tests/fixtures/`
- [ ] Ekstrak teks dari sample PDF → tidak kosong
- [ ] Ekstrak teks dari sample DOCX → tidak kosong
- [ ] File JPEG → raise error

### 5.2 Frontend QA Manual (2 hari)

Buat checklist QA dan jalankan satu per satu di browser:

**Auth Flow:**
- [ ] Register akun baru
- [ ] Logout dan login ulang
- [ ] Coba akses dashboard tanpa login
- [ ] Forgot password flow

**Analysis Flow:**
- [ ] Upload PDF → submit → tunggu → lihat hasil
- [ ] Upload DOCX → submit → tunggu → lihat hasil
- [ ] Coba upload file PNG → error muncul
- [ ] Coba submit tanpa file → validasi muncul
- [ ] Coba submit tanpa JD → validasi muncul
- [ ] Lihat list di dashboard → ada entry baru
- [ ] Klik entry → masuk ke detail
- [ ] Edit label → berhasil tersimpan
- [ ] Hapus analisis → hilang dari list

**Cross-browser:**
- [ ] Chrome (desktop)
- [ ] Firefox (desktop)
- [ ] Safari (jika ada Mac)
- [ ] Chrome Mobile (Android/iOS)

### 5.3 Bug Fix Sprint (1–2 hari)

- [ ] Prioritaskan bug berdasarkan severity: Critical → High → Medium
- [ ] Buat daftar bug di Notion/Trello/GitHub Issues
- [ ] Selesaikan minimal semua bug Critical dan High sebelum launch
- [ ] Retest semua bug yang sudah diperbaiki

**Deliverable Phase 5:** Tidak ada bug critical. Semua core flow berjalan mulus.

---

## Phase 6 — Deployment & Launch
**Durasi:** 3–4 hari  
**Goal:** Aplikasi live di production

### 6.1 Infrastructure Setup (1 hari)

Pilih salah satu:

**Opsi A: Railway (Recommended untuk solo dev)**
- [ ] Buat akun Railway
- [ ] Deploy PostgreSQL service di Railway
- [ ] Setup environment variables di Railway dashboard
- [ ] Connect ke GitHub repo untuk auto-deploy

**Opsi B: VPS ($5/bulan — Hetzner/DigitalOcean)**
- [ ] Setup Ubuntu 22.04
- [ ] Install Docker + Docker Compose
- [ ] Setup Nginx sebagai reverse proxy
- [ ] Setup SSL dengan Certbot (Let's Encrypt)

### 6.2 Backend Deployment (1 hari)

- [ ] Buat `Dockerfile` untuk backend:
  ```dockerfile
  FROM python:3.12-slim
  WORKDIR /app
  COPY requirements.txt .
  RUN pip install --no-cache-dir -r requirements.txt
  COPY . .
  CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
  ```
- [ ] Set semua environment variables di production
- [ ] Jalankan `alembic upgrade head` di production DB
- [ ] Verifikasi `/api/v1/docs` bisa diakses (atau disable di production)
- [ ] Test semua endpoint via curl atau Postman

### 6.3 Frontend Deployment (1 hari)

- [ ] Set `NUXT_PUBLIC_API_BASE` ke URL backend production
- [ ] Build: `npm run build`
- [ ] Deploy ke Railway / Vercel / Netlify
- [ ] Verifikasi semua halaman bisa diakses
- [ ] Verifikasi tidak ada CORS error di browser console

### 6.4 Production Checklist (0.5 hari)

**Security:**
- [ ] HTTPS aktif di semua URL
- [ ] Environment variables tidak ter-expose di frontend
- [ ] `/api/v1/docs` disabled di production (atau di-protect)
- [ ] `DEBUG=False` di backend

**Functionality:**
- [ ] Register akun baru di production → berhasil
- [ ] Upload resume di production → dapat AI result
- [ ] Semua link dan navigasi berfungsi

**Monitoring:**
- [ ] Setup UptimeRobot (gratis) untuk monitoring uptime
- [ ] Pastikan ada cara untuk cek logs jika ada masalah

### 6.5 Soft Launch (0.5 hari)

- [ ] Share ke 3–5 orang untuk user testing awal
- [ ] Kumpulkan feedback (Google Form atau langsung chat)
- [ ] Monitor logs selama 24 jam pertama
- [ ] Siapkan hotfix plan jika ada critical bug post-launch

**Deliverable Phase 6:** Aplikasi live, bisa diakses publik, monitoring aktif.

---

## Appendix A — Daily Standup Template (Solo Dev)

Karena solo dev, tracking harian penting untuk menjaga momentum:

```
Tanggal: ___________
Phase: ___________

✅ Selesai kemarin:
- 

🎯 Target hari ini:
- 

🚧 Blocker / yang belum jelas:
- 

📊 Estimasi selesai phase ini: ___ hari lagi
```

---

## Appendix B — Definition of Done

Sebuah task dianggap **Done** jika:
1. Kode sudah ditulis dan berfungsi sesuai spesifikasi
2. Sudah ditest manual (minimal happy path + 1 error case)
3. Tidak ada console error / warning yang tidak perlu
4. Sudah di-commit ke repo dengan commit message yang jelas

---

## Appendix C — Risk & Mitigation

| Risk | Probabilitas | Dampak | Mitigation |
|---|---|---|---|
| OpenAI API mahal / quota habis | Sedang | Tinggi | Set spending limit di OpenAI dashboard; tambah rate limit per user |
| PDF parsing gagal untuk format tertentu | Tinggi | Sedang | Beri pesan error jelas; sarankan user convert ke format standar |
| JWT token bocor | Rendah | Tinggi | Gunakan httpOnly cookie; set expire pendek |
| Solo dev burnout / stuck | Sedang | Tinggi | Break phase jadi task kecil; skip fitur non-esensial jika deadline mepet |
| Database data loss | Rendah | Tinggi | Aktifkan automated backup di managed DB provider |

---

## Appendix D — Scope Cut (Jika Deadline Mepet)

Jika waktu tidak cukup, potong dalam urutan ini (yang dipotong tidak merusak core value):

1. ~~Forgot password / reset password~~ → User bisa hubungi admin untuk reset manual
2. ~~Pagination di dashboard~~ → Load semua (max 50 item)
3. ~~Edit label analisis~~ → Label auto-generated saja
4. ~~Animasi ScoreGauge~~ → Tampilkan angka statis saja
5. ~~Responsive mobile~~ → Desktop-first dulu

**Yang TIDAK boleh dipotong:** Register/Login, Upload Resume, AI Analysis, Lihat Hasil.
