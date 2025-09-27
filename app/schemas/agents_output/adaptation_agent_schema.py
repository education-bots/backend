from pydantic import BaseModel
from typing import Literal, Optional
from datetime import datetime


class AdaptationDecision(BaseModel):
    action: Literal["advance", "practice", "remediation"]              # "advance", "practice", or "remediation"
    items_requested: int     # how many new items/exercises to fetch
    difficulty: Literal["easy", "medium", "hard"]          # "easy", "medium", "hard"
    reason: str              # teacher-friendly explanation


class MasteryUpdate(BaseModel):
    previous_mastery: float
    new_mastery: float
    confidence: Literal["low", "medium", "high"]         # "low", "medium", "high"


class AdaptationMetadata(BaseModel):
    updated_at: datetime
    model: Literal["EWMA", "Bayesian"]               # e.g. "EWMA", "Bayesian"
    alpha: Optional[float]   # smoothing parameter if used


class AdaptationOutputSchema(BaseModel):
    adaptation_id: str
    learner_id: str
    skill_id: str
    new_mastery: float
    decision: AdaptationDecision
    mastery_update: MasteryUpdate
    metadata: AdaptationMetadata
