import { useState, useEffect } from 'react'

function cleanText(text) {
  if (!text) return ''
  return text
    .replace(/\*\*/g, '')
    .replace(/\*([^*]+)\*/g, '$1')
    .replace(/`([^`]+)`/g, '$1')
    .trim()
}

function cleanIntervention(text) {
  let cleaned = cleanText(text)
  cleaned = cleaned.replace(/\s*Confirmation:\s*\{.*\}\s*$/s, '')
  cleaned = cleaned.replace(/\s*\{[^}]*"status"[^}]*\}\s*/g, '')
  return cleaned.trim()
}

function getInterventionMeta(text) {
  const lower = text.toLowerCase()
  if (lower.includes('medication') || lower.includes('reminder'))
    return { icon: '\u{1F48A}', label: 'Medication Reminder', color: '#8b5cf6' }
  if (lower.includes('social worker') || lower.includes('referral'))
    return { icon: '\u{1F91D}', label: 'Social Worker Referral', color: '#3b82f6' }
  if (lower.includes('home health') || lower.includes('visit'))
    return { icon: '\u{1F3E0}', label: 'Home Health Visit', color: '#10b981' }
  if (lower.includes('appointment') || lower.includes('follow'))
    return { icon: '\u{1F4C5}', label: 'Follow-up Appointment', color: '#f59e0b' }
  return { icon: '\u2705', label: 'Action', color: '#6b7280' }
}

function RiskBadge({ level }) {
  const config = {
    high: { label: 'HIGH RISK', className: 'badge-high' },
    moderate: { label: 'MODERATE RISK', className: 'badge-moderate' },
    low: { label: 'LOW RISK', className: 'badge-low' },
  }
  const c = config[level] || { label: level?.toUpperCase() || 'UNKNOWN', className: 'badge-unknown' }
  return <span className={`risk-badge ${c.className}`}>{c.label}</span>
}

function RiskGauge({ score }) {
  if (score == null) return null
  const color = score > 60 ? '#ef4444' : score > 30 ? '#f59e0b' : '#16a34a'
  const arcLength = Math.max((score / 100) * 251.2, 1)
  return (
    <div className="gauge-container">
      <svg viewBox="0 0 200 130" className="gauge-svg">
        <path d="M 20 110 A 80 80 0 0 1 180 110" fill="none" stroke="#e5e7eb" strokeWidth="14" strokeLinecap="round" />
        <path d="M 20 110 A 80 80 0 0 1 180 110" fill="none" stroke={color} strokeWidth="14" strokeLinecap="round"
          strokeDasharray={`${arcLength} 251.2`}
          style={{ transition: 'stroke-dasharray 1s ease-out' }} />
        <text x="30" y="128" fill="#9ca3af" fontSize="10" fontFamily="inherit">0</text>
        <text x="160" y="128" fill="#9ca3af" fontSize="10" fontFamily="inherit">100</text>
      </svg>
      <div className="gauge-score">{score}</div>
      <div className="gauge-sublabel">out of 100</div>
    </div>
  )
}

function App() {
  const [patients, setPatients] = useState([])
  const [patientId, setPatientId] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetch('/api/patients')
      .then(res => res.json())
      .then(data => setPatients(data))
      .catch(() => {})
  }, [])

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const response = await fetch('/api/assess-risk', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ patient_id: patientId }),
      })

      if (!response.ok) {
        const detail = await response.json().catch(() => ({}))
        throw new Error(detail.detail || 'Failed to assess patient risk')
      }

      const data = await response.json()
      setResult(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const getPatientName = (id) => {
    const p = patients.find(pt => pt.id === id)
    return p ? p.name : id
  }

  const hasResult = result && result.status === 'completed'
  const showRightPanel = loading || hasResult || error || (result && result.status === 'error')

  return (
    <>
      <nav className="top-bar">
        <div className="top-bar-left">
          <span className="logo">CarePath AI</span>
        </div>
        <div className="top-bar-right">
          <div className="nav-items">
            <span className="nav-active">Dashboard</span>
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

      <div className={`app-wrapper ${showRightPanel ? 'has-result' : ''}`}>
        {/* Left panel: form */}
        <div className="panel-form">
          <div className="form-card">
            <h1>CarePath AI</h1>
            <p className="subtitle">AI-powered readmission risk assessment</p>

            <form onSubmit={handleSubmit} className="form">
              <div className="input-group">
                <label htmlFor="patientId">Select Patient</label>
                <select
                  id="patientId"
                  value={patientId}
                  onChange={(e) => setPatientId(e.target.value)}
                  required
                >
                  <option value="" disabled>Select a patient...</option>
                  {patients.map(p => (
                    <option key={p.id} value={p.id}>
                      {p.name} (ID: {p.id}) - Age {p.age}
                    </option>
                  ))}
                </select>
              </div>
              <button type="submit" disabled={loading || !patientId}>
                {loading ? (
                  <span className="btn-loading">
                    <svg className="spinner" viewBox="0 0 50 50">
                      <circle cx="25" cy="25" r="20" fill="none" stroke="currentColor" strokeWidth="5" strokeLinecap="round" strokeDasharray="31.4 31.4" opacity="0.3" />
                      <circle cx="25" cy="25" r="20" fill="none" stroke="currentColor" strokeWidth="5" strokeLinecap="round" strokeDasharray="31.4 100" strokeDashoffset="0" />
                    </svg>
                    Analyzing...
                  </span>
                ) : (
                  'Assess Risk'
                )}
              </button>
            </form>
          </div>
        </div>

        {/* Right panel */}
        {showRightPanel && (
          <div className="panel-result">
            {/* Loading skeleton */}
            {loading && (
              <div className="loading-panel">
                <div className="loading-header">
                  <div className="skeleton skeleton-title" />
                  <div className="skeleton skeleton-badge" />
                </div>
                <div className="loading-steps">
                  <div className="loading-step active">
                    <div className="step-dot">
                      <svg className="spinner-sm" viewBox="0 0 50 50">
                        <circle cx="25" cy="25" r="20" fill="none" stroke="#8b5cf6" strokeWidth="5" strokeLinecap="round" strokeDasharray="31.4 31.4" opacity="0.3" />
                        <circle cx="25" cy="25" r="20" fill="none" stroke="#8b5cf6" strokeWidth="5" strokeLinecap="round" strokeDasharray="31.4 100" strokeDashoffset="0" />
                      </svg>
                    </div>
                    <div>
                      <div className="step-label">Analyzing discharge summary</div>
                      <div className="step-sub">Clinical analyst reviewing patient records...</div>
                    </div>
                  </div>
                  <div className="loading-step">
                    <div className="step-dot pending" />
                    <div>
                      <div className="step-label">Reviewing patient history</div>
                      <div className="step-sub">Historical analyst checking FHIR data...</div>
                    </div>
                  </div>
                  <div className="loading-step">
                    <div className="step-dot pending" />
                    <div>
                      <div className="step-label">Calculating risk score</div>
                      <div className="step-sub">Synthesizing clinical and social factors...</div>
                    </div>
                  </div>
                  <div className="loading-step">
                    <div className="step-dot pending" />
                    <div>
                      <div className="step-label">Generating intervention plan</div>
                      <div className="step-sub">Scheduling follow-ups and referrals...</div>
                    </div>
                  </div>
                </div>
                <div className="result-top-row">
                  <div className="card skeleton-card"><div className="skeleton skeleton-gauge" /></div>
                  <div className="card skeleton-card"><div className="skeleton skeleton-rec" /></div>
                </div>
                <div className="result-bottom-row">
                  <div className="card skeleton-card">
                    <div className="skeleton skeleton-line" />
                    <div className="skeleton skeleton-line short" />
                    <div className="skeleton skeleton-line" />
                  </div>
                  <div className="card skeleton-card">
                    <div className="skeleton skeleton-line" />
                    <div className="skeleton skeleton-line short" />
                    <div className="skeleton skeleton-line" />
                  </div>
                </div>
              </div>
            )}

            {/* Error */}
            {!loading && (error || (result && result.status === 'error')) && (
              <div className="error">
                <strong>Error:</strong> {error || result?.message}
              </div>
            )}

            {/* Results */}
            {!loading && hasResult && (
              <>
                <div className="result-header-bar">
                  <div>
                    <h2>Risk Assessment Report</h2>
                    <span className="patient-label">
                      {getPatientName(result.patient_id)} ({result.patient_id})
                    </span>
                  </div>
                  {result.risk_level && <RiskBadge level={result.risk_level} />}
                </div>

                <div className="result-top-row">
                  <div className="card score-card">
                    <RiskGauge score={result.risk_score} />
                  </div>
                  {result.discharge_recommendation && (
                    <div className={`card discharge-card ${result.discharge_recommendation === 'hold_discharge_for_review' ? 'rec-hold' : 'rec-proceed'}`}>
                      <div className="rec-icon">
                        {result.discharge_recommendation === 'hold_discharge_for_review' ? '\u26A0\uFE0F' : '\u2705'}
                      </div>
                      <div className="rec-label">Discharge Recommendation</div>
                      <div className="rec-value">
                        {result.discharge_recommendation === 'hold_discharge_for_review'
                          ? 'Hold for Review'
                          : 'Proceed with Discharge'}
                      </div>
                    </div>
                  )}
                </div>

                <div className="result-bottom-row">
                  {result.risk_factors && result.risk_factors.length > 0 && (
                    <div className="card">
                      <h3>
                        <span className="section-icon">{'\u26A0'}</span>
                        Risk Factors
                        <span className="section-count">{result.risk_factors.length}</span>
                      </h3>
                      <div className="card-scroll">
                        <ul className="factor-list">
                          {result.risk_factors.map((factor, i) => (
                            <li key={i}>{cleanText(factor)}</li>
                          ))}
                        </ul>
                      </div>
                    </div>
                  )}

                  {result.intervention_plan && result.intervention_plan.length > 0 && (
                    <div className="card">
                      <h3>
                        <span className="section-icon">{'\u2714'}</span>
                        Intervention Plan
                        <span className="section-count">{result.intervention_plan.length}</span>
                      </h3>
                      <div className="card-scroll">
                        <div className="intervention-cards">
                          {result.intervention_plan.map((item, i) => {
                            const meta = getInterventionMeta(item)
                            const cleaned = cleanIntervention(item)
                            return (
                              <div key={i} className="intervention-card">
                                <div className="intervention-icon-wrapper" style={{ background: `${meta.color}12`, color: meta.color }}>
                                  <span className="intervention-icon">{meta.icon}</span>
                                </div>
                                <div className="intervention-content">
                                  <div className="intervention-type" style={{ color: meta.color }}>{meta.label}</div>
                                  <div className="intervention-detail">{cleaned}</div>
                                </div>
                              </div>
                            )
                          })}
                        </div>
                      </div>
                    </div>
                  )}
                </div>

                {result.summary && (
                  <div className="card summary-card">
                    <h3>
                      <span className="section-icon">{'\u{1F4CB}'}</span>
                      Clinical Summary
                    </h3>
                    <p>{cleanText(result.summary)}</p>
                  </div>
                )}
              </>
            )}
          </div>
        )}
      </div>
    </>
  )
}

export default App
