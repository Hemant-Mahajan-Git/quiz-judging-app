from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import secrets
from typing import Optional, List, Dict
import base64
from datetime import datetime

app = FastAPI(
    title="Quiz Judging Application",
    description="A lightweight quiz judging system with role-based access",
    version="1.0.0"
)

# CORS middleware to allow frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# DATA MODELS
# ============================================================================

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    token: str
    user: dict
    message: str

class CandidateResponse(BaseModel):
    id: int
    name: str

class MarkRequest(BaseModel):
    candidate_id: int
    score: int  # 0-100

class MarkResponse(BaseModel):
    judge_id: str
    candidate_id: int
    score: int

class CandidateScoresResponse(BaseModel):
    candidate_id: int
    candidate_name: str
    marks: List[dict]
    average: Optional[float] = None
    total: Optional[int] = None

# ============================================================================
# IN-MEMORY DATA STORAGE
# ============================================================================

# Users with in-memory storage
USERS_DB = [
    {
        "id": "judge1",
        "username": "judge1",
        "password": base64.b64encode(b"pass123").decode(),
        "role": "judge",
        "name": "Judge 1"
    },
    {
        "id": "judge2",
        "username": "judge2",
        "password": base64.b64encode(b"pass123").decode(),
        "role": "judge",
        "name": "Judge 2"
    },
    {
        "id": "judge3",
        "username": "judge3",
        "password": base64.b64encode(b"pass123").decode(),
        "role": "judge",
        "name": "Judge 3"
    },
    {
        "id": "superjudge",
        "username": "superjudge",
        "password": base64.b64encode(b"superpass").decode(),
        "role": "superjudge",
        "name": "Super Judge"
    }
]

# Candidates database
CANDIDATES_DB = [
    {"id": 1, "name": "Alice Johnson"},
    {"id": 2, "name": "Bob Smith"},
    {"id": 3, "name": "Charlie Brown"},
    {"id": 4, "name": "Diana Prince"},
    {"id": 5, "name": "Ethan Hunt"}
]

# Marks database: {judge_id -> {candidate_id -> score}}
MARKS_DB: Dict[str, Dict[int, int]] = {}

# Active sessions: {token -> {user_id, role, username}}
ACTIVE_SESSIONS: Dict[str, dict] = {}

# ============================================================================
# AUTHENTICATION UTILITIES
# ============================================================================

def encode_password(password: str) -> str:
    """Encode password using base64 (basic encoding, not for production)"""
    return base64.b64encode(password.encode()).decode()

def verify_password(plain: str, encoded: str) -> bool:
    """Verify plain password against encoded password"""
    return encode_password(plain) == encoded

def generate_token() -> str:
    """Generate a random token"""
    return secrets.token_urlsafe(32)

def get_current_user(token: str) -> dict:
    """Get current user from token"""
    if token not in ACTIVE_SESSIONS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    return ACTIVE_SESSIONS[token]

# ============================================================================
# AUTHENTICATION ENDPOINTS
# ============================================================================

@app.post("/api/login", response_model=LoginResponse)
def login(request: LoginRequest):
    """
    Login endpoint for judges and super judge
    Returns a token on successful authentication
    """
    # Find user
    user = None
    for u in USERS_DB:
        if u["username"] == request.username:
            user = u
            break
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    # Verify password
    if not verify_password(request.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    # Generate token
    token = generate_token()
    ACTIVE_SESSIONS[token] = {
        "user_id": user["id"],
        "username": user["username"],
        "role": user["role"],
        "name": user["name"]
    }
    
    return LoginResponse(
        token=token,
        user={
            "user_id": user["id"],
            "username": user["username"],
            "role": user["role"],
            "name": user["name"]
        },
        message=f"Welcome {user['name']}!"
    )

@app.post("/api/logout")
def logout(token: str):
    """
    Logout endpoint - invalidate token
    """
    if token in ACTIVE_SESSIONS:
        del ACTIVE_SESSIONS[token]
    
    return {"message": "Logged out successfully"}

@app.get("/api/verify")
def verify_token(token: str):
    """
    Verify if token is valid
    """
    user = get_current_user(token)
    return {"valid": True, "user": user}

# ============================================================================
# CANDIDATES ENDPOINTS
# ============================================================================

@app.get("/api/candidates", response_model=List[CandidateResponse])
def get_candidates(token: str):
    """
    Get all candidates (accessible to all authenticated users)
    """
    user = get_current_user(token)
    return CANDIDATES_DB

# ============================================================================
# MARKS ENDPOINTS
# ============================================================================

@app.post("/api/marks")
def submit_marks(mark_request: MarkRequest, token: str):
    """
    Submit marks for a candidate
    Only judges can submit marks
    """
    user = get_current_user(token)
    
    # Only judges can submit marks
    if user["role"] not in ["judge", "superjudge"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only judges can submit marks"
        )
    
    # Validate score range
    if not (0 <= mark_request.score <= 100):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Score must be between 0 and 100"
        )
    
    # Validate candidate exists
    candidate = next((c for c in CANDIDATES_DB if c["id"] == mark_request.candidate_id), None)
    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found"
        )
    
    # Store mark
    judge_id = user["user_id"]
    if judge_id not in MARKS_DB:
        MARKS_DB[judge_id] = {}
    
    MARKS_DB[judge_id][mark_request.candidate_id] = mark_request.score
    
    return {
        "message": f"Marks submitted successfully for {candidate['name']}",
        "candidate_id": mark_request.candidate_id,
        "score": mark_request.score
    }

