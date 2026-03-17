from typing import List, Dict
from pydantic import BaseModel
from src.ontology.manager import OntologyManager
from src.parser.schema import TMRFrame

class AuditDecision(BaseModel):
    is_compliant: bool
    compliant_subcategories: List[str]
    violated_subcategories: Dict[str, List[str]] # Subcategory -> Missing Preconditions
    decision_trace: List[str]

class SymbolicAuditor:
    def __init__(self, ontology_manager: OntologyManager):
        self.ontology = ontology_manager

    def audit(self, tmr: TMRFrame) -> AuditDecision:
        all_subcats = self.ontology.get_all_subcategories()
        compliant_subcats = []
        violated_subcats = {}
        trace = []
        
        # Determine relevant subcategories based on context/action
        # In a real system, this mapping would be more sophisticated.
        # For this prototype, we'll check against all defined subcategories.
        
        for sub_id in all_subcats:
            required_preconditions = self.ontology.get_preconditions(sub_id)
            missing = [p for p in required_preconditions if p not in tmr.statuses]
            
            if not missing:
                compliant_subcats.append(sub_id)
                trace.append(f"Subcategory {sub_id}: All preconditions met ({', '.join(required_preconditions)})")
            else:
                violated_subcats[sub_id] = missing
                trace.append(f"Subcategory {sub_id}: Missing preconditions: {', '.join(missing)}")
                
        is_compliant = len(violated_subcats) == 0
        
        return AuditDecision(
            is_compliant=is_compliant,
            compliant_subcategories=compliant_subcats,
            violated_subcategories=violated_subcats,
            decision_trace=trace
        )

if __name__ == "__main__":
    from src.ontology.manager import OntologyManager
    from src.parser.schema import TMRFrame
    
    manager = OntologyManager("zero-hallucination-auditor/src/ontology/nist_rmf.json")
    auditor = SymbolicAuditor(manager)
    
    # Test TMR
    test_tmr = TMRFrame(
        action="Deploy",
        target_object="CreditWise Model",
        context="Finance",
        statuses=["BiasTestingDone", "MetricsDefined", "ContextEstablished", "SystemBoundariesDefined"]
    )
    
    decision = auditor.audit(test_tmr)
    print(decision.json(indent=2))
