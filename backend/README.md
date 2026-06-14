# Backend - Quiz Judging Application

FastAPI-based backend for the Quiz Judging Application.

## 🚀 Setup

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Server

```bash
python main.py
```

Server will start on `http://localhost:8000`

## 📚 API Documentation

Once the server is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🔑 Test Credentials

### Judges
- `judge1` / `pass123`
- `judge2` / `pass123`
- `judge3` / `pass123`

### Super Judge
- `superjudge` / `superpass`

## 🛠️ API Endpoints

### Authentication
```
POST /api/login
  - Login with username and password
  - Returns: token, user info

POST /api/logout
  - Logout (invalidate token)

GET /api/verify?token=<token>
  - Verify if token is valid
```

### Candidates
```
GET /api/candidates?token=<token>
  - Get all candidates
```

### Marks
```
POST /api/marks?token=<token>
  - Submit marks for a candidate
  - Body: {"candidate_id": int, "score": 0-100}

GET /api/marks?token=<token>
  - Get marks (filtered by role)
  - Judges: see only their marks
  - Super Judge: see all marks

GET /api/marks/{candidate_id}?token=<token>
  - Get marks for specific candidate
  - Judges: see only their mark
  - Super Judge: see all marks with average/total

GET /api/leaderboard?token=<token>
  - Get leaderboard (Super Judge only)
  - Returns candidates sorted by average score

GET /api/stats?token=<token>
  - Get overall statistics (Super Judge only)
```

## 📊 Data Structure

### User Object
```json
{
  "user_id": "judge1",
  "username": "judge1",
  "role": "judge",
  "name": "Judge 1"
}
```

### Candidate Object
```json
{
  "id": 1,
  "name": "Alice Johnson"
}
```

### Mark Object
```json
{
  "judge_id": "judge1",
  "candidate_id": 1,
  "score": 85
}
```

## 🔒 Security Features

- Token-based authentication
- Basic password encoding (base64 - not for production)
- Role-based access control
- Judges isolated from each other's marks
- Super Judge has full access

## 🧪 Testing with cURL

### Login
```bash
curl -X POST "http://localhost:8000/api/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "judge1", "password": "pass123"}'
```

### Get Candidates
```bash
curl "http://localhost:8000/api/candidates?token=<YOUR_TOKEN>"
```

### Submit Marks
```bash
curl -X POST "http://localhost:8000/api/marks?token=<YOUR_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"candidate_id": 1, "score": 85}'
```

### Get Your Marks
```bash
curl "http://localhost:8000/api/marks?token=<YOUR_TOKEN>"
```

## 📝 Notes

- All data is in-memory and resets on server restart
- No database is required
- This is a demonstration application
- For production, use proper authentication (JWT), password hashing (bcrypt), and a database
