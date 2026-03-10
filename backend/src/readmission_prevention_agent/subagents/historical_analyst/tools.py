import json
import os

def get_fhir_data(patient_id: str) -> dict:
    """
    Retrieve historical patient data from a FHIR JSON file.
    
    Args:
        patient_id: The unique identifier for the patient (e.g., "bradly_fisher")
        
    Returns:
        A dictionary containing the FHIR bundle data.
    """
    # Map patient_id to filename if necessary, here we assume it's part of the filename
    # For mock purposes, we'll look for patient_{patient_id}.json in the data directory
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../.."))
    data_path = os.path.join(base_dir, "data", f"patient_{patient_id}.json")
    
    try:
        with open(data_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"error": f"FHIR data not found for patient {patient_id} at {data_path}"}
    except Exception as e:
        return {"error": f"Error loading FHIR data: {str(e)}"}
