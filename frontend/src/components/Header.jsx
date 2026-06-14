import React from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'

const Header = ({ user, onLogout }) => {
  const navigate = useNavigate()

  const handleLogout = async () => {
    try {
      const token = localStorage.getItem('token')
      await axios.post('http://localhost:8000/api/logout', null, {
        params: { token }
      })
      
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      onLogout()
      navigate('/login')
    } catch (error) {
      console.error('Logout error:', error)
      // Still logout locally even if API call fails
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      onLogout()
      navigate('/login')
    }
  }

  return (
    <header style={styles.header}>
      <div style={styles.container}>
        <div style={styles.logo}>
          <h1 style={styles.title}>🎯 Quiz Judging</h1>
        </div>
        
        <div style={styles.userInfo}>
          <div style={styles.userDetails}>
            <span style={styles.userName}>{user?.name}</span>
            <span style={styles.role}>{user?.role === 'superjudge' ? '👑 Super Judge' : '🧑‍⚖️ Judge'}</span>
          </div>
          <button 
            onClick={handleLogout}
            style={styles.logoutBtn}
          >
            Logout
          </button>
        </div>
      </div>
    </header>
  )
}

const styles = {
  header: {
    backgroundColor: 'var(--primary)',
    color: 'white',
    padding: '1rem 0',
    boxShadow: '0 1px 3px 0 rgba(0, 0, 0, 0.1)',
    marginBottom: '2rem'
  },
  container: {
    maxWidth: '1200px',
    margin: '0 auto',
    padding: '0 1rem',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center'
  },
  logo: {
    flex: 1
  },
  title: {
    margin: 0,
    fontSize: '1.5rem',
    fontWeight: '700'
  },
  userInfo: {
    display: 'flex',
    alignItems: 'center',
    gap: '1.5rem'
  },
  userDetails: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'flex-end',
    gap: '0.25rem'
  },
  userName: {
    fontWeight: '600',
    fontSize: '0.95rem'
  },
  role: {
    fontSize: '0.85rem',
    opacity: 0.9
  },
  logoutBtn: {
    backgroundColor: 'rgba(255, 255, 255, 0.2)',
    color: 'white',
    border: '1px solid rgba(255, 255, 255, 0.3)',
    padding: '0.5rem 1rem',
    borderRadius: '0.5rem',
    cursor: 'pointer',
    fontSize: '0.9rem',
    transition: 'all 0.2s'
  }
}

export default Header
