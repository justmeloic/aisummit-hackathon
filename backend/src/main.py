import re
import uuid

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from google.genai import types
from google.adk.runners import InMemoryRunner

from src.readmission_prevention_agent import root_agent
from src.data.patient_data import get_all_patients

load_dotenv()

app = FastAPI(
    title="Readmission Prevention API",
    description="API for patient readmission risk assessment",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

APP_NAME = "readmission_prevention"
runner = InMemoryRunner(agent=root_agent, app_name=APP_NAME)
session_service = runner.session_service


class PatientRequest(BaseModel):
    patient_id: str


class RiskAssessmentResponse(BaseModel):
    patient_id: str
    risk_score: float | None = None
    risk_level: str | None = None
    discharge_recommendation: str | None = None
    risk_factors: list[str] | None = None
    intervention_plan: list[str] | None = None
    summary: str | None = None
    raw_response: str | None = None
    status: str
    message: str | None = None


def parse_agent_response(text: str) -> dict:
    """Parse the structured agent response into fields."""
    result = {
        "risk_score": None,
        "risk_level": None,
        "discharge_recommendation": None,
        "risk_factors": [],
        "intervention_plan": [],
        "summary": None,
    }

    score_match = re.search(r"Risk Score:\s*(\d+)", text, re.IGNORECASE)
    if score_match:
        result["risk_score"] = float(score_match.group(1))

    level_match = re.search(r"Risk Level:\s*(low|moderate|high)", text, re.IGNORECASE)
    if level_match:
        result["risk_level"] = level_match.group(1).lower()

    rec_match = re.search(
        r"Discharge Recommendation:\s*(proceed_with_discharge|hold_discharge_for_review)",
        text,
        re.IGNORECASE,
    )
    if rec_match:
        result["discharge_recommendation"] = rec_match.group(1).lower()

    factors_match = re.search(
        r"RISK FACTORS:\s*\n(.*?)(?=\n\s*(?:INTERVENTION|SUMMARY|$))",
        text,
        re.DOTALL | re.IGNORECASE,
    )
    if factors_match:
        factors_text = factors_match.group(1)
        result["risk_factors"] = [
            line.strip().lstrip("- *").strip()
            for line in factors_text.strip().split("\n")
            if line.strip() and line.strip() not in ("-", "*")
        ]

    interventions_match = re.search(
        r"INTERVENTION PLAN:\s*\n(.*?)(?=\n\s*(?:SUMMARY|$))",
        text,
        re.DOTALL | re.IGNORECASE,
    )
    if interventions_match:
        interventions_text = interventions_match.group(1)
        result["intervention_plan"] = [
            line.strip().lstrip("- *").strip()
            for line in interventions_text.strip().split("\n")
            if line.strip() and line.strip() not in ("-", "*")
        ]

    summary_match = re.search(
        r"SUMMARY:\s*\n(.*?)$", text, re.DOTALL | re.IGNORECASE
    )
    if summary_match:
        result["summary"] = summary_match.group(1).strip()

    return result


@app.get("/")
async def root():
    return {"message": "Readmission Prevention API", "status": "healthy"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.get("/api/patients")
async def list_patients():
    """Return list of available patients for the frontend dropdown."""
    return get_all_patients()


@app.post("/api/assess-risk", response_model=RiskAssessmentResponse)
async def assess_risk(request: PatientRequest):
    """
    Assess readmission risk for a patient.
    Uses the ADK agent to analyze discharge summary and patient history.
    """
    try:
        user_id = f"doctor_{uuid.uuid4().hex[:8]}"
        session = await session_service.create_session(
            app_name=APP_NAME, user_id=user_id
        )

        message = types.Content(
            parts=[
                types.Part(
                    text=f"Assess readmission risk for patient {request.patient_id}"
                )
            ],
            role="user",
        )

        final_text = ""
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session.id,
            new_message=message,
        ):
            if (
                event.is_final_response()
                and event.content
                and event.content.parts
            ):
                for part in event.content.parts:
                    if part.text:
                        final_text += part.text

        if not final_text:
            return RiskAssessmentResponse(
                patient_id=request.patient_id,
                status="error",
                message="Agent did not produce a response.",
            )

        parsed = parse_agent_response(final_text)

        return RiskAssessmentResponse(
            patient_id=request.patient_id,
            risk_score=parsed["risk_score"],
            risk_level=parsed["risk_level"],
            discharge_recommendation=parsed["discharge_recommendation"],
            risk_factors=parsed["risk_factors"],
            intervention_plan=parsed["intervention_plan"],
            summary=parsed["summary"],
            raw_response=final_text,
            status="completed",
            message="Risk assessment completed successfully.",
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
