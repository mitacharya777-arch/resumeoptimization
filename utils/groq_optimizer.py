"""
Groq API-based Resume Optimizer
Provides intelligent resume optimization using Groq's fast LLM API.
"""

import os
from typing import Dict, List, Optional, Tuple
try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False


class GroqResumeOptimizer:
    """Resume optimizer using Groq API for fast, intelligent suggestions."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('GROQ_API_KEY')
        self.client = None
        
        if GROQ_AVAILABLE and self.api_key:
            try:
                self.client = Groq(api_key=self.api_key)
            except Exception as e:
                print(f"Warning: Could not initialize Groq client: {e}")
        elif not GROQ_AVAILABLE:
            print("Warning: groq package not installed. Install with: pip install groq")
    
    def is_available(self) -> bool:
        """Check if Groq API is available."""
        return self.client is not None
    
    def optimize_resume_for_job(
        self,
        resume_text: str,
        job_description: str,
        model: str = "llama-3.3-70b-versatile"
    ) -> Dict:
        """
        Optimize entire resume for a specific job description.
        
        Returns:
            Dictionary with optimized sections and suggestions
        """
        if not self.is_available():
            return {"error": "Groq API not available. Set GROQ_API_KEY environment variable."}
        
        try:
            prompt = self._build_optimization_prompt(resume_text, job_description)
            
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": """You are an expert resume writer and ATS optimization specialist. 
                        Your task is to optimize resumes to match job descriptions while maintaining 
                        authenticity and truthfulness. Provide specific, actionable improvements."""
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=4000
            )
            
            result_text = response.choices[0].message.content
            return self._parse_optimization_result(result_text)
        
        except Exception as e:
            return {"error": f"Error optimizing resume: {str(e)}"}
    
    def optimize_section(
        self,
        section_name: str,
        section_content: str,
        job_description: str,
        model: str = "llama-3.3-70b-versatile"
    ) -> Dict:
        """
        Optimize a specific resume section for a job description.
        
        Args:
            section_name: Name of the section (e.g., "Experience", "Summary")
            section_content: Current content of the section
            job_description: Job description to optimize against
            model: Groq model to use
        
        Returns:
            Dictionary with optimized content and suggestions
        """
        if not self.is_available():
            return {"error": "Groq API not available."}
        
        try:
            prompt = f"""Optimize the following {section_name} section of a resume to better match this job description.

JOB DESCRIPTION:
{job_description[:2000]}

CURRENT {section_name.upper()} SECTION:
{section_content}

Please provide:
1. An optimized version of this section that:
   - Incorporates relevant keywords from the job description
   - Maintains truthfulness and accuracy
   - Uses action verbs and quantifiable achievements
   - Is ATS-friendly
   - Is concise and impactful

2. A list of specific changes made and why they improve the resume for this job.

Format your response as:
OPTIMIZED SECTION:
[optimized content here]

CHANGES MADE:
1. [change description]
2. [change description]
..."""

            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert resume writer specializing in ATS optimization and job-specific tailoring."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            result_text = response.choices[0].message.content
            return self._parse_section_result(result_text, section_name)
        
        except Exception as e:
            return {"error": f"Error optimizing section: {str(e)}"}
    
    def generate_keyword_suggestions(
        self,
        resume_text: str,
        job_description: str,
        model: str = "llama-3.3-70b-versatile"
    ) -> Dict:
        """
        Generate specific keyword suggestions to add to resume.
        
        Returns:
            Dictionary with missing keywords and where to add them
        """
        if not self.is_available():
            return {"error": "Groq API not available."}
        
        try:
            prompt = f"""Analyze this resume and job description to identify:
1. Important keywords from the job description that are missing from the resume
2. Where in the resume these keywords should be added (which sections)
3. How to naturally incorporate these keywords

RESUME:
{resume_text[:3000]}

JOB DESCRIPTION:
{job_description[:2000]}

