import os

def get_discharge_summary(patient_id: str) -> str:
    """
    Retrieve the discharge summary for a patient.
    
    Args:
        patient_id: The unique identifier for the patient (e.g., "bradly_fisher")
        
    Returns:
        The full discharge summary text.
    """
    # For mock purposes, we'll try to find a file in data/discharge_summaries/
    # or fallback to the patient_data.py mock DB handled in the main toolset
    # but for this sub-agent we'll look for specific txt files if they exist.
    
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../.."))
    summary_path = os.path.join(base_dir, "data", "discharge_summaries", f"{patient_id}.txt")
    
    if os.path.exists(summary_path):
        with open(summary_path, 'r') as f:
            return f.read()
            
    # Fallback/Default for hackathon demonstration if file doesn't exist
    from src.data.patient_data import get_patient_discharge_summary
    # Map "bradly_fisher" to "P12345" style if needed, but here we assume IDs match or are handled
    return get_patient_discharge_summary(patient_id)
