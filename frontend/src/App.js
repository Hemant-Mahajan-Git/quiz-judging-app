import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import axios from 'axios';
import './App.css';
import Home from './pages/Home';
import NotFound from './pages/NotFound';

function App() {
  const [backendHealth, setBackendHealth] = useState(null);

  useEffect(() => {
    // Check backend health on app load
    axios.get('/api/health')
      .then(response => {
        setBackendHealth(response.data.status);
        console.log('Backend is connected:', response.data);
      })
      .catch(error => {
        console.error('Backend connection failed:', error);
        setBackendHealth('disconnected');
      });
  }, []);

  return (
    <Router>
      <div className="App">
        <header className="App-header">
          <h1>Quiz Judging App</h1>
          <p className="backend-status">
            Backend: <span className={backendHealth === 'disconnected' ? 'error' : 'success'}>
              {backendHealth ? backendHealth : 'checking...'}
            </span>
          </p>
        </header>
        <main className="App-main">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