Provide a structured list of:
- Missing keywords (prioritized by importance)
- Recommended sections to add each keyword
- Example phrases or sentences that incorporate the keywords naturally

Format as:
MISSING KEYWORDS:
1. [keyword] - Add to [section] - Example: "[example phrase]"
2. [keyword] - Add to [section] - Example: "[example phrase]"
..."""

            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a resume optimization expert specializing in keyword optimization for ATS systems."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.5,
                max_tokens=2000
            )
            
            return {"suggestions": response.choices[0].message.content}
        
        except Exception as e:
            return {"error": f"Error generating keyword suggestions: {str(e)}"}
    
    def create_optimized_resume(
        self,
        resume_text: str,
        job_description: str,
        model: str = "llama-3.3-70b-versatile"
    ) -> Dict:
        """
        Create a fully optimized version of the resume.
        
        Returns:
            Complete optimized resume text
        """
        if not self.is_available():
            return {"error": "Groq API not available."}
        
        try:
            prompt = f"""Create an optimized version of this resume tailored specifically for this job description.

JOB DESCRIPTION:
{job_description[:2000]}

ORIGINAL RESUME:
{resume_text[:4000]}

Please create a complete, optimized resume that:
1. Incorporates relevant keywords from the job description naturally
2. Emphasizes experiences and skills most relevant to the job
3. Uses action verbs and quantifiable achievements
4. Is ATS-friendly (no complex formatting, standard section names)
5. Maintains all truthful information from the original
6. Reorders content to highlight most relevant experience first
7. Optimizes the summary/objective to match the job

Provide the complete optimized resume, maintaining the same structure but with improved content."""

            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": """You are an expert resume writer. Create optimized resumes that are 
                        both ATS-friendly and compelling to human recruiters. Always maintain truthfulness."""
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=4000
            )
            
            optimized_resume = response.choices[0].message.content
            
            # Extract just the resume content (remove any explanatory text)
            if "OPTIMIZED RESUME:" in optimized_resume:
                optimized_resume = optimized_resume.split("OPTIMIZED RESUME:")[-1].strip()
            elif "RESUME:" in optimized_resume:
                optimized_resume = optimized_resume.split("RESUME:")[-1].strip()
            
            return {
                "optimized_resume": optimized_resume,
                "original_resume": resume_text
            }
        
        except Exception as e:
            return {"error": f"Error creating optimized resume: {str(e)}"}
    
    def _build_optimization_prompt(self, resume_text: str, job_description: str) -> str:
        """Build comprehensive optimization prompt."""
        return f"""Analyze and optimize this resume for the following job description.

JOB DESCRIPTION:
{job_description[:2000]}

CURRENT RESUME:
{resume_text[:4000]}

Please provide:
1. Overall match score (0-100%) and explanation
2. Optimized version of each major section (Summary, Experience, Skills, etc.)
3. Specific keyword additions needed
4. Content improvements for each section
5. ATS optimization recommendations

Format your response clearly with sections marked."""

    def _parse_optimization_result(self, result_text: str) -> Dict:
        """Parse the optimization result into structured format."""
        # Simple parsing - can be enhanced
        return {
            "analysis": result_text,
            "raw_response": result_text
        }
    
    def _parse_section_result(self, result_text: str, section_name: str) -> Dict:
        """Parse section optimization result."""
        optimized_section = ""
        changes = []
        
        if "OPTIMIZED SECTION:" in result_text:
            parts = result_text.split("OPTIMIZED SECTION:")
            if len(parts) > 1:
                optimized_section = parts[1].split("CHANGES MADE:")[0].strip()
        
        if "CHANGES MADE:" in result_text:
            changes_text = result_text.split("CHANGES MADE:")[-1]
            changes = [
                line.strip() 
                for line in changes_text.split('\n') 
                if line.strip() and (line.strip()[0].isdigit() or line.strip().startswith('-'))
            ]
        
        return {
            "section_name": section_name,
            "optimized_content": optimized_section or result_text,
            "changes": changes,
            "raw_response": result_text
        }

