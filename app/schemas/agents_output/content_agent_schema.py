from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class Passage(BaseModel):
    passage_id: str
    text: str
    source_pdf: str
    page: int
    difficulty_level: Optional[str]
    reading_level: str
    
class PracticeItem(BaseModel):
    item_id: str
    prompt: str
    type: str
    options: Optional[List[str]] = None
    correct: str
    
class ContentCuratorMetadata(BaseModel):
    aligned_curriculum: str
    retrieved_at: datetime
    
class ContentCuratorOutputSchema(BaseModel):
    curation_id: str
    learner_id: str
    skill_id: str
    topic: str
    passage: List[Passage]
    practice_items: List[PracticeItem]
    metadata: ContentCuratorMetadata