from src.data.patient_data import get_patient_discharge_summary


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
