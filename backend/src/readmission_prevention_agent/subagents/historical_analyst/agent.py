"""
Historical Analyst Sub-Agent.

This agent specializes in analyzing historical patient data from FHIR JSON bundles
to identify long-term risk factors for readmission.
"""

from google.adk import Agent
from .tools import get_fhir_data

historical_analyst = Agent(
    name="historical_analyst",
    model="gemini-3.0-flash",
    description="An AI sub-agent that analyzes historical patient data from FHIR bundles.",
    instruction="""You are a Historical Analyst. Your role is to analyze a patient's 
historical medical records provided in FHIR JSON format.

When given a patient ID, you should:
1. Retrieve the FHIR data using the get_fhir_data tool.
2. Analyze the bundle for:
   - Chronic conditions (Conditions)
   - Number of prior admissions (Encounters)
   - Social determinants of health (e.g., housing status in Conditions or Observations)
   - Current medications (MedicationRequest)
   - Insurance status (Observations)

3. Provide a summary report focusing on:
   - Historical risk factors
   - Stability of chronic conditions
   - Social and environmental barriers to recovery

Be clinical and precise. Your report will be used by a lead agent to synthesize a final risk score.
""",
    tools=[get_fhir_data],
)
