# Quiz Judging Application

A lightweight web-based quiz judging system with role-based access control. Judges can assign marks to candidates while maintaining privacy of their own marks. The Super Judge has full visibility of all marks from all judges.

## 🎯 Features

- **Authentication System**: Simple in-memory login (3 Judges + 1 Super Judge)
- **Judge Dashboard**: View candidates and assign marks privately
- **Super Judge Dashboard**: View all marks from all judges
- **Role-Based Access**: Judges restricted to own marks, Super Judge has full access
- **In-Memory Storage**: No database required, data resets on server restart
- **Basic Security**: Token-based authentication

## 📋 Credentials

### Judge Accounts
- **Judge 1**: username: `judge1`, password: `pass123`
- **Judge 2**: username: `judge2`, password: `pass123`
- **Judge 3**: username: `judge3`, password: `pass123`

### Super Judge Account
- **Super Judge**: username: `superjudge`, password: `superpass`

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
python main.py
```

Backend runs on: `http://localhost:8000`

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on: `http://localhost:5173`

## 📁 Project Structure

```
quiz-judging-app/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── requirements.txt         # Python dependencies
│   └── README.md               # Backend documentation
├── frontend/
│   ├── src/
│   │   ├── components/         # React components
│   │   ├── pages/              # Page components
│   │   ├── App.jsx             # Main app component
│   │   └── main.jsx            # Entry point
│   ├── package.json            # Node dependencies
│   ├── vite.config.js          # Vite configuration
│   └── README.md               # Frontend documentation
├── README.md                   # This file
└── .gitignore
```

## 🔐 Security Features

- In-memory token-based authentication
- Judges can only view their own marks
- Super Judge has unrestricted access
- Passwords not stored in plain text (basic encoding)

## 📊 Data Structure

### Users
```python
users = [
    {"username": "judge1", "password_hash": "...", "role": "judge"},
    {"username": "superjudge", "password_hash": "...", "role": "superjudge"}
]
```

### Candidates
```python
candidates = [
    {"id": 1, "name": "Candidate 1"},
    {"id": 2, "name": "Candidate 2"}
]
```

### Marks
```python
marks = [
    {"judge_id": "judge1", "candidate_id": 1, "score": 85},
    {"judge_id": "judge2", "candidate_id": 1, "score": 90}
]
```

## 🎮 Usage

1. **Login**: Enter credentials from the credentials list above
2. **Judge View**:
   - See all candidates
   - Assign marks (0-100)
   - View only your own submitted marks
   - Cannot see other judges' marks
3. **Super Judge View**:
   - See all candidates
   - View marks from ALL judges
   - See total and average scores

## 🛠️ API Endpoints

### Authentication
- `POST /api/login` - Login with username/password
- `POST /api/logout` - Logout

### Candidates
- `GET /api/candidates` - Get all candidates

### Marks
- `GET /api/marks` - Get marks (filtered by role)
- `POST /api/marks` - Submit marks
- `GET /api/marks/<candidate_id>` - Get marks for specific candidate

## 📝 Notes

- All data is stored in-memory and will be reset when the server restarts
- This is a demonstration application and not suitable for production
- Judges are completely isolated from each other's marks
- Super Judge has complete visibility and administrative access

## 🔄 Workflow

```
Candidate Registration → Judge Login → Assign Marks → Super Judge Reviews All Marks
```

## 📄 License

MIT
