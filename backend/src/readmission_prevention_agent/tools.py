"""
Tools for the Readmission Prevention Agent.
These tools allow the agent to access patient data.
"""

from src.data.patient_data import get_patient_discharge_summary, get_patient_history


def get_discharge_summary(patient_id: str) -> str:
    """
    Retrieve the discharge summary for a patient.

    Args:
        patient_id: The unique identifier for the patient (e.g., "P12345")

    Returns:
        The full discharge summary text containing diagnosis, medications,
        hospital course, and follow-up instructions.
    """
    return get_patient_discharge_summary(patient_id)


def get_patient_history_data(patient_id: str) -> dict:
    """
    Retrieve historical patient data including prior admissions,
    chronic conditions, and social determinants of health.

    Args:
        patient_id: The unique identifier for the patient (e.g., "P12345")

    Returns:
        A dictionary containing:
        - name: Patient name
        - age: Patient age
        - prior_admissions_12_months: Number of hospital admissions in past year
        - chronic_conditions: List of chronic medical conditions
        - social_determinants: Dict with housing, transportation, caregiver info
        - medication_adherence_history: Rating of medication compliance
        - missed_appointments_6_months: Number of missed appointments
    """
    return get_patient_history(patient_id)
