from app.llm.openai_client import OpenAIClient
from app.utils.logger import get_logger
from app.utils.exceptions import CodeReviewException
from app.schemas.agent_schema import CodeReviewResult, CodeIssue
from typing import List, Dict, Any
import json
import time

logger = get_logger(__name__)

class CodeReviewAgent:
    def __init__(self):
        self.llm_client = OpenAIClient()
        self.agent_type = "code_review"
    
    async def review_code(
        self,
        code: str,
        language: str,
        file_path: str = "unknown.py",
        review_type: str = "full"  # full, security, performance, style
    ) -> CodeReviewResult:
        """Review code for issues"""
        start_time = time.time()
        
        try:
            logger.info(f"Code review agent: Reviewing {file_path}")
            
            # Determine review focus
            if review_type == "security":
                issues = await self._security_review(code, language)
            elif review_type == "performance":
                issues = await self._performance_review(code, language)
            elif review_type == "style":
                issues = await self._style_review(code, language)
            else:
                issues = await self._full_review(code, language)
            
            # Calculate quality scores
            quality_score = self._calculate_quality_score(issues)
            complexity_score = self._calculate_complexity(code)
            
            # Extract security issues
            security_issues = [
                i.message for i in issues 
                if "security" in i.message.lower() or i.severity == "error"
            ]
            
            # Performance concerns
            performance_concerns = [
                i.message for i in issues 
                if "performance" in i.message.lower()
            ]
            
            result = CodeReviewResult(
                file_path=file_path,
                language=language,
                issues=issues,
                quality_score=quality_score,
                complexity_score=complexity_score,
                security_issues=security_issues,
                performance_concerns=performance_concerns
            )
            
            processing_time = time.time() - start_time
            logger.info(f"Code review completed in {processing_time:.2f}s")
            
            return result
            
        except Exception as e:
            logger.error(f"Code review failed: {str(e)}")
            raise CodeReviewException(f"Code review failed: {str(e)}")
    
    async def _full_review(self, code: str, language: str) -> List[CodeIssue]:
        """Perform full code review"""
        prompt = f"""
        Review this {language} code for issues:
        
        ```{language}
        {code[:2000]}
        ```
        
        Identify:
        1. Bugs and logical errors
        2. Security vulnerabilities
        3. Performance issues
        4. Code style problems
        5. Best practices violations
        
        For each issue, provide:
        - line number (if applicable)
        - severity (error/warning/info)
        - message describing the issue
        - suggestion to fix
        - rule/category
        
        Return as JSON array.
        """
        
        messages = [
            {"role": "system", "content": "You are a senior software engineer doing code reviews."},
            {"role": "user", "content": prompt}
        ]
        
        response = await self.llm_client.get_chat_completion_text(
            messages,
            model_type="high",
            temperature=0.2
        )
        
        return self._parse_issues(response)
    
    async def _security_review(self, code: str, language: str) -> List[CodeIssue]:
        """Security-focused code review"""
        prompt = f"""
        Perform a security audit on this {language} code:
        
        ```{language}
        {code[:2000]}
        ```
        
        Look for:
        1. Injection vulnerabilities (SQL, command, etc.)
        2. Authentication/authorization issues
        3. Sensitive data exposure
        4. Input validation problems
        5. Insecure dependencies
        
        Return as JSON array of security issues.
        """
        
        messages = [
            {"role": "system", "content": "You are a security expert performing code audit."},
            {"role": "user", "content": prompt}
        ]
        
        response = await self.llm_client.get_chat_completion_text(
            messages,
            model_type="high",
            temperature=0.2
        )
        
        return self._parse_issues(response)
    
    async def _performance_review(self, code: str, language: str) -> List[CodeIssue]:
        """Performance-focused code review"""
        prompt = f"""
        Analyze this {language} code for performance issues:
        
        ```{language}
        {code[:2000]}
        ```
        
        Check for:
        1. Inefficient algorithms
        2. Memory leaks
        3. Unnecessary operations
        4. Database query issues
        5. Caching opportunities
        
        Return as JSON array of performance issues.
        """
        
        messages = [
            {"role": "system", "content": "You are a performance optimization expert."},
            {"role": "user", "content": prompt}
        ]
        
        response = await self.llm_client.get_chat_completion_text(
            messages,
            model_type="medium",
            temperature=0.2
        )
        
        return self._parse_issues(response)
    
    async def _style_review(self, code: str, language: str) -> List[CodeIssue]:
        """Style-focused code review"""
        prompt = f"""
        Check this {language} code for style issues:
        
        ```{language}
        {code[:2000]}
        ```
        
        Check against:
        1. Naming conventions
        2. Code formatting
        3. Documentation
        4. Complexity
        5. Best practices
        
        Return as JSON array of style issues.
        """
        
        messages = [
            {"role": "system", "content": "You are a code quality expert."},
            {"role": "user", "content": prompt}
        ]
        
        response = await self.llm_client.get_chat_completion_text(
            messages,
            model_type="medium",
            temperature=0.1
        )
        
        return self._parse_issues(response)
    
    async def suggest_fixes(self, issues: List[CodeIssue], code: str) -> Dict[str, str]:
        """Suggest fixes for identified issues"""
        suggestions = {}
        
        for issue in issues[:5]:  # Limit to top 5 issues
            prompt = f"""
            Suggest a fix for this code issue:
            
            Issue: {issue.message}
            Suggestion: {issue.suggestion}
            
            Original code snippet:
            ```
            {code[issue.line-3:issue.line+3] if issue.line else code[:200]}
            ```
            
            Provide the corrected code snippet.
            """
            
            messages = [
                {"role": "system", "content": "You are an expert programmer."},
                {"role": "user", "content": prompt}
            ]
            
            try:
                fix = await self.llm_client.get_chat_completion_text(
                    messages,
                    model_type="medium",
                    temperature=0.2
                )
                suggestions[issue.message[:50]] = fix
            except:
                suggestions[issue.message[:50]] = issue.suggestion
        
        return suggestions
    
    def _calculate_quality_score(self, issues: List[CodeIssue]) -> float:
        """Calculate code quality score (0-100)"""
        if not issues:
            return 100.0
        
        severity_weights = {
            "error": 10,
            "warning": 5,
            "info": 1
        }
        
        total_penalty = 0
        for issue in issues:
            total_penalty += severity_weights.get(issue.severity, 1)
        
        # Max penalty is 100 (if 10 errors)
        score = max(0, 100 - total_penalty)
        return score
    
    def _calculate_complexity(self, code: str) -> float:
        """Calculate code complexity score"""
        # Simplified complexity calculation
        lines = code.split('\n')
        total_lines = len(lines)
        
        # Count complex structures
        complexity_factors = 0
        complexity_factors += code.count('if ')
        complexity_factors += code.count('for ')
        complexity_factors += code.count('while ')
        complexity_factors += code.count('switch')
        complexity_factors += code.count('try:')
        complexity_factors += code.count('except')
        
        if total_lines == 0:
            return 0.0
        
        # Score from 0-100, higher is more complex
        complexity = min(100, (complexity_factors / max(1, total_lines)) * 50)
        return complexity
    
    def _parse_issues(self, response: str) -> List[CodeIssue]:
        """Parse issues from LLM response"""
        issues = []
        
        try:
            # Find JSON array
            start = response.find('[')
            end = response.rfind(']') + 1
            
            if start >= 0 and end > start:
                issues_data = json.loads(response[start:end])
                
                for issue_data in issues_data:
                    issue = CodeIssue(
                        line=issue_data.get("line"),
                        severity=issue_data.get("severity", "info"),
                        message=issue_data.get("message", "Unknown issue"),
                        suggestion=issue_data.get("suggestion", ""),
                        rule=issue_data.get("rule")
                    )
                    issues.append(issue)
        except Exception as e:
            logger.error(f"Failed to parse issues: {str(e)}")
            
            # Add default issue
            issues.append(CodeIssue(
                line=None,
                severity="info",
                message="Code review completed",
                suggestion="No specific issues identified",
                rule="general"
            ))
        
        return issues