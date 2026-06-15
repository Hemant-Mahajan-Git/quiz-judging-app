# Multi-Region Multi-Tenancy Evaluation System - Architecture Document

## 🏗️ System Architecture Overview

### High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        Global Admin (Top Tier)                  │
│  - Create/Manage Regions                                        │
│  - Onboard Superjudges across all regions                       │
│  - View Global Analytics & Dashboard                            │
└──────────────────────────┬──────────────────────────────────────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
    ┌─────▼─────┐    ┌─────▼─────┐    ┌────▼──────┐
    │ Region A  │    │ Region B  │    │ Region C  │
    │           │    │           │    │           │
    │┌─────────┐│    │┌─────────┐│    │┌────────┐ │
    ││Superjudge││    ││Superjudge││    ││Superjudge│
    │└────┬────┘│    │└────┬────┘│    │└────┬───┘ │
    │     │     │    │     │     │    │     │     │
    │  ┌──┴──┐  │    │  ┌──┴──┐  │    │  ┌──┴──┐  │
    │  │Judge│  │    │  │Judge│  │    │  │Judge│  │
    │  │Judge│  │    │  │Judge│  │    │  │Judge│  │
    │  └──┬──┘  │    │  └──┬──┘  │    │  └──┬──┘  │
    │     │     │    │     │     │    │     │     │
    │  ┌──▼────────┐ │  ┌──▼────────┐ │  ┌──▼────────┐
    │  │Candidates │ │  │Candidates │ │  │Candidates │
    │  └───────────┘ │  └───────────┘ │  └───────────┘
    └─────────────────┘  └─────────────┘  └────────────┘
```

## 📊 Multi-Tenancy Strategy

### Approach: **Row-Level Tenancy**
- Single database, single schema
- All tables include `region_id` as a foreign key
- Row-level security enforced at application and database level
- Judges/Superjudges filtered by their assigned region
- Global Admin can view across all regions

## 🔑 Key Components

### 1. **Backend Stack**
- **Framework:** FastAPI (Python)
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Authentication:** JWT Tokens + bcrypt password hashing
- **API:** RESTful with comprehensive endpoints

### 2. **Frontend Stack**
- **Framework:** React 18 + TypeScript
- **Build Tool:** Vite
- **UI Framework:** Tailwind CSS + shadcn/ui components
- **State Management:** React Context API
- **HTTP Client:** Axios

### 3. **Database**
- **Engine:** PostgreSQL 13+
- **Connection Pool:** pgbouncer (optional for scaling)
- **Migrations:** Alembic

## 🔐 Authentication & Authorization Flow

```
┌────────────────┐
│  User Login    │
└────────┬───────┘
         │
         ▼
┌────────────────────────────┐
│ Verify Credentials         │
│ + Check Region Access      │
└────────┬───────────────────┘
         │
         ▼
┌────────────────────────────┐
│ Generate JWT Token         │
│ Include: user_id,          │
│ role, region_id            │
└────────┬───────────────────┘
         │
         ▼
