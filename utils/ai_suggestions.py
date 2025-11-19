"""
ADVANCED FEATURE: AI-Powered Resume Suggestions
Uses OpenAI API for intelligent resume optimization recommendations.
Requires OPENAI_API_KEY environment variable.
"""

import os
from typing import Dict, List, Optional
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class AISuggestions:
    """Generate AI-powered suggestions for resume optimization."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.client = None
        
        if OPENAI_AVAILABLE and self.api_key:
            try:
                self.client = OpenAI(api_key=self.api_key)
            except Exception as e:
                print(f"Warning: Could not initialize OpenAI client: {e}")
    
    def is_available(self) -> bool:
        """Check if AI suggestions are available."""
        return self.client is not None
    
    def generate_suggestions(
        self, 
        resume_text: str, 
        job_description: str = None,
        analysis_results: Dict = None
    ) -> List[str]:
        """Generate AI-powered suggestions."""
        if not self.is_available():
            return ["AI suggestions not available. Set OPENAI_API_KEY environment variable."]
        
        try:
            prompt = self._build_prompt(resume_text, job_description, analysis_results)
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional resume optimization expert. Provide specific, actionable suggestions to improve resumes for job applications."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            suggestions_text = response.choices[0].message.content
            # Parse suggestions (assuming numbered list)
            suggestions = [
                s.strip() 
                for s in suggestions_text.split('\n') 
                if s.strip() and (s.strip()[0].isdigit() or s.strip().startswith('-'))
            ]
            
            return suggestions[:10]  # Limit to 10 suggestions
        
        except Exception as e:
            return [f"Error generating AI suggestions: {str(e)}"]
    
    def _build_prompt(
        self, 
        resume_text: str, 
        job_description: str = None,
        analysis_results: Dict = None
    ) -> str:
        """Build prompt for AI."""
        prompt = "Analyze this resume and provide specific improvement suggestions:\n\n"
        prompt += "RESUME:\n"
        prompt += resume_text[:2000] + "\n\n"  # Limit resume text
        
        if job_description:
            prompt += "JOB DESCRIPTION:\n"
            prompt += job_description[:1000] + "\n\n"  # Limit job description
        
        if analysis_results:
            prompt += "CURRENT ANALYSIS:\n"
            if 'job_match' in analysis_results:
                prompt += f"Match Score: {analysis_results['job_match']['score']}%\n"
            if 'resume_quality' in analysis_results:
                prompt += f"Quality Score: {analysis_results['resume_quality']['quality_score']}/100\n"
            prompt += "\n"
        
        prompt += "Provide 5-7 specific, actionable suggestions to improve this resume for the job application. Focus on:\n"
        prompt += "1. Content improvements\n"
        prompt += "2. Keyword optimization\n"
        prompt += "3. Structure and formatting\n"
        prompt += "4. Missing elements\n"
        prompt += "5. ATS optimization\n\n"
        prompt += "Format as a numbered list."
        
        return prompt
    
    def improve_section(
        self, 
        section_name: str, 
        section_content: str, 
        job_description: str = None
    ) -> str:
        """Get AI suggestions for improving a specific section."""
        if not self.is_available():
            return "AI suggestions not available."
        
        try:
            prompt = f"Improve the following {section_name} section of a resume"
            if job_description:
                prompt += f" for this job: {job_description[:500]}"
            prompt += f":\n\n{section_content}\n\n"
            prompt += "Provide an improved version that is more impactful and ATS-friendly."
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional resume writer. Improve resume sections to be more impactful and ATS-friendly."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=300,
                temperature=0.7
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            return f"Error: {str(e)}"

