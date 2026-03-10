from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Readmission Prevention API",
    description="API for patient readmission risk assessment",
    version="0.1.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class PatientRequest(BaseModel):
    patient_id: str


class RiskAssessmentResponse(BaseModel):
    patient_id: str
    risk_score: float | None = None
    risk_level: str | None = None
    risk_factors: list[str] | None = None
    intervention_plan: list[str] | None = None
    status: str
    message: str | None = None


@app.get("/")
async def root():
    return {"message": "Readmission Prevention API", "status": "healthy"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/api/assess-risk", response_model=RiskAssessmentResponse)
async def assess_risk(request: PatientRequest):
    """
    Assess readmission risk for a patient.
    Uses the ADK agent to analyze discharge summary and patient history.
    """
    try:
        # TODO: Integrate with ADK agent
        # For now, return a placeholder response
        return RiskAssessmentResponse(
            patient_id=request.patient_id,
            risk_score=0.0,
            risk_level="pending",
            risk_factors=[],
            intervention_plan=[],
            status="pending",
            message="Agent integration pending. Submit patient ID like P12345, P67890, or P11111."
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
