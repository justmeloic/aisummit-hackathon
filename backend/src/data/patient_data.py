# Mock Patient Data for Development

This module provides sample patient data for testing the Readmission Prevention Agent.

PATIENTS_DB = {
    "P12345": {
        "name": "John Smith",
        "age": 72,
        "discharge_summary": """
        Patient: John Smith, 72-year-old male
        Admission Date: 2026-03-05
        Discharge Date: 2026-03-10
        
        Primary Diagnosis: Congestive Heart Failure (CHF) exacerbation
        Secondary Diagnoses: Type 2 Diabetes, Hypertension, COPD
        
        Hospital Course:
        Patient admitted with acute CHF exacerbation presenting with dyspnea, 
        peripheral edema, and elevated BNP. Treated with IV diuretics with good response.
        Oxygen requirements normalized. Patient educated on daily weights and fluid restriction.
        
        Discharge Medications:
        - Furosemide 40mg BID (increased from 20mg)
        - Lisinopril 10mg daily
        - Metoprolol 25mg BID
        - Metformin 1000mg BID
        - Aspirin 81mg daily
        - Albuterol inhaler PRN
        
        Length of Stay: 5 days
        
        Follow-up: Cardiology in 1 week, PCP in 2 weeks
        """,
        "history": {
            "prior_admissions_12_months": 3,
            "chronic_conditions": ["CHF", "COPD", "Type 2 Diabetes", "Hypertension"],
            "social_determinants": {
                "lives_alone": True,
                "housing_status": "stable",
                "transportation_access": "limited",
                "caregiver_support": "minimal"
            },
            "medication_adherence_history": "poor",
            "missed_appointments_6_months": 4
        }
    },
    "P67890": {
        "name": "Mary Johnson",
        "age": 58,
        "discharge_summary": """
        Patient: Mary Johnson, 58-year-old female
        Admission Date: 2026-03-08
        Discharge Date: 2026-03-10
        
        Primary Diagnosis: Community-acquired pneumonia
        Secondary Diagnoses: None
        
        Hospital Course:
        Patient admitted with fever, cough, and right lower lobe infiltrate on chest X-ray.
        Treated with IV antibiotics (ceftriaxone and azithromycin) with good clinical response.
        Afebrile for 24 hours prior to discharge.
        
        Discharge Medications:
        - Azithromycin 250mg daily x 3 more days
        - Acetaminophen PRN for fever
        
        Length of Stay: 2 days
        
        Follow-up: PCP in 1 week
        """,
        "history": {
            "prior_admissions_12_months": 0,
            "chronic_conditions": [],
            "social_determinants": {
                "lives_alone": False,
                "housing_status": "stable",
                "transportation_access": "good",
                "caregiver_support": "strong"
            },
            "medication_adherence_history": "good",
            "missed_appointments_6_months": 0
        }
    },
    "P11111": {
        "name": "Robert Williams",
        "age": 81,
        "discharge_summary": """
        Patient: Robert Williams, 81-year-old male
        Admission Date: 2026-03-01
        Discharge Date: 2026-03-10
        
        Primary Diagnosis: Hip fracture s/p surgical repair
        Secondary Diagnoses: Dementia, Atrial Fibrillation, CKD Stage 3
        
        Hospital Course:
        Patient admitted after fall at home resulting in left hip fracture.
        Underwent ORIF on hospital day 2. Post-operative course complicated by
        delirium requiring close monitoring. Physical therapy initiated.
        Patient making slow progress with mobility.
        
        Discharge Medications:
        - Warfarin 5mg daily (INR goal 2-3)
        - Donepezil 10mg at bedtime
        - Oxycodone 5mg q6h PRN pain
        - Calcium + Vitamin D daily
        - Bisacodyl PRN constipation
        - Apixaban held - on Warfarin
        
        Length of Stay: 9 days
        
        Discharge Disposition: Skilled Nursing Facility
        Follow-up: Orthopedics in 2 weeks, INR check in 3 days
        """,
        "history": {
            "prior_admissions_12_months": 2,
            "chronic_conditions": ["Dementia", "Atrial Fibrillation", "CKD Stage 3", "Osteoporosis"],
            "social_determinants": {
                "lives_alone": True,
                "housing_status": "unstable - fall risk at home",
                "transportation_access": "none",
                "caregiver_support": "minimal - daughter lives out of state"
            },
            "medication_adherence_history": "poor - cognitive impairment",
            "missed_appointments_6_months": 6
        }
    }
}


def get_patient_discharge_summary(patient_id: str) -> str:
    """Get the discharge summary for a patient."""
    patient = PATIENTS_DB.get(patient_id)
    if patient:
        return patient["discharge_summary"]
    return f"No discharge summary found for patient {patient_id}"


def get_patient_history(patient_id: str) -> dict:
    """Get the historical data for a patient."""
    patient = PATIENTS_DB.get(patient_id)
    if patient:
        return {
            "name": patient["name"],
            "age": patient["age"],
            **patient["history"]
        }
    return {"error": f"No history found for patient {patient_id}"}