┌────────────────────────────┐
│ Return Token + User Info   │
│ Store in localStorage      │
└────────────────────────────┘
```

## 🗂️ Directory Structure

```
multi-tenant-evaluation-system/
├── backend/
│   ├── alembic/                    # Database migrations
│   │   ├── versions/
│   │   └── env.py
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                # FastAPI app entry
│   │   ├── config.py              # Configuration
│   │   ├── models/                # SQLAlchemy models
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── region.py
│   │   │   ├── candidate.py
│   │   │   └── evaluation.py
│   │   ├── schemas/               # Pydantic schemas
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── region.py
│   │   │   ├── candidate.py
│   │   │   └── evaluation.py
│   │   ├── crud/                  # CRUD operations
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── region.py
│   │   │   ├── candidate.py
│   │   │   └── evaluation.py
│   │   ├── api/                   # API routes
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── users.py
│   │   │   ├── regions.py
│   │   │   ├── candidates.py
│   │   │   └── evaluations.py
│   │   ├── core/                  # Core utilities
│   │   │   ├── __init__.py
│   │   │   ├── security.py        # JWT, hashing
│   │   │   ├── deps.py            # Dependency injection
│   │   │   └── exceptions.py
│   │   └── db/
│   │       ├── __init__.py
│   │       └── database.py        # Database connection
│   ├── requirements.txt
│   ├── .env.example
│   └── README.md
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── common/
│   │   │   │   ├── Header.tsx
│   │   │   │   ├── Sidebar.tsx
│   │   │   │   ├── RegionSelector.tsx
│   │   │   │   └── LoadingSpinner.tsx
│   │   │   ├── auth/
│   │   │   │   ├── LoginForm.tsx
│   │   │   │   ├── SignupForm.tsx
│   │   │   │   └── RegionSelectionPage.tsx
│   │   │   ├── admin/
│   │   │   │   ├── AdminDashboard.tsx
│   │   │   │   ├── RegionManagement.tsx
│   │   │   │   └── UserManagement.tsx
│   │   │   ├── superjudge/
│   │   │   │   ├── SuperjudgeDashboard.tsx
│   │   │   │   ├── JudgeApproval.tsx
│   │   │   │   ├── CandidateManagement.tsx
│   │   │   │   └── RegionalAnalytics.tsx
│   │   │   └── judge/
│   │   │       ├── JudgeDashboard.tsx
│   │   │       ├── EvaluationForm.tsx
│   │   │       ├── CandidateList.tsx
│   │   │       └── EvaluationHistory.tsx
│   │   ├── pages/
│   │   │   ├── LoginPage.tsx
│   │   │   ├── SignupPage.tsx
│   │   │   ├── RegionSelectionPage.tsx
│   │   │   ├── DashboardPage.tsx
│   │   │   └── NotFoundPage.tsx
│   │   ├── context/
│   │   │   ├── AuthContext.tsx
│   │   │   └── RegionContext.tsx
│   │   ├── hooks/
│   │   │   ├── useAuth.ts
│   │   │   ├── useRegion.ts
│   │   │   └── useFetch.ts
│   │   ├── services/
│   │   │   ├── api.ts              # Axios instance
│   │   │   ├── authService.ts
│   │   │   ├── regionService.ts
│   │   │   ├── candidateService.ts
│   │   │   └── evaluationService.ts
│   │   ├── types/
│   │   │   └── index.ts
│   │   ├── utils/
│   │   │   ├── constants.ts
│   │   │   ├── validators.ts
│   │   │   └── formatters.ts
│   │   ├── styles/
│   │   │   ├── globals.css
│   │   │   └── tailwind.css
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   ├── vite.config.ts
│   ├── tsconfig.json
│   └── tailwind.config.js
│
├── docs/
│   ├── DATABASE_SCHEMA.md
│   ├── API_DOCUMENTATION.md
│   ├── DEPLOYMENT.md
│   └── TROUBLESHOOTING.md
│
└── README.md
```

## 📋 Data Flow

### Candidate Evaluation Flow

```
1. Judge logs in
   ↓
2. System checks JWT token and extracts region_id
   ↓
3. Judge selects candidate (filtered by region_id)
   ↓
4. Judge enters evaluation scores
   ↓
5. Backend validates:
   - Candidate belongs to judge's region
   - Judge hasn't already evaluated this candidate
   - Score is within valid range
   ↓
6. Save evaluation with:
   - judge_id, candidate_id, region_id, timestamp
   ↓
7. Superjudge can view all evaluations for their region
   ↓
8. Global Admin can view across all regions
```

## 🔒 Security Layers

1. **JWT Token Validation:** All protected routes verify JWT
2. **Region Isolation:** Every query filters by region_id
3. **Role-Based Access Control (RBAC):** Different endpoints for different roles
4. **Password Security:** bcrypt hashing with salt
5. **Request Validation:** Pydantic schemas
6. **CORS:** Configured for frontend origin

## 🚀 Scalability Considerations

- **Horizontal Scaling:** Stateless API servers behind load balancer
- **Database Optimization:** Indices on (region_id, user_id), (candidate_id, region_id)
- **Caching:** Redis for region lists, user permissions
- **Async Jobs:** Celery for report generation, notifications
- **CDN:** For static assets

## 🔄 Region Switching Logic

```
User with multi-region access:
1. Presented with region dropdown on login
2. Selected region encoded in JWT
3. On region change:
   - Logout from current session
   - Login with same credentials but new region
   - New JWT generated with new region_id
```

## 📈 Future Enhancements

- Advanced analytics dashboard
- Real-time notifications
- Export to CSV/PDF
- Multi-language support
- Mobile app
- Audit logging
- 2FA authentication
