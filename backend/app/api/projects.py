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

router = APIRouter(prefix="/projects", tags=["projects"])
logger = get_logger(__name__)

# Orchestrator initialization and rate limiter setup
orchestrator = Orchestrator()
rate_limiter = RateLimiter()

async def get_request_id(request: Request) -> str:
    request_id = request.headers.get("X-Request-ID")
    if not request_id:
        request_id = f"req_{uuid.uuid4().hex[:12]}"
    return request_id

@router.post("/analyze")
async def analyze_project(
    request: Request,
    project_request: ProjectRequest,
    background_tasks: BackgroundTasks,
    request_id: str = Depends(get_request_id)
):
    """Analyze project using ALL agents"""
    start_time = time.time()
    
    with LoggerContext(
        request_id=request_id,
        endpoint="/analyze",
        project_name=project_request.name
    ) as log:
        
        try:
            log.info(f"🚀 Starting project analysis with ALL agents")
            log.info(f"🤖 Active agents: {', '.join(orchestrator.get_active_agents())}")
            
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
            
            # Call orchestrator (jo saare agents ko manage karega)
            log.info("⏳ Calling orchestrator with all agents...")
            result = await orchestrator.process_project_request(project_request.dict())
            
            processing_time = time.time() - start_time
            log.info(f"✅ All agents completed in {processing_time:.2f}s")
            
            # Return combined response
            return {
                "success": True,
                "message": "Project analysis completed with all agents",
                "data": result,
                "request_id": request_id,
                "processing_time": f"{processing_time:.2f}s",
                "agents_used": orchestrator.get_active_agents()
            }
            
        except ValidationException as e:
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