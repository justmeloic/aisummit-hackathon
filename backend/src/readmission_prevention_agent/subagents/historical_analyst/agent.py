"""
Historical Analyst Sub-Agent.

Analyzes historical patient data to identify long-term risk factors for readmission.
"""

from google.adk import Agent
from .tools import get_patient_history_data

historical_analyst = Agent(
    name="historical_analyst",
    model="gemini-2.5-flash",
    description="Analyzes historical patient data including prior admissions, chronic conditions, and social determinants of health.",
    instruction="""You are a Historical Analyst. Your role is to analyze a patient's
historical medical records to identify long-term risk factors for readmission.

When given a patient ID, you should:
1. Retrieve the patient history using the get_patient_history_data tool.
2. Analyze the data for:
   - Number of prior admissions in the last 12 months
   - Chronic conditions and their severity
   - Social determinants of health (housing, transportation, caregiver support)
   - Medication adherence history
   - Missed appointment patterns

3. Provide a concise summary report focusing on:
   - Historical risk factors with severity assessment
   - Social and environmental barriers to recovery
   - Patterns that predict readmission (e.g., frequent prior admissions + poor adherence)

Be clinical and precise. Your report will be used by a lead agent to synthesize a final risk score.
""",
    tools=[get_patient_history_data],
)
