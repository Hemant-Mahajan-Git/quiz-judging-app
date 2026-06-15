# Multi-Region Evaluation System - Database Schema

## Overview
This document describes the complete PostgreSQL schema for the multi-region, multi-tenant evaluation system.

## Entity-Relationship Diagram

```
┌──────────────┐
│   regions    │
├──────────────┤
│ region_id (PK)│
│ name         │
│ description  │
│ created_at   │
└──────┬───────┘
       │
       │ (1 to Many)
       │
       ▼
┌──────────────────┐        ┌──────────────────┐
│     users        │◄───────┤   evaluations    │
├──────────────────┤        ├──────────────────┤
│ user_id (PK)     │        │ eval_id (PK)     │
│ full_name        │        │ candidate_id (FK)│
│ email            │        │ judge_id (FK)    │
│ password_hash    │        │ region_id (FK)   │
│ role             │        │ scores_criteria  │
│ region_id (FK)   │        │ total_score      │
│ is_approved      │        │ timestamp        │
│ created_at       │        │ updated_at       │
└──────┬───────────┘        └──────────────────┘
       │ (1 to Many)                ▲
       │                            │
       │                     (Many to 1)
       │                            │
       ▼                            │
┌──────────────────┐        ┌──────────────────┐
│   candidates     │────────┤   evaluations    │
├──────────────────┤        ├──────────────────┤
│ candidate_id (PK)│        │ evaluation_id (FK)│
│ name             │        │ candidate_id (FK)│
│ email            │        └──────────────────┘
│ phone            │
│ region_id (FK)   │
│ registration_num │
│ created_at       │
└──────────────────┘
```

## Table Definitions

### 1. regions
Stores information about different regions in the system.

```sql
CREATE TABLE regions (
    region_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    timezone VARCHAR(50) DEFAULT 'UTC',
    is_active BOOLEAN DEFAULT true,
    created_by UUID REFERENCES users(user_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT region_name_not_empty CHECK (length(name) > 0)
);

CREATE INDEX idx_regions_active ON regions(is_active);
```

### 2. users
Stores all users: Admin, Superjudges, Judges.

```sql
CREATE TYPE user_role AS ENUM ('admin', 'superjudge', 'judge', 'candidate');
CREATE TYPE approval_status AS ENUM ('pending', 'approved', 'rejected');

CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role user_role NOT NULL,
    region_id UUID REFERENCES regions(region_id) ON DELETE SET NULL,
    is_approved approval_status DEFAULT 'pending',
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    
    CONSTRAINT email_unique_per_region UNIQUE (email, region_id),
    CONSTRAINT admin_no_region CHECK (role != 'admin' OR region_id IS NULL),
    CONSTRAINT full_name_not_empty CHECK (length(full_name) > 0)
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_region ON users(region_id);
CREATE INDEX idx_users_role_region ON users(role, region_id);
CREATE INDEX idx_users_active ON users(is_active);
```

### 3. candidates
Stores candidate information for each region.

```sql
CREATE TABLE candidates (
    candidate_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    candidate_name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    phone VARCHAR(20),
    registration_number VARCHAR(100),
    region_id UUID NOT NULL REFERENCES regions(region_id) ON DELETE CASCADE,
    description TEXT,
    status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT candidate_name_not_empty CHECK (length(candidate_name) > 0),
    CONSTRAINT region_registration_unique UNIQUE (region_id, registration_number)
);

CREATE INDEX idx_candidates_region ON candidates(region_id);
CREATE INDEX idx_candidates_status ON candidates(status);
```

### 4. evaluations
Stores all evaluation scores from judges.

