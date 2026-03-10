import json
from src.data.patient_data import get_patient_history


def get_patient_history_data(patient_id: str) -> dict:
    """
    Retrieve historical patient data including prior admissions,
    chronic conditions, and social determinants of health.

    Args:
        patient_id: The unique identifier for the patient (e.g., "P12345")

    Returns:
        A dictionary containing patient name, age, prior admissions,
        chronic conditions, social determinants, medication adherence,
        and missed appointments.
    """
    return get_patient_history(patient_id)
