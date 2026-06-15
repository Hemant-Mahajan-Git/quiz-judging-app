# Multi-Region Evaluation System - API Documentation

## Base URL
```
http://localhost:8000/api/v1
```

## Authentication
All endpoints (except `/auth/login` and `/auth/signup`) require a JWT token in the Authorization header:

```
Authorization: Bearer <jwt_token>
```

## Response Format
All responses follow this format:

```json
{
  "success": true,
  "data": { ... },
  "message": "Operation successful",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

---

## 🔐 Authentication Endpoints

### POST /auth/login
Authenticate user and return JWT token.

**Request Body:**
```json
{
  "email": "judge@example.com",
  "password": "secure_password",
  "region_id": "region-uuid-here"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIs...",
    "user": {
      "user_id": "user-uuid",
      "full_name": "John Judge",
      "email": "judge@example.com",
      "role": "judge",
      "region_id": "region-uuid"
    },
    "expires_in": 3600
  }
}
```

### POST /auth/signup
Create new user account (Judge, Superjudge, Candidate).

**Request Body:**
```json
{
  "full_name": "Jane Judge",
  "email": "jane@example.com",
  "password": "secure_password",
  "role": "judge",
  "region_id": "region-uuid-here"
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "data": {
    "user_id": "user-uuid",
    "full_name": "Jane Judge",
    "email": "jane@example.com",
    "role": "judge",
    "region_id": "region-uuid",
    "is_approved": false
  },
  "message": "User created successfully. Pending approval from Superjudge."
}
```

---

## 🌍 Region Endpoints

### GET /regions
Get all available regions (public endpoint).

**Response (200 OK):**
```json
{
  "success": true,
  "data": [
    {
      "region_id": "region-uuid-1",
      "name": "North America",
      "description": "Candidates from North American region",
      "timezone": "America/New_York",
      "is_active": true
    },
    {
      "region_id": "region-uuid-2",
      "name": "Europe",
      "description": "Candidates from European region",
      "timezone": "Europe/London",
      "is_active": true
    }
  ]
}
```

### POST /regions (Admin Only)
Create a new region.

**Request Body:**
```json
{
  "name": "Asia Pacific",
  "description": "Candidates from Asia Pacific region",
  "timezone": "Asia/Singapore"
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "data": {
    "region_id": "new-region-uuid",
    "name": "Asia Pacific",
    "description": "Candidates from Asia Pacific region",
    "timezone": "Asia/Singapore",
    "is_active": true
  }
}
```

---

## 👥 User Management Endpoints

### GET /users/me
Get current authenticated user info.

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "user_id": "user-uuid",
    "full_name": "John Judge",
    "email": "judge@example.com",
    "role": "judge",
    "region_id": "region-uuid",
    "is_approved": true,
    "created_at": "2024-01-10T15:30:00Z"
  }
}
```

### GET /users/pending-judges (Superjudge Only)
Get list of pending judge approvals in the region.

**Response (200 OK):**
```json
{
  "success": true,
  "data": [
    {
      "user_id": "judge-uuid-1",
      "full_name": "Alice Judge",
      "email": "alice@example.com",
      "created_at": "2024-01-15T10:00:00Z",
      "is_approved": false
    },
    {
      "user_id": "judge-uuid-2",
      "full_name": "Bob Judge",
      "email": "bob@example.com",
      "created_at": "2024-01-16T12:30:00Z",
      "is_approved": false
    }
  ]
}
```

