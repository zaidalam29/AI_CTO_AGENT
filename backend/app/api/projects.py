# app/api/projects.py
from fastapi import APIRouter, Request, Depends, BackgroundTasks
from fastapi.responses import JSONResponse
from app.schemas.project_schema import ProjectRequest
from app.core.orchestrator import Orchestrator
from app.utils.logger import get_logger, LoggerContext
from app.utils.exceptions import ValidationException
from app.utils.rate_limiter import RateLimiter
import uuid
import time
import asyncio
from typing import Dict, Any

router = APIRouter(prefix="/projects", tags=["projects"])
logger = get_logger(__name__)

# Orchestrator initialization and rate limiter setup
orchestrator = Orchestrator()
rate_limiter = RateLimiter()

# Store metrics
metrics_data = {
    "total_requests": 0,
    "successful_requests": 0,
    "failed_requests": 0,
    "total_processing_time": 0,
    "average_processing_time": 0,
    "requests_by_endpoint": {},
    "requests_by_agent": {},
    "start_time": time.time()
}

async def get_request_id(request: Request) -> str:
    """Generate or extract request ID"""
    request_id = request.headers.get("X-Request-ID")
    if not request_id:
        request_id = f"req_{uuid.uuid4().hex[:12]}"
    return request_id

def update_metrics(endpoint: str, success: bool, processing_time: float, agents_used: list = None):
    """Update metrics data"""
    global metrics_data
    
    metrics_data["total_requests"] += 1
    if success:
        metrics_data["successful_requests"] += 1
    else:
        metrics_data["failed_requests"] += 1
    
    metrics_data["total_processing_time"] += processing_time
    metrics_data["average_processing_time"] = metrics_data["total_processing_time"] / metrics_data["total_requests"]
    
    # Update endpoint metrics
    if endpoint not in metrics_data["requests_by_endpoint"]:
        metrics_data["requests_by_endpoint"][endpoint] = 0
    metrics_data["requests_by_endpoint"][endpoint] += 1
    
    # Update agent metrics
    if agents_used:
        for agent in agents_used:
            if agent not in metrics_data["requests_by_agent"]:
                metrics_data["requests_by_agent"][agent] = 0
            metrics_data["requests_by_agent"][agent] += 1

@router.post("/analyze")
async def analyze_project(
    request: Request,
    project_request: ProjectRequest,
    background_tasks: BackgroundTasks,
    request_id: str = Depends(get_request_id)
):
    """Analyze project using ALL agents"""
    start_time = time.time()
    success = False
    agents_used = []
    
    with LoggerContext(
        request_id=request_id,
        endpoint="/analyze",
        project_name=project_request.name
    ) as log:
        
        try:
            log.info(f"🚀 Starting project analysis with ALL agents")
            agents_used = orchestrator.get_active_agents()
            log.info(f"🤖 Active agents: {', '.join(agents_used)}")
            
            # Validate input
            if not project_request.requirements.strip():
                raise ValidationException("Requirements cannot be empty")
            
            # Rate limiting
            client_ip = request.client.host if request.client else "unknown"
            is_allowed, limit_info = await rate_limiter.check_limit(client_ip)
            
            if not is_allowed:
                return JSONResponse(
                    status_code=429,
                    content={
                        "success": False,
                        "error": {
                            "code": "RATE_LIMIT_EXCEEDED",
                            "message": "Too many requests",
                            "details": limit_info
                        },
                        "request_id": request_id
                    }
                )
            
            # Call orchestrator
            log.info("⏳ Calling orchestrator with all agents...")
            result = await orchestrator.process_project_request(project_request.dict())
            
            processing_time = time.time() - start_time
            success = True
            log.info(f"✅ All agents completed in {processing_time:.2f}s")
            
            # Update metrics in background
            background_tasks.add_task(
                update_metrics,
                endpoint="/analyze",
                success=True,
                processing_time=processing_time,
                agents_used=agents_used
            )
            
            # Return combined response
            return {
                "success": True,
                "message": "Project analysis completed with all agents",
                "data": result,
                "request_id": request_id,
                "processing_time": f"{processing_time:.2f}s",
                "agents_used": agents_used
            }
            
        except ValidationException as e:
            processing_time = time.time() - start_time
            background_tasks.add_task(
                update_metrics,
                endpoint="/analyze",
                success=False,
                processing_time=processing_time
            )
            
            return JSONResponse(
                status_code=422,
                content={
                    "success": False,
                    "error": {
                        "code": "VALIDATION_ERROR",
                        "message": e.message
                    },
                    "request_id": request_id
                }
            )
            
        except Exception as e:
            processing_time = time.time() - start_time
            background_tasks.add_task(
                update_metrics,
                endpoint="/analyze",
                success=False,
                processing_time=processing_time
            )
            
            log.error(f"❌ Error: {str(e)}", exc_info=True)
            return JSONResponse(
                status_code=500,
                content={
                    "success": False,
                    "error": {
                        "code": "INTERNAL_SERVER_ERROR",
                        "message": str(e) if request.app.debug else "Internal server error"
                    },
                    "request_id": request_id
                }
            )

# ============= ADD THESE MISSING ENDPOINTS =============

@router.get("/health")
async def projects_health():
    """Health check for projects API"""
    return {
        "status": "healthy",
        "service": "projects-api",
        "timestamp": time.time(),
        "agents_available": orchestrator.get_active_agents()
    }

