from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from enum import Enum

class CommunicationIntent(str, Enum):
    REPORT = "REPORT"
    REQUEST_INFO = "REQUEST_INFO"
    GREETING = "GREETING"

class TMRFrame(BaseModel):
    """Text Meaning Representation Frame representing a system action or event."""
    action: str = Field(description="The primary action being performed")
    target_object: str = Field(description="The object of the action")
    context: str = Field(description="The domain or context of the action")
    statuses: List[str] = Field(default_factory=list, description="List of identified preconditions/statuses")
    raw_input: Optional[str] = None

class TMRParseResult(BaseModel):
    frame: TMRFrame
    explanation: str

class MentalMeaningRepresentation(BaseModel):
    """The agent's internal reasoning about compliance."""
    is_compliant: bool
    met_subcategories: List[str]
    violated_subcategories: Dict[str, List[str]] # Subcat -> Missing Preconditions
    gap_analysis: str = Field(description="Internal summary of what is missing")
    trustworthiness_impact: Dict[str, List[str]] # Subcat -> Affected Characteristics
    actionability_score: float = Field(description="Score between 0 and 1 indicating if we have enough info")

class GenerationMeaningRepresentation(BaseModel):
    """Structured specification of what to communicate."""
    intent: CommunicationIntent
    content_payload: Dict[str, Any]
    tone: str = "professional"
    trace_summary: Optional[str] = None
