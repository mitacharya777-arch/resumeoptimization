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

    # ========== ENHANCED AI OPTIMIZATION METHODS ==========

    def analyze_job_description(
        self,
        job_description: str,
        model: str = "llama-3.3-70b-versatile"
    ) -> Dict:
        """
        Analyze job description to extract key requirements before optimization.

        Returns:
            Dictionary with extracted requirements, skills, experience level, industry
        """
        if not self.is_available():
            return {"error": "Groq API not available."}

        try:
            prompt = f"""Analyze this job description and extract key information:

JOB DESCRIPTION:
{job_description}

Please provide a structured analysis in this exact format:

REQUIRED_SKILLS:
- [skill 1]
- [skill 2]
...

YEARS_OF_EXPERIENCE:
[number] years (specify if entry-level, mid-level, senior, or executive)

INDUSTRY:
[industry name - e.g., Technology, Finance, Healthcare, etc.]

SENIORITY_LEVEL:
[entry-level, mid-level, senior, or executive]

CRITICAL_KEYWORDS:
- [keyword 1]
- [keyword 2]
...

ATS_KEYWORDS:
- [keyword 1]
- [keyword 2]
...

Keep responses concise and focused on what's most important for resume optimization."""

            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert job description analyst. Extract structured information that will help optimize resumes for this role."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,  # Lower temperature for more consistent extraction
                max_tokens=1500
            )

            result = response.choices[0].message.content
            return self._parse_job_analysis(result)

        except Exception as e:
            return {"error": f"Error analyzing job description: {str(e)}"}

    def multi_stage_optimize(
        self,
        resume_text: str,
        job_description: str,
        job_analysis: Dict,
        model: str = "llama-3.3-70b-versatile"
    ) -> Dict:
        """
        Perform multi-stage optimization:
        Stage 1: Content improvement
        Stage 2: ATS keyword optimization
        Stage 3: Format and consistency check

        Returns:
            Dictionary with final optimized resume and stage details
        """
        if not self.is_available():
            return {"error": "Groq API not available."}

        try:
            # Stage 1: Content Improvement
            # Extract Education section from original resume to make it crystal clear
            education_section = ""
            resume_lines = resume_text.split('\n')
            education_start = -1
            education_end = -1

            for i, line in enumerate(resume_lines):
                if 'EDUCATION' in line.upper() and education_start == -1:
                    education_start = i
                elif education_start != -1 and education_end == -1:
                    # Check if we hit another major section
                    if any(keyword in line.upper() for keyword in ['EXPERIENCE', 'SKILLS', 'PROJECTS', 'CERTIFICATIONS', 'SUMMARY']):
                        education_end = i
                        break

            # If we found education section, extract it
            if education_start != -1:
                if education_end == -1:
                    education_end = len(resume_lines)
                education_section = '\n'.join(resume_lines[education_start:education_end]).strip()

            stage1_prompt = f"""STAGE 1: CONTENT IMPROVEMENT

🔴🔴🔴 EDUCATION SECTION FROM ORIGINAL RESUME (MUST BE COPIED EXACTLY): 🔴🔴🔴
{education_section if education_section else "NO EDUCATION SECTION FOUND IN ORIGINAL RESUME"}

YOU MUST COPY THE ABOVE EDUCATION SECTION EXACTLY, CHARACTER-BY-CHARACTER IN YOUR OPTIMIZED RESUME.
DO NOT MODIFY IT. DO NOT ENHANCE IT. JUST COPY IT EXACTLY.

JOB DESCRIPTION:
{job_description[:2000]}

RESUME:
{resume_text[:4000]}

JOB ANALYSIS:
- Seniority: {job_analysis.get('seniority_level', 'Not specified')}
- Industry: {job_analysis.get('industry', 'Not specified')}
- Required Skills: {', '.join(job_analysis.get('required_skills', [])[:10])}

🚨 MANDATORY SECTION REQUIREMENTS (NON-NEGOTIABLE):
The optimized resume MUST include these sections in this order:
1. HEADER (name, title, contact info)
2. SUMMARY or PROFESSIONAL SUMMARY
3. SKILLS (MANDATORY - must be present and enhanced)
4. EXPERIENCE
5. EDUCATION (MANDATORY - MUST BE COPIED EXACTLY, WORD-FOR-WORD FROM ORIGINAL - NO CHANGES ALLOWED)
6. PROJECTS (if present in original)

⚠️⚠️⚠️ EDUCATION SECTION - ABSOLUTE REQUIREMENT ⚠️⚠️⚠️
If you remove or modify the EDUCATION section in ANY way, you have COMPLETELY FAILED this task.
The EDUCATION section is SACRED - it must be preserved EXACTLY as written in the original resume.

❗ CRITICAL - SKILLS SECTION (MANDATORY):
- The SKILLS section MUST be present in the optimized resume
- PRESERVE all existing skills from the original resume's SKILLS section
- ADD missing job-relevant skills (programming languages, tools, technologies from job description)
- REORGANIZE skills to put most relevant skills first
- GROUP related skills together (e.g., "Programming Languages:", "Tools:", "Technologies:")
- You may REMOVE only outdated/irrelevant skills that don't match the job
- Include all required skills from job description: {', '.join(job_analysis.get('required_skills', [])[:10])}
- If original resume has a SKILLS section, you MUST include an enhanced version in the optimized resume

🔴🔴🔴 CRITICAL - EDUCATION SECTION (MANDATORY - READ THIS TWICE) 🔴🔴🔴
- The EDUCATION section MUST be copied EXACTLY as it appears in the original resume
- DO NOT modify, enhance, rewrite, or improve the EDUCATION section in ANY way
- Copy it word-for-word, line-by-line, character-by-character, punctuation-by-punctuation
- If the original resume has an EDUCATION section, you MUST include it COMPLETELY UNCHANGED
- DO NOT add dates, DO NOT remove dates, DO NOT add degrees, DO NOT format differently
- Simply COPY and PASTE the EDUCATION section from the original resume EXACTLY as written
- This is THE MOST IMPORTANT requirement - if you modify Education, you have FAILED completely

Now improve the resume content by:
1. Emphasizing relevant experience for {job_analysis.get('seniority_level', 'this')} level
2. Using strong action verbs and quantifiable achievements
3. Highlighting skills that match the job requirements
4. Reordering experience to put most relevant first
5. Optimizing the summary/objective for this specific role

CRITICAL EXPERIENCE SECTION FORMATTING:
For EVERY job entry in the EXPERIENCE section, you MUST use this EXACT format:
- Line 1: COMPANY NAME IN ALL CAPS, Location | JOB TITLE IN ALL CAPS | Month YYYY - Month YYYY (or Present)
- Line 2+: Bullet points with achievements

Example:
MICROSOFT, Redmond, WA | SOFTWARE ENGINEER | June 2020 - Present
- Developed cloud infrastructure serving 10M+ users
- Led team of 5 engineers in migration project

CRITICAL PROJECT SECTION FORMATTING:
For EVERY project entry in the PROJECTS/PROJECTS section, you MUST use this EXACT format:
- Line 1: PROJECT NAME IN ALL CAPS
- Line 2+: Bullet points with project details

Example:
E-COMMERCE PLATFORM
- Built full-stack web application using React and Node.js
- Implemented payment gateway integration with Stripe

CRITICAL HEADER FORMATTING:
The header MUST follow this EXACT format:
Line 1: [Full Name]
Line 2: [Professional Title from original resume - e.g., Software Engineer, Data Scientist, etc.]
Line 3: [Contact info on one line separated by " | "]

Example:
John Doe
Software Engineer
(555) 123-4567 | john@email.com | linkedin.com/in/johndoe | github.com/johndoe | portfolio.com

🚨 ABSOLUTE REQUIREMENTS (WILL FAIL IF NOT FOLLOWED):
1. SKILLS SECTION: MUST be present in the optimized resume. Enhance the original SKILLS section - do NOT remove it.
2. 🔴 EDUCATION SECTION: MUST be copied EXACTLY word-for-word from the original resume. NO modifications, NO formatting changes, NO enhancements. Copy character-by-character including spacing, punctuation, dates, degrees, everything. This is THE MOST CRITICAL requirement.
3. HEADER: PRESERVE professional title and ALL contact information (Phone, Email, LinkedIn, GitHub, Portfolio, etc.)
4. EXPERIENCE: Company names in ALL CAPS. Job titles in ALL CAPS. This is MANDATORY.
5. PROJECTS: Project names in ALL CAPS. This is MANDATORY.

🔴🔴🔴 CRITICAL: If the optimized resume is missing the EDUCATION section or has ANY modifications to it, you have COMPLETELY FAILED the task. The EDUCATION section must be a perfect, exact, character-for-character copy from the original resume.

Provide the complete improved resume."""

            stage1_response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are an expert resume writer focusing on content quality and relevance."},
                    {"role": "user", "content": stage1_prompt}
                ],
                temperature=0.7,
                max_tokens=4000
            )

            stage1_resume = stage1_response.choices[0].message.content.strip()

            # Stage 2: ATS Keyword Optimization
            critical_keywords = job_analysis.get('critical_keywords', [])
            ats_keywords = job_analysis.get('ats_keywords', [])

            stage2_prompt = f"""STAGE 2: ATS KEYWORD OPTIMIZATION

RESUME FROM STAGE 1:
{stage1_resume[:4000]}

CRITICAL KEYWORDS TO INCORPORATE:
{', '.join(critical_keywords[:15])}

ATS KEYWORDS:
{', '.join(ats_keywords[:15])}

Optimize for ATS by:
1. Naturally incorporating the critical keywords listed above
2. Using exact keyword phrases from the job description
3. Including synonyms and related terms
4. Ensuring keywords appear in relevant sections (not keyword stuffing)
5. Using standard section headers (SUMMARY, EXPERIENCE, EDUCATION, SKILLS)
6. UPDATING the SKILLS section to include relevant ATS keywords and critical keywords

CRITICAL SKILLS SECTION OPTIMIZATION:
- ADD missing job-relevant skills from the critical keywords and ATS keywords lists above to the SKILLS section
- REORGANIZE skills to put most relevant ATS keywords first
- GROUP related skills together (e.g., "Programming Languages:", "Tools:", "Technologies:")
- REMOVE outdated or irrelevant skills if they don't match the job requirements
- Ensure all critical keywords from the job description are naturally incorporated into the SKILLS section
- Make the SKILLS section keyword-rich for ATS optimization while keeping it natural and relevant

CRITICAL EXPERIENCE SECTION FORMATTING:
For EVERY job entry in the EXPERIENCE section, you MUST maintain this EXACT format from Stage 1:
- Line 1: COMPANY NAME IN ALL CAPS, Location | JOB TITLE IN ALL CAPS | Month YYYY - Month YYYY (or Present)
- Line 2+: Bullet points with achievements

CRITICAL PROJECT SECTION FORMATTING:
For EVERY project entry in the PROJECTS section, you MUST maintain this EXACT format from Stage 1:
- Line 1: PROJECT NAME IN ALL CAPS
- Line 2+: Bullet points with project details

CRITICAL HEADER FORMATTING - COPY FROM STAGE 1:
The header MUST follow this EXACT format from Stage 1:
Line 1: [Full Name]
Line 2: [Professional Title - e.g., Software Engineer]
Line 3: [Contact info on one line separated by " | "]

🚨 ABSOLUTE REQUIREMENTS FROM STAGE 1 (MANDATORY):
1. SKILLS SECTION: MUST be present and enhanced from Stage 1. Do NOT remove it. Add ATS keywords naturally.
2. 🔴🔴🔴 EDUCATION SECTION: MUST be copied EXACTLY, CHARACTER-BY-CHARACTER as it appears in Stage 1. NO modifications, NO enhancements, NO formatting changes allowed. This is THE MOST CRITICAL requirement. Copy and paste it EXACTLY.
3. HEADER: Keep professional title and ALL contact information exactly as in Stage 1.
4. EXPERIENCE: Company names in ALL CAPS. Job titles in ALL CAPS.
5. PROJECTS: Project names in ALL CAPS.

🔴🔴🔴 CRITICAL FAILURE CONDITION: If you remove the SKILLS section or make ANY change to the EDUCATION section (even a single character, space, or punctuation mark), you have COMPLETELY FAILED this task. The EDUCATION section must be a perfect exact copy from Stage 1.

Provide the complete ATS-optimized resume."""

            stage2_response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are an ATS optimization specialist. Incorporate keywords naturally without stuffing."},
                    {"role": "user", "content": stage2_prompt}
                ],
                temperature=0.6,
                max_tokens=4000
            )

            stage2_resume = stage2_response.choices[0].message.content.strip()

            # Stage 3: Format and Consistency Check
            stage3_prompt = f"""STAGE 3: FORMAT AND CONSISTENCY CHECK

RESUME FROM STAGE 2:
{stage2_resume[:4000]}

Perform final quality check:
1. Ensure consistent formatting throughout
2. Check for grammar and spelling
3. Verify all bullet points use parallel structure
4. Ensure dates are consistent (e.g., all "Month YYYY" format)
5. Remove any duplicate information
6. Ensure professional tone throughout
7. Verify resume is ATS-friendly (no complex formatting)
8. DO NOT use markdown formatting like **bold** or *italic* - use plain text only
9. Verify the SKILLS section is well-organized and includes all relevant skills from Stage 2

CRITICAL SKILLS SECTION FORMATTING:
- Ensure the SKILLS section from Stage 2 is preserved with all added job-relevant skills
- Skills should be organized logically (most relevant first, grouped by category if applicable)
- Remove any duplicate skills
- Verify skills are presented in a clean, ATS-friendly format (comma-separated or categorized)
- The SKILLS section should be comprehensive and keyword-rich without appearing stuffed

CRITICAL EXPERIENCE SECTION FORMATTING - THIS IS MANDATORY:
For EVERY SINGLE job entry in the EXPERIENCE section, you MUST use this EXACT format:
- Line 1: COMPANY NAME IN ALL CAPS, Location | JOB TITLE IN ALL CAPS | Month YYYY - Month YYYY (or Present)
- Line 2+: Bullet points with achievements

Example (COPY THIS FORMAT EXACTLY):
MICROSOFT, Redmond, WA | SENIOR SOFTWARE ENGINEER | January 2020 - Present
- Developed cloud infrastructure serving 10M+ users
- Led team of 5 engineers in migration project

GOOGLE, Mountain View, CA | SOFTWARE ENGINEER | June 2018 - December 2019
- Built scalable APIs handling 1M+ requests per day
- Optimized database queries reducing latency by 40%

CRITICAL PROJECT SECTION FORMATTING - THIS IS MANDATORY:
For EVERY project entry in the PROJECTS section, you MUST use this EXACT format:
- Line 1: PROJECT NAME IN ALL CAPS
- Line 2+: Bullet points with project details

Example (COPY THIS FORMAT EXACTLY):
E-COMMERCE PLATFORM
- Built full-stack web application using React and Node.js
- Implemented payment gateway integration with Stripe
- Deployed on AWS with CI/CD pipeline

MACHINE LEARNING CLASSIFIER
- Developed ML model to predict customer churn with 92% accuracy
- Used Python, TensorFlow, and scikit-learn

CRITICAL HEADER FORMATTING - COPY FROM STAGE 2:
The header MUST follow this EXACT format from Stage 2:
Line 1: [Full Name]
Line 2: [Professional Title - e.g., Software Engineer]
Line 3: [Contact info on one line separated by " | "]

Example:
Abhishek Panda
Software Engineer
(224) 844-6987 | pandaabhishek34@gmail.com | linkedin.com/in/abhishek-rabindra-panda | github.com/pandaabhishek38 | abhishekrabindrapanda-portfolio.vercel.app

🚨 ABSOLUTE REQUIREMENTS FROM STAGE 2 (NON-NEGOTIABLE):
1. SKILLS SECTION: MUST be present in the final resume. Verify it's included from Stage 2. Do NOT remove it.
2. 🔴🔴🔴 EDUCATION SECTION: MUST be copied EXACTLY, CHARACTER-BY-CHARACTER as it appears in Stage 2. NO modifications, NO grammar fixes, NO formatting changes, NO enhancements allowed whatsoever. This is THE SINGLE MOST CRITICAL requirement of the entire task. Copy it EXACTLY.
3. HEADER: Professional title and ALL contact information must be exactly as in Stage 2.
4. Company names MUST be in ALL CAPS (e.g., MICROSOFT, GOOGLE, AMAZON)
5. Job titles MUST be in ALL CAPS (e.g., SENIOR SOFTWARE ENGINEER, DATA SCIENTIST)
6. Project names MUST be in ALL CAPS (e.g., E-COMMERCE PLATFORM, MACHINE LEARNING CLASSIFIER)
7. Plain text only. NO markdown formatting (**bold**, *italic*, etc.). ATS systems cannot parse markdown.
8. Dates in Title Case (Month YYYY format)

🔴🔴🔴 CRITICAL FAILURE CONDITION: The final resume MUST include both SKILLS and EDUCATION sections. If the EDUCATION section is missing or has even ONE character changed from Stage 2, you have COMPLETELY FAILED the entire task. The EDUCATION section must be a perfect, exact, character-for-character copy from Stage 2.

🚫 DO NOT ADD ANY COMMENTARY, RECOMMENDATIONS, OR NEXT STEPS:
- DO NOT add "Recommended actions" or "Suggestions" at the end
- DO NOT add any explanations of what you changed
- DO NOT add "Next steps" or "Further improvements"
- Provide ONLY the resume content itself - nothing more
- The resume should end with the last section (typically PROJECTS or EDUCATION)

Provide the final, polished resume in plain text format with NO additional commentary."""

            stage3_response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a meticulous resume editor focused on quality, consistency, and professionalism."},
                    {"role": "user", "content": stage3_prompt}
                ],
                temperature=0.5,
                max_tokens=4000
            )

            final_resume = stage3_response.choices[0].message.content.strip()

            # Clean up the final resume - remove AI preambles and commentary
            # Common preamble patterns to remove
            preamble_markers = [
                "FINAL RESUME:",
                "Here's the final",
                "Here is the final",
                "After conducting",
                "I've made",
                "I have made",
                "The final resume",
                "Below is",
                "Here's the polished",
                "Here is the polished"
            ]

            # Check if any preamble exists and remove everything before it
            lines = final_resume.split('\n')
            resume_start_index = 0

            for i, line in enumerate(lines):
                line_lower = line.lower().strip()
                # Skip empty lines
                if not line_lower:
                    continue
                # Check if this line is a preamble
                is_preamble = any(marker.lower() in line_lower for marker in preamble_markers)
                if is_preamble:
                    resume_start_index = i + 1
                    continue
                # If we find a line that looks like the start of a resume (name or contact), stop
                # Resume typically starts with a name (capitalized words) or contact info
                if not is_preamble and (
                    line.strip() and
                    (line.strip()[0].isupper() or '@' in line or 'phone' in line_lower or 'email' in line_lower)
                ):
                    resume_start_index = i
                    break

            # Reconstruct resume from the detected start (for preview - includes trailing commentary)
            final_resume_with_commentary = '\n'.join(lines[resume_start_index:]).strip()

            # Create a clean version for download (remove trailing AI commentary)
            # Find where the actual resume ends and commentary begins
            resume_lines = lines[resume_start_index:]
            clean_resume_end = len(resume_lines)

            # Patterns that indicate the start of trailing commentary
            commentary_indicators = [
                "I've made the following adjustments",
                "I have made the following adjustments",
                "The following adjustments",
                "The final resume is",
                "This resume is polished",
                "This polished resume",
                "ready for submission",
                "effectively showcases",
                "showcasing your",
                "showcases your",
                "strong candidate for passing",
                "Here are the changes",
                "Changes made:",
                "Improvements made:",
                "clear, concise, and professional manner",
                "Recommended actions",
                "Recommended action",
                "Recommendations:",
                "Next steps:",
                "Additional recommendations",
                "Further recommendations",
                "To further improve",
                "For additional improvement",
                "Consider the following",
                "You may also want to",
                "It would be beneficial to",
                "I recommend",
                "I suggest",
                "Suggestion:",
                "Suggestions:"
            ]

            # Patterns for bullet-pointed commentary (AI describing what it did)
            commentary_bullet_patterns = [
                "* Ensured",
                "* Verified",
                "* Corrected",
                "* Removed",
                "* Maintained",
                "* Fixed",
                "* Updated",
                "* Confirmed",
                "* Standardized",
                "- Ensured",
                "- Verified",
                "- Corrected",
                "- Removed",
                "- Maintained",
                "- Fixed",
                "- Updated",
                "- Confirmed",
                "- Standardized"
            ]

            # Common words in AI commentary about changes
            commentary_action_words = [
                "ensured", "verified", "corrected", "removed", "maintained",
                "fixed", "updated", "confirmed", "standardized", "professional tone",
                "ats-friendly", "parallel structure", "consistent formatting"
            ]

            # Search backwards to find where commentary starts
            import re
            for i in range(len(resume_lines) - 1, -1, -1):
                line = resume_lines[i].strip()
                line_lower = line.lower()

                # Check for explicit commentary indicators
                if any(indicator.lower() in line_lower for indicator in commentary_indicators):
                    clean_resume_end = i
                    continue

                # Check for bullet points describing AI's changes
                if any(line.startswith(pattern) for pattern in commentary_bullet_patterns):
                    clean_resume_end = i
                    continue

                # Check for numbered list items (1. , 2. , etc.) with commentary action words
                if re.match(r'^\d+\.\s+', line):
                    if any(action_word in line_lower for action_word in commentary_action_words):
                        clean_resume_end = i
                        continue

                # If we found commentary, keep looking backwards for more
                if clean_resume_end < len(resume_lines):
                    continue

                # Stop if we hit a legitimate resume section header
                # (all caps headers like EDUCATION, SKILLS, EXPERIENCE, etc.)
                if line.isupper() and len(line.split()) <= 3 and len(line) > 2:
                    break

            # Clean version without trailing commentary
            download_resume = '\n'.join(resume_lines[:clean_resume_end]).strip()

            # Remove markdown bold formatting (**text**) - not ATS-friendly
            final_resume_with_commentary = final_resume_with_commentary.replace('**', '')
            download_resume = download_resume.replace('**', '')

            return {
                "optimized_resume": download_resume,  # For preview (clean version)
                "download_resume": download_resume,  # For download (clean)
                "original_resume": resume_text,
                "stages": {
                    "stage1_content": "Content improved",
                    "stage2_keywords": f"Added {len(critical_keywords)} critical keywords",
                    "stage3_format": "Format and consistency checked"
                },
                "multi_stage": True
            }

        except Exception as e:
            return {"error": f"Error in multi-stage optimization: {str(e)}"}

    def calculate_ats_score(
        self,
        resume_text: str,
        job_description: str,
        model: str = "llama-3.3-70b-versatile"
    ) -> Dict:
        """
        Calculate ATS compatibility score for common ATS systems.

        Checks for: Workday, Greenhouse, Lever compatibility

        Returns:
            Dictionary with ATS score and specific recommendations
        """
        if not self.is_available():
            return {"error": "Groq API not available."}

        try:
            prompt = f"""Analyze this resume for ATS (Applicant Tracking System) compatibility.

RESUME:
{resume_text[:3000]}

JOB DESCRIPTION:
{job_description[:1500]}

Evaluate ATS compatibility for common systems (Workday, Greenhouse, Lever):

1. KEYWORD MATCH: How well do resume keywords match job description? (0-100)
2. FORMAT SCORE: Is formatting ATS-friendly? (0-100)
   - Standard fonts, no tables/columns
   - Standard section headers
   - No images or graphics
   - Simple bullet points
3. SECTION COMPLETENESS: Are all standard sections present? (0-100)
4. OVERALL ATS SCORE: (0-100)

Provide response in this format:
KEYWORD_MATCH: [score]
FORMAT_SCORE: [score]
SECTION_SCORE: [score]
OVERALL_SCORE: [score]

DO NOT provide recommendations or suggestions. Only provide the scores."""

            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are an ATS compatibility expert familiar with Workday, Greenhouse, and Lever systems."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1000
            )

            result = response.choices[0].message.content
            return self._parse_ats_score(result)

        except Exception as e:
            return {"error": f"Error calculating ATS score: {str(e)}"}

    def _parse_job_analysis(self, analysis_text: str) -> Dict:
        """Parse job description analysis into structured format."""
        result = {
            "required_skills": [],
            "years_of_experience": "Not specified",
            "industry": "Not specified",
            "seniority_level": "mid-level",
            "critical_keywords": [],
            "ats_keywords": []
        }

        lines = analysis_text.split('\n')
        current_section = None

        for line in lines:
            line = line.strip()
            if not line:
                continue

            if "REQUIRED_SKILLS:" in line:
                current_section = "skills"
            elif "YEARS_OF_EXPERIENCE:" in line:
                current_section = "experience"
            elif "INDUSTRY:" in line:
                current_section = "industry"
            elif "SENIORITY_LEVEL:" in line:
                current_section = "seniority"
            elif "CRITICAL_KEYWORDS:" in line:
                current_section = "critical"
            elif "ATS_KEYWORDS:" in line:
                current_section = "ats"
            elif line.startswith('-') or line.startswith('•'):
                item = line.lstrip('-•').strip()
                if current_section == "skills":
                    result["required_skills"].append(item)
                elif current_section == "critical":
                    result["critical_keywords"].append(item)
                elif current_section == "ats":
                    result["ats_keywords"].append(item)
            elif current_section == "experience" and not line.endswith(':'):
                result["years_of_experience"] = line
            elif current_section == "industry" and not line.endswith(':'):
                result["industry"] = line
            elif current_section == "seniority" and not line.endswith(':'):
                result["seniority_level"] = line.lower()

        return result

    def _parse_ats_score(self, score_text: str) -> Dict:
        """Parse ATS score analysis into structured format."""
        result = {
            "keyword_match": 0,
            "format_score": 0,
            "section_score": 0,
            "overall_score": 0,
            "recommendations": []
        }

        lines = score_text.split('\n')

        for line in lines:
            line = line.strip()
            if not line:
                continue

            if "KEYWORD_MATCH:" in line:
                try:
                    result["keyword_match"] = int(line.split(':')[1].strip())
                except:
                    pass
            elif "FORMAT_SCORE:" in line:
                try:
                    result["format_score"] = int(line.split(':')[1].strip())
                except:
                    pass
            elif "SECTION_SCORE:" in line:
                try:
                    result["section_score"] = int(line.split(':')[1].strip())
                except:
                    pass
            elif "OVERALL_SCORE:" in line:
                try:
                    result["overall_score"] = int(line.split(':')[1].strip())
                except:
                    pass

        return result

