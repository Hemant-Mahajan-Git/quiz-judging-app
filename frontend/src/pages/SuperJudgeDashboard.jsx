import React, { useState, useEffect } from 'react'
import axios from 'axios'
import Header from '../components/Header'
import './Dashboard.css'

const SuperJudgeDashboard = ({ user, onLogout }) => {
  const [candidates, setCandidates] = useState([])
  const [allMarks, setAllMarks] = useState([])
  const [leaderboard, setLeaderboard] = useState([])
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [activeTab, setActiveTab] = useState('marks') // 'marks' or 'leaderboard'

  const token = localStorage.getItem('token')

  useEffect(() => {
    fetchAllData()
    // Refresh every 10 seconds
    const interval = setInterval(fetchAllData, 10000)
    return () => clearInterval(interval)
  }, [])

  const fetchAllData = async () => {
    try {
      setError('')

      // Fetch candidates
      const candidatesRes = await axios.get('http://localhost:8000/api/candidates', {
        params: { token }
      })
      setCandidates(candidatesRes.data)

      // Fetch all marks
      const marksRes = await axios.get('http://localhost:8000/api/marks', {
        params: { token }
      })
      setAllMarks(marksRes.data)

      // Fetch leaderboard
      const leaderboardRes = await axios.get('http://localhost:8000/api/leaderboard', {
        params: { token }
      })
      setLeaderboard(leaderboardRes.data)

      // Fetch stats
      const statsRes = await axios.get('http://localhost:8000/api/stats', {
        params: { token }
      })
      setStats(statsRes.data)

      setLoading(false)
    } catch (err) {
      setError('Failed to load data')
      console.error(err)
      setLoading(false)
    }
  }

  const getMark = (candidateId, judgeId) => {
    const mark = allMarks.find(
      m => m.candidate_id === candidateId && m.judge_id === judgeId
    )
    return mark ? mark.score : '-'
  }

  const getAverageScore = (candidateId) => {
    const marks = allMarks.filter(m => m.candidate_id === candidateId)
    if (marks.length === 0) return 0
    const avg = marks.reduce((sum, m) => sum + m.score, 0) / marks.length
    return avg.toFixed(2)
  }

  const getScoreBadgeClass = (score) => {
    if (score === '-') return 'score-badge'
    const numScore = parseInt(score)
    if (numScore >= 80) return 'score-badge high'
    if (numScore >= 60) return 'score-badge medium'
    return 'score-badge low'
  }

  const getUniqueJudges = () => {
    const judges = new Set(allMarks.map(m => m.judge_id))
    return Array.from(judges).sort()
  }

  if (loading) {
    return (
      <>
        <Header user={user} onLogout={onLogout} />
        <div style={{ textAlign: 'center', padding: '2rem' }}>
          Loading...
        </div>
      </>
    )
  }

  const judges = getUniqueJudges()

  return (
    <>
      <Header user={user} onLogout={onLogout} />
      
      <div className="container">
        <div className="dashboard-header">
          <h2>👑 Super Judge Dashboard</h2>
          <p>View all marks and candidate scores</p>
        </div>

        {error && <div className="alert alert-error">{error}</div>}

        {/* Stats Cards */}
        {stats && (
          <div className="grid grid-3" style={{ marginBottom: '2rem' }}>
            <div className="card stats-card">
              <h4 style={{ margin: '0 0 0.5rem 0', color: 'var(--gray-600)' }}>Total Candidates</h4>
              <div style={{ fontSize: '2rem', fontWeight: '700', color: 'var(--primary)' }}>
                {stats.total_candidates}
              </div>
            </div>
            
            <div className="card stats-card">
              <h4 style={{ margin: '0 0 0.5rem 0', color: 'var(--gray-600)' }}>Total Judges</h4>
              <div style={{ fontSize: '2rem', fontWeight: '700', color: 'var(--primary)' }}>
                {stats.total_judges}
              </div>
            </div>
            
            <div className="card stats-card">
              <h4 style={{ margin: '0 0 0.5rem 0', color: 'var(--gray-600)' }}>Average Score</h4>
              <div style={{ fontSize: '2rem', fontWeight: '700', color: 'var(--primary)' }}>
                {stats.average_score}
              </div>
            </div>
          </div>
        )}

        {/* Tabs */}
        <div style={{ display: 'flex', gap: '1rem', marginBottom: '1.5rem' }}>
          <button
            onClick={() => setActiveTab('marks')}
            style={{
              padding: '0.75rem 1.5rem',
              backgroundColor: activeTab === 'marks' ? 'var(--primary)' : 'var(--gray-200)',
              color: activeTab === 'marks' ? 'white' : 'var(--gray-700)',
              border: 'none',
              borderRadius: '0.5rem',
              cursor: 'pointer',
              fontSize: '1rem',
              fontWeight: '500'
            }}
          >
            📋 All Marks
          </button>
          
          <button
            onClick={() => setActiveTab('leaderboard')}
            style={{
              padding: '0.75rem 1.5rem',
              backgroundColor: activeTab === 'leaderboard' ? 'var(--primary)' : 'var(--gray-200)',
              color: activeTab === 'leaderboard' ? 'white' : 'var(--gray-700)',
              border: 'none',
              borderRadius: '0.5rem',
              cursor: 'pointer',
              fontSize: '1rem',
              fontWeight: '500'
            }}
          >
            🏆 Leaderboard
          </button>
        </div>

        {/* Marks Table */}
        {activeTab === 'marks' && (
          <div className="card">
            <h3 style={{ marginTop: 0 }}>All Candidates & Marks</h3>
            
            {candidates.length === 0 ? (
              <div className="empty-state">
                <p>No candidates available</p>
              </div>
            ) : (
              <div style={{ overflowX: 'auto' }}>
                <table className="marks-table">
                  <thead>
                    <tr>
                      <th>Candidate</th>
                      {judges.map(judge => (
                        <th key={judge}>{judge}</th>
                      ))}
                      <th>Average</th>
                    </tr>
                  </thead>
                  <tbody>
                    {candidates.map(candidate => (
                      <tr key={candidate.id}>
                        <td>
                          <strong>{candidate.name}</strong>
                          <div style={{ fontSize: '0.85rem', color: 'var(--gray-500)' }}>ID: {candidate.id}</div>
                        </td>
                        {judges.map(judge => {
                          const score = getMark(candidate.id, judge)
                          return (
                            <td key={`${candidate.id}-${judge}`}>
                              <span className={getScoreBadgeClass(score)}>
                                {score}
                              </span>
                            </td>
                          )
                        })}
                        <td>
                          <strong style={{ color: 'var(--primary)', fontSize: '1.1rem' }}>
                            {getAverageScore(candidate.id)}
                          </strong>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        )}

        {/* Leaderboard */}
        {activeTab === 'leaderboard' && (
          <div>
            <div className="section-title">Leaderboard</div>
            
            {leaderboard.length === 0 ? (
              <div className="card empty-state">
                <p>No scores yet</p>
              </div>
            ) : (
              <div className="leaderboard">
                {leaderboard.map((item, index) => {
                  let rankClass = 'other'
                  if (index === 0) rankClass = 'top-1'
                  else if (index === 1) rankClass = 'top-2'
                  else if (index === 2) rankClass = 'top-3'

                  return (
                    <div key={item.candidate_id} className={`leaderboard-item ${rankClass}`}>
                      <div className="leaderboard-rank">
                        {index === 0 ? '🥇' : index === 1 ? '🥈' : index === 2 ? '🥉' : index + 1}
                      </div>
                      
                      <div className="leaderboard-details">
                        <div className="leaderboard-name">{item.candidate_name}</div>
                        <div className="leaderboard-meta">ID: {item.candidate_id} • Judges: {item.judges_count}</div>
                      </div>
                      
                      <div className="leaderboard-score">
                        <div className="leaderboard-avg">{item.average_score}</div>
                        <div className="leaderboard-judges">Total: {item.total_score}</div>
                      </div>
                    </div>
                  )
                })}
              </div>
            )}
          </div>
        )}
      </div>
    </>
  )
}

export default SuperJudgeDashboard
