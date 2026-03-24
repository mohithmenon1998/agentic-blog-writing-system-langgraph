import operator
from typing_extensions import TypedDict, List, Optional, Annotated, Literal
from uuid import UUID, uuid4
from agents.schemas import EvidenceItem, Plan

class State(TypedDict):
    
    topic: str
    mode: str
    needs_research: bool
    queries: List[str]
    evidence: List[EvidenceItem]
    plan: Optional[Plan]
    
    sections: Annotated[List[tuple[UUID, str]], operator.add]
    final: str