@router.get("/metrics")
async def get_metrics():
    """Get API metrics and statistics"""
    global metrics_data
    
    uptime = time.time() - metrics_data["start_time"]
    
    return {
        "success": True,
        "data": {
            "total_requests": metrics_data["total_requests"],
            "successful_requests": metrics_data["successful_requests"],
            "failed_requests": metrics_data["failed_requests"],
            "success_rate": f"{(metrics_data['successful_requests'] / max(1, metrics_data['total_requests']) * 100):.2f}%",
            "average_processing_time": f"{metrics_data['average_processing_time']:.2f}s",
            "total_processing_time": f"{metrics_data['total_processing_time']:.2f}s",
            "requests_by_endpoint": metrics_data["requests_by_endpoint"],
            "requests_by_agent": metrics_data["requests_by_agent"],
            "uptime": f"{uptime:.2f}s",
            "uptime_formatted": format_uptime(uptime),
            "rate_limit": {
                "requests_per_minute": rate_limiter.requests_per_minute,
                "total_requests_tracked": rate_limiter.total_requests
            }
        },
        "timestamp": time.time()
    }

@router.get("/stats")
async def get_stats():
    """Get detailed statistics about analyzed projects"""
    # This would typically come from database
    # For now, return metrics data
    return await get_metrics()

@router.delete("/metrics/reset")
async def reset_metrics():
    """Reset metrics counter (admin only)"""
    global metrics_data
    
    # In production, add authentication here
    metrics_data = {
        "total_requests": 0,
        "successful_requests": 0,
        "failed_requests": 0,
        "total_processing_time": 0,
        "average_processing_time": 0,
        "requests_by_endpoint": {},
        "requests_by_agent": {},
        "start_time": time.time()
    }
    
    # Reset rate limiter
    rate_limiter.requests.clear()
    rate_limiter.total_requests = 0
    
    return {
        "success": True,
        "message": "Metrics reset successfully",
        "timestamp": time.time()
    }

@router.get("/config")
async def get_config():
    """Get current configuration (sanitized)"""
    from app.config import settings
    
    # Return non-sensitive config
    return {
        "app_name": settings.APP_NAME,
        "environment": settings.ENVIRONMENT,
        "debug": settings.DEBUG,
        "rate_limit_requests": settings.RATE_LIMIT_REQUESTS,
        "rate_limit_period": settings.RATE_LIMIT_PERIOD,
        "log_level": settings.LOG_LEVEL,
        "vector_db_path": settings.VECTOR_DB_PATH,
        "agents_available": orchestrator.get_active_agents()
    }

@router.get("/agents")
async def list_agents():
    """List all available agents and their status"""
    agents = orchestrator.get_active_agents()
    
    agent_info = []
    for agent_name in agents:
        agent_info.append({
            "name": agent_name,
            "status": "active",
            "description": get_agent_description(agent_name)
        })
    
    return {
        "success": True,
        "total_agents": len(agent_info),
        "agents": agent_info
    }

@router.get("/agent/{agent_name}")
async def get_agent_info(agent_name: str):
    """Get information about a specific agent"""
    agents = orchestrator.get_active_agents()
    
    if agent_name not in agents:
        return JSONResponse(
            status_code=404,
            content={
                "success": False,
                "error": f"Agent '{agent_name}' not found"
            }
        )
    
    return {
        "success": True,
        "agent": {
            "name": agent_name,
            "description": get_agent_description(agent_name),
            "status": "active",
            "capabilities": get_agent_capabilities(agent_name)
        }
    }

@router.get("/version")
async def get_version():
    """Get API version information"""
    return {
        "success": True,
        "version": "1.0.0",
        "api_version": "v1",
        "build_date": "2024-02-20",
        "python_version": "3.9+",
        "dependencies": {
            "fastapi": "0.104+",
            "openai": "1.3+",
            "chromadb": "0.4+"
        }
    }

@router.get("/ping")
async def ping():
    """Simple ping endpoint for connectivity testing"""
    return {
        "success": True,
        "message": "pong",
        "timestamp": time.time()
    }

# Helper functions
def format_uptime(seconds: float) -> str:
    """Format uptime in human readable format"""
    days = int(seconds // 86400)
    hours = int((seconds % 86400) // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    
    parts = []
    if days > 0:
        parts.append(f"{days}d")
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    parts.append(f"{seconds}s")
    
    return " ".join(parts)

def get_agent_description(agent_name: str) -> str:
    """Get description for each agent"""
    descriptions = {
        "planner": "Analyzes requirements, extracts features, estimates timeline and cost",
        "architect": "Designs system architecture, database schema, and API specifications",
        "risk": "Identifies technical, business, and security risks with ML predictions",
        "sprint": "Creates detailed sprint plans with user stories and story points",
        "devops": "Designs CI/CD pipelines, infrastructure requirements, and monitoring",
        "code_review": "Analyzes code quality, security issues, and performance concerns"
    }
    return descriptions.get(agent_name, "AI agent for project analysis")

def get_agent_capabilities(agent_name: str) -> list:
    """Get capabilities for each agent"""
    capabilities = {
        "planner": ["Feature extraction", "Tech stack recommendation", "Cost estimation", "Timeline prediction"],
        "architect": ["System design", "Database schema", "API design", "Scaling strategy"],
        "risk": ["Risk identification", "ML-based prediction", "Mitigation strategies", "Risk scoring"],
        "sprint": ["Sprint planning", "User story creation", "Story point estimation", "Velocity calculation"],
        "devops": ["CI/CD pipeline", "Infrastructure design", "Monitoring setup", "Backup strategy"],
        "code_review": ["Code quality analysis", "Security audit", "Performance review", "Fix suggestions"]
    }
    return capabilities.get(agent_name, ["Project analysis"])