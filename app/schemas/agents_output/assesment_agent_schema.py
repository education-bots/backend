from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class QuizItems(BaseModel):
    item_id: str
    prompt: str
    type: str
    options: Optional[List[str]] = None
    expected_answer: str
    learner_response: Optional[str] = None
    is_correct: Optional[bool] = None
    hints_used: Optional[int] = 0
    time_taken_seconds: Optional[int] = None
    detected_misconceptions: Optional[List[str]] = None
    
class QuizSummary(BaseModel):
    total_items: int
    correct_items: int
    accuracy: float
    average_time_per_item_seconds: float
    hints_total: int
    misconceptions_deteected: List[str]
    
class MasteryEstimated(BaseModel):
    previous_mastery: float
    updated_mastery: float
    confidence: str
    
class AssessmentMetadata(BaseModel):
    assesment_type: str
    generated_at: datetime
    source: str
    
class AssessmentOutputSchema(BaseModel):
    assessment_id: str
    learner_id: str
    skill_id: str
    grade_level: str
    micro_quiz: List[QuizItems]
    summary: QuizSummary
    mastery_estimated: MasteryEstimated
    metadata: AssessmentMetadata