from app.agents.planner_agent import PlannerAgent
from app.agents.architect_agent import ArchitectAgent
from app.agents.risk_agent import RiskAgent
from app.agents.sprint_agent import SprintAgent
from app.agents.devops_agent import DevOpsAgent
from app.agents.code_review_agent import CodeReviewAgent
from app.memory.vector_store import VectorStore
from app.utils.logger import get_logger
from app.utils.exceptions import AppException
from typing import Dict, Any, List
import asyncio
import json 
import time
import traceback

logger = get_logger(__name__)

class Orchestrator:
    def __init__(self):
        """Initialize all agents"""
        # Initialize all agents
        self.planner = PlannerAgent()
        self.architect = ArchitectAgent()
        self.risk = RiskAgent()
        self.sprint = SprintAgent()
        self.devops = DevOpsAgent()
        self.code_review = CodeReviewAgent()
        self.vector_store = VectorStore()
        
        logger.info(f"Orchestrator initialized with {len(self.get_active_agents())} agents")
    
    def get_active_agents(self) -> List[str]:
        """Get list of active agents"""
        return [
            "planner", "architect", "risk", 
            "sprint", "devops", "code_review"
        ]

    async def process_project_request(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Main orchestrator function - ALL AGENTS ko parallel call karta hai"""
        start_time = time.time()
        project_name = project_data.get("name", "Untitled Project")
        requirements = project_data.get("requirements", "")
        
        logger.info(f"🚀 Orchestrator started for project: {project_name}")
        logger.info(f"📋 Agents to execute: {', '.join(self.get_active_agents())}")
        
        try:
            # === PARALLEL AGENT EXECUTION ===
            logger.info("⏳ Executing all agents in parallel...")
            
            # Planner execute karo
            planner_result = await self.planner.create_project_plan(requirements)
            
            # 🔥 FIX: Convert ProjectPlan object to dictionary
            planner_dict = self._project_plan_to_dict(planner_result)
            
            # Extract features and tech stack
            features = planner_dict.get("features", [])
            tech_stack = planner_dict.get("tech_stack", {})
            
            # Ab baaki agents ko call karo planner ke results ke saath
            logger.info("📋 Running remaining agents with planner results...")
            
            # Create tasks for remaining agents
            architect_task = self.architect.design_system_architecture(
                requirements, 
                [f.get("name", "") for f in features]
            )
            
            risk_task = self.risk.assess_project_risks(
                requirements,
                [f.get("name", "") for f in features],
                tech_stack,
                project_data.get("timeline", "Not specified"),
                project_data.get("budget_range")
            )
            
            sprint_task = self.sprint.create_sprint_plan(
                features,
                5, 14, None
            )
            
            devops_task = self.devops.create_devops_plan(
                tech_stack,
                project_data.get("project_type", "web_app")
            )
            
            # Execute remaining agents in parallel
            remaining_results = await asyncio.gather(
                architect_task,
                risk_task,
                sprint_task,
                devops_task,
                return_exceptions=True
            )
            
            # Extract results
            architect_result, risk_result, sprint_result, devops_result = remaining_results
            
            # Handle any errors
            agent_results = {
                "planner": planner_dict,
                "architect": self._handle_agent_result(architect_result, "architect"),
                "risk": self._handle_agent_result(risk_result, "risk"),
                "sprint": self._handle_agent_result(sprint_result, "sprint"),
                "devops": self._handle_agent_result(devops_result, "devops"),
            }
            
            # Combine results
            final_response = self._combine_agent_results(
                project_name,
                requirements,
                agent_results
            )
            
            processing_time = time.time() - start_time
            logger.info(f"All agents completed in {processing_time:.2f} seconds")
            
            return final_response
            
        except Exception as e:
            logger.error(f"Orchestrator error: {str(e)}")
            import traceback
            traceback.print_exc()
            raise AppException(f"Orchestrator failed: {str(e)}")
    
    def _project_plan_to_dict(self, plan) -> Dict[str, Any]:
        """Convert ProjectPlan object to dictionary"""
        try:
            if hasattr(plan, 'dict'):
                return plan.dict()
            elif isinstance(plan, dict):
                return plan
            else:
                # Manual conversion
                return {
                    "features": [
                        {
                            "name": f.name,
                            "description": f.description,
                            "priority": f.priority,
                            "estimated_hours": f.estimated_hours
                        } for f in getattr(plan, 'features', [])
                    ],
                    "tech_stack": {
                        "frontend": getattr(getattr(plan, 'tech_stack', {}), 'frontend', []),
                        "backend": getattr(getattr(plan, 'tech_stack', {}), 'backend', []),
                        "database": getattr(getattr(plan, 'tech_stack', {}), 'database', []),
                        "devops": getattr(getattr(plan, 'tech_stack', {}), 'devops', []),
                        "third_party": getattr(getattr(plan, 'tech_stack', {}), 'third_party', [])
                    },
                    "sprints": [
                        {
                            "number": s.number,
                            "name": s.name,
                            "duration_weeks": s.duration_weeks,
                            "features": s.features,
                            "deliverables": s.deliverables
                        } for s in getattr(plan, 'sprints', [])
                    ],
                    "architecture": getattr(plan, 'architecture', {}),
                    "risks": [
                        {
                            "category": r.category,
                            "description": r.description,
                            "probability": r.probability,
                            "impact": r.impact,
                            "mitigation": r.mitigation
                        } for r in getattr(plan, 'risks', [])
                    ],
                    "estimated_timeline_months": getattr(plan, 'estimated_timeline_months', 0),
                    "estimated_cost_range": getattr(plan, 'estimated_cost_range', 'Not estimated')
                }
        except Exception as e:
            logger.error(f"Error converting project plan: {str(e)}")
            return {
                "features": [],
                "tech_stack": {},
                "sprints": [],
                "architecture": {},
                "risks": [],
                "estimated_timeline_months": 0,
                "estimated_cost_range": "Error in conversion"
            }
    
    def _handle_agent_result(self, result: Any, agent_name: str) -> Dict:
        """Handle individual agent results (including errors)"""
        if isinstance(result, Exception):
            logger.error(f"{agent_name} agent failed: {str(result)}")
            return {
                "status": "error",
                "error": str(result),
                "data": {}
            }
        
        # Convert to dict if needed
        if hasattr(result, 'dict'):
            data = result.dict()
        elif isinstance(result, dict):
            data = result
        else:
            data = {"result": str(result)}
        
        return {
            "status": "success",
            "data": data
        }
    
    def _handle_agent_result(self, result: Any, agent_name: str) -> Dict:
        """Handle individual agent results (including errors)"""
        if isinstance(result, Exception):
            logger.error(f"{agent_name} agent failed: {str(result)}")
            return {
                "status": "error",
                "error": str(result),
                "data": {}
            }
        return {
            "status": "success",
            "data": result if isinstance(result, dict) else {"result": str(result)}
        }
    
    def _is_success(self, result: Any) -> str:
        """Check if agent succeeded"""
        if isinstance(result, dict) and result.get("status") == "error":
            return "Failed"
        return "Success"
    
    def _combine_agent_results(
        self,
        project_name: str,
        requirements: str,
        agent_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Combine all agents' results into single response"""
        
        # Planner results
        planner_data = agent_results["planner"] if isinstance(agent_results["planner"], dict) else {}
        
        # Architect results
        architect_data = agent_results["architect"].get("data", {}) if agent_results["architect"].get("status") == "success" else {}
        
        # Risk results
        risk_data = agent_results["risk"].get("data", {}) if agent_results["risk"].get("status") == "success" else {}
        
        # Sprint results
        sprint_data = agent_results["sprint"].get("data", {}) if agent_results["sprint"].get("status") == "success" else {}
        
        # DevOps results
        devops_data = agent_results["devops"].get("data", {}) if agent_results["devops"].get("status") == "success" else {}
        
        # Combined response
        return {
            "project_name": project_name,
            "requirements_summary": requirements[:200] + "..." if len(requirements) > 200 else requirements,
            "timestamp": time.time(),
            
            # Section 1: Project Planning (Planner Agent)
            "project_planning": {
                "features": planner_data.get("features", []),
                "tech_stack": planner_data.get("tech_stack", {}),
                "estimated_timeline_months": planner_data.get("estimated_timeline_months", 0),
                "estimated_cost_range": planner_data.get("estimated_cost_range", "Not estimated")
            },
            
            # Section 2: System Architecture (Architect Agent)
            "system_architecture": {
                "high_level_design": architect_data.get("high_level_design", {}),
                "database_schema": architect_data.get("database_schema", {}),
                "api_design": architect_data.get("api_design", {}),
                "components": architect_data.get("components", []),
                "scaling_plan": architect_data.get("scaling_plan", {})
            },
            
            # Section 3: Risk Assessment (Risk Agent)
            "risk_assessment": {
                "overall_risk_score": risk_data.get("overall_risk_score", 0),
                "risk_level": risk_data.get("risk_level", "Unknown"),
                "risks": risk_data.get("risks", []),
                "critical_risks": risk_data.get("critical_risks", []),
                "mitigation_strategies": risk_data.get("mitigation_strategies", [])
            },
            
            # Section 4: Sprint Planning (Sprint Agent)
            "sprint_planning": {
                "total_sprints": sprint_data.get("total_sprints", 0),
                "sprints": sprint_data.get("sprints", []),
                "team_capacity": sprint_data.get("team_capacity", 0),
                "estimated_velocity": sprint_data.get("estimated_velocity", 0),
                "timeline": sprint_data.get("timeline", {})
            },
            
            # Section 5: DevOps & Infrastructure (DevOps Agent)
            "devops_plan": {
                "ci_cd_pipeline": devops_data.get("ci_cd_pipeline", []),
                "infrastructure": devops_data.get("infrastructure", {}),
                "deployment_strategy": str(devops_data.get("deployment_strategy", "rolling")),
                "monitoring_tools": devops_data.get("monitoring_tools", []),
                "backup_strategy": devops_data.get("backup_strategy", "Not specified"),
                "disaster_recovery": devops_data.get("disaster_recovery", "Not specified")
            },
            
            # Agent Status Summary
            "agent_status": {
                agent: results.get("status", "unknown")
                for agent, results in agent_results.items()
            }
        }
    
    async def _store_result(self, project_name: str, requirements: str, result: Dict):
        """Store result in vector database"""
        try:
            embedding = await self.planner.llm_client.create_embedding(requirements)
            await self.vector_store.add_document(
                "projects",
                json.dumps(result),
                embedding,
                {"project_name": project_name, "timestamp": time.time()}
            )
        except Exception as e:
            logger.warning(f"Failed to store in vector DB: {str(e)}")