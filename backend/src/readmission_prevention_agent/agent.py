"""
Readmission Prevention Agent using Google ADK.

This agent orchestrates the risk assessment by delegating tasks to specialized sub-agents.
"""

from google.adk import Agent
from .subagents.historical_analyst import historical_analyst
from .subagents.clinical_analyst import clinical_analyst

# Wrapper functions to use sub-agents as tools
def run_historical_analysis(patient_id: str) -> str:
    """
    Delegate historical patient data analysis to the historical_analyst sub-agent.
    Args:
        patient_id: The unique identifier for the patient.
    Returns:
        A report on historical risk factors and social determinants.
    """
    return historical_analyst.run(f"Analyze historical data for patient {patient_id}")

def run_clinical_analysis(patient_id: str) -> str:
    """
    Delegate immediate clinical analysis to the clinical_analyst sub-agent.
    Args:
        patient_id: The unique identifier for the patient.
    Returns:
        A report on clinical risk factors from the discharge summary.
    """
    return clinical_analyst.run(f"Analyze clinical data for patient {patient_id}")

# Main agent that orchestrates the risk assessment
root_agent = Agent(
    name="readmission_prevention_agent",
    model="gemini-3.0-flash",
    description="An AI agent that assesses patient readmission risk by orchestrating specialized sub-agents.",
    instruction="""You are the Readmission Prevention Agent Lead. Your role is to assess 
the risk of a patient being readmitted by coordinating the analysis from your sub-agents.

When given a patient ID, you should:
1. Call the `run_historical_analysis` tool to retrieve and analyze the patient's long-term
   history, chronic conditions, and social determinants from FHIR data.
   
2. Call the `run_clinical_analysis` tool to retrieve and analyze the patient's current
   discharge summary for immediate clinical risk factors and medication changes.
   
3. Synthesize the findings from both tools to provide:
   - A final risk score (0-100)
   - A risk level: "low", "moderate", or "high"
   - A comprehensive summary of key risk factors (clinical + historical)
   - A prioritized intervention plan with specific recommendations

Be the final authority on the risk assessment. Ensure the final report is cohesive, 
actionable, and clearly links the risk factors to the recommended interventions.
""",
    tools=[run_historical_analysis, run_clinical_analysis],
)
