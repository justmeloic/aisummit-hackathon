import { useState, useEffect } from 'react'

function cleanText(text) {
  if (!text) return ''
  return text.replace(/\*\*/g, '').replace(/\*([^*]+)\*/g, '$1').replace(/`([^`]+)`/g, '$1').trim()
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
  const arcLength = Math.max((score / 100) * 251.2, 12)
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

  const handleAssess = (id) => {
    setPatientId(id)
    setLoading(true)
    setError(null)
    setResult(null)

    fetch('/api/assess-risk', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ patient_id: id }),
    })
      .then(async res => {
        if (!res.ok) {
          const detail = await res.json().catch(() => ({}))
          throw new Error(detail.detail || 'Failed to assess patient risk')
        }
        return res.json()
      })
      .then(data => setResult(data))
      .catch(err => setError(err.message))
      .finally(() => setLoading(false))
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    if (patientId) handleAssess(patientId)
  }

  const getPatientName = (id) => {
    const p = patients.find(pt => pt.id === id)
    return p ? p.name : id
  }

  const getInitials = (name) => name.split(' ').map(n => n[0]).join('').toUpperCase()

  const patientPhotos = {
    alice_johnson: '/alice.png',
    bob_smith: '/bob.webp',
    charlie_davis: '/charlie.png',
  }

  const hasResult = result && result.status === 'completed'
  const showReport = loading || hasResult || error || (result && result.status === 'error')

  return (
    <>
      <nav className="top-bar">
        <div className="top-bar-left">
          <img src="/logo.png" alt="CarePath AI" className="logo-img" /><span className="logo">CarePath AI</span>
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

      <div className={`app-wrapper ${showReport ? 'has-result' : ''}`}>
        {/* Left panel */}
        <div className="panel-form">
          {/* Dashboard header */}
          <div className="dash-header">
            <h1>Discharge Dashboard</h1>
            <p className="subtitle">Patients pending readmission risk assessment</p>
          </div>

          {/* Stats row */}
          <div className="stats-row">
            <div className="stat-card">
              <div className="stat-value">{patients.length}</div>
              <div className="stat-label">Pending</div>
            </div>
            <div className="stat-card stat-assessed">
              <div className="stat-value">{result ? 1 : 0}</div>
              <div className="stat-label">Assessed</div>
            </div>
            <div className="stat-card stat-high">
              <div className="stat-value">{hasResult && result.risk_level === 'high' ? 1 : 0}</div>
              <div className="stat-label">High Risk</div>
            </div>
          </div>

          {/* Patient cards */}
          <div className="patient-list-header">
            <span>Patients to Assess</span>
          </div>
          <div className="patient-cards">
            {patients.map(p => (
              <div
                key={p.id}
                className={`patient-card ${patientId === p.id ? 'selected' : ''} ${loading && patientId === p.id ? 'assessing' : ''}`}
                onClick={() => !loading && handleAssess(p.id)}
              >
                {patientPhotos[p.id]
                  ? <img src={patientPhotos[p.id]} alt={p.name} className="patient-avatar-img" />
                  : <div className="patient-avatar">{getInitials(p.name)}</div>
                }
                <div className="patient-info-col">
                  <div className="patient-name">{p.name}</div>
                  <div className="patient-meta">Age {p.age} &middot; {p.id}</div>
                </div>
                <div className="patient-action">
                  {loading && patientId === p.id ? (
                    <svg className="spinner-sm" viewBox="0 0 50 50">
                      <circle cx="25" cy="25" r="20" fill="none" stroke="#8b5cf6" strokeWidth="5" strokeLinecap="round" strokeDasharray="31.4 31.4" opacity="0.3" />
                      <circle cx="25" cy="25" r="20" fill="none" stroke="#8b5cf6" strokeWidth="5" strokeLinecap="round" strokeDasharray="31.4 100" strokeDashoffset="0" />
                    </svg>
                  ) : hasResult && result.patient_id === p.id ? (
                    <RiskBadge level={result.risk_level} />
                  ) : (
                    <span className="assess-btn">Assess</span>
                  )}
                </div>
              </div>
            ))}
          </div>

          {/* Dropdown fallback for custom ID */}
          <form onSubmit={handleSubmit} className="form-alt">
            <select
              value={patientId}
              onChange={(e) => setPatientId(e.target.value)}
            >
              <option value="" disabled>Or select manually...</option>
              {patients.map(p => (
                <option key={p.id} value={p.id}>{p.name}</option>
              ))}
            </select>
            <button type="submit" disabled={loading || !patientId}>Assess</button>
          </form>
        </div>

        {/* Right panel: report */}
        <div className="panel-result">
          {!showReport && (
            <div className="empty-state">
              <div className="empty-icon">&#x1F50D;</div>
              <h2>Select a patient to assess</h2>
              <p>Click on a patient card to run the AI-powered readmission risk assessment. The multi-agent system will analyze their discharge summary, medical history, and social factors.</p>
            </div>
          )}

          {loading && (
            <div className="loading-panel">
              <div className="loading-header-bar">
                <h2>Analyzing: {getPatientName(patientId)}</h2>
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
                <div className="loading-step"><div className="step-dot pending" /><div><div className="step-label">Reviewing patient history</div><div className="step-sub">Historical analyst checking FHIR data...</div></div></div>
                <div className="loading-step"><div className="step-dot pending" /><div><div className="step-label">Calculating risk score</div><div className="step-sub">Synthesizing clinical and social factors...</div></div></div>
                <div className="loading-step"><div className="step-dot pending" /><div><div className="step-label">Generating intervention plan</div><div className="step-sub">Scheduling follow-ups and referrals...</div></div></div>
              </div>
              <div className="result-top-row">
                <div className="card skeleton-card"><div className="skeleton skeleton-gauge" /></div>
                <div className="card skeleton-card"><div className="skeleton skeleton-rec" /></div>
              </div>
              <div className="result-bottom-row">
                <div className="card skeleton-card"><div className="skeleton skeleton-line" /><div className="skeleton skeleton-line short" /><div className="skeleton skeleton-line" /></div>
                <div className="card skeleton-card"><div className="skeleton skeleton-line" /><div className="skeleton skeleton-line short" /><div className="skeleton skeleton-line" /></div>
              </div>
            </div>
          )}

          {!loading && (error || (result && result.status === 'error')) && (
            <div className="error"><strong>Error:</strong> {error || result?.message}</div>
          )}

          {!loading && hasResult && (
            <>
              <div className="result-header-bar">
                <div>
                  <h2>Risk Assessment Report</h2>
                  <span className="patient-label">{getPatientName(result.patient_id)} ({result.patient_id})</span>
                </div>
                {result.risk_level && <RiskBadge level={result.risk_level} />}
              </div>
              <div className="result-top-row">
                <div className="card score-card"><RiskGauge score={result.risk_score} /></div>
                {result.discharge_recommendation && (
                  <div className={`card discharge-card ${result.discharge_recommendation === 'hold_discharge_for_review' ? 'rec-hold' : 'rec-proceed'}`}>
                    <div className="rec-icon">{result.discharge_recommendation === 'hold_discharge_for_review' ? '\u26A0\uFE0F' : '\u2705'}</div>
                    <div className="rec-label">Discharge Recommendation</div>
                    <div className="rec-value">{result.discharge_recommendation === 'hold_discharge_for_review' ? 'Hold for Review' : 'Proceed with Discharge'}</div>
                  </div>
                )}
              </div>
              <div className="result-bottom-row">
                {result.risk_factors?.length > 0 && (
                  <div className="card">
                    <h3><span className="section-icon">{'\u26A0'}</span>Risk Factors<span className="section-count">{result.risk_factors.length}</span></h3>
                    <div className="card-scroll"><ul className="factor-list">{result.risk_factors.map((f, i) => <li key={i}>{cleanText(f)}</li>)}</ul></div>
                  </div>
                )}
                {result.intervention_plan?.length > 0 && (
                  <div className="card">
                    <h3><span className="section-icon">{'\u2714'}</span>Intervention Plan<span className="section-count">{result.intervention_plan.length}</span></h3>
                    <div className="card-scroll"><div className="intervention-cards">
                      {result.intervention_plan.map((item, i) => {
                        const meta = getInterventionMeta(item)
                        return (
                          <div key={i} className="intervention-card">
                            <div className="intervention-icon-wrapper" style={{ background: `${meta.color}12`, color: meta.color }}><span className="intervention-icon">{meta.icon}</span></div>
                            <div className="intervention-content"><div className="intervention-type" style={{ color: meta.color }}>{meta.label}</div><div className="intervention-detail">{cleanIntervention(item)}</div></div>
                          </div>
                        )
                      })}
                    </div></div>
                  </div>
                )}
              </div>
              {result.summary && (
                <div className="card summary-card"><h3><span className="section-icon">{'\u{1F4CB}'}</span>Clinical Summary</h3><p>{cleanText(result.summary)}</p></div>
              )}
            </>
          )}
        </div>
      </div>
    </>
  )
}

export default App