### POST /users/{user_id}/approve (Superjudge Only)
Approve a pending judge in the region.

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Judge approved successfully"
}
```

### POST /users/{user_id}/reject (Superjudge Only)
Reject a pending judge.

**Request Body:**
```json
{
  "reason": "Does not meet qualifications"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Judge rejected successfully"
}
```

---

## 🎓 Candidate Endpoints

### GET /candidates
Get all candidates in the user's region.

**Query Parameters:**
- `page` (optional): Page number (default: 1)
- `per_page` (optional): Items per page (default: 10)
- `status` (optional): Filter by status ('active', 'completed')

**Response (200 OK):**
```json
{
  "success": true,
  "data": [
    {
      "candidate_id": "cand-uuid-1",
      "candidate_name": "Alice Smith",
      "email": "alice@example.com",
      "phone": "+1-555-0123",
      "registration_number": "CAN-001",
      "region_id": "region-uuid",
      "status": "active",
      "evaluation_count": 2,
      "average_score": 85.5,
      "created_at": "2024-01-10T15:30:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 10,
    "total": 25,
    "total_pages": 3
  }
}
```

### POST /candidates (Superjudge Only)
Add a new candidate to the region.

**Request Body:**
```json
{
  "candidate_name": "Charlie Brown",
  "email": "charlie@example.com",
  "phone": "+1-555-0456",
  "registration_number": "CAN-002",
  "description": "Computer Science Degree holder"
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "data": {
    "candidate_id": "cand-uuid-new",
    "candidate_name": "Charlie Brown",
    "email": "charlie@example.com",
    "phone": "+1-555-0456",
    "registration_number": "CAN-002",
    "region_id": "region-uuid",
    "status": "active",
    "created_at": "2024-01-20T10:00:00Z"
  }
}
```

### GET /candidates/{candidate_id}
Get detailed information about a candidate.

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "candidate_id": "cand-uuid-1",
    "candidate_name": "Alice Smith",
    "email": "alice@example.com",
    "phone": "+1-555-0123",
    "registration_number": "CAN-001",
    "region_id": "region-uuid",
    "status": "active",
    "evaluations": [
      {
        "evaluation_id": "eval-uuid-1",
        "judge_name": "John Judge",
        "total_score": 85,
        "created_at": "2024-01-15T10:00:00Z"
      },
      {
        "evaluation_id": "eval-uuid-2",
        "judge_name": "Jane Judge",
        "total_score": 86,
        "created_at": "2024-01-16T14:30:00Z"
      }
    ],
    "average_score": 85.5,
    "created_at": "2024-01-10T15:30:00Z"
  }
}
```

---

## 📊 Evaluation Endpoints

### POST /evaluations
Submit an evaluation for a candidate.

**Request Body:**
```json
{
  "candidate_id": "cand-uuid-1",
  "scores_criteria": {
    "technical_skills": 85,
    "communication": 90,
    "problem_solving": 88
  },
  "total_score": 87.67,
  "comments": "Strong technical background with excellent communication skills."
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "data": {
    "evaluation_id": "eval-uuid-new",
    "candidate_id": "cand-uuid-1",
    "judge_id": "judge-uuid",
    "region_id": "region-uuid",
    "total_score": 87.67,
    "scores_criteria": {
      "technical_skills": 85,
      "communication": 90,
      "problem_solving": 88
    },
    "comments": "Strong technical background with excellent communication skills.",
    "created_at": "2024-01-20T11:00:00Z"
  },
  "message": "Evaluation submitted successfully"
}
```

### GET /evaluations
Get all evaluations for the current user.

**Query Parameters:**
- `candidate_id` (optional): Filter by candidate
- `from_date` (optional): Filter evaluations from date (ISO 8601)
- `to_date` (optional): Filter evaluations to date (ISO 8601)

**Response (200 OK):**
```json
{
  "success": true,
  "data": [
    {
      "evaluation_id": "eval-uuid-1",
      "candidate_name": "Alice Smith",
      "total_score": 87.67,
      "comments": "Strong technical background...",
      "created_at": "2024-01-20T11:00:00Z"
    }
  ]
}
```

### GET /evaluations/region/summary (Superjudge Only)
Get summary of all evaluations in the region.

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "total_evaluations": 45,
    "total_judges": 5,
    "total_candidates": 12,
    "average_score": 82.3,
    "highest_score": 98.5,
    "lowest_score": 65.0,
    "completion_rate": "75%",
    "evaluations_by_judge": [
      {
        "judge_name": "John Judge",
        "evaluations_count": 10,
        "average_score": 84.2
      }
    ]
  }
}
```

### PUT /evaluations/{evaluation_id}
Update an evaluation.

**Request Body:**
```json
{
  "total_score": 88.5,
  "comments": "Updated comment"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Evaluation updated successfully"
}
```

---

## 📈 Analytics Endpoints

### GET /analytics/dashboard (Admin Only)
Get global analytics dashboard.

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "total_regions": 3,
    "total_users": 150,
    "total_candidates": 500,
    "total_evaluations": 2300,
    "regions_breakdown": [
      {
        "region_name": "North America",
        "judges_count": 20,
        "candidates_count": 150,
        "evaluations_count": 800,
        "average_score": 83.5
      }
    ]
  }
}
```

### GET /analytics/region (Superjudge Only)
Get regional analytics.

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "judges_count": 20,
    "approved_judges": 15,
    "pending_judges": 5,
    "candidates_count": 150,
    "evaluations_count": 800,
    "average_score": 83.5,
    "completion_percentage": 85
  }
}
```

---

## ❌ Error Responses

### 400 Bad Request
```json
{
  "success": false,
  "error": "INVALID_INPUT",
  "message": "Invalid email format"
}
```

### 401 Unauthorized
```json
{
  "success": false,
  "error": "UNAUTHORIZED",
  "message": "Invalid credentials"
}
```

### 403 Forbidden
```json
{
  "success": false,
  "error": "FORBIDDEN",
  "message": "You do not have permission to access this resource"
}
```

### 404 Not Found
```json
{
  "success": false,
  "error": "NOT_FOUND",
  "message": "Candidate not found"
}
```

### 500 Internal Server Error
```json
{
  "success": false,
  "error": "INTERNAL_ERROR",
  "message": "An unexpected error occurred"
}
```
