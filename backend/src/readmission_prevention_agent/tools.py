"""
Intervention tools for the Readmission Prevention Agent.
These simulate proactive interventions for high-risk patients in a demo environment.
"""

import datetime


def schedule_follow_up_appointment(
    patient_id: str, department: str, days_from_now: int
) -> dict:
    """
    Schedule a follow-up appointment for a patient.

    Args:
        patient_id: The unique identifier for the patient.
        department: The department for the follow-up (e.g., "Cardiology", "Primary Care").
        days_from_now: Number of days from today to schedule the appointment.

    Returns:
        Confirmation of the scheduled appointment.
    """
    appt_date = datetime.date.today() + datetime.timedelta(days=days_from_now)
    return {
        "status": "scheduled",
        "patient_id": patient_id,
        "department": department,
        "date": appt_date.isoformat(),
        "confirmation": f"APPT-{patient_id}-{appt_date.strftime('%Y%m%d')}",
        "message": f"Follow-up appointment scheduled with {department} on {appt_date.isoformat()}.",
    }


def send_medication_reminder(
    patient_id: str, medications: list[str], frequency: str
) -> dict:
    """
    Enroll a patient in automated medication reminder text messages.

    Args:
        patient_id: The unique identifier for the patient.
        medications: List of medication names to include in reminders.
        frequency: How often to send reminders (e.g., "daily", "twice_daily", "weekly").

    Returns:
        Confirmation of the reminder enrollment.
    """
    return {
        "status": "enrolled",
        "patient_id": patient_id,
        "medications": medications,
        "frequency": frequency,
        "channel": "SMS",
        "message": f"Patient {patient_id} enrolled in {frequency} medication reminders for: {', '.join(medications)}.",
    }


def refer_to_social_worker(patient_id: str, reason: str, priority: str) -> dict:
    """
    Create a referral to a social worker for a patient.

    Args:
        patient_id: The unique identifier for the patient.
        reason: The reason for the referral (e.g., "unstable housing", "lack of caregiver support").
        priority: Priority level - "routine", "urgent", or "emergent".

    Returns:
        Confirmation of the social worker referral.
    """
    return {
        "status": "referred",
        "patient_id": patient_id,
        "reason": reason,
        "priority": priority,
        "referral_id": f"SW-{patient_id}-{datetime.date.today().strftime('%Y%m%d')}",
        "message": f"Social worker referral created for patient {patient_id} ({priority} priority): {reason}.",
    }


def arrange_home_health_visit(
    patient_id: str, visit_type: str, days_from_now: int
) -> dict:
    """
    Arrange a home health visit for a patient after discharge.

    Args:
        patient_id: The unique identifier for the patient.
        visit_type: Type of visit (e.g., "nursing", "physical_therapy", "medication_reconciliation").
        days_from_now: Number of days from today for the first visit.

    Returns:
        Confirmation of the home health visit arrangement.
    """
    visit_date = datetime.date.today() + datetime.timedelta(days=days_from_now)
    return {
        "status": "arranged",
        "patient_id": patient_id,
        "visit_type": visit_type,
        "first_visit_date": visit_date.isoformat(),
        "message": f"Home health {visit_type} visit arranged for patient {patient_id} on {visit_date.isoformat()}.",
    }
