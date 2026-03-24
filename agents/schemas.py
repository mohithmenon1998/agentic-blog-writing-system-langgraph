from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from typing_extensions import TypedDict, List, Optional, Annotated, Literal


# SHEMAS
class Task(BaseModel):
    id: UUID = Field( default_factory= uuid4)
    title: str

    goal: str = Field(
        ...,
        description="One sentence describing what the reader should be able to do/understand after this section.",
    )
    bullets: List[str] = Field(
        ...,
        min_length=3,
        max_length=5,
        description="3–5 concrete, non-overlapping subpoints to cover in this section.",
    )
    target_words: int = Field(
        ...,
        description="Target word count for this section (120–450).",
    )
    tags: List[str] = Field(default_factory= list)
    requires_research: bool = False
    requires_citations: bool = False
    requires_code: bool = False
    
    
class Plan(BaseModel):
    blog_title: str
    audience: str
    tone: str
    blog_kind: Literal["explainer", "tutorial", "news_roundup", "comparison", "system_design"] = "explainer"
    constraints: List[str] = Field(default_factory= list)
    tasks: List[Task]
    
    
class EvidenceItem(BaseModel):
    title: str
    url: str
    published_at: Optional[str] = None
    content: Optional[str] = None  
    source: Optional[str] = None
        
    
class RouterDecision(BaseModel):
    needs_research: bool = Field(description="Boolean flag indicating whether the query requires assistance from a research agent. Set to true if external research is needed to answer the query; otherwise, set to false", default= False)
    
    mode: Literal["closed_book", "Hybrid", "open_book"] = Field(description="Controls research involvement: closed_book (no research), open_book (full research), hybrid (partial research augmentation")
    
    queries: List[str]


class EvidencePack(BaseModel):
    evidence: List[EvidenceItem]
    