from pydantic import BaseModel
from datetime import datetime


class PolicyDecision(BaseModel):
    status: str   # "approved" or "blocked"
    reason: str   # brief explanation for teachers/admins


class PolicyMetadata(BaseModel):
    checked_at: datetime
    rules_version: str  # version of curriculum/safety ruleset


class SafetyPolicyOutput(BaseModel):
    policy_id: str
    curation_id: str
    status: str          # "approved" or "blocked"
    reason: str          # why the decision was made
    metadata: PolicyMetadata
