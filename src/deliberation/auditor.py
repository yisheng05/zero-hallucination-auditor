from typing import List, Dict
from src.ontology.manager import OntologyManager
from src.perception.schema import MentalMeaningRepresentation
from src.memory.situation_model import SituationModel

class SymbolicAuditor:
    def __init__(self, ontology_manager: OntologyManager):
        self.ontology = ontology_manager

    def deliberate(self, memory: SituationModel) -> MentalMeaningRepresentation:
        all_subcats = self.ontology.get_all_subcategories()
        met_subcats = []
        violated_subcats = {}
        trustworthiness_impact = {}
        
        statuses = memory.consolidated_statuses
        
        for sub_id in all_subcats:
            required = self.ontology.get_preconditions(sub_id)
            if not required:
                continue
                
            missing = [p for p in required if p not in statuses]
            
            if not missing:
                met_subcats.append(sub_id)
            else:
                violated_subcats[sub_id] = missing
                impacted = self.ontology.get_trustworthiness_impact(sub_id)
                if impacted:
                    trustworthiness_impact[sub_id] = impacted

        is_compliant = len(violated_subcats) == 0
        
        # Simple actionability score: ratio of met subcategories to total checked
        total_checked = len(met_subcats) + len(violated_subcats)
        score = len(met_subcats) / total_checked if total_checked > 0 else 0.0
        
        gap_summary = f"Audit complete. Met {len(met_subcats)} subcategories. {len(violated_subcats)} subcategories have missing preconditions."
        
        return MentalMeaningRepresentation(
            is_compliant=is_compliant,
            met_subcategories=met_subcats,
            violated_subcategories=violated_subcats,
            gap_analysis=gap_summary,
            trustworthiness_impact=trustworthiness_impact,
            actionability_score=score
        )
