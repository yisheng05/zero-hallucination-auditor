import pytest
from src.ontology.manager import OntologyManager
from src.engine.auditor import SymbolicAuditor
from src.parser.schema import TMRFrame

@pytest.fixture
def ontology_manager():
    return OntologyManager("zero-hallucination-auditor/src/ontology/nist_rmf.json")

@pytest.fixture
def auditor(ontology_manager):
    return SymbolicAuditor(ontology_manager)

def test_compliant_scenario(auditor):
    # TMR with ALL preconditions for all subcategories in nist_rmf.json
    all_preconditions = [
        "PolicyExists", "RolesDefined", 
        "ContextEstablished", "SystemBoundariesDefined",
        "BiasTestingDone", "MetricsDefined",
        "RiskMitigationsImplemented", "HumanInTheLoop"
    ]
    tmr = TMRFrame(
        action="Deploy",
        target_object="SafeModel",
        context="Finance",
        statuses=all_preconditions
    )
    
    decision = auditor.audit(tmr)
    assert decision.is_compliant is True
    assert len(decision.violated_subcategories) == 0

def test_non_compliant_scenario(auditor):
    # Missing everything
    tmr = TMRFrame(
        action="Deploy",
        target_object="RiskyModel",
        context="Healthcare",
        statuses=[]
    )
    
    decision = auditor.audit(tmr)
    assert decision.is_compliant is False
    assert "MAP-1.1" in decision.violated_subcategories
    assert "ContextEstablished" in decision.violated_subcategories["MAP-1.1"]
    assert "SystemBoundariesDefined" in decision.violated_subcategories["MAP-1.1"]

def test_partial_compliant_scenario(auditor):
    # Only some preconditions met
    tmr = TMRFrame(
        action="Test",
        target_object="ModelA",
        context="Generic",
        statuses=["PolicyExists", "RolesDefined", "BiasTestingDone", "MetricsDefined"]
    )
    
    decision = auditor.audit(tmr)
    assert decision.is_compliant is False
    assert "GOVERN-1.1" in decision.compliant_subcategories
    assert "MEASURE-2.1" in decision.compliant_subcategories
    assert "MAP-1.1" in decision.violated_subcategories
    assert "MANAGE-1.1" in decision.violated_subcategories