```sql
CREATE TABLE evaluations (
    evaluation_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    candidate_id UUID NOT NULL REFERENCES candidates(candidate_id) ON DELETE CASCADE,
    judge_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    region_id UUID NOT NULL REFERENCES regions(region_id) ON DELETE CASCADE,
    
    -- Evaluation Criteria (JSON for flexibility)
    scores_criteria JSONB DEFAULT '{}',
    total_score DECIMAL(5, 2) CHECK (total_score >= 0 AND total_score <= 100),
    comments TEXT,
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT unique_judge_candidate_region UNIQUE (candidate_id, judge_id, region_id),
    CONSTRAINT score_within_range CHECK (total_score >= 0 AND total_score <= 100)
);

CREATE INDEX idx_evaluations_candidate ON evaluations(candidate_id);
CREATE INDEX idx_evaluations_judge ON evaluations(judge_id);
CREATE INDEX idx_evaluations_region ON evaluations(region_id);
CREATE INDEX idx_evaluations_created_at ON evaluations(created_at);
```

### 5. evaluation_criteria (Optional - for standardized scoring)
Stores evaluation criteria definitions per region.

```sql
CREATE TABLE evaluation_criteria (
    criteria_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    region_id UUID NOT NULL REFERENCES regions(region_id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    max_score DECIMAL(5, 2) DEFAULT 100,
    weight DECIMAL(3, 2) DEFAULT 1.0,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT criteria_name_region_unique UNIQUE (region_id, name)
);

CREATE INDEX idx_criteria_region ON evaluation_criteria(region_id);
```

### 6. audit_logs (For compliance)
Tracks all user actions for audit.

```sql
CREATE TABLE audit_logs (
    log_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(user_id) ON DELETE SET NULL,
    region_id UUID REFERENCES regions(region_id) ON DELETE SET NULL,
    action VARCHAR(100) NOT NULL,
    entity_type VARCHAR(50),
    entity_id UUID,
    old_values JSONB,
    new_values JSONB,
    ip_address INET,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_audit_user ON audit_logs(user_id);
CREATE INDEX idx_audit_region ON audit_logs(region_id);
CREATE INDEX idx_audit_action ON audit_logs(action);
CREATE INDEX idx_audit_created_at ON audit_logs(created_at);
```

## Sample Data Queries

### Insert a new region
```sql
INSERT INTO regions (name, description, timezone)
VALUES ('North America', 'Candidates from North American region', 'America/New_York');
```

### Insert a superjudge
```sql
INSERT INTO users (full_name, email, password_hash, role, region_id, is_approved)
VALUES ('John Evaluator', 'john@example.com', '$2b$12$...', 'superjudge', '<region_id>', 'approved');
```

### Insert a candidate
```sql
INSERT INTO candidates (candidate_name, email, registration_number, region_id)
VALUES ('Alice Smith', 'alice@example.com', 'CAN-001', '<region_id>');
```

### Insert an evaluation
```sql
INSERT INTO evaluations (
    candidate_id, judge_id, region_id, 
    scores_criteria, total_score, comments
) VALUES (
    '<candidate_id>', '<judge_id>', '<region_id>',
    '{"technical": 85, "communication": 90}', 87.5,
    'Excellent performance'
);
```

## Views for Analytics

### Regional Candidate Scores Summary
```sql
CREATE VIEW regional_scores_summary AS
SELECT 
    c.candidate_id,
    c.candidate_name,
    r.name AS region_name,
    COUNT(e.evaluation_id) as evaluation_count,
    AVG(e.total_score) as average_score,
    MIN(e.total_score) as min_score,
    MAX(e.total_score) as max_score
FROM candidates c
LEFT JOIN evaluations e ON c.candidate_id = e.candidate_id
LEFT JOIN regions r ON c.region_id = r.region_id
GROUP BY c.candidate_id, c.candidate_name, r.name;
```

### Judge Evaluation Activity
```sql
CREATE VIEW judge_evaluation_activity AS
SELECT 
    u.user_id,
    u.full_name,
    r.name AS region_name,
    COUNT(e.evaluation_id) as total_evaluations,
    MAX(e.created_at) as last_evaluation_date
FROM users u
LEFT JOIN evaluations e ON u.user_id = e.judge_id
LEFT JOIN regions r ON u.region_id = r.region_id
WHERE u.role = 'judge'
GROUP BY u.user_id, u.full_name, r.name;
```

## Migration Script (Alembic)

```bash
# Initialize alembic
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Initial schema creation"

# Apply migration
alembic upgrade head
```
