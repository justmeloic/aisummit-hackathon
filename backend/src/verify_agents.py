import sys
import os

# Ensure backend/src is in PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.readmission_prevention_agent.agent import root_agent
from src.readmission_prevention_agent.subagents.historical_analyst import historical_analyst
from src.readmission_prevention_agent.subagents.clinical_analyst import clinical_analyst

def verify_structure():
    print("Verifying Multi-Agent Structure...")
    
    # Check root agent
    print(f"Root Agent Name: {root_agent.name}")
    print(f"Root Agent Model: {root_agent.model}")
    
    # Check sub-agents
    print("\nChecking Sub-Agents Registration:")
    # Assuming ADK stores sub-agents in a list or similar internal attribute
    # Here we just verify we can import them and they have the correct names
    print(f"- Historical Analyst: {historical_analyst.name} (Model: {historical_analyst.model})")
    print(f"- Clinical Analyst: {clinical_analyst.name} (Model: {clinical_analyst.model})")
    
    # Verify Tools
    print("\nVerifying Tooling:")
    print(f"- Historical Analyst Tools: {[t.__name__ for t in historical_analyst.tools]}")
    print(f"- Clinical Analyst Tools: {[t.__name__ for t in clinical_analyst.tools]}")

def test_mock_retrieval(patient_id="bradly_fisher"):
    print(f"\nTesting Mock Data Retrieval for: {patient_id}")
    
    from src.readmission_prevention_agent.subagents.historical_analyst.tools import get_fhir_data
    from src.readmission_prevention_agent.subagents.clinical_analyst.tools import get_discharge_summary
    
    print("\n--- FHIR Data Sample ---")
    fhir_data = get_fhir_data(patient_id)
    if "error" in fhir_data:
        print(f"Error: {fhir_data['error']}")
    else:
        print(f"Resource Type: {fhir_data.get('resourceType')}")
        print(f"Entries: {len(fhir_data.get('entry', []))}")
        
    print("\n--- Discharge Summary Sample ---")
    summary = get_discharge_summary(patient_id)
    print(summary[:200] + "...")

if __name__ == "__main__":
    verify_structure()
    test_mock_retrieval()
