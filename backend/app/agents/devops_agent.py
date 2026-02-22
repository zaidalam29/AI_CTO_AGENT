from app.llm.openai_client import OpenAIClient
from app.utils.logger import get_logger
from app.utils.exceptions import DevOpsException
from app.schemas.agent_schema import DevOpsPlan, InfrastructureRequirement, DeploymentStrategy
from typing import Dict, Any, List, Optional
import json
import time
import asyncio

logger = get_logger(__name__)

class DevOpsAgent:
    def __init__(self):
        self.llm_client = OpenAIClient()
        self.agent_type = "devops"
    
    async def create_devops_plan(
        self,
        tech_stack: Dict[str, List[str]],
        project_type: str,
        expected_load: str = "medium",
        compliance_reqs: List[str] = None
    ) -> DevOpsPlan:
        """Create complete DevOps plan"""
        start_time = time.time()
        
        try:
            logger.info("DevOps agent: Creating infrastructure plan")
            
            if compliance_reqs is None:
                compliance_reqs = []
            
            # Parallel planning
            ci_cd_task = self._design_ci_cd_pipeline(tech_stack)
            infra_task = self._design_infrastructure(tech_stack, expected_load)
            monitoring_task = self._setup_monitoring(tech_stack)
            backup_task = self._design_backup_strategy(project_type)
            dr_task = self._design_disaster_recovery(project_type)
            
            # Wait for all tasks
            ci_cd, infra, monitoring, backup, dr = await asyncio.gather(
                ci_cd_task,
                infra_task,
                monitoring_task,
                backup_task,
                dr_task,
                return_exceptions=True
            )
            
            # Handle errors
            if isinstance(ci_cd, Exception):
                logger.error(f"CI/CD design failed: {str(ci_cd)}")
                ci_cd = self._default_ci_cd_pipeline()  # 👈 Use default strings
            
            if isinstance(infra, Exception):
                logger.error(f"Infrastructure design failed: {str(infra)}")
                infra = self._default_infrastructure()
            
            # Determine deployment strategy
            deployment_strategy = await self._choose_deployment_strategy(
                project_type, expected_load
            )
            
            # 🔥 FIX: Ensure ci_cd is list of strings, not dicts
            ci_cd_strings = []
            if isinstance(ci_cd, list):
                for item in ci_cd:
                    if isinstance(item, dict):
                        # Extract string from dict
                        ci_cd_strings.append(item.get('step', str(item)))
                    else:
                        ci_cd_strings.append(str(item))
            else:
                ci_cd_strings = self._default_ci_cd_pipeline()
            
            # Handle monitoring
            monitoring_tools = []
            if not isinstance(monitoring, Exception):
                if isinstance(monitoring, list):
                    monitoring_tools = [str(m) for m in monitoring]
                else:
                    monitoring_tools = [str(monitoring)]
            else:
                monitoring_tools = ["Prometheus", "Grafana", "ELK Stack"]
            
            # Create plan with proper types
            plan = DevOpsPlan(
                ci_cd_pipeline=ci_cd_strings,  # 👈 Now list of strings
                infrastructure=infra if not isinstance(infra, Exception) else self._default_infrastructure(),
                deployment_strategy=deployment_strategy,
                monitoring_tools=monitoring_tools,
                backup_strategy=str(backup) if not isinstance(backup, Exception) else "Daily backups with 30-day retention",
                disaster_recovery=str(dr) if not isinstance(dr, Exception) else "Multi-region failover with RTO=4h, RPO=15m"
            )
            
            processing_time = time.time() - start_time
            logger.info(f"DevOps plan created in {processing_time:.2f}s")
            
            return plan
            
        except Exception as e:
            logger.error(f"DevOps planning failed: {str(e)}")
            # Return default plan on error
            return self._default_devops_plan()
    
    def _default_ci_cd_pipeline(self) -> List[str]:
        """Default CI/CD pipeline as list of strings"""
        return [
            "Git for version control",
            "GitHub Actions for CI/CD automation",
            "Code linting and formatting checks",
            "Unit tests execution",
            "Integration tests execution",
            "Security scanning (SAST)",
            "Build and package application",
            "Push to container registry",
            "Deploy to staging environment",
            "Smoke tests on staging",
            "Deploy to production (blue-green)",
            "Post-deployment monitoring"
        ]
    
    def _default_devops_plan(self) -> DevOpsPlan:
        """Default DevOps plan when everything fails"""
        return DevOpsPlan(
            ci_cd_pipeline=self._default_ci_cd_pipeline(),
            infrastructure=self._default_infrastructure(),
            deployment_strategy=DeploymentStrategy.ROLLING,
            monitoring_tools=["Prometheus", "Grafana", "ELK Stack", "Sentry"],
            backup_strategy="Daily full backups with 30-day retention. Hourly incremental backups.",
            disaster_recovery="Multi-region deployment with automated failover. RTO: 4 hours, RPO: 15 minutes."
        )
    
    async def _design_ci_cd_pipeline(self, tech_stack: Dict[str, List[str]]) -> List[str]:
        """Design CI/CD pipeline - returns list of strings"""
        prompt = f"""
        Design a CI/CD pipeline for this tech stack:
        
        {json.dumps(tech_stack, indent=2)}
        
        Return a list of pipeline steps as simple strings.
        Example format: ["Step 1 description", "Step 2 description", ...]
        
        Just return the JSON array, nothing else.
        """
        
        messages = [
            {"role": "system", "content": "You are a DevOps engineer. Always return JSON arrays of strings."},
            {"role": "user", "content": prompt}
        ]
        
        try:
            response = await self.llm_client.get_chat_completion_text(
                messages,
                model_type="medium",
                temperature=0.2
            )
            
            # Parse response
            try:
                # Find JSON array
                start = response.find('[')
                end = response.rfind(']') + 1
                if start >= 0 and end > start:
                    pipeline = json.loads(response[start:end])
                    # Ensure all items are strings
                    return [str(item) for item in pipeline]
            except:
                pass
        except Exception as e:
            logger.error(f"CI/CD design failed: {str(e)}")
        
        return self._default_ci_cd_pipeline()
    
    async def _setup_monitoring(self, tech_stack: Dict[str, List[str]]) -> List[str]:
        """Setup monitoring tools - returns list of strings"""
        monitoring_tools = []
        
        # Basic monitoring always included
        monitoring_tools.extend([
            "Prometheus for metrics collection",
            "Grafana for visualization",
            "ELK Stack for log aggregation"
        ])
        
        # Add tech-specific monitoring
        backend = tech_stack.get("backend", [])
        frontend = tech_stack.get("frontend", [])
        database = tech_stack.get("database", [])
        
        if any("Python" in b for b in backend):
            monitoring_tools.append("Sentry for Python error tracking")
        
        if any("React" in f for f in frontend):
            monitoring_tools.append("Google Analytics for user behavior")
        
        if any("PostgreSQL" in d for d in database):
            monitoring_tools.append("pg_stat_statements for query performance")
        
        if any("MongoDB" in d for d in database):
            monitoring_tools.append("MongoDB Atlas monitoring")
        
        # APM
        monitoring_tools.append("New Relic or DataDog for APM")
        
        # Alerting
        monitoring_tools.append("PagerDuty for alerting")
        
        return monitoring_tools
    
    async def _design_backup_strategy(self, project_type: str) -> str:
        """Design backup strategy - returns string"""
        prompt = f"""
        Design a backup strategy for a {project_type} project.
        
        Return a concise paragraph describing:
        1. Backup frequency
        2. Retention policy
        3. Backup types
        4. Storage location
        5. Recovery testing
        """
        
        messages = [
            {"role": "system", "content": "You are a DevOps engineer."},
            {"role": "user", "content": prompt}
        ]
        
        try:
            response = await self.llm_client.get_chat_completion_text(
                messages,
                model_type="fast",
                temperature=0.2
            )
            return response.strip()
        except:
            return "Daily full backups with 30-day retention. Hourly incremental backups. Multi-region encrypted storage. Monthly recovery testing."
    
    async def _design_disaster_recovery(self, project_type: str) -> str:
        """Design disaster recovery plan - returns string"""
        prompt = f"""
        Design a disaster recovery plan for a {project_type} project.
        
        Return a concise paragraph including:
        1. RTO (Recovery Time Objective)
        2. RPO (Recovery Point Objective)
        3. Failover strategy
        4. Data replication
        5. Testing procedure
        """
        
        messages = [
            {"role": "system", "content": "You are a disaster recovery expert."},
            {"role": "user", "content": prompt}
        ]
        
        try:
            response = await self.llm_client.get_chat_completion_text(
                messages,
                model_type="fast",
                temperature=0.2
            )
            return response.strip()
        except:
            return "RTO: 4 hours, RPO: 15 minutes. Active-Passive failover with automated DNS switch. Synchronous replication for critical data. Quarterly DR drills. Multi-region deployment."
    
    def _default_infrastructure(self) -> Dict[str, InfrastructureRequirement]:
        """Default infrastructure requirements"""
        return {
            "web_server": InfrastructureRequirement(
                resource_type="compute",
                min_value="2x 2 CPU, 4GB RAM",
                max_value="4x 4 CPU, 8GB RAM",
                recommended="2x t3.medium instances"
            ),
            "application_server": InfrastructureRequirement(
                resource_type="compute",
                min_value="2x 4 CPU, 8GB RAM",
                max_value="4x 8 CPU, 16GB RAM",
                recommended="2x t3.large instances"
            ),
            "database": InfrastructureRequirement(
                resource_type="database",
                min_value="db.t3.small",
                max_value="db.t3.large with read replicas",
                recommended="db.t3.medium with Multi-AZ"
            ),
            "cache": InfrastructureRequirement(
                resource_type="cache",
                min_value="cache.t3.micro",
                max_value="cache.t3.small cluster",
                recommended="cache.t3.micro"
            ),
            "storage": InfrastructureRequirement(
                resource_type="storage",
                min_value="100GB SSD",
                max_value="1TB SSD with auto-scaling",
                recommended="250GB SSD"
            ),
            "cdn": InfrastructureRequirement(
                resource_type="network",
                min_value="Standard CDN",
                max_value="Enterprise CDN with WAF",
                recommended="Standard CDN with SSL"
            )
        }
    
    async def _design_infrastructure(self, tech_stack: Dict[str, List[str]], expected_load: str) -> Dict[str, InfrastructureRequirement]:
        """Design infrastructure requirements"""
        # Determine scale based on expected load
        scale_factor = {
            "low": 1,
            "medium": 2,
            "high": 4,
            "very_high": 8
        }.get(expected_load, 2)
        
        return {
            "web_server": InfrastructureRequirement(
                resource_type="compute",
                min_value=f"{scale_factor}x 2 CPU, 4GB RAM",
                max_value=f"{scale_factor * 4}x 4 CPU, 8GB RAM",
                recommended=f"{scale_factor * 2}x t3.medium instances"
            ),
            "application_server": InfrastructureRequirement(
                resource_type="compute",
                min_value=f"{scale_factor}x 4 CPU, 8GB RAM",
                max_value=f"{scale_factor * 4}x 8 CPU, 16GB RAM",
                recommended=f"{scale_factor * 2}x t3.large instances"
            ),
            "database": InfrastructureRequirement(
                resource_type="database",
                min_value="db.t3.small",
                max_value="db.t3.large with read replicas",
                recommended="db.t3.medium with Multi-AZ"
            ),
            "cache": InfrastructureRequirement(
                resource_type="cache",
                min_value="cache.t3.micro",
                max_value="cache.t3.medium cluster",
                recommended="cache.t3.small"
            ),
            "storage": InfrastructureRequirement(
                resource_type="storage",
                min_value="100GB SSD",
                max_value="1TB SSD with auto-scaling",
                recommended="250GB SSD"
            ),
            "cdn": InfrastructureRequirement(
                resource_type="network",
                min_value="Standard CDN",
                max_value="Enterprise CDN with WAF",
                recommended="Standard CDN with SSL"
            )
        }
    
    async def _choose_deployment_strategy(self, project_type: str, expected_load: str) -> DeploymentStrategy:
        """Choose appropriate deployment strategy"""
        if expected_load in ["high", "very_high"]:
            return DeploymentStrategy.BLUE_GREEN
        elif expected_load == "medium":
            return DeploymentStrategy.CANARY
        else:
            return DeploymentStrategy.ROLLING