# Frontend - Quiz Judging Application

React + Vite frontend for the Quiz Judging Application.

## 🚀 Setup

### Install Dependencies

```bash
npm install
```

### Development Server

```bash
npm run dev
```

App will be available at `http://localhost:5173`

### Build for Production

```bash
npm run build
```

## 📁 Project Structure

```
src/
├── components/
│   ├── Header.jsx           # Header component with user info and logout
│   └── ProtectedRoute.jsx   # Route protection component
├── pages/
│   ├── LoginPage.jsx        # Login page
│   ├── JudgeDashboard.jsx   # Judge dashboard
│   ├── SuperJudgeDashboard.jsx  # Super judge dashboard
│   └── Dashboard.css        # Dashboard styles
├── App.jsx                  # Main app component with routing
├── index.css                # Global styles
└── main.jsx                 # Entry point
```

## 🔐 Authentication

- Uses localStorage to store auth token
- Token-based API communication
- Automatic logout on token expiration

## 🎨 Styling

- CSS-in-JS for component styles
- Global CSS file for utility classes
- Responsive design for mobile and desktop

## 🔌 API Integration

- Axios for API calls
- Base URL: `http://localhost:8000`
- All requests include authentication token

## 📱 Features

### Judge Dashboard
- View all candidates
- Assign marks (0-100)
- View only your own marks
- Update marks anytime
- Real-time validation

### Super Judge Dashboard
- View all marks from all judges
- Leaderboard with rankings
- Statistics overview
- Auto-refresh every 10 seconds

## 🚨 Troubleshooting

### Port Already in Use
```bash
npm run dev -- --port 5174
```

### Backend Not Responding
- Ensure backend is running on `http://localhost:8000`
- Check CORS configuration
- Verify API endpoints

### Authentication Issues
- Clear localStorage: `localStorage.clear()`
- Check token in browser DevTools
- Verify backend token generation
