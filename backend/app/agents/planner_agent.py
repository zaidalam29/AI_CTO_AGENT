from app.llm.openai_client import OpenAIClient
from app.memory.vector_store import VectorStore
from app.utils.logger import get_logger
from app.utils.exceptions import AppException
from app.schemas.project_schema import Feature, Sprint, TechStack, Risk, ProjectPlan
from typing import Dict, Any, List, Optional
import json
import asyncio
from datetime import datetime

logger = get_logger(__name__)

class PlannerAgent:
    def __init__(self):
        self.llm_client = OpenAIClient()
        self.vector_store = VectorStore()
        
    async def extract_features(self, requirements: str) -> List[Feature]:
        """Extract features from requirements"""
        try:
            prompt = f"""
            Analyze these project requirements and extract key features.
            For each feature, provide:
            - name: Short feature name
            - description: Detailed description
            - priority: high/medium/low
            - estimated_hours: Estimated development hours
            
            Requirements:
            {requirements}
            
            Return as JSON array with format:
            [{{"name": "...", "description": "...", "priority": "...", "estimated_hours": 0}}]
            """
            
            messages = [
                {
                    "role": "system",
                    "content": "You are a product manager expert at breaking down requirements into features."
                },
                {"role": "user", "content": prompt}
            ]
            
            response = await self.llm_client.get_chat_completion_text(
                messages,
                model_type="medium",
                temperature=0.3
            )
            
            # Parse JSON response
            try:
                # Find JSON in response
                start = response.find('[')
                end = response.rfind(']') + 1
                if start >= 0 and end > start:
                    json_str = response[start:end]
                    features_data = json.loads(json_str)
                else:
                    features_data = json.loads(response)
                
                # Convert to Feature objects
                features = []
                for f in features_data:
                    feature = Feature(
                        name=f.get("name", "Unnamed"),
                        description=f.get("description", ""),
                        priority=f.get("priority", "medium"),
                        estimated_hours=f.get("estimated_hours")
                    )
                    features.append(feature)
                    
                return features
                
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse features JSON: {e}")
                # Return default feature
                return [Feature(
                    name="Main Feature",
                    description=requirements[:200],
                    priority="high",
                    estimated_hours=None
                )]
                
        except Exception as e:
            logger.error(f"Feature extraction failed: {str(e)}")
            raise AppException(f"Feature extraction failed: {str(e)}")
    
    async def suggest_tech_stack(self, requirements: str, features: List[Feature]) -> TechStack:
        """Suggest technology stack"""
        try:
            feature_names = [f.name for f in features]
            prompt = f"""
            Based on these requirements and features, suggest an appropriate technology stack.
            
            Requirements: {requirements[:500]}
            
            Features: {', '.join(feature_names)}
            
            Return as JSON with keys: frontend, backend, database, devops, third_party
            Each should be an array of technologies.
            """
            
            messages = [
                {
                    "role": "system",
                    "content": "You are a solutions architect expert at choosing technology stacks."
                },
                {"role": "user", "content": prompt}
            ]
            
            response = await self.llm_client.get_chat_completion_text(
                messages,
                model_type="medium",
                temperature=0.2
            )
            
            # Parse JSON
            try:
                # Find JSON in response
                start = response.find('{')
                end = response.rfind('}') + 1
                if start >= 0 and end > start:
                    json_str = response[start:end]
                    stack_data = json.loads(json_str)
                else:
                    stack_data = json.loads(response)
                
                return TechStack(
                    frontend=stack_data.get("frontend", []),
                    backend=stack_data.get("backend", []),
                    database=stack_data.get("database", []),
                    devops=stack_data.get("devops", []),
                    third_party=stack_data.get("third_party", [])
                )
                
            except json.JSONDecodeError:
                logger.warning("Failed to parse tech stack JSON, using defaults")
                return TechStack(
                    frontend=["React", "TypeScript"],
                    backend=["Python", "FastAPI"],
                    database=["PostgreSQL"],
                    devops=["Docker", "AWS"],
                    third_party=[]
                )
                
        except Exception as e:
            logger.error(f"Tech stack suggestion failed: {str(e)}")
            return TechStack()  # Return empty stack on error
    
    async def create_sprints(self, features: List[Feature]) -> List[Sprint]:
        """Create sprint plan"""
        try:
            # Group features into sprints (simplified logic)
            sprints = []
            features_per_sprint = max(2, len(features) // 4)  # 4 sprints
            
            for i in range(0, len(features), features_per_sprint):
                sprint_features = features[i:i + features_per_sprint]
                sprint_num = i // features_per_sprint + 1
                
                sprint = Sprint(
                    number=sprint_num,
                    name=f"Sprint {sprint_num}",
                    duration_weeks=2,
                    features=[f.name for f in sprint_features],
                    deliverables=[f"Implement {f.name}" for f in sprint_features]
                )
                sprints.append(sprint)
                
                if len(sprints) >= 4:  # Max 4 sprints
                    break
            
            return sprints or [Sprint(
                number=1,
                name="Initial Sprint",
                duration_weeks=2,
                features=["Setup", "Basic Features"],
                deliverables=["Project setup", "Core functionality"]
            )]
            
        except Exception as e:
            logger.error(f"Sprint creation failed: {str(e)}")
            return [Sprint(
                number=1,
                name="Default Sprint",
                duration_weeks=2,
                features=["Implementation"],
                deliverables=["Project completion"]
            )]
    
    async def assess_risks(self, requirements: str, features: List[Feature]) -> List[Risk]:
        """Assess project risks"""
        try:
            prompt = f"""
            Identify potential risks for this project.
            For each risk, provide:
            - category: technical/business/timeline/resource
            - description: What could go wrong
            - probability: 0.0 to 1.0
            - impact: low/medium/high
            - mitigation: How to prevent or handle
            
            Requirements: {requirements[:500]}
            Features: {', '.join([f.name for f in features])}
            
            Return as JSON array.
            """
            
            messages = [
                {
                    "role": "system",
                    "content": "You are a risk management expert for software projects."
                },
                {"role": "user", "content": prompt}
            ]
            
            response = await self.llm_client.get_chat_completion_text(
                messages,
                model_type="medium",
                temperature=0.4
            )
            
            # Parse JSON
            try:
                start = response.find('[')
                end = response.rfind(']') + 1
                if start >= 0 and end > start:
                    json_str = response[start:end]
                    risks_data = json.loads(json_str)
                else:
                    risks_data = json.loads(response)
                
                risks = []
                for r in risks_data:
                    risk = Risk(
                        category=r.get("category", "technical"),
                        description=r.get("description", ""),
                        probability=float(r.get("probability", 0.5)),
                        impact=r.get("impact", "medium"),
                        mitigation=r.get("mitigation", "")
                    )
                    risks.append(risk)
                    
                return risks
                
            except (json.JSONDecodeError, ValueError):
                logger.warning("Failed to parse risks JSON")
                return [Risk(
                    category="technical",
                    description="Technical complexity risk",
                    probability=0.5,
                    impact="medium",
                    mitigation="Regular technical reviews and prototyping"
                )]
                
        except Exception as e:
            logger.error(f"Risk assessment failed: {str(e)}")
            return []
    
    async def create_project_plan(self, requirements: str) -> ProjectPlan:
        """Create complete project plan"""
        try:
            logger.info("Starting project plan creation")
            
            # Run tasks in parallel where possible
            features_task = self.extract_features(requirements)
            tech_stack_task = self.suggest_tech_stack(requirements, [])
            
            # Wait for features first
            features = await features_task
            
            # Then run dependent tasks
            sprints_task = self.create_sprints(features)
            risks_task = self.assess_risks(requirements, features)
            
            # Update tech stack with features
            tech_stack = await self.suggest_tech_stack(requirements, features)
            sprints = await sprints_task
            risks = await risks_task
            
            # Calculate estimates
            total_hours = sum(f.estimated_hours or 40 for f in features)
            timeline_months = round((total_hours / 160) * 1.3, 1)  # 160 hours/month with 30% buffer
            
            # Cost estimate (simplified)
            hourly_rate = 100  # $100/hour average
            cost_min = total_hours * hourly_rate * 0.8
            cost_max = total_hours * hourly_rate * 1.2
            
            # Create architecture (simplified)
            architecture = {
                "high_level_design": "Microservices architecture with separate frontend and backend",
                "components": [
                    {"name": "Frontend App", "type": "UI", "tech": tech_stack.frontend},
                    {"name": "Backend API", "type": "API", "tech": tech_stack.backend},
                    {"name": "Database", "type": "Data Store", "tech": tech_stack.database}
                ],
                "data_flow": "Client -> API -> Database",
                "scaling_strategy": "Horizontal scaling with load balancers",
                "tech_stack": tech_stack
            }
            
            # Create final plan
            plan = ProjectPlan(
                features=features,
                tech_stack=tech_stack,
                sprints=sprints,
                architecture=architecture,
                risks=risks,
                estimated_timeline_months=timeline_months,
                estimated_cost_range=f"${cost_min:,.0f} - ${cost_max:,.0f}"
            )
            
            # Store in vector DB for future reference
            await self.store_plan(requirements, plan)
            
            logger.info(f"Project plan created successfully: {len(features)} features")
            return plan
            
        except Exception as e:
            logger.error(f"Project plan creation failed: {str(e)}")
            raise AppException(f"Failed to create project plan: {str(e)}")
    
    async def store_plan(self, requirements: str, plan: ProjectPlan):
        """Store plan in vector database"""
        try:
            # Create embedding for requirements
            embedding = await self.llm_client.create_embedding(requirements)
            
            # Store in vector DB
            await self.vector_store.add_document(
                collection_name="project_plans",
                document=json.dumps({
                    "requirements": requirements,
                    "features": [f.dict() for f in plan.features],
                    "tech_stack": plan.tech_stack.dict()
                }),
                embedding=embedding,
                metadata={
                    "type": "project_plan",
                    "feature_count": len(plan.features),
                    "timeline": plan.estimated_timeline_months
                }
            )
            
        except Exception as e:
            logger.warning(f"Failed to store plan in vector DB: {str(e)}")