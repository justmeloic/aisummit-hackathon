# Data module for mock patient data
from .patient_data import PATIENTS_DB, get_patient_discharge_summary, get_patient_history

__all__ = ["PATIENTS_DB", "get_patient_discharge_summary", "get_patient_history"]
