import { useState } from 'react'

function App() {
  const [patientId, setPatientId] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const response = await fetch('/api/assess-risk', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ patient_id: patientId }),
      })

      if (!response.ok) {
        throw new Error('Failed to assess patient risk')
      }

      const data = await response.json()
      setResult(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <>
      <nav className="top-bar">
        <div className="top-bar-left">
          <span className="logo">🏥 CarePath AI</span>
        </div>
        <div className="top-bar-right">
          <div className="nav-items">
            <span>Dashboard</span>
            <span>Patients</span>
            <span>Reports</span>
          </div>
          <div className="user-profile">
            <div className="avatar">JD</div>
            <div className="user-info">
              <span className="user-name">Dr. Jane Doe</span>
              <span className="user-role">Cardiology Dept</span>
            </div>
          </div>
        </div>
      </nav>

      <div className="app-wrapper">
        <div className="container">
          <h1>
            <span role="img" aria-label="hospital" style={{ fontSize: '1.2em' }}>🏥</span> CarePath AI
          </h1>
          <p className="subtitle">
            AI-powered patient readmission risk assessment
          </p>

          <form onSubmit={handleSubmit} className="form">
            <div className="input-group">
              <label htmlFor="patientId">Select Patient</label>
              <select
                id="patientId"
                value={patientId}
                onChange={(e) => setPatientId(e.target.value)}
                required
              >
                <option value="" disabled>Select a patient to assess...</option>
                <option value="P12345">John Smith (ID: P12345) - Age 72</option>
                <option value="P67890">Mary Johnson (ID: P67890) - Age 58</option>
                <option value="P11111">Robert Williams (ID: P11111) - Age 81</option>
              </select>
            </div>
            <button type="submit" disabled={loading || !patientId}>
              {loading ? (
                <span style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px' }}>
                  <svg className="spinner" viewBox="0 0 50 50" style={{ width: '20px', height: '20px', animation: 'spin 1s linear infinite' }}>
                    <circle cx="25" cy="25" r="20" fill="none" stroke="currentColor" strokeWidth="5" strokeLinecap="round" strokeDasharray="31.4 31.4" opacity="0.3"></circle>
                    <circle cx="25" cy="25" r="20" fill="none" stroke="currentColor" strokeWidth="5" strokeLinecap="round" strokeDasharray="31.4 100" strokeDashoffset="0"></circle>
                  </svg>
                  Assessing Risk...
                </span>
              ) : (
                'Assess Readmission Risk'
              )}
            </button>
          </form>

          {error && (
            <div className="error">
              <span role="img" aria-label="error" style={{ marginRight: '8px' }}>⚠️</span>
              <strong>Error:</strong> {error}
            </div>
          )}

          {result && (
            <div className="result">
              <h2>
                <span role="img" aria-label="analytics" style={{ marginRight: '8px' }}>📊</span>
                Assessment Result
              </h2>
              <pre>{JSON.stringify(result, null, 2)}</pre>
            </div>
          )}
        </div>
      </div>
    </>
  )
}

export default App
