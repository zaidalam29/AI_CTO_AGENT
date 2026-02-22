from app.llm.openai_client import OpenAIClient
from app.ml.risk_model import RiskPredictionModel
from app.utils.logger import get_logger
from app.utils.exceptions import RiskException
from app.schemas.agent_schema import RiskAssessment, RiskCategory
from typing import List, Dict, Any, Optional
import json
import time
import asyncio 
import numpy as np

logger = get_logger(__name__)


class RiskAgent:
    def __init__(self):
        self.llm_client = OpenAIClient()
        self.ml_model = RiskPredictionModel()  # ML model for risk prediction
        self.agent_type = "risk"
    
    async def assess_project_risks(
        self,
        requirements: str,
        features: List[str],
        tech_stack: Dict[str, List[str]],
        timeline: str,
        budget: str = None
    ) -> Dict[str, Any]:
        """Complete risk assessment for project"""
        start_time = time.time()
        
        try:
            logger.info("Risk agent: Starting risk assessment")
            
            # Parallel risk assessments
            ml_risks_task = self._predict_ml_risks(requirements, features)
            technical_risks_task = self._assess_technical_risks(tech_stack)
            timeline_risks_task = self._assess_timeline_risks(timeline, features)
            business_risks_task = self._assess_business_risks(requirements, budget)
            security_risks_task = self._assess_security_risks(tech_stack)
            
            # Wait for all assessments
            ml_risks, tech_risks, timeline_risks, business_risks, security_risks = await asyncio.gather(
                ml_risks_task,
                technical_risks_task,
                timeline_risks_task,
                business_risks_task,
                security_risks_task,
                return_exceptions=True
            )
            
            # Compile all risks
            all_risks = []
            
            # Add ML predicted risks
            if not isinstance(ml_risks, Exception):
                all_risks.extend(ml_risks)
            
            # Add technical risks
            if not isinstance(tech_risks, Exception):
                all_risks.extend(tech_risks)
            
            # Add timeline risks
            if not isinstance(timeline_risks, Exception):
                all_risks.extend(timeline_risks)
            
            # Add business risks
            if not isinstance(business_risks, Exception):
                all_risks.extend(business_risks)
            
            # Add security risks
            if not isinstance(security_risks, Exception):
                all_risks.extend(security_risks)
            
            # Calculate overall risk score
            overall_risk_score = self._calculate_risk_score(all_risks)
            
            # Generate mitigation strategies
            mitigations = await self._generate_mitigation_strategies(all_risks)
            
            # Create risk report
            risk_report = {
                "overall_risk_score": overall_risk_score,
                "risk_level": self._get_risk_level(overall_risk_score),
                "risks": [risk.dict() for risk in all_risks],
                "mitigation_strategies": mitigations,
                "critical_risks": [r.dict() for r in all_risks if r.impact == "critical"],
                "high_risks": [r.dict() for r in all_risks if r.impact == "high"],
                "medium_risks": [r.dict() for r in all_risks if r.impact == "medium"],
                "low_risks": [r.dict() for r in all_risks if r.impact == "low"],
                "risk_trends": await self._analyze_risk_trends(requirements)
            }
            
            processing_time = time.time() - start_time
            logger.info(f"Risk assessment completed in {processing_time:.2f}s")
            
            return risk_report
            
        except Exception as e:
            logger.error(f"Risk assessment failed: {str(e)}")
            raise RiskException(f"Risk assessment failed: {str(e)}")
    
    async def _predict_ml_risks(self, requirements: str, features: List[str]) -> List[RiskAssessment]:
        """Use ML model to predict risks"""
        try:
            # Extract features for ML model
            text_features = requirements + " " + " ".join(features)
            
            # Get ML predictions
            predictions = self.ml_model.predict_risks(text_features)
            
            risks = []
            for pred in predictions:
                risk = RiskAssessment(
                    category=RiskCategory(pred.get("category", "technical")),
                    description=pred.get("description", "ML predicted risk"),
                    probability=float(pred.get("probability", 0.5)),
                    impact=pred.get("impact", "medium"),
                    mitigation=pred.get("mitigation", "Monitor and adjust"),
                    owner="Project Manager"
                )
                risks.append(risk)
            
            return risks
            
        except Exception as e:
            logger.error(f"ML risk prediction failed: {str(e)}")
            return []
    
    async def _assess_technical_risks(self, tech_stack: Dict[str, List[str]]) -> List[RiskAssessment]:
        """Assess technical risks based on tech stack"""
        risks = []
        
        try:
            prompt = f"""
            Analyze this technology stack and identify technical risks:
            
            Tech Stack: {json.dumps(tech_stack, indent=2)}
            
            For each risk, provide:
            - category: Always "technical"
            - description: What could go wrong
            - probability: 0.0 to 1.0
            - impact: low/medium/high/critical
            - mitigation: How to prevent
            
            Return as JSON array.
            """
            
            messages = [
                {"role": "system", "content": "You are a technical risk expert."},
                {"role": "user", "content": prompt}
            ]
            
            response = await self.llm_client.get_chat_completion_text(
                messages,
                model_type="medium",
                temperature=0.3
            )
            
            # Parse response
            try:
                start = response.find('[')
                end = response.rfind(']') + 1
                if start >= 0 and end > start:
                    risks_data = json.loads(response[start:end])
                    
                    for r in risks_data:
                        risk = RiskAssessment(
                            category=RiskCategory.TECHNICAL,
                            description=r.get("description", "Technical risk"),
                            probability=float(r.get("probability", 0.5)),
                            impact=r.get("impact", "medium"),
                            mitigation=r.get("mitigation", "Technical review"),
                            owner="Tech Lead"
                        )
                        risks.append(risk)
            except:
                # Add default risks
                risks.append(RiskAssessment(
                    category=RiskCategory.TECHNICAL,
                    description="Technology learning curve",
                    probability=0.6,
                    impact="medium",
                    mitigation="Allocate time for learning, conduct POCs",
                    owner="Tech Lead"
                ))
                
        except Exception as e:
            logger.error(f"Technical risk assessment failed: {str(e)}")
        
        return risks
    
    async def _assess_timeline_risks(self, timeline: str, features: List[str]) -> List[RiskAssessment]:
        """Assess timeline risks"""
        risks = []
        
        # Basic timeline risk
        risks.append(RiskAssessment(
            category=RiskCategory.TIMELINE,
            description="Project timeline may be underestimated",
            probability=0.7,
            impact="high",
            mitigation="Add buffer time, use agile methodology",
            owner="Project Manager"
        ))
        
        # Feature complexity risk
        if len(features) > 10:
            risks.append(RiskAssessment(
                category=RiskCategory.TIMELINE,
                description=f"Large number of features ({len(features)}) may cause timeline overrun",
                probability=0.8,
                impact="high",
                mitigation="Prioritize features, consider MVP approach",
                owner="Product Manager"
            ))
        
        return risks
    
    async def _assess_business_risks(self, requirements: str, budget: str = None) -> List[RiskAssessment]:
        """Assess business risks"""
        risks = []
        
        try:
            prompt = f"""
            Identify business risks for this project:
            
            Requirements: {requirements[:500]}
            Budget: {budget if budget else 'Not specified'}
            
            Consider:
            - Market risks
            - Competition
            - Budget constraints
            - ROI concerns
            
            Return as JSON array with risk objects.
            """
            
            messages = [
                {"role": "system", "content": "You are a business risk analyst."},
                {"role": "user", "content": prompt}
            ]
            
            response = await self.llm_client.get_chat_completion_text(
                messages,
                model_type="medium",
                temperature=0.3
            )
            
            # Parse response
            try:
                start = response.find('[')
                end = response.rfind(']') + 1
                if start >= 0 and end > start:
                    risks_data = json.loads(response[start:end])
                    
                    for r in risks_data:
                        risk = RiskAssessment(
                            category=RiskCategory.BUSINESS,
                            description=r.get("description", "Business risk"),
                            probability=float(r.get("probability", 0.5)),
                            impact=r.get("impact", "medium"),
                            mitigation=r.get("mitigation", "Business review"),
                            owner="Product Owner"
                        )
                        risks.append(risk)
            except:
                # Default business risk
                risks.append(RiskAssessment(
                    category=RiskCategory.BUSINESS,
                    description="Market acceptance risk",
                    probability=0.5,
                    impact="high",
                    mitigation="Conduct market research, MVP testing",
                    owner="Product Manager"
                ))
                
        except Exception as e:
            logger.error(f"Business risk assessment failed: {str(e)}")
        
        return risks
    
    async def _assess_security_risks(self, tech_stack: Dict[str, List[str]]) -> List[RiskAssessment]:
        """Assess security risks"""
        risks = []
        
        # Common security risks
        risks.append(RiskAssessment(
            category=RiskCategory.SECURITY,
            description="Authentication and authorization vulnerabilities",
            probability=0.6,
            impact="critical",
            mitigation="Implement strong auth, regular security audits",
            owner="Security Lead"
        ))
        
        risks.append(RiskAssessment(
            category=RiskCategory.SECURITY,
            description="Data breach risk",
            probability=0.4,
            impact="critical",
            mitigation="Encrypt sensitive data, follow security best practices",
            owner="Security Lead"
        ))
        
        # Tech-specific risks
        if "React" in tech_stack.get("frontend", []):
            risks.append(RiskAssessment(
                category=RiskCategory.SECURITY,
                description="XSS vulnerabilities in frontend",
                probability=0.5,
                impact="high",
                mitigation="Use proper escaping, Content Security Policy",
                owner="Frontend Lead"
            ))
        
        return risks
    
    async def _generate_mitigation_strategies(self, risks: List[RiskAssessment]) -> List[Dict]:
        """Generate mitigation strategies for risks"""
        strategies = []
        
        for risk in risks:
            strategy = {
                "risk_description": risk.description,
                "mitigation": risk.mitigation,
                "owner": risk.owner,
                "priority": "high" if risk.impact in ["high", "critical"] else "medium",
                "timeline": "Immediate" if risk.probability > 0.7 else "Plan for next sprint"
            }
            strategies.append(strategy)
        
        return strategies
    
    def _calculate_risk_score(self, risks: List[RiskAssessment]) -> float:
        """Calculate overall risk score (0-100)"""
        if not risks:
            return 0.0
        
        weights = {
            "critical": 1.0,
            "high": 0.7,
            "medium": 0.4,
            "low": 0.1
        }
        
        total_score = 0
        for risk in risks:
            impact_weight = weights.get(risk.impact, 0.5)
            total_score += risk.probability * impact_weight * 100
        
        return min(100, total_score / len(risks))
    
    def _get_risk_level(self, score: float) -> str:
        """Get risk level based on score"""
        if score >= 70:
            return "Critical"
        elif score >= 50:
            return "High"
        elif score >= 30:
            return "Medium"
        else:
            return "Low"
    
    async def _analyze_risk_trends(self, requirements: str) -> List[Dict]:
        """Analyze risk trends over time"""
        # This would typically use historical data
        # For now, return simulated trends
        return [
            {"phase": "Development", "risk_level": "High"},
            {"phase": "Testing", "risk_level": "Medium"},
            {"phase": "Deployment", "risk_level": "Low"},
            {"phase": "Maintenance", "risk_level": "Medium"}
        ]