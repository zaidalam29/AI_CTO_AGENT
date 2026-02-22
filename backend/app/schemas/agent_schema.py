from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum

class AgentType(str, Enum):
    PLANNER = "planner"
    ARCHITECT = "architect"
    RISK = "risk"
    CODE_REVIEW = "code_review"
    DEVOPS = "devops"
    SPRINT = "sprint"
    SECURITY = "security"
    TESTING = "testing"

class AgentStatus(str, Enum):
    IDLE = "idle"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class AgentTask(BaseModel):
    """Task for agent to process"""
    task_id: str
    agent_type: AgentType
    input_data: Dict[str, Any]
    priority: TaskPriority = TaskPriority.MEDIUM
    context: Optional[Dict[str, Any]] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class AgentResponse(BaseModel):
    """Response from agent"""
    task_id: str
    agent_type: AgentType
    status: AgentStatus
    output_data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    processing_time: float
    metadata: Dict[str, Any] = Field(default_factory=dict)

# Risk Assessment Schemas
class RiskCategory(str, Enum):
    TECHNICAL = "technical"
    BUSINESS = "business"
    TIMELINE = "timeline"
    RESOURCE = "resource"
    SECURITY = "security"
    COMPLIANCE = "compliance"

class RiskAssessment(BaseModel):
    category: RiskCategory
    description: str
    probability: float  # 0-1
    impact: str  # low, medium, high, critical
    mitigation: str
    owner: Optional[str] = None
    deadline: Optional[datetime] = None

# Code Review Schemas
class CodeIssue(BaseModel):
    line: Optional[int]
    severity: str  # error, warning, info
    message: str
    suggestion: str
    rule: Optional[str] = None

class CodeReviewResult(BaseModel):
    file_path: str
    language: str
    issues: List[CodeIssue]
    quality_score: float  # 0-100
    complexity_score: float
    security_issues: List[str]
    performance_concerns: List[str]

# DevOps Schemas
class DeploymentStrategy(str, Enum):
    BLUE_GREEN = "blue_green"
    CANARY = "canary"
    ROLLING = "rolling"
    RECREATE = "recreate"

class InfrastructureRequirement(BaseModel):
    resource_type: str  # cpu, memory, storage
    min_value: str
    max_value: str
    recommended: str

class DevOpsPlan(BaseModel):
    ci_cd_pipeline: List[str]
    infrastructure: Dict[str, InfrastructureRequirement]
    deployment_strategy: DeploymentStrategy
    monitoring_tools: List[str]
    backup_strategy: str
    disaster_recovery: str

# Sprint Schemas
class UserStory(BaseModel):
    id: str
    title: str
    description: str
    points: int
    dependencies: List[str] = []
    assignee: Optional[str] = None

class SprintPlan(BaseModel):
    sprint_number: int
    duration_days: int
    start_date: datetime
    end_date: datetime
    user_stories: List[UserStory]
    goals: List[str]
    risks: List[str]
    capacity: int  # story points