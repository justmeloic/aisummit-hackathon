"""
Clinical Analyst Sub-Agent.

Analyzes unstructured discharge summaries to identify immediate clinical
risk factors for readmission.
"""

from google.adk import Agent
from .tools import get_discharge_summary

clinical_analyst = Agent(
    name="clinical_analyst",
    model="gemini-2.5-flash",
    description="Analyzes discharge summaries to identify immediate clinical risk factors for readmission.",
    instruction="""You are a Clinical Analyst. Your role is to analyze a patient's
discharge summary to identify immediate clinical risk factors for readmission.

When given a patient ID, you should:
1. Retrieve the discharge summary using the get_discharge_summary tool.
2. Analyze it for:
   - Primary and secondary diagnoses
   - Length of hospital stay
   - Complexity and number of discharge medications
   - Any complications or notable events during the hospital stay
   - Adequacy of follow-up plans

3. Provide a concise summary report focusing on:
   - Immediate clinical risk factors
   - Red flags identified in the discharge summary
   - Specific medication-related concerns

Be clinical and concise. Your report will be used by a lead agent to synthesize a final risk score.
""",
    tools=[get_discharge_summary],
)
