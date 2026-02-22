from openai import AsyncOpenAI, APIError, RateLimitError, APITimeoutError
from app.config import settings
from app.utils.logger import get_logger
from app.utils.exceptions import OpenAIException
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)
from typing import List, Dict, Any, Optional
import asyncio
import tiktoken

logger = get_logger(__name__)

class OpenAIClient:
    def __init__(self):
        if not settings.OPENAI_API_KEY:
            logger.warning("⚠️ OpenAI API key not configured")
            self.client = None
        else:
            self.client = AsyncOpenAI(
                api_key=settings.OPENAI_API_KEY,
                timeout=60.0,
                max_retries=0
            )
        
        self.models = {
            "high": "gpt-3.5-turbo-16k",  # Fallback models
            "medium": "gpt-3.5-turbo",
            "fast": "gpt-3.5-turbo"
        }
        self.embedding_model = "text-embedding-ada-002"
        
        # Token counter
        try:
            self.encoding = tiktoken.get_encoding("cl100k_base")
        except:
            self.encoding = None
    
    def count_tokens(self, text: str) -> int:
        """Count tokens in text"""
        if self.encoding:
            try:
                return len(self.encoding.encode(text))
            except:
                return len(text) // 4
        return len(text) // 4
    
    async def chat_completion(
        self, 
        messages: List[Dict[str, str]], 
        model_type: str = "medium",
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> Dict[str, Any]:
        """Get chat completion from OpenAI"""
        
        # Agar client nahi hai to mock response do
        if not self.client:
            logger.warning("OpenAI client not available, returning mock response")
            return {
                "content": json.dumps({
                    "message": "OpenAI API key not configured. Please add your API key in .env file",
                    "features": [
                        {"name": "Sample Feature", "description": "This is a sample feature", "priority": "medium"}
                    ]
                }),
                "model": "mock",
                "usage": {"total_tokens": 0}
            }
        
        try:
            # Select model
            model = self.models.get(model_type, self.models["medium"])
            
            # Log token usage
            input_tokens = self.count_tokens(str(messages))
            logger.info(f"OpenAI request - Model: {model}")
            
            # Make API call
            response = await self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            result = {
                "content": response.choices[0].message.content,
                "model": response.model,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens if response.usage else 0,
                    "completion_tokens": response.usage.completion_tokens if response.usage else 0,
                    "total_tokens": response.usage.total_tokens if response.usage else 0
                }
            }
            
            return result
            
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            # Return mock response on error
            return {
                "content": json.dumps({
                    "error": str(e),
                    "features": [
                        {"name": "Error Recovery Feature", "description": "API error occurred", "priority": "high"}
                    ]
                }),
                "model": "error",
                "usage": {"total_tokens": 0}
            }
    
    async def get_chat_completion_text(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Get just the text content"""
        result = await self.chat_completion(messages, **kwargs)
        return result["content"]
    
    async def create_embedding(self, text: str) -> List[float]:
        """Create embedding for text"""
        if not self.client:
            logger.warning("OpenAI client not available, returning random embedding")
            import random
            return [random.random() for _ in range(1536)]
        
        try:
            if len(text) > 8000:
                text = text[:8000]
            
            response = await self.client.embeddings.create(
                model=self.embedding_model,
                input=text
            )
            
            return response.data[0].embedding
            
        except Exception as e:
            logger.error(f"Embedding error: {str(e)}")
            import random
            return [random.random() for _ in range(1536)]