from typing import List, Set
from pydantic import BaseModel, Field
from src.perception.schema import TMRFrame

class SituationModel(BaseModel):
    """Tracks the state of the audit across multiple turns."""
    actions: List[TMRFrame] = Field(default_factory=list)
    consolidated_statuses: Set[str] = Field(default_factory=set)
    target_object: str = ""
    context: str = ""

    def update(self, tmr: TMRFrame):
        self.actions.append(tmr)
        self.consolidated_statuses.update(tmr.statuses)
        if tmr.target_object:
            self.target_object = tmr.target_object
        if tmr.context:
            self.context = tmr.context

    def clear(self):
        self.actions = []
        self.consolidated_statuses = set()
        self.target_object = ""
        self.context = ""
