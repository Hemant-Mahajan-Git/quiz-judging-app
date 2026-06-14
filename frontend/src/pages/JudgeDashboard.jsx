import React, { useState, useEffect } from 'react'
import axios from 'axios'
import Header from '../components/Header'
import './Dashboard.css'

const JudgeDashboard = ({ user, onLogout }) => {
  const [candidates, setCandidates] = useState([])
  const [marks, setMarks] = useState({})
  const [submittedMarks, setSubmittedMarks] = useState({})
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [submitting, setSubmitting] = useState(false)

  const token = localStorage.getItem('token')

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      setLoading(true)
      setError('')

      // Fetch candidates
      const candidatesRes = await axios.get('http://localhost:8000/api/candidates', {
        params: { token }
      })
      setCandidates(candidatesRes.data)

      // Fetch marks submitted by this judge
      const marksRes = await axios.get('http://localhost:8000/api/marks', {
        params: { token }
      })
      
      const marksMap = {}
      marksRes.data.forEach(mark => {
        marksMap[mark.candidate_id] = mark.score
      })
      setSubmittedMarks(marksMap)
    } catch (err) {
      setError('Failed to load data')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleMarkChange = (candidateId, value) => {
    const numValue = value === '' ? '' : Math.min(100, Math.max(0, parseInt(value) || 0))
    setMarks(prev => ({
      ...prev,
      [candidateId]: numValue
    }))
    setSuccess('') // Clear success message when user starts editing
  }

  const handleSubmitMark = async (candidateId) => {
    const score = marks[candidateId]
    
    if (score === '' || score === undefined) {
      setError('Please enter a score')
      return
    }

    if (score < 0 || score > 100) {
      setError('Score must be between 0 and 100')
      return
    }

    try {
      setSubmitting(true)
      setError('')
      setSuccess('')

      await axios.post('http://localhost:8000/api/marks', 
        {
          candidate_id: candidateId,
          score: parseInt(score)
        },
        { params: { token } }
      )

      // Update submitted marks
      setSubmittedMarks(prev => ({
        ...prev,
        [candidateId]: score
      }))
      
      // Clear the input
      setMarks(prev => ({
        ...prev,
        [candidateId]: ''
      }))
      
      setSuccess(`Mark submitted for candidate ${candidateId}`)
      setTimeout(() => setSuccess(''), 3000)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to submit mark')
    } finally {
      setSubmitting(false)
    }
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

  return (
    <>
      <Header user={user} onLogout={onLogout} />
      
      <div className="container">
        <div className="dashboard-header">
          <h2>Judge Dashboard</h2>
          <p>Assign marks to candidates</p>
        </div>

        {error && <div className="alert alert-error">{error}</div>}
        {success && <div className="alert alert-success">{success}</div>}

        <div className="dashboard-content">
          <div className="candidates-list">
            <div className="section-title">Candidates</div>
            
            {candidates.length === 0 ? (
              <div className="empty-state">
                <p>No candidates available</p>
              </div>
            ) : (
              <div className="grid grid-2">
                {candidates.map(candidate => (
                  <div key={candidate.id} className="card candidate-card">
                    <div className="candidate-header">
                      <h3>{candidate.name}</h3>
                      <span className="candidate-id">ID: {candidate.id}</span>
                    </div>

                    <div className="marks-section">
                      {submittedMarks[candidate.id] !== undefined ? (
                        <div className="submitted-mark">
                          <div className="mark-label">Your Mark</div>
                          <div className="mark-value">{submittedMarks[candidate.id]}/100</div>
                        </div>
                      ) : (
                        <div className="no-mark">
                          <p>No mark submitted</p>
                        </div>
                      )}
                    </div>

                    <div className="input-group">
                      <input
                        type="number"
                        min="0"
                        max="100"
                        value={marks[candidate.id] ?? ''}
                        onChange={(e) => handleMarkChange(candidate.id, e.target.value)}
                        placeholder="Enter score (0-100)"
                        disabled={submitting}
                      />
                      <button
                        onClick={() => handleSubmitMark(candidate.id)}
                        className="btn-primary btn-small"
                        disabled={submitting || marks[candidate.id] === undefined || marks[candidate.id] === ''}
                      >
                        {submitting ? 'Submitting...' : 'Submit'}
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          <div className="sidebar">
            <div className="card stats-card">
              <h3>Your Stats</h3>
              <div className="stat-item">
                <span className="stat-label">Total Candidates</span>
                <span className="stat-value">{candidates.length}</span>
              </div>
              <div className="stat-item">
                <span className="stat-label">Marks Submitted</span>
                <span className="stat-value">{Object.keys(submittedMarks).length}</span>
              </div>
              <div className="stat-item">
                <span className="stat-label">Remaining</span>
                <span className="stat-value">{candidates.length - Object.keys(submittedMarks).length}</span>
              </div>
            </div>

            <div className="card info-card">
              <h3>📋 Guidelines</h3>
              <ul className="guidelines">
                <li>Score range: 0-100</li>
                <li>You can update marks anytime</li>
                <li>Your marks are private</li>
                <li>Only you can see your marks</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </>
  )
}

export default JudgeDashboard
