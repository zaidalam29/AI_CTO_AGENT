from app.llm.openai_client import OpenAIClient
from app.memory.vector_store import VectorStore
from app.utils.logger import get_logger
from app.utils.exceptions import ArchitectException
from app.schemas.agent_schema import AgentResponse, AgentStatus
from typing import Dict, Any, List
import json
import time
import asyncio

logger = get_logger(__name__)

class ArchitectAgent:
    def __init__(self):
        self.llm_client = OpenAIClient()
        self.vector_store = VectorStore()
        self.agent_type = "architect"
    
    async def design_system_architecture(
        self,
        requirements: str,
        features: List[str],
        constraints: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Design complete system architecture"""
        start_time = time.time()
        
        try:
            logger.info("Architect agent: Starting architecture design")
            
            # Parallel architecture tasks
            high_level_design_task = self._create_high_level_design(requirements, features)
            database_design_task = self._design_database_schema(requirements, features)
            api_design_task = self._design_api_spec(requirements, features)
            scaling_plan_task = self._create_scaling_plan(requirements, features)
            
            # Wait for all tasks
            high_level, database, api, scaling = await asyncio.gather(
                high_level_design_task,
                database_design_task,
                api_design_task,
                scaling_plan_task,
                return_exceptions=True
            )
            
            # Handle any errors
            architecture = {}
            for task_result, name in [
                (high_level, "high_level"),
                (database, "database"),
                (api, "api"),
                (scaling, "scaling")
            ]:
                if isinstance(task_result, Exception):
                    logger.error(f"Architecture task {name} failed: {str(task_result)}")
                    architecture[name] = {"error": str(task_result)}
                else:
                    architecture[name] = task_result
            
            # Combine all designs
            final_architecture = {
                "high_level_design": architecture.get("high_level", {}),
                "database_schema": architecture.get("database", {}),
                "api_design": architecture.get("api", {}),
                "scaling_plan": architecture.get("scaling", {}),
                "components": await self._identify_components(requirements, features),
                "tech_stack": await self._suggest_tech_stack(requirements, features),
                "data_flow": await self._design_data_flow(requirements)
            }
            
            # Store in vector DB
            await self._store_architecture(requirements, final_architecture)
            
            processing_time = time.time() - start_time
            logger.info(f"Architecture design completed in {processing_time:.2f}s")
            
            return final_architecture
            
        except Exception as e:
            logger.error(f"Architecture design failed: {str(e)}")
            raise ArchitectException(f"Architecture design failed: {str(e)}")
    
    async def _create_high_level_design(self, requirements: str, features: List[str]) -> Dict:
        """Create high-level system design"""
        prompt = f"""
        Create a high-level system design for this project.
        
        Requirements: {requirements[:500]}
        Key Features: {', '.join(features)}
        
        Include:
        1. System context diagram (textual)
        2. Main components and their responsibilities
        3. Component interactions
        4. Technology choices for each component
        
        Return as JSON with keys: context, components, interactions, technologies
        """
        
        messages = [
            {"role": "system", "content": "You are a solutions architect expert."},
            {"role": "user", "content": prompt}
        ]
        
        response = await self.llm_client.get_chat_completion_text(
            messages,
            model_type="high",
            temperature=0.3
        )
        
        return self._parse_json_response(response, {
            "context": "System context diagram pending",
            "components": [],
            "interactions": [],
            "technologies": {}
        })
    
    async def _design_database_schema(self, requirements: str, features: List[str]) -> Dict:
        """Design database schema"""
        prompt = f"""
        Design database schema for this project.
        
        Requirements: {requirements[:500]}
        Features: {', '.join(features)}
        
        Include:
        1. Tables/Collections
        2. Relationships
        3. Indexes
        4. Data types
        5. Estimated size
        
        Return as JSON with keys: tables, relationships, indexes, estimated_size
        """
        
        messages = [
            {"role": "system", "content": "You are a database architect expert."},
            {"role": "user", "content": prompt}
        ]
        
        response = await self.llm_client.get_chat_completion_text(
            messages,
            model_type="medium",
            temperature=0.2
        )
        
        return self._parse_json_response(response, {
            "tables": [],
            "relationships": [],
            "indexes": [],
            "estimated_size": "To be determined"
        })
    
    async def _design_api_spec(self, requirements: str, features: List[str]) -> Dict:
        """Design API specifications"""
        prompt = f"""
        Design API specifications for this project.
        
        Requirements: {requirements[:500]}
        Features: {', '.join(features)}
        
        Include:
        1. REST endpoints
        2. Request/Response formats
        3. Authentication
        4. Rate limiting
        5. Versioning strategy
        
        Return as JSON with keys: endpoints, auth, rate_limits, versioning
        """
        
        messages = [
            {"role": "system", "content": "You are an API design expert."},
            {"role": "user", "content": prompt}
        ]
        
        response = await self.llm_client.get_chat_completion_text(
            messages,
            model_type="medium",
            temperature=0.2
        )
        
        return self._parse_json_response(response, {
            "endpoints": [],
            "auth": "JWT based authentication",
            "rate_limits": "1000 requests/hour",
            "versioning": "URL versioning (/v1/)"
        })
    
    async def _create_scaling_plan(self, requirements: str, features: List[str]) -> Dict:
        """Create scaling plan"""
        prompt = f"""
        Create a scaling plan for this project.
        
        Requirements: {requirements[:500]}
        Features: {', '.join(features)}
        
        Include:
        1. Horizontal vs vertical scaling
        2. Load balancing strategy
        3. Caching strategy
        4. CDN usage
        5. Database scaling
        
        Return as JSON with keys: scaling_type, load_balancing, caching, cdn, db_scaling
        """
        
        messages = [
            {"role": "system", "content": "You are a scalability expert."},
            {"role": "user", "content": prompt}
        ]
        
        response = await self.llm_client.get_chat_completion_text(
            messages,
            model_type="medium",
            temperature=0.3
        )
        
        return self._parse_json_response(response, {
            "scaling_type": "Horizontal scaling",
            "load_balancing": "Round-robin with health checks",
            "caching": "Redis/Memcached",
            "cdn": "CloudFront/CloudFlare",
            "db_scaling": "Read replicas, sharding"
        })
    
    async def _identify_components(self, requirements: str, features: List[str]) -> List[Dict]:
        """Identify system components"""
        prompt = f"""
        Identify the main components of this system.
        
        Requirements: {requirements[:500]}
        Features: {', '.join(features)}
        
        For each component, provide:
        - name
        - purpose
        - technologies
        - dependencies
        
        Return as JSON array.
        """
        
        messages = [
            {"role": "system", "content": "You are a system architect."},
            {"role": "user", "content": prompt}
        ]
        
        response = await self.llm_client.get_chat_completion_text(
            messages,
            model_type="medium",
            temperature=0.2
        )
        
        return self._parse_json_response(response, [
            {"name": "Frontend", "purpose": "User interface", "technologies": ["React"], "dependencies": []},
            {"name": "Backend API", "purpose": "Business logic", "technologies": ["FastAPI"], "dependencies": ["Frontend"]},
            {"name": "Database", "purpose": "Data storage", "technologies": ["PostgreSQL"], "dependencies": ["Backend API"]}
        ])
    
    async def _suggest_tech_stack(self, requirements: str, features: List[str]) -> Dict:
        """Suggest technology stack"""
        prompt = f"""
        Suggest a complete technology stack for this project.
        
        Requirements: {requirements[:500]}
        Features: {', '.join(features)}
        
        Return as JSON with keys:
        frontend, backend, database, cache, message_queue, monitoring, ci_cd
        Each should be an array of technologies with versions.
        """
        
        messages = [
            {"role": "system", "content": "You are a technology stack expert."},
            {"role": "user", "content": prompt}
        ]
        
        response = await self.llm_client.get_chat_completion_text(
            messages,
            model_type="medium",
            temperature=0.2
        )
        
        return self._parse_json_response(response, {
            "frontend": ["React 18", "TypeScript 5", "Tailwind CSS"],
            "backend": ["Python 3.11", "FastAPI", "SQLAlchemy"],
            "database": ["PostgreSQL 15", "Redis 7"],
            "cache": ["Redis"],
            "message_queue": ["RabbitMQ"],
            "monitoring": ["Prometheus", "Grafana"],
            "ci_cd": ["GitHub Actions", "Docker", "Kubernetes"]
        })
    
    async def _design_data_flow(self, requirements: str) -> Dict:
        """Design data flow"""
        prompt = f"""
        Design the data flow for this system.
        
        Requirements: {requirements[:500]}
        
        Include:
        1. How data enters the system
        2. How it's processed
        3. Where it's stored
        4. How it's retrieved
        5. Data validation and transformation
        
        Return as JSON with keys: entry_points, processing_pipeline, storage, retrieval, validation
        """
        
        messages = [
            {"role": "system", "content": "You are a data architect."},
            {"role": "user", "content": prompt}
        ]
        
        response = await self.llm_client.get_chat_completion_text(
            messages,
            model_type="medium",
            temperature=0.2
        )
        
        return self._parse_json_response(response, {
            "entry_points": ["API endpoints", "Webhooks"],
            "processing_pipeline": ["Validation", "Business logic", "Storage"],
            "storage": ["Primary database", "Cache", "File storage"],
            "retrieval": ["API queries", "Cached responses"],
            "validation": ["Input validation", "Business rule validation"]
        })
    
    async def _store_architecture(self, requirements: str, architecture: Dict):
        """Store architecture in vector DB"""
        try:
            embedding = await self.llm_client.create_embedding(requirements)
            await self.vector_store.add_document(
                collection_name="architectures",
                document=json.dumps(architecture),
                embedding=embedding,
                metadata={"type": "system_architecture"}
            )
        except Exception as e:
            logger.warning(f"Failed to store architecture: {str(e)}")
    
    def _parse_json_response(self, response: str, default: Any) -> Any:
        """Parse JSON from LLM response"""
        try:
            # Find JSON in response
            start = response.find('{')
            if start == -1:
                start = response.find('[')
            end = response.rfind('}') + 1
            if end == 0:
                end = response.rfind(']') + 1
            
            if start >= 0 and end > start:
                json_str = response[start:end]
                return json.loads(json_str)
            else:
                return default
        except:
            return default