@app.get("/api/marks")
def get_marks(token: str):
    """
    Get marks
    - Judges see only their own marks
    - Super Judge sees all marks
    """
    user = get_current_user(token)
    judge_id = user["user_id"]
    
    if user["role"] == "judge":
        # Judges see only their own marks
        marks = []
        if judge_id in MARKS_DB:
            for candidate_id, score in MARKS_DB[judge_id].items():
                marks.append({
                    "judge_id": judge_id,
                    "candidate_id": candidate_id,
                    "score": score
                })
        return marks
    
    elif user["role"] == "superjudge":
        # Super Judge sees all marks
        all_marks = []
        for j_id, marks_dict in MARKS_DB.items():
            for candidate_id, score in marks_dict.items():
                all_marks.append({
                    "judge_id": j_id,
                    "candidate_id": candidate_id,
                    "score": score
                })
        return all_marks
    
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Insufficient permissions"
    )

@app.get("/api/marks/{candidate_id}")
def get_candidate_marks(candidate_id: int, token: str):
    """
    Get marks for a specific candidate
    - Judges see only their own marks for this candidate
    - Super Judge sees all marks for this candidate
    """
    user = get_current_user(token)
    judge_id = user["user_id"]
    
    # Validate candidate exists
    candidate = next((c for c in CANDIDATES_DB if c["id"] == candidate_id), None)
    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found"
        )
    
    if user["role"] == "judge":
        # Judge sees only their own mark
        if judge_id in MARKS_DB and candidate_id in MARKS_DB[judge_id]:
            score = MARKS_DB[judge_id][candidate_id]
            return CandidateScoresResponse(
                candidate_id=candidate_id,
                candidate_name=candidate["name"],
                marks=[{"judge_id": judge_id, "score": score}]
            )
        else:
            return CandidateScoresResponse(
                candidate_id=candidate_id,
                candidate_name=candidate["name"],
                marks=[]
            )
    
    elif user["role"] == "superjudge":
        # Super Judge sees all marks for this candidate
        marks = []
        for j_id, marks_dict in MARKS_DB.items():
            if candidate_id in marks_dict:
                marks.append({
                    "judge_id": j_id,
                    "score": marks_dict[candidate_id]
                })
        
        # Calculate average and total
        scores = [m["score"] for m in marks]
        average = sum(scores) / len(scores) if scores else 0
        total = sum(scores)
        
        return CandidateScoresResponse(
            candidate_id=candidate_id,
            candidate_name=candidate["name"],
            marks=marks,
            average=round(average, 2),
            total=total
        )
    
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Insufficient permissions"
    )

@app.get("/api/leaderboard")
def get_leaderboard(token: str):
    """
    Get leaderboard with all candidates and their average scores
    Only accessible to Super Judge
    """
    user = get_current_user(token)
    
    if user["role"] != "superjudge":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Super Judge can view leaderboard"
        )
    
    leaderboard = []
    
    for candidate in CANDIDATES_DB:
        marks = []
        for j_id, marks_dict in MARKS_DB.items():
            if candidate["id"] in marks_dict:
                marks.append(marks_dict[candidate["id"]])
        
        if marks:
            average = sum(marks) / len(marks)
            leaderboard.append({
                "candidate_id": candidate["id"],
                "candidate_name": candidate["name"],
                "average_score": round(average, 2),
                "total_score": sum(marks),
                "judges_count": len(marks)
            })
    
    # Sort by average score (descending)
    leaderboard.sort(key=lambda x: x["average_score"], reverse=True)
    
    return leaderboard

@app.get("/api/stats")
def get_stats(token: str):
    """
    Get overall statistics
    Only accessible to Super Judge
    """
    user = get_current_user(token)
    
    if user["role"] != "superjudge":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Super Judge can view stats"
        )
    
    total_marks_submitted = 0
    all_scores = []
    
    for j_id, marks_dict in MARKS_DB.items():
        total_marks_submitted += len(marks_dict)
        all_scores.extend(marks_dict.values())
    
    average_score = sum(all_scores) / len(all_scores) if all_scores else 0
    
    return {
        "total_marks_submitted": total_marks_submitted,
        "total_candidates": len(CANDIDATES_DB),
        "total_judges": len([u for u in USERS_DB if u["role"] == "judge"]),
        "average_score": round(average_score, 2),
        "judges_with_submissions": len(MARKS_DB)
    }

# ============================================================================
# HEALTH CHECK
# ============================================================================

@app.get("/api/health")
def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "Quiz Judging Application"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
