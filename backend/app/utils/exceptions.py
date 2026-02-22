from fastapi import status
from typing import Any, Dict, Optional

class AppException(Exception):
    """Base application exception"""
    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(message)

class NotFoundException(AppException):
    """Resource not found exception"""
    def __init__(self, resource: str, resource_id: Any = None):
        message = f"{resource} not found"
        if resource_id:
            message += f" with id: {resource_id}"
        super().__init__(
            message=message,
            status_code=status.HTTP_404_NOT_FOUND
        )

class ValidationException(AppException):
    """Validation error exception"""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            details=details
        )

class AuthenticationException(AppException):
    """Authentication error exception"""
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED
        )

class AuthorizationException(AppException):
    """Authorization error exception"""
    def __init__(self, message: str = "Not authorized"):
        super().__init__(
            message=message,
            status_code=status.HTTP_403_FORBIDDEN
        )

class RateLimitException(AppException):
    """Rate limit exceeded exception"""
    def __init__(self, message: str = "Rate limit exceeded"):
        super().__init__(
            message=message,
            status_code=status.HTTP_429_TOO_MANY_REQUESTS
        )

# ============= LLM Exceptions =============
class LLMException(AppException):
    """Base LLM service exception"""
    def __init__(self, message: str, provider: str, details: Optional[Dict] = None):
        super().__init__(
            message=f"{provider} error: {message}",
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            details={"provider": provider, **(details or {})}
        )

class OpenAIException(LLMException):
    """OpenAI specific exception"""
    def __init__(self, message: str, details: Optional[Dict] = None):
        super().__init__(message, "OpenAI", details)

class OpenRouterException(LLMException):
    """OpenRouter specific exception"""
    def __init__(self, message: str, details: Optional[Dict] = None):
        super().__init__(message, "OpenRouter", details)

class CohereException(LLMException):
    """Cohere specific exception"""
    def __init__(self, message: str, details: Optional[Dict] = None):
        super().__init__(message, "Cohere", details)

# ============= Agent Exceptions =============
class AgentException(AppException):
    """Base agent exception"""
    def __init__(self, message: str, agent_name: str, details: Optional[Dict] = None):
        super().__init__(
            message=f"{agent_name} agent error: {message}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            details={"agent": agent_name, **(details or {})}
        )

class PlannerException(AgentException):
    """Planner agent exception"""
    def __init__(self, message: str, details: Optional[Dict] = None):
        super().__init__(message, "Planner", details)

class ArchitectException(AgentException):
    """Architect agent exception"""
    def __init__(self, message: str, details: Optional[Dict] = None):
        super().__init__(message, "Architect", details)

class RiskException(AgentException):
    """Risk agent exception"""
    def __init__(self, message: str, details: Optional[Dict] = None):
        super().__init__(message, "Risk", details)

class CodeReviewException(AgentException):
    """Code review agent exception"""
    def __init__(self, message: str, details: Optional[Dict] = None):
        super().__init__(message, "CodeReview", details)

class DevOpsException(AgentException):
    """DevOps agent exception"""
    def __init__(self, message: str, details: Optional[Dict] = None):
        super().__init__(message, "DevOps", details)

class SprintException(AgentException):
    """Sprint agent exception"""
    def __init__(self, message: str, details: Optional[Dict] = None):
        super().__init__(message, "Sprint", details)

# ============= Database Exceptions =============
class DatabaseException(AppException):
    """Database exception"""
    def __init__(self, message: str, details: Optional[Dict] = None):
        super().__init__(
            message=f"Database error: {message}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            details=details
        )

class VectorStoreException(AppException):
    """Vector store exception"""
    def __init__(self, message: str, details: Optional[Dict] = None):
        super().__init__(
            message=f"Vector store error: {message}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            details=details
        )

# ============= MCP Exceptions =============
class MCPException(AppException):
    """MCP tool exception"""
    def __init__(self, message: str, tool: str, details: Optional[Dict] = None):
        super().__init__(
            message=f"MCP {tool} error: {message}",
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            details={"tool": tool, **(details or {})}
        )