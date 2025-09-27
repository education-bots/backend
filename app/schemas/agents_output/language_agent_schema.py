from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class AdaptedContent(BaseModel):
    content_id: str
    text_language: str
    text_in_english: str
    codeswitched_text: Optional[str] = None
    reading_level: str
    
class AdaptedPracticeItem(BaseModel):
    item_id: str
    prompt_language: str
    prompt_in_english: str
    expected_answer: str
    
class LanguageBridgeMetadata(BaseModel):
    translation_style: str
    grade_adjustment: str
    adapted_at: datetime
    
class LanguageBridgeOutputSchema(BaseModel):
    bridge_id: str
    curation_id: str
    adapted_content: List[AdaptedContent]
    adapted_practice_items: List[AdaptedPracticeItem]
    metadata: LanguageBridgeMetadata