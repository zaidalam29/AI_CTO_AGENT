from app.llm.openai_client import OpenAIClient
from app.utils.logger import get_logger
from app.utils.exceptions import SprintException
from app.schemas.agent_schema import SprintPlan, UserStory
from typing import List, Dict, Any, Optional
import json
import time
import asyncio 
from datetime import datetime, timedelta
import re 

logger = get_logger(__name__)

class SprintAgent:
    def __init__(self):
        self.llm_client = OpenAIClient()
        self.agent_type = "sprint"
    

    async def create_sprint_plan(
        self,
        features: List[Dict],
        team_size: int = 5,
        sprint_duration_days: int = 14,
        start_date: datetime = None
    ) -> Dict[str, Any]:
        """Create detailed sprint plan - OPTIMIZED"""
        start_time = time.time()
        
        try:
            logger.info("Sprint agent: Creating sprint plan")
            
            if start_date is None:
                start_date = datetime.now()
            
            # Calculate team capacity
            team_capacity = team_size * sprint_duration_days * 4  # 4 hours per day average
            
            # Simple sprint planning without LLM calls
            sprints = []
            features_per_sprint = max(2, len(features) // 4)
            
            for i in range(0, len(features), features_per_sprint):
                sprint_features = features[i:i + features_per_sprint]
                sprint_num = i // features_per_sprint + 1
                
                # Create user stories without LLM
                user_stories = []
                for j, feat in enumerate(sprint_features):
                    story = {
                        "id": f"US-{sprint_num}-{j+1}",
                        "title": f"Implement {feat.get('name', 'feature')}",
                        "description": feat.get('description', ''),
                        "points": feat.get('estimated_hours', 40) // 8,  # Convert hours to story points
                        "dependencies": []
                    }
                    user_stories.append(story)
                
                sprint = {
                    "sprint_number": sprint_num,
                    "duration_days": sprint_duration_days,
                    "start_date": (start_date + timedelta(days=(sprint_num-1)*sprint_duration_days)).isoformat(),
                    "end_date": (start_date + timedelta(days=sprint_num*sprint_duration_days)).isoformat(),
                    "user_stories": user_stories,
                    "goals": [f"Complete {len(user_stories)} user stories for sprint {sprint_num}"],
                    "risks": ["Dependencies between stories", "Technical complexity"],
                    "capacity": sum(s.get('points', 5) for s in user_stories)
                }
                sprints.append(sprint)
                
                if len(sprints) >= 4:
                    break
            
            # Calculate velocity
            total_points = sum(s.get('capacity', 0) for s in sprints)
            velocity = total_points / max(1, len(sprints))
            
            sprint_plan = {
                "total_sprints": len(sprints),
                "sprints": sprints,
                "team_capacity": team_capacity,
                "estimated_velocity": velocity,
                "timeline": {
                    "start_date": start_date.isoformat(),
                    "end_date": (start_date + timedelta(days=len(sprints)*sprint_duration_days)).isoformat(),
                    "total_days": len(sprints) * sprint_duration_days
                },
                "recommendations": [
                    "Hold daily stand-up meetings",
                    "Conduct sprint planning before each sprint",
                    "Review and retro after each sprint",
                    f"Team velocity estimated at {velocity:.1f} points per sprint"
                ]
            }
            
            processing_time = time.time() - start_time
            logger.info(f"Sprint plan created in {processing_time:.2f}s")
            
            return sprint_plan
            
        except Exception as e:
            logger.error(f"Sprint planning failed: {str(e)}")
            return {
                "total_sprints": 1,
                "sprints": [{
                    "sprint_number": 1,
                    "duration_days": 14,
                    "start_date": datetime.now().isoformat(),
                    "end_date": (datetime.now() + timedelta(days=14)).isoformat(),
                    "user_stories": [{
                        "id": "US-1-1",
                        "title": "Implement core features",
                        "description": "Implement all features in first sprint",
                        "points": 40,
                        "dependencies": []
                    }],
                    "goals": ["Complete MVP features"],
                    "risks": ["Timeline risk"],
                    "capacity": 40
                }],
                "team_capacity": 280,
                "estimated_velocity": 40,
                "timeline": {
                    "start_date": datetime.now().isoformat(),
                    "end_date": (datetime.now() + timedelta(days=14)).isoformat(),
                    "total_days": 14
                },
                "recommendations": ["Start with MVP, iterate based on feedback"]
            }
    
    async def _create_user_stories(self, features: List[Dict]) -> List[UserStory]:
        """Break down features into user stories"""
        user_stories = []
        
        for i, feature in enumerate(features):
            prompt = f"""
            Break down this feature into user stories:
            
            Feature: {feature.get('name', 'Unnamed')}
            Description: {feature.get('description', '')}
            
            Create 3-5 user stories in the format:
            "As a [user], I want to [action] so that [benefit]"
            
            Return as JSON array.
            """
            
            messages = [
                {"role": "system", "content": "You are an agile coach expert at creating user stories."},
                {"role": "user", "content": prompt}
            ]
            
            try:
                response = await self.llm_client.get_chat_completion_text(
                    messages,
                    model_type="medium",
                    temperature=0.3
                )
                
                # Parse stories
                stories_data = self._parse_json_response(response, [])
                
                for j, story_data in enumerate(stories_data[:5]):  # Max 5 per feature
                    story = UserStory(
                        id=f"US-{i+1}-{j+1}",
                        title=story_data.get("title", f"Story for {feature.get('name', 'feature')}"),
                        description=story_data.get("description", story_data.get("story", "")),
                        points=0,  # Will estimate later
                        dependencies=[]
                    )
                    user_stories.append(story)
                    
            except Exception as e:
                logger.error(f"Failed to create user stories for feature {i}: {str(e)}")
                # Add default story
                story = UserStory(
                    id=f"US-{i+1}-1",
                    title=f"Implement {feature.get('name', 'feature')}",
                    description=feature.get('description', ''),
                    points=5,
                    dependencies=[]
                )
                user_stories.append(story)
        
        return user_stories
    
    async def _estimate_story_points(self, user_stories: List[UserStory]) -> List[UserStory]:
        """Estimate story points for each user story"""
        for story in user_stories:
            prompt = f"""
            Estimate story points for this user story (using Fibonacci: 1,2,3,5,8,13,21):
            
            Story: {story.title}
            Description: {story.description}
            
            Consider complexity, effort, and uncertainty.
            Return only the number.
            """
            
            messages = [
                {"role": "system", "content": "You are an agile estimator."},
                {"role": "user", "content": prompt}
            ]
            
            try:
                response = await self.llm_client.get_chat_completion_text(
                    messages,
                    model_type="fast",
                    temperature=0.1
                )
                
                # Extract number from response
                import re
                numbers = re.findall(r'\d+', response)
                if numbers:
                    points = int(numbers[0])
                    # Map to Fibonacci-like numbers
                    if points <= 1:
                        story.points = 1
                    elif points <= 3:
                        story.points = 3
                    elif points <= 5:
                        story.points = 5
                    elif points <= 8:
                        story.points = 8
                    elif points <= 13:
                        story.points = 13
                    else:
                        story.points = 21
                else:
                    story.points = 5  # Default
                    
            except Exception as e:
                logger.error(f"Failed to estimate story: {story.id}")
                story.points = 5
        
        return user_stories
    
    async def _plan_sprints(
        self,
        user_stories: List[UserStory],
        team_capacity: int,
        sprint_duration: int,
        start_date: datetime
    ) -> List[SprintPlan]:
        """Plan stories into sprints"""
        sprints = []
        
        # Sort stories by complexity (simplified)
        sorted_stories = sorted(user_stories, key=lambda x: x.points, reverse=True)
        
        current_sprint_stories = []
        current_sprint_points = 0
        sprint_number = 1
        current_start = start_date
        
        for story in sorted_stories:
            if current_sprint_points + story.points <= team_capacity:
                current_sprint_stories.append(story)
                current_sprint_points += story.points
            else:
                # Create sprint
                if current_sprint_stories:
                    sprint = SprintPlan(
                        sprint_number=sprint_number,
                        duration_days=sprint_duration,
                        start_date=current_start,
                        end_date=current_start + timedelta(days=sprint_duration),
                        user_stories=current_sprint_stories,
                        goals=[f"Complete {len(current_sprint_stories)} user stories"],
                        risks=["Dependencies between stories"],
                        capacity=current_sprint_points
                    )
                    sprints.append(sprint)
                    
                    # Reset for next sprint
                    sprint_number += 1
                    current_start = current_start + timedelta(days=sprint_duration)
                    current_sprint_stories = [story]
                    current_sprint_points = story.points
        
        # Add last sprint
        if current_sprint_stories:
            sprint = SprintPlan(
                sprint_number=sprint_number,
                duration_days=sprint_duration,
                start_date=current_start,
                end_date=current_start + timedelta(days=sprint_duration),
                user_stories=current_sprint_stories,
                goals=[f"Complete {len(current_sprint_stories)} user stories"],
                risks=["Last sprint risks"],
                capacity=current_sprint_points
            )
            sprints.append(sprint)
        
        return sprints
    
    async def _calculate_velocity(self, sprints: List[SprintPlan]) -> float:
        """Calculate team velocity"""
        if not sprints:
            return 0.0
        
        total_points = sum(s.capacity for s in sprints)
        return total_points / len(sprints)
    
    async def _create_timeline(self, sprints: List[SprintPlan], start_date: datetime) -> Dict:
        """Create project timeline"""
        return {
            "start_date": start_date.isoformat(),
            "end_date": (start_date + timedelta(days=len(sprints) * 14)).isoformat(),
            "total_days": len(sprints) * 14,
            "sprint_schedule": [
                {
                    "sprint": s.sprint_number,
                    "start": s.start_date.isoformat(),
                    "end": s.end_date.isoformat()
                }
                for s in sprints
            ]
        }
    
    async def _generate_recommendations(self, sprints: List[SprintPlan], team_size: int) -> List[str]:
        """Generate sprint planning recommendations"""
        recommendations = []
        
        if len(sprints) > 6:
            recommendations.append("Consider reducing scope or increasing team size")
        
        if team_size < 3:
            recommendations.append("Small team may need longer sprints")
        
        recommendations.append("Hold daily stand-ups and sprint reviews")
        recommendations.append("Track velocity and adjust future sprints accordingly")
        
        return recommendations
    
    def _parse_json_response(self, response: str, default: Any) -> Any:
        """Parse JSON from LLM response"""
        try:
            start = response.find('[')
            if start == -1:
                start = response.find('{')
            end = response.rfind(']') + 1
            if end == 0:
                end = response.rfind('}') + 1
            
            if start >= 0 and end > start:
                return json.loads(response[start:end])
            return default
        except:
            return default