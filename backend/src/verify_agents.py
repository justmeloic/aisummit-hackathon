"""Quick verification script for the multi-agent structure."""

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.readmission_prevention_agent.agent import root_agent
from src.readmission_prevention_agent.subagents.historical_analyst import historical_analyst
from src.readmission_prevention_agent.subagents.clinical_analyst import clinical_analyst


def verify_structure():
    print("Verifying Multi-Agent Structure...")

    print(f"\nRoot Agent: {root_agent.name} (Model: {root_agent.model})")
    print(f"  Tools: {[t.name if hasattr(t, 'name') else t.__name__ for t in root_agent.tools]}")

    print(f"\nSub-Agents:")
    print(f"  - Clinical Analyst: {clinical_analyst.name} (Model: {clinical_analyst.model})")
    print(f"    Tools: {[t.__name__ for t in clinical_analyst.tools]}")
    print(f"  - Historical Analyst: {historical_analyst.name} (Model: {historical_analyst.model})")
    print(f"    Tools: {[t.__name__ for t in historical_analyst.tools]}")


def test_mock_retrieval(patient_id="P12345"):
    print(f"\nTesting Mock Data Retrieval for: {patient_id}")

    from src.readmission_prevention_agent.subagents.historical_analyst.tools import get_patient_history_data
    from src.readmission_prevention_agent.subagents.clinical_analyst.tools import get_discharge_summary

    print("\n--- Patient History ---")
    history = get_patient_history_data(patient_id)
    print(history)

    print("\n--- Discharge Summary (first 200 chars) ---")
    summary = get_discharge_summary(patient_id)
    print(summary[:200].strip() + "...")


if __name__ == "__main__":
    verify_structure()
    test_mock_retrieval()
