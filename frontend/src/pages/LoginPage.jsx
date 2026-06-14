import React, { useState } from 'react'
import axios from 'axios'
import './LoginPage.css'

const LoginPage = ({ onLogin }) => {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      const response = await axios.post('http://localhost:8000/api/login', {
        username,
        password
      })

      const { token, user } = response.data
      onLogin(token, user)
    } catch (err) {
      setError(err.response?.data?.detail || 'Login failed. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const demoAccounts = [
    { username: 'judge1', password: 'pass123', role: 'Judge 1' },
    { username: 'judge2', password: 'pass123', role: 'Judge 2' },
    { username: 'judge3', password: 'pass123', role: 'Judge 3' },
    { username: 'superjudge', password: 'superpass', role: 'Super Judge' }
  ]

  const fillDemo = (user) => {
    setUsername(user.username)
    setPassword(user.password)
  }

  return (
    <div className="login-container">
      <div className="login-wrapper">
        <div className="login-header">
          <h1>🎯 Quiz Judging Application</h1>
          <p>Role-Based Judging System</p>
        </div>

        <form onSubmit={handleSubmit} className="login-form">
          {error && <div className="alert alert-error">{error}</div>}

          <div className="form-group">
            <label htmlFor="username">Username</label>
            <input
              type="text"
              id="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Enter username"
              disabled={loading}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter password"
              disabled={loading}
              required
            />
          </div>

          <button 
            type="submit" 
            className="btn-primary" 
            disabled={loading}
            style={{ width: '100%' }}
          >
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>

        <div className="demo-section">
          <h3>Demo Accounts</h3>
          <div className="demo-accounts">
            {demoAccounts.map((account) => (
              <div key={account.username} className="demo-account">
                <div className="demo-info">
                  <div className="demo-role">{account.role}</div>
                  <div className="demo-creds">
                    <small>{account.username} / {account.password}</small>
                  </div>
                </div>
                <button
                  type="button"
                  className="btn-outline btn-small"
                  onClick={() => fillDemo(account)}
                >
                  Use
                </button>
              </div>
            ))}
          </div>
        </div>

        <div className="info-section">
          <h3>ℹ️ How It Works</h3>
          <ul>
            <li><strong>Judges:</strong> Can view candidates and assign marks. Marks are private - other judges cannot see them.</li>
            <li><strong>Super Judge:</strong> Can view all marks from all judges and see overall statistics.</li>
            <li><strong>Marks:</strong> Score range is 0-100 for each candidate.</li>
          </ul>
        </div>
      </div>
    </div>
  )
}

export default LoginPage
