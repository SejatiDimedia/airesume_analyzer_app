# Product Requirements Document (PRD)
## AI Resume Analyzer

**Version:** 1.0  
**Date:** Juni 2026  
**Author:** Solo Developer  
**Status:** Draft

---

## 1. Overview

### 1.1 Problem Statement
Job seekers sering tidak tahu apakah resume mereka cukup kuat untuk posisi yang dilamar. HR/rekruter menghabiskan waktu berjam-jam mereview resume yang tidak relevan. Tidak ada tools yang murah, simpel, dan berbasis AI untuk menganalisis kesesuaian resume dengan job description secara otomatis.

### 1.2 Product Vision
AI Resume Analyzer adalah aplikasi web yang membantu job seeker mengoptimalkan resume mereka dengan memberikan analisis berbasis AI: skor kesesuaian dengan job description, feedback spesifik, dan saran perbaikan yang actionable.

### 1.3 Target User
- **Primary:** Job seeker yang aktif melamar pekerjaan
- **Secondary:** Fresh graduate yang belum berpengalaman membuat resume profesional

---

## 2. Goals & Non-Goals

### Goals
- User bisa upload resume (PDF/DOCX) dan paste job description
- AI menganalisis kesesuaian resume vs job description (match score)
- AI memberikan feedback: kekuatan, kelemahan, dan saran perbaikan
- User bisa melihat riwayat analisis sebelumnya
- Sistem berjalan dengan biaya infra yang rendah (< $20/bulan untuk early-stage)

### Non-Goals (v1.0)
- Tidak ada fitur edit resume langsung di aplikasi
- Tidak ada multi-language support (hanya Bahasa Inggris dan Indonesia)
- Tidak ada integrasi dengan job board (LinkedIn, Indeed, dll)
- Tidak ada fitur team/collaboration
- Tidak ada mobile app native

---

## 3. User Stories

### Authentication
- Sebagai user baru, aku ingin bisa register dengan email & password agar bisa menyimpan riwayat analisis
- Sebagai user, aku ingin bisa login dan logout dengan aman
- Sebagai user, aku ingin bisa reset password jika lupa

### Core Feature
- Sebagai job seeker, aku ingin upload file resume (PDF/DOCX) agar bisa dianalisis AI
- Sebagai job seeker, aku ingin paste job description dari lowongan yang aku lamar
- Sebagai job seeker, aku ingin melihat **match score** (0–100) antara resume dan JD
- Sebagai job seeker, aku ingin mendapat **feedback terstruktur**: skills yang match, skills yang kurang, dan saran konkret
- Sebagai job seeker, aku ingin melihat **daftar riwayat** analisis yang pernah aku lakukan

### History & Management
- Sebagai user, aku ingin memberi nama/label pada setiap analisis agar mudah dicari
- Sebagai user, aku ingin bisa menghapus riwayat analisis yang sudah tidak relevan

---

## 4. Feature Specifications

### 4.1 Authentication
| Feature | Detail |
|---|---|
| Register | Email + Password, validasi email unik |
| Login | JWT-based, token disimpan di httpOnly cookie |
| Logout | Invalidate token di server |
| Reset Password | Email link (simple token, expire 1 jam) |

### 4.2 Resume Upload & Parsing
| Feature | Detail |
|---|---|
| Format didukung | PDF, DOCX |
| Max file size | 5 MB |
| Parsing | Ekstrak teks dari file, simpan teks mentah di DB |
| Storage | File tidak disimpan permanen (diparse lalu dibuang) |

> **Catatan:** File tidak disimpan di storage permanen untuk menghemat biaya dan menghindari kompleksitas object storage. Hanya teks hasil parse yang disimpan.

### 4.3 AI Analysis
| Feature | Detail |
|---|---|
| Input | Teks resume + Job Description |
| Output | Match score (0–100), strengths, weaknesses, suggestions |
| AI Provider | OpenAI API (GPT-4o-mini untuk efisiensi biaya) |
| Response format | JSON terstruktur (via structured output / function calling) |
| Caching | Hasil analisis dicache di DB, tidak memanggil AI ulang untuk input identik |

**Output Schema:**
```json
{
  "match_score": 78,
  "summary": "Resume kamu cukup relevan untuk posisi ini...",
  "strengths": ["Python experience matches requirement", "..."],
  "weaknesses": ["No mention of Docker", "..."],
  "suggestions": ["Add Docker/containerization experience", "..."],
  "keyword_analysis": {
    "matched": ["Python", "FastAPI"],
    "missing": ["Docker", "Kubernetes"]
  }
}
```

### 4.4 Analysis History
| Feature | Detail |
|---|---|
| List | Tampil semua analisis user, sorted by newest |
| Detail | Tampil hasil lengkap dari analisis yang dipilih |
| Label | User bisa beri nama custom (default: "Analysis - [tanggal]") |
| Delete | Soft delete (is_deleted flag) |
| Pagination | 10 item per halaman |

---

## 5. UX Flow

```
Landing Page
    ↓
Register / Login
    ↓
Dashboard (riwayat analisis)
    ↓
New Analysis Page
    ├── Upload Resume (PDF/DOCX)
    ├── Paste Job Description
    ├── [Opsional] Beri nama analisis
    └── Klik "Analyze"
         ↓
     Loading State (AI processing ~5–15 detik)
         ↓
     Result Page
         ├── Match Score (visual gauge)
         ├── Summary
         ├── Strengths / Weaknesses / Suggestions
         └── Keyword Analysis
```

---

## 6. Non-Functional Requirements

| Kategori | Requirement |
|---|---|
| Performance | Halaman load < 2 detik; AI response < 20 detik |
| Security | Password di-hash (bcrypt); JWT expire 7 hari; rate limit pada endpoint AI |
| Availability | 99% uptime (single server, acceptable untuk solo dev) |
| Scalability | Tidak perlu scale di v1; desain harus mudah di-scale jika perlu |
| Cost | Infra < $20/bulan untuk < 100 active users |

---

## 7. Success Metrics (v1.0)

- User bisa selesaikan full flow (register → upload → dapat hasil) tanpa error
- AI analysis selesai < 20 detik untuk 95% request
- Cost per analysis < $0.02 (GPT-4o-mini pricing)

---

## 8. Out of Scope / Future Considerations

- Resume builder / editor
- ATS (Applicant Tracking System) simulation
- Batch analysis (banyak JD sekaligus)
- Fitur berbagi hasil analisis via link publik
- Paket premium / monetisasi
