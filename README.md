# Readmission Prevention Agent

An AI-powered system that automates the identification of high-risk patients at the moment of discharge, enabling proactive intervention to prevent costly readmissions.

## Project Structure

```
├── frontend/                    # React frontend
│   └── src/
├── backend/
│   ├── requirements.txt
│   └── src/
│       ├── main.py              # FastAPI server
│       ├── data/                # Mock patient data
│       └── readmission_prevention_agent/  # Google ADK agent
```

## Quick Start

### Backend

```bash
cd backend
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
uvicorn src.main:app --reload --port 8000
```

The API will be available at http://localhost:8000

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The app will be available at http://localhost:3000

### Run Agent with ADK Web UI
```bash
cd backend
source .venv/bin/activate
adk web src/readmission_prevention_agent
```

## Sample Patient IDs
- `P12345` - High risk (CHF, multiple comorbidities)
- `P67890` - Low risk (pneumonia, no history)
- `P11111` - Very high risk (hip fracture, dementia, poor support)

## Architecture

- **Frontend**: React app for submitting patient IDs
- **Backend**: FastAPI server with integrated ADK agent
- **Agent**: Google ADK multi-agent system for risk assessment
  - Analyzes discharge summaries for clinical risk factors
  - Queries patient history for historical patterns
  - Calculates risk score and generates intervention plan
