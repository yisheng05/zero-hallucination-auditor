from src.perception.schema import (
    MentalMeaningRepresentation, 
    GenerationMeaningRepresentation, 
    CommunicationIntent
)

class ActionSpecifier:
    def __init__(self, actionability_threshold: float = 0.5):
        self.threshold = actionability_threshold

    def specify(self, mmr: MentalMeaningRepresentation) -> GenerationMeaningRepresentation:
        """Determines whether to report or ask for more info."""
        
        # Heuristic: If we are missing critical MAP or GOVERN info, request info
        critical_missing = False
        for sub_id in mmr.violated_subcategories:
            if sub_id.startswith("MAP") or sub_id.startswith("GOVERN"):
                critical_missing = True
                break
        
        if mmr.actionability_score < self.threshold or critical_missing:
            # We don't have enough info for a final audit
            return GenerationMeaningRepresentation(
                intent=CommunicationIntent.REQUEST_INFO,
                content_payload={
                    "missing_preconditions": list(set([p for p_list in mmr.violated_subcategories.values() for p in p_list])),
                    "gap_summary": mmr.gap_analysis
                },
                tone="helpful"
            )
        else:
            # We have enough to provide a formal report
            return GenerationMeaningRepresentation(
                intent=CommunicationIntent.REPORT,
                content_payload={
                    "is_compliant": mmr.is_compliant,
                    "met": mmr.met_subcategories,
                    "violated": mmr.violated_subcategories,
                    "trust_impact": mmr.trustworthiness_impact
                },
                tone="professional"
            )
        
