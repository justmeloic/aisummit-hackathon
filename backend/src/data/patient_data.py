"""
Patient data access for the Readmission Prevention Agent.
Reads discharge summaries from text files and FHIR bundles from JSON files.
"""

import json
import os

DATA_DIR = os.path.dirname(os.path.abspath(__file__))
DISCHARGE_DIR = os.path.join(DATA_DIR, "discharge_summaries")

PATIENTS = {
    "alice_johnson": {
        "name": "Alice Johnson",
        "age": 40,
        "fhir_file": "patient_alice_johnson.json",
        "discharge_file": "alice_johnson_summary.txt",
    },
    "bob_smith": {
        "name": "Bob Smith",
        "age": 70,
        "fhir_file": "patient_bob_smith.json",
        "discharge_file": "bob_smith_summary.txt",
    },
    "charlie_davis": {
        "name": "Charlie Davis",
        "age": 76,
        "fhir_file": "patient_charlie_davis.json",
        "discharge_file": "charlie_davis_summary.txt",
    },
}


def get_patient_discharge_summary(patient_id: str) -> str:
    """Get the discharge summary for a patient from a text file."""
    patient = PATIENTS.get(patient_id)
    if not patient:
        return f"No discharge summary found for patient {patient_id}"

    filepath = os.path.join(DISCHARGE_DIR, patient["discharge_file"])
    try:
        with open(filepath, "r") as f:
            return f.read()
    except FileNotFoundError:
        return f"Discharge summary file not found for patient {patient_id}"


def get_patient_history(patient_id: str) -> dict:
    """Get the FHIR bundle historical data for a patient from a JSON file."""
    patient = PATIENTS.get(patient_id)
    if not patient:
        return {"error": f"No history found for patient {patient_id}"}

    filepath = os.path.join(DATA_DIR, patient["fhir_file"])
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"error": f"FHIR data file not found for patient {patient_id}"}


def get_all_patients() -> list[dict]:
    """Return a list of all patients for the frontend dropdown."""
    return [
        {"id": pid, "name": p["name"], "age": p["age"]}
        for pid, p in PATIENTS.items()
    ]
