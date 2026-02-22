from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class ProjectType(str, Enum):
    WEB_APP = "web_app"
    MOBILE_APP = "mobile_app"
    API = "api"
    ML_SERVICE = "ml_service"
    ECOMMERCE = "ecommerce"
    OTHER = "other"

class ProjectStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class ProjectRequest(BaseModel):
    """Project analysis request schema"""
    name: str = Field(..., min_length=3, max_length=100)
    requirements: str = Field(..., min_length=10, max_length=10000)
    project_type: ProjectType = ProjectType.WEB_APP
    budget_range: Optional[str] = Field(None, max_length=50)
    timeline: Optional[str] = Field(None, max_length=50)
    
    @field_validator('name')
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError('Project name cannot be empty')
        return v.strip()
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "E-commerce Platform",
                "requirements": "Build a modern e-commerce platform with user auth, product catalog...",
                "project_type": "web_app",
                "budget_range": "$50,000 - $100,000",
                "timeline": "3 months"
            }
        }
    )

class Feature(BaseModel):
    name: str
    description: str
    priority: str  # high, medium, low
    estimated_hours: Optional[int] = None

class Sprint(BaseModel):
    number: int
    name: str
    duration_weeks: int
    features: List[str]
    deliverables: List[str]

class TechStack(BaseModel):
    frontend: List[str] = []
    backend: List[str] = []
    database: List[str] = []
    devops: List[str] = []
    third_party: List[str] = []

class Architecture(BaseModel):
    high_level_design: str
    components: List[Dict[str, Any]]
    data_flow: str
    scaling_strategy: str
    tech_stack: TechStack

class Risk(BaseModel):
    category: str
    description: str
    probability: float  # 0-1
    impact: str  # low, medium, high
    mitigation: str

class ProjectPlan(BaseModel):
    """Complete project plan response"""
    features: List[Feature]
    tech_stack: TechStack
    sprints: List[Sprint]
    architecture: Architecture
    risks: List[Risk]
    estimated_timeline_months: float
    estimated_cost_range: str
    
class ProjectResponse(BaseModel):
    """Project analysis response schema"""
    success: bool
    message: Optional[str] = None
    data: Optional[ProjectPlan] = None
    error: Optional[Dict[str, Any]] = None
    request_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": True,
                "data": {
                    "features": [],
                    "tech_stack": {},
                    "sprints": [],
                    "architecture": {},
                    "risks": [],
                    "estimated_timeline_months": 3.5,
                    "estimated_cost_range": "$50,000 - $75,000"
                },
                "request_id": "req_123456",
                "timestamp": "2024-01-01T00:00:00"
            }
        }
    )