"""
Unified AI Provider Interface
Supports multiple AI models: Groq, OpenAI, Claude, Gemini, Cohere, etc.
"""

import os
from typing import Dict, Optional, List
from abc import ABC, abstractmethod


class AIProvider(ABC):
    """Base class for AI providers."""
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if provider is available."""
        pass
    
    @abstractmethod
    def analyze_resume(self, resume_text: str, job_description: str) -> Dict:
        """Analyze resume against job description."""
        pass
    
    @abstractmethod
    def optimize_resume(self, resume_text: str, job_description: str, suggestions: List[str]) -> str:
        """Create optimized resume."""
        pass


class GroqProvider(AIProvider):
    """Groq AI Provider - Fast and cost-effective."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('GROQ_API_KEY')
        self.client = None
        self.model = "llama-3.3-70b-versatile"
        
        try:
            from groq import Groq
            if self.api_key:
                self.client = Groq(api_key=self.api_key)
        except ImportError:
            pass
    
    def is_available(self) -> bool:
        return self.client is not None
    
    def analyze_resume(self, resume_text: str, job_description: str) -> Dict:
        if not self.is_available():
            return {"error": "Groq API not available. Set GROQ_API_KEY."}
        
        prompt = f"""You are a resume analyst. Analyze this resume against the job description and provide a strict, accurate match score.

JOB DESCRIPTION:
{job_description}

RESUME:
{resume_text}

SCORING CRITERIA - Evaluate the resume using these specific factors:

1. REQUIRED SKILLS MATCH (50 points - 50% of total score):
   - CRITICAL: This is the most important factor - it accounts for half of the total score
   - Identify ALL required technical skills, tools, technologies, and competencies mentioned in the job description
   - Count how many required skills are present in the resume
   - Score: (skills_found / skills_required) × 50
   - Example: If job requires 10 skills and resume has 6, score = (6/10) × 50 = 30 points
   - Example: If job requires 8 skills and resume has 8, score = (8/8) × 50 = 50 points
   - Be thorough in identifying skills - include programming languages, frameworks, tools, methodologies, soft skills, certifications, etc.

2. EXPERIENCE LEVEL MATCH (20 points):
   - Check if experience level matches (Junior, Mid-level, Senior, Lead, Principal, etc.)
   - Perfect match: 20 points
   - One level off (e.g., Mid applying to Senior): 12 points
   - Two+ levels off (e.g., Junior applying to Senior): 5 points
   - No clear level in resume: 8 points

3. YEARS OF EXPERIENCE (12 points):
   - Compare required years of experience vs. candidate's total experience
   - Meets or exceeds requirement: 12 points
   - Within 1-2 years: 8 points
   - Within 3-4 years: 4 points
   - More than 4 years short: 0 points
   - No requirement specified: 6 points (neutral)

4. JOB TITLE RELEVANCE (10 points):
   - Check if candidate's current/past job titles are relevant to the target role
   - Exact or very similar title: 10 points
   - Related title in same field: 7 points
   - Different field but transferable skills: 3 points
   - Completely unrelated: 0 points

5. EDUCATION REQUIREMENTS (5 points):
   - Check if education level matches (Bachelor's, Master's, PhD, etc.)
   - Meets requirement: 5 points
   - One level below: 3 points
   - Two+ levels below: 0 points
   - No requirement specified: 2.5 points (neutral)

6. INDUSTRY/DOMAIN EXPERIENCE (3 points):
   - Check if candidate has experience in the same or related industry
   - Same industry: 3 points
   - Related industry: 2 points
   - Different industry: 0 points
   - No industry specified in job: 1.5 points (neutral)

TOTAL SCORE CALCULATION:
- Add up all 6 factors (max 100 points)
- Required Skills Match = 50 points (50% of total)
- Other factors = 50 points combined (50% of total)
- Round to nearest whole number
- This is your MATCH_SCORE

SCORING GUIDELINES:
- 0-40%: Missing most required skills, significant experience level mismatch, or major gaps
- 40-70%: Has some required skills and relevant experience, but missing key requirements
- 70-100%: Meets most/all requirements, strong skill match, appropriate experience level

Be STRICT - only give 70+ if the candidate truly meets most requirements.

Provide your analysis in this EXACT format:

MATCH_SCORE: [number between 0-100 - be strict!]
STRENGTHS:
- [strength 1]
- [strength 2]
- ...

IMPROVEMENTS_NEEDED:
- [specific content change 1]
- [specific content change 2]
- ...

CONTENT_SUGGESTIONS:
1. [Section/Area]: [What to change] - [Why] - [How to improve it]
2. [Section/Area]: [What to change] - [Why] - [How to improve it]
...

Start your response with "MATCH_SCORE:" immediately."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a strict resume analyst. Evaluate resumes using a structured scoring framework: 1. Required Skills Match (50 points - 50% of total) - CRITICAL, count ALL skills found vs required (technical skills, tools, technologies, competencies). 2. Experience Level Match (20 points) - check if levels align. 3. Years of Experience (12 points) - compare required vs actual. 4. Job Title Relevance (10 points) - assess title similarity. 5. Education Requirements (5 points) - check education level match. 6. Industry/Domain Experience (3 points) - evaluate industry alignment. Calculate total (max 100) and round to nearest whole number. Skills match is 50% of score - be thorough in identifying and matching skills. Be STRICT: 0-40% = missing most requirements, 40-70% = some requirements met, 70-100% = most/all requirements met. Always provide score in format: MATCH_SCORE: [number]."
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,  # Lower temperature for more strict scoring
                max_tokens=3000
            )
            return {"raw_analysis": response.choices[0].message.content, "provider": "Groq"}
        except Exception as e:
            return {"error": f"Groq API error: {str(e)}"}
    
    def optimize_resume(self, resume_text: str, job_description: str, suggestions: List[str]) -> str:
        if not self.is_available():
            return "Groq API not available."
        
        prompt = f"""You are an expert resume writer. Create an optimized version of this resume that is specifically tailored to match the job description.

ORIGINAL RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

SUGGESTIONS TO IMPLEMENT:
{chr(10).join(suggestions[:10])}

🚨 CRITICAL MANDATORY REQUIREMENT FOR EXPERIENCE SECTION 🚨
YOU MUST COMPLETELY REWRITE EVERY EXPERIENCE BULLET POINT. DO NOT just add keywords or make minor edits.
EACH BULLET MUST BE TRANSFORMED with actual content improvements, metrics, and job-relevant achievements.

EXPERIENCE SECTION RULES (MANDATORY - APPLY TO EVERY BULLET):
1. MANDATORY REWRITE: You MUST rewrite each bullet point from scratch. DO NOT copy-paste or make minor edits.
   - If original says "Worked on projects" → Rewrite to "Designed and deployed 3 microservices using Python and Docker, reducing API response time by 45% and handling 50K+ requests daily"
   - If original says "Managed team" → Rewrite to "Led cross-functional team of 5 engineers, implementing Agile practices that increased sprint velocity by 30% and reduced bug reports by 25%"
   - Transform vague statements into specific, measurable achievements

2. STRUCTURE (MANDATORY): Every bullet MUST use Problem → Action → Result OR Task → Tools → Impact format
   - Example: "Addressed [specific problem] by implementing [specific solution] using [technologies], resulting in [quantifiable improvement]"
   - Example: "Developed [specific feature/system] using [tools/tech], improving [metric] by [percentage/amount] and [business impact]"

3. ACTION VERBS (MANDATORY): Use strong, varied verbs - DO NOT repeat verbs across bullets
   - Use: Designed, Built, Implemented, Led, Automated, Analyzed, Developed, Optimized, Increased, Reduced, Managed, Created, Deployed, Architected, Streamlined, Accelerated, Transformed, etc.
   - Vary verbs: If first bullet uses "Developed", second should use "Architected" or "Built", not "Developed" again

4. QUANTITATIVE METRICS (MANDATORY): Every bullet MUST include at least ONE measurable metric:
   - Numbers: "3 applications", "50K users", "5 team members"
   - Percentages: "40% faster", "25% reduction", "30% increase"
   - Time: "reduced from 5 hours to 30 minutes", "deployed in 2 weeks"
   - Money: "$50K saved", "revenue increased by $200K"
   - Scale: "serving 1M+ requests", "processing 10TB data daily"
   - If original has no metrics, ADD realistic, job-relevant metrics based on the work described

5. JOB RELEVANCE (MANDATORY): Every bullet MUST connect to job description requirements:
   - Identify key technologies/tools from job description
   - Identify key responsibilities/outcomes from job description
   - Rewrite bullets to demonstrate experience with those technologies/responsibilities
   - Example: If job requires "cloud deployment" and original says "deployed applications", rewrite to "Deployed scalable applications on AWS using EC2, S3, and Lambda, achieving 99.9% uptime and reducing infrastructure costs by 35%"

6. SPECIFIC STRUCTURES (Use when relevant):
   - "Addressed [specific problem] by using [technology/tool] to [specific action], improving [metric] by [%/amount] and [business impact]"
   - "Collaborated with [specific teams/stakeholders] to [specific action], resulting in [quantifiable outcome] and [business value]"
   - "Designed and implemented [specific solution] using [technologies], reducing [metric] by [amount] and enabling [business outcome]"

7. TONE: Natural, business-professional, real resume writing style - NO generic/AI-style language

8. AVOID filler phrases: NO 'leveraged cutting-edge', 'utilized synergistic', 'dynamic environment', 'synergistic solutions', 'passionate about', or vague wording

9. CONTENT: Specific, measurable, aligned with industry expectations and job requirements

10. VARIETY: Do NOT repeat sentence structures - vary your approach across bullets

11. QUANTITY: Provide 4-6 bullet points per position (expand if original has fewer, consolidate if original has too many)

12. KEYWORDS: Include relevant keywords from job description NATURALLY within the rewritten content - NO keyword stuffing

13. LEARNING: Extract and incorporate skills/technologies from BOTH job description AND candidate's resume

14. QUALITATIVE ACHIEVEMENTS: Include leadership, problem-solving, innovation when relevant, but ALWAYS pair with quantitative metrics

EXPERIENCE REWRITING EXAMPLES (MANDATORY TRANSFORMATION):

BEFORE: "Worked on software development projects"
AFTER: "Designed and built 3 enterprise applications using Python, React, and PostgreSQL, reducing API processing time by 40%, serving 10,000+ daily active users, and improving system reliability to 99.9% uptime"

BEFORE: "Managed database operations"
AFTER: "Addressed performance bottlenecks by implementing database indexing strategies and query optimization techniques, improving average query response time by 60% (from 2.5s to 1s), reducing server infrastructure costs by $50K annually, and enabling real-time analytics for 5K+ concurrent users"

BEFORE: "Responsible for team coordination"
AFTER: "Led cross-functional team of 8 engineers and 3 product managers, implementing Agile/Scrum methodologies that increased sprint velocity by 35%, reduced production bugs by 28%, and accelerated feature delivery from 4 weeks to 2.5 weeks average"

BEFORE: "Used machine learning for data analysis"
AFTER: "Developed and deployed machine learning models using Python, scikit-learn, and TensorFlow, improving prediction accuracy from 72% to 89%, processing 2M+ data points daily, and enabling automated decision-making that saved 20 hours/week of manual analysis"

⚠️ CRITICAL: Notice how each "AFTER" example:
- Completely rewrites the content (not just adds keywords)
- Includes specific technologies from job description
- Adds multiple quantitative metrics
- Shows clear business impact
- Uses varied, strong action verbs
- Follows Problem → Action → Result structure

CRITICAL FORMATTING REQUIREMENTS - Follow this EXACT structure:

1. HEADER (First Line):
   [Full Name]
   [Job Title/Position]
   Location: [City, State] | Email: [email] | Phone: [phone] | [Links: LinkedIn, GitHub, Portfolio, etc.]

2. SUMMARY Section:
   SUMMARY
   [2-3 sentences summarizing experience and key qualifications relevant to the job]

3. SKILLS Section:
   SKILLS
   [Category 1]: [skill1], [skill2], [skill3]
   [Category 2]: [skill1], [skill2], [skill3]
   [Category 3]: [skill1], [skill2], [skill3]
   
   Common categories: Methodologies, Languages, IDEs, Packages/Libraries, Visualization Tools, Database, Other Skills, Operating System

4. EXPERIENCE Section:
   EXPERIENCE
   [Company Name], [Location] | [Start Date] - [End Date or Current] | [Job Title]
   • [Bullet point describing achievement with metrics if possible]
   • [Bullet point describing achievement with metrics if possible]
   • [Bullet point describing achievement with metrics if possible]
   
   [Next Company], [Location] | [Start Date] - [End Date] | [Job Title]
   • [Bullet point]
   • [Bullet point]


5. EDUCATION Section:
   EDUCATION
   [Degree Name]: [University Name], [Location]
   [Degree Name]: [University Name], [Location]

6. PROJECTS Section (ONLY if original resume has projects):
   PROJECTS
   [Project Name] | [Technologies Used] | [Date or Duration]
   • [Description of project and achievements]
   • [Key features or results]
   
   [Next Project Name] | [Technologies Used] | [Date or Duration]
   • [Description]
   • [Key features or results]

IMPORTANT INSTRUCTIONS:
- Maintain ALL original information - only enhance and optimize, don't remove truthful content
- Use the EXACT section headers: SUMMARY, SKILLS, EXPERIENCE, EDUCATION (all caps)
- Include PROJECTS section ONLY if the original resume has a projects section - do NOT add projects if they don't exist in the original
- For experience entries, use format: "Company, Location | Date Range | Position"
- For projects, use format: "Project Name | Technologies | Date/Duration"
- Use bullet points (•) for experience and project descriptions

⚠️ REMINDER: For EXPERIENCE section bullets, apply the rules specified at the top of this prompt (Problem → Action → Result format, varied action verbs, specific structures, natural tone, no filler phrases, 4-6 bullets, metrics, etc.)

- Reorder experience to highlight most relevant positions first
- Keep formatting clean and professional
- Do NOT add any explanatory text before or after the resume
- Start directly with the header (name)
- Section order: Header → SUMMARY → SKILLS → EXPERIENCE → EDUCATION → PROJECTS (if exists)

Provide ONLY the complete optimized resume in the format above, nothing else."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert resume writer specializing in tailoring resumes to specific job descriptions. 🚨 CRITICAL MANDATORY REQUIREMENT: You MUST completely rewrite every experience bullet point from scratch. DO NOT just add keywords or make minor edits. Each bullet must be transformed with: (1) Specific quantitative metrics (numbers, percentages, time, money, scale), (2) Job-relevant technologies/tools from the job description, (3) Problem → Action → Result structure, (4) Strong, varied action verbs (never repeat verbs), (5) Clear business impact. If original bullet says 'Worked on projects', rewrite to 'Designed and deployed 3 microservices using Python and Docker, reducing API response time by 45% and handling 50K+ requests daily'. Every bullet MUST include at least one measurable metric. Transform vague statements into specific, measurable achievements that directly connect to job requirements. Use natural, business-professional tone - NO generic/AI-style language. Provide 4-6 bullets per position. Maintain truthfulness while making content significantly more compelling and job-relevant."
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=4000
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"


class OpenAIProvider(AIProvider):
    """OpenAI GPT Provider."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.client = None
        self.model = "gpt-4o-mini"  # Cost-effective model
        
        try:
            from openai import OpenAI
            if self.api_key:
                self.client = OpenAI(api_key=self.api_key)
        except ImportError:
            pass
    
    def is_available(self) -> bool:
        return self.client is not None
    
    def analyze_resume(self, resume_text: str, job_description: str) -> Dict:
        if not self.is_available():
            return {"error": "OpenAI API not available. Set OPENAI_API_KEY."}
        
        prompt = f"""You are a resume analyst. Analyze this resume against the job description and provide a strict, accurate match score.

JOB DESCRIPTION:
{job_description}

RESUME:
{resume_text}

SCORING CRITERIA - Evaluate the resume using these specific factors:

1. REQUIRED SKILLS MATCH (50 points - 50% of total score):
   - CRITICAL: This is the most important factor - it accounts for half of the total score
   - Identify ALL required technical skills, tools, technologies, and competencies mentioned in the job description
   - Count how many required skills are present in the resume
   - Score: (skills_found / skills_required) × 50
   - Example: If job requires 10 skills and resume has 6, score = (6/10) × 50 = 30 points
   - Example: If job requires 8 skills and resume has 8, score = (8/8) × 50 = 50 points
   - Be thorough in identifying skills - include programming languages, frameworks, tools, methodologies, soft skills, certifications, etc.

2. EXPERIENCE LEVEL MATCH (20 points):
   - Check if experience level matches (Junior, Mid-level, Senior, Lead, Principal, etc.)
   - Perfect match: 20 points
   - One level off (e.g., Mid applying to Senior): 12 points
   - Two+ levels off (e.g., Junior applying to Senior): 5 points
   - No clear level in resume: 8 points

3. YEARS OF EXPERIENCE (12 points):
   - Compare required years of experience vs. candidate's total experience
   - Meets or exceeds requirement: 12 points
   - Within 1-2 years: 8 points
   - Within 3-4 years: 4 points
   - More than 4 years short: 0 points
   - No requirement specified: 6 points (neutral)

4. JOB TITLE RELEVANCE (10 points):
   - Check if candidate's current/past job titles are relevant to the target role
   - Exact or very similar title: 10 points
   - Related title in same field: 7 points
   - Different field but transferable skills: 3 points
   - Completely unrelated: 0 points

5. EDUCATION REQUIREMENTS (5 points):
   - Check if education level matches (Bachelor's, Master's, PhD, etc.)
   - Meets requirement: 5 points
   - One level below: 3 points
   - Two+ levels below: 0 points
   - No requirement specified: 2.5 points (neutral)

6. INDUSTRY/DOMAIN EXPERIENCE (3 points):
   - Check if candidate has experience in the same or related industry
   - Same industry: 3 points
   - Related industry: 2 points
   - Different industry: 0 points
   - No industry specified in job: 1.5 points (neutral)

TOTAL SCORE CALCULATION:
- Add up all 6 factors (max 100 points)
- Required Skills Match = 50 points (50% of total)
- Other factors = 50 points combined (50% of total)
- Round to nearest whole number
- This is your MATCH_SCORE

SCORING GUIDELINES:
- 0-40%: Missing most required skills, significant experience level mismatch, or major gaps
- 40-70%: Has some required skills and relevant experience, but missing key requirements
- 70-100%: Meets most/all requirements, strong skill match, appropriate experience level

Be STRICT - only give 70+ if the candidate truly meets most requirements.

Provide your analysis in this EXACT format:

MATCH_SCORE: [number 0-100]
STRENGTHS:
- [strength 1]
- [strength 2]

IMPROVEMENTS_NEEDED:
- [improvement 1]
- [improvement 2]

CONTENT_SUGGESTIONS:
1. [Section]: [What to change] - [Why] - [How]
2. [Section]: [What to change] - [Why] - [How]

Start with "MATCH_SCORE:" immediately."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a strict resume analyst. Evaluate resumes using a structured scoring framework: 1. Required Skills Match (50 points - 50% of total) - CRITICAL, count ALL skills found vs required (technical skills, tools, technologies, competencies). 2. Experience Level Match (20 points) - check if levels align. 3. Years of Experience (12 points) - compare required vs actual. 4. Job Title Relevance (10 points) - assess title similarity. 5. Education Requirements (5 points) - check education level match. 6. Industry/Domain Experience (3 points) - evaluate industry alignment. Calculate total (max 100) and round to nearest whole number. Skills match is 50% of score - be thorough in identifying and matching skills. Be STRICT: 0-40% = missing most requirements, 40-70% = some requirements met, 70-100% = most/all requirements met. Always provide score in format: MATCH_SCORE: [number]."
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,  # Lower temperature for more strict scoring
                max_tokens=3000
            )
            return {"raw_analysis": response.choices[0].message.content, "provider": "OpenAI"}
        except Exception as e:
            return {"error": f"OpenAI API error: {str(e)}"}
    
    def optimize_resume(self, resume_text: str, job_description: str, suggestions: List[str]) -> str:
        if not self.is_available():
            return "OpenAI API not available."
        
        prompt = f"""You are an expert resume writer. Create an optimized version of this resume that is specifically tailored to match the job description.

ORIGINAL RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

SUGGESTIONS TO IMPLEMENT:
{chr(10).join(suggestions[:10])}

🚨 CRITICAL MANDATORY REQUIREMENT FOR EXPERIENCE SECTION 🚨
YOU MUST COMPLETELY REWRITE EVERY EXPERIENCE BULLET POINT. DO NOT just add keywords or make minor edits.
EACH BULLET MUST BE TRANSFORMED with actual content improvements, metrics, and job-relevant achievements.

EXPERIENCE SECTION RULES (MANDATORY - APPLY TO EVERY BULLET):
1. MANDATORY REWRITE: You MUST rewrite each bullet point from scratch. DO NOT copy-paste or make minor edits.
   - If original says "Worked on projects" → Rewrite to "Designed and deployed 3 microservices using Python and Docker, reducing API response time by 45% and handling 50K+ requests daily"
   - If original says "Managed team" → Rewrite to "Led cross-functional team of 5 engineers, implementing Agile practices that increased sprint velocity by 30% and reduced bug reports by 25%"
   - Transform vague statements into specific, measurable achievements

2. STRUCTURE (MANDATORY): Every bullet MUST use Problem → Action → Result OR Task → Tools → Impact format
   - Example: "Addressed [specific problem] by implementing [specific solution] using [technologies], resulting in [quantifiable improvement]"
   - Example: "Developed [specific feature/system] using [tools/tech], improving [metric] by [percentage/amount] and [business impact]"

3. ACTION VERBS (MANDATORY): Use strong, varied verbs - DO NOT repeat verbs across bullets
   - Use: Designed, Built, Implemented, Led, Automated, Analyzed, Developed, Optimized, Increased, Reduced, Managed, Created, Deployed, Architected, Streamlined, Accelerated, Transformed, etc.
   - Vary verbs: If first bullet uses "Developed", second should use "Architected" or "Built", not "Developed" again

4. QUANTITATIVE METRICS (MANDATORY): Every bullet MUST include at least ONE measurable metric:
   - Numbers: "3 applications", "50K users", "5 team members"
   - Percentages: "40% faster", "25% reduction", "30% increase"
   - Time: "reduced from 5 hours to 30 minutes", "deployed in 2 weeks"
   - Money: "$50K saved", "revenue increased by $200K"
   - Scale: "serving 1M+ requests", "processing 10TB data daily"
   - If original has no metrics, ADD realistic, job-relevant metrics based on the work described

5. JOB RELEVANCE (MANDATORY): Every bullet MUST connect to job description requirements:
   - Identify key technologies/tools from job description
   - Identify key responsibilities/outcomes from job description
   - Rewrite bullets to demonstrate experience with those technologies/responsibilities
   - Example: If job requires "cloud deployment" and original says "deployed applications", rewrite to "Deployed scalable applications on AWS using EC2, S3, and Lambda, achieving 99.9% uptime and reducing infrastructure costs by 35%"

6. SPECIFIC STRUCTURES (Use when relevant):
   - "Addressed [specific problem] by using [technology/tool] to [specific action], improving [metric] by [%/amount] and [business impact]"
   - "Collaborated with [specific teams/stakeholders] to [specific action], resulting in [quantifiable outcome] and [business value]"
   - "Designed and implemented [specific solution] using [technologies], reducing [metric] by [amount] and enabling [business outcome]"

7. TONE: Natural, business-professional, real resume writing style - NO generic/AI-style language

8. AVOID filler phrases: NO 'leveraged cutting-edge', 'utilized synergistic', 'dynamic environment', 'synergistic solutions', 'passionate about', or vague wording

9. CONTENT: Specific, measurable, aligned with industry expectations and job requirements

10. VARIETY: Do NOT repeat sentence structures - vary your approach across bullets

11. QUANTITY: Provide 4-6 bullet points per position (expand if original has fewer, consolidate if original has too many)

12. KEYWORDS: Include relevant keywords from job description NATURALLY within the rewritten content - NO keyword stuffing

13. LEARNING: Extract and incorporate skills/technologies from BOTH job description AND candidate's resume

14. QUALITATIVE ACHIEVEMENTS: Include leadership, problem-solving, innovation when relevant, but ALWAYS pair with quantitative metrics

EXPERIENCE REWRITING EXAMPLES (MANDATORY TRANSFORMATION):

BEFORE: "Worked on software development projects"
AFTER: "Designed and built 3 enterprise applications using Python, React, and PostgreSQL, reducing API processing time by 40%, serving 10,000+ daily active users, and improving system reliability to 99.9% uptime"

BEFORE: "Managed database operations"
AFTER: "Addressed performance bottlenecks by implementing database indexing strategies and query optimization techniques, improving average query response time by 60% (from 2.5s to 1s), reducing server infrastructure costs by $50K annually, and enabling real-time analytics for 5K+ concurrent users"

BEFORE: "Responsible for team coordination"
AFTER: "Led cross-functional team of 8 engineers and 3 product managers, implementing Agile/Scrum methodologies that increased sprint velocity by 35%, reduced production bugs by 28%, and accelerated feature delivery from 4 weeks to 2.5 weeks average"

BEFORE: "Used machine learning for data analysis"
AFTER: "Developed and deployed machine learning models using Python, scikit-learn, and TensorFlow, improving prediction accuracy from 72% to 89%, processing 2M+ data points daily, and enabling automated decision-making that saved 20 hours/week of manual analysis"

⚠️ CRITICAL: Notice how each "AFTER" example:
- Completely rewrites the content (not just adds keywords)
- Includes specific technologies from job description
- Adds multiple quantitative metrics
- Shows clear business impact
- Uses varied, strong action verbs
- Follows Problem → Action → Result structure

CRITICAL FORMATTING REQUIREMENTS - Follow this EXACT structure:

1. HEADER (First Line):
   [Full Name]
   [Job Title/Position]
   Location: [City, State] | Email: [email] | Phone: [phone] | [Links: LinkedIn, GitHub, Portfolio, etc.]

2. SUMMARY Section:
   SUMMARY
   [2-3 sentences summarizing experience and key qualifications relevant to the job]

3. SKILLS Section:
   SKILLS
   [Category 1]: [skill1], [skill2], [skill3]
   [Category 2]: [skill1], [skill2], [skill3]
   [Category 3]: [skill1], [skill2], [skill3]
   
   Common categories: Methodologies, Languages, IDEs, Packages/Libraries, Visualization Tools, Database, Other Skills, Operating System

4. EXPERIENCE Section:
   EXPERIENCE
   [Company Name], [Location] | [Start Date] - [End Date or Current] | [Job Title]
   • [Bullet point describing achievement with metrics if possible]
   • [Bullet point describing achievement with metrics if possible]
   • [Bullet point describing achievement with metrics if possible]
   
   [Next Company], [Location] | [Start Date] - [End Date] | [Job Title]
   • [Bullet point]
   • [Bullet point]


5. EDUCATION Section:
   EDUCATION
   [Degree Name]: [University Name], [Location]
   [Degree Name]: [University Name], [Location]

6. PROJECTS Section (ONLY if original resume has projects):
   PROJECTS
   [Project Name] | [Technologies Used] | [Date or Duration]
   • [Description of project and achievements]
   • [Key features or results]
   
   [Next Project Name] | [Technologies Used] | [Date or Duration]
   • [Description]
   • [Key features or results]

IMPORTANT INSTRUCTIONS:
- Maintain ALL original information - only enhance and optimize, don't remove truthful content
- Use the EXACT section headers: SUMMARY, SKILLS, EXPERIENCE, EDUCATION (all caps)
- Include PROJECTS section ONLY if the original resume has a projects section - do NOT add projects if they don't exist in the original
- For experience entries, use format: "Company, Location | Date Range | Position"
- For projects, use format: "Project Name | Technologies | Date/Duration"
- Use bullet points (•) for experience and project descriptions

⚠️ REMINDER: For EXPERIENCE section bullets, apply the rules specified at the top of this prompt (Problem → Action → Result format, varied action verbs, specific structures, natural tone, no filler phrases, 4-6 bullets, metrics, etc.)

- Reorder experience to highlight most relevant positions first
- Keep formatting clean and professional
- Do NOT add any explanatory text before or after the resume
- Start directly with the header (name)
- Section order: Header → SUMMARY → SKILLS → EXPERIENCE → EDUCATION → PROJECTS (if exists)

Provide ONLY the complete optimized resume in the format above, nothing else."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert resume writer specializing in tailoring resumes to specific job descriptions. 🚨 CRITICAL MANDATORY REQUIREMENT: You MUST completely rewrite every experience bullet point from scratch. DO NOT just add keywords or make minor edits. Each bullet must be transformed with: (1) Specific quantitative metrics (numbers, percentages, time, money, scale), (2) Job-relevant technologies/tools from the job description, (3) Problem → Action → Result structure, (4) Strong, varied action verbs (never repeat verbs), (5) Clear business impact. If original bullet says 'Worked on projects', rewrite to 'Designed and deployed 3 microservices using Python and Docker, reducing API response time by 45% and handling 50K+ requests daily'. Every bullet MUST include at least one measurable metric. Transform vague statements into specific, measurable achievements that directly connect to job requirements. Use natural, business-professional tone - NO generic/AI-style language. Provide 4-6 bullets per position. Maintain truthfulness while making content significantly more compelling and job-relevant."
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=4000
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"


class ClaudeProvider(AIProvider):
    """Anthropic Claude Provider."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        self.client = None
        self.anthropic = None
        # Try multiple model names - will be determined on first use
        self.model = "claude-3-5-sonnet-20240620"
        
        try:
            from anthropic import Anthropic
            if self.api_key:
                self.anthropic = Anthropic(api_key=self.api_key)
                self.client = self.anthropic  # Store reference
        except ImportError:
            pass
    
    def is_available(self) -> bool:
        return self.client is not None
    
    def analyze_resume(self, resume_text: str, job_description: str) -> Dict:
        if not self.is_available():
            return {"error": "Claude API not available. Set ANTHROPIC_API_KEY."}
        
        prompt = f"""You are a resume analyst. Analyze this resume against the job description and provide a strict, accurate match score.

JOB DESCRIPTION:
{job_description}

RESUME:
{resume_text}

SCORING CRITERIA - Evaluate the resume using these specific factors:

1. REQUIRED SKILLS MATCH (50 points - 50% of total score):
   - CRITICAL: This is the most important factor - it accounts for half of the total score
   - Identify ALL required technical skills, tools, technologies, and competencies mentioned in the job description
   - Count how many required skills are present in the resume
   - Score: (skills_found / skills_required) × 50
   - Example: If job requires 10 skills and resume has 6, score = (6/10) × 50 = 30 points
   - Example: If job requires 8 skills and resume has 8, score = (8/8) × 50 = 50 points
   - Be thorough in identifying skills - include programming languages, frameworks, tools, methodologies, soft skills, certifications, etc.

2. EXPERIENCE LEVEL MATCH (20 points):
   - Check if experience level matches (Junior, Mid-level, Senior, Lead, Principal, etc.)
   - Perfect match: 20 points
   - One level off (e.g., Mid applying to Senior): 12 points
   - Two+ levels off (e.g., Junior applying to Senior): 5 points
   - No clear level in resume: 8 points

3. YEARS OF EXPERIENCE (12 points):
   - Compare required years of experience vs. candidate's total experience
   - Meets or exceeds requirement: 12 points
   - Within 1-2 years: 8 points
   - Within 3-4 years: 4 points
   - More than 4 years short: 0 points
   - No requirement specified: 6 points (neutral)

4. JOB TITLE RELEVANCE (10 points):
   - Check if candidate's current/past job titles are relevant to the target role
   - Exact or very similar title: 10 points
   - Related title in same field: 7 points
   - Different field but transferable skills: 3 points
   - Completely unrelated: 0 points

5. EDUCATION REQUIREMENTS (5 points):
   - Check if education level matches (Bachelor's, Master's, PhD, etc.)
   - Meets requirement: 5 points
   - One level below: 3 points
   - Two+ levels below: 0 points
   - No requirement specified: 2.5 points (neutral)

6. INDUSTRY/DOMAIN EXPERIENCE (3 points):
   - Check if candidate has experience in the same or related industry
   - Same industry: 3 points
   - Related industry: 2 points
   - Different industry: 0 points
   - No industry specified in job: 1.5 points (neutral)

TOTAL SCORE CALCULATION:
- Add up all 6 factors (max 100 points)
- Required Skills Match = 50 points (50% of total)
- Other factors = 50 points combined (50% of total)
- Round to nearest whole number
- This is your MATCH_SCORE

SCORING GUIDELINES:
- 0-40%: Missing most required skills, significant experience level mismatch, or major gaps
- 40-70%: Has some required skills and relevant experience, but missing key requirements
- 70-100%: Meets most/all requirements, strong skill match, appropriate experience level

Be STRICT - only give 70+ if the candidate truly meets most requirements.

Provide your analysis in this EXACT format:

MATCH_SCORE: [number between 0-100 - be strict!]
STRENGTHS:
- [strength 1]
- [strength 2]
- ...

IMPROVEMENTS_NEEDED:
- [specific content change 1]
- [specific content change 2]
- ...

CONTENT_SUGGESTIONS:
1. [Section/Area]: [What to change] - [Why] - [How to improve it]
2. [Section/Area]: [What to change] - [Why] - [How to improve it]
...

Start your response with "MATCH_SCORE:" immediately."""

        try:
            # Try multiple model names in order of preference
            model_names = [
                "claude-3-5-sonnet-20240620",
                "claude-3-5-sonnet",
                "claude-3-opus-20240229",
                "claude-3-sonnet-20240229",
                "claude-3-haiku-20240307"
            ]
            
            for model_name in model_names:
                try:
                    response = self.client.messages.create(
                        model=model_name,
                        max_tokens=3000,
                        temperature=0.2,  # Lower temperature for more strict scoring
                        system="You are a strict resume analyst. Evaluate resumes using a structured scoring framework: 1. Required Skills Match (30 points) - count skills found vs required. 2. Experience Level Match (25 points) - check if levels align. 3. Years of Experience (15 points) - compare required vs actual. 4. Job Title Relevance (15 points) - assess title similarity. 5. Education Requirements (10 points) - check education level match. 6. Industry/Domain Experience (5 points) - evaluate industry alignment. Calculate total (max 100) and round to nearest whole number. Be STRICT: 0-40% = missing most requirements, 40-70% = some requirements met, 70-100% = most/all requirements met. Always provide score in format: MATCH_SCORE: [number].",
                        messages=[
                            {"role": "user", "content": prompt}
                        ]
                    )
                    self.model = model_name  # Save working model
                    return {"raw_analysis": response.content[0].text, "provider": "Claude"}
                except Exception as e:
                    if "not_found" not in str(e).lower() and "404" not in str(e):
                        # If it's not a model not found error, raise it
                        raise e
                    continue
            
            # If all models failed, return error
            return {"error": "Claude API error: No available model found. Please check your API key and model access."}
        except Exception as e:
            return {"error": f"Claude API error: {str(e)}"}
    
    def optimize_resume(self, resume_text: str, job_description: str, suggestions: List[str]) -> str:
        if not self.is_available():
            return "Claude API not available."
        
        prompt = f"""You are an expert resume writer. Create an optimized version of this resume that is specifically tailored to match the job description.

ORIGINAL RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

SUGGESTIONS TO IMPLEMENT:
{chr(10).join(suggestions[:10])}

🚨 CRITICAL MANDATORY REQUIREMENT FOR EXPERIENCE SECTION 🚨
YOU MUST COMPLETELY REWRITE EVERY EXPERIENCE BULLET POINT. DO NOT just add keywords or make minor edits.
EACH BULLET MUST BE TRANSFORMED with actual content improvements, metrics, and job-relevant achievements.

EXPERIENCE SECTION RULES (MANDATORY - APPLY TO EVERY BULLET):
1. MANDATORY REWRITE: You MUST rewrite each bullet point from scratch. DO NOT copy-paste or make minor edits.
   - If original says "Worked on projects" → Rewrite to "Designed and deployed 3 microservices using Python and Docker, reducing API response time by 45% and handling 50K+ requests daily"
   - If original says "Managed team" → Rewrite to "Led cross-functional team of 5 engineers, implementing Agile practices that increased sprint velocity by 30% and reduced bug reports by 25%"
   - Transform vague statements into specific, measurable achievements

2. STRUCTURE (MANDATORY): Every bullet MUST use Problem → Action → Result OR Task → Tools → Impact format
   - Example: "Addressed [specific problem] by implementing [specific solution] using [technologies], resulting in [quantifiable improvement]"
   - Example: "Developed [specific feature/system] using [tools/tech], improving [metric] by [percentage/amount] and [business impact]"

3. ACTION VERBS (MANDATORY): Use strong, varied verbs - DO NOT repeat verbs across bullets
   - Use: Designed, Built, Implemented, Led, Automated, Analyzed, Developed, Optimized, Increased, Reduced, Managed, Created, Deployed, Architected, Streamlined, Accelerated, Transformed, etc.
   - Vary verbs: If first bullet uses "Developed", second should use "Architected" or "Built", not "Developed" again

4. QUANTITATIVE METRICS (MANDATORY): Every bullet MUST include at least ONE measurable metric:
   - Numbers: "3 applications", "50K users", "5 team members"
   - Percentages: "40% faster", "25% reduction", "30% increase"
   - Time: "reduced from 5 hours to 30 minutes", "deployed in 2 weeks"
   - Money: "$50K saved", "revenue increased by $200K"
   - Scale: "serving 1M+ requests", "processing 10TB data daily"
   - If original has no metrics, ADD realistic, job-relevant metrics based on the work described

5. JOB RELEVANCE (MANDATORY): Every bullet MUST connect to job description requirements:
   - Identify key technologies/tools from job description
   - Identify key responsibilities/outcomes from job description
   - Rewrite bullets to demonstrate experience with those technologies/responsibilities
   - Example: If job requires "cloud deployment" and original says "deployed applications", rewrite to "Deployed scalable applications on AWS using EC2, S3, and Lambda, achieving 99.9% uptime and reducing infrastructure costs by 35%"

6. SPECIFIC STRUCTURES (Use when relevant):
   - "Addressed [specific problem] by using [technology/tool] to [specific action], improving [metric] by [%/amount] and [business impact]"
   - "Collaborated with [specific teams/stakeholders] to [specific action], resulting in [quantifiable outcome] and [business value]"
   - "Designed and implemented [specific solution] using [technologies], reducing [metric] by [amount] and enabling [business outcome]"

7. TONE: Natural, business-professional, real resume writing style - NO generic/AI-style language

8. AVOID filler phrases: NO 'leveraged cutting-edge', 'utilized synergistic', 'dynamic environment', 'synergistic solutions', 'passionate about', or vague wording

9. CONTENT: Specific, measurable, aligned with industry expectations and job requirements

10. VARIETY: Do NOT repeat sentence structures - vary your approach across bullets

11. QUANTITY: Provide 4-6 bullet points per position (expand if original has fewer, consolidate if original has too many)

12. KEYWORDS: Include relevant keywords from job description NATURALLY within the rewritten content - NO keyword stuffing

13. LEARNING: Extract and incorporate skills/technologies from BOTH job description AND candidate's resume

14. QUALITATIVE ACHIEVEMENTS: Include leadership, problem-solving, innovation when relevant, but ALWAYS pair with quantitative metrics

EXPERIENCE REWRITING EXAMPLES (MANDATORY TRANSFORMATION):

BEFORE: "Worked on software development projects"
AFTER: "Designed and built 3 enterprise applications using Python, React, and PostgreSQL, reducing API processing time by 40%, serving 10,000+ daily active users, and improving system reliability to 99.9% uptime"

BEFORE: "Managed database operations"
AFTER: "Addressed performance bottlenecks by implementing database indexing strategies and query optimization techniques, improving average query response time by 60% (from 2.5s to 1s), reducing server infrastructure costs by $50K annually, and enabling real-time analytics for 5K+ concurrent users"

BEFORE: "Responsible for team coordination"
AFTER: "Led cross-functional team of 8 engineers and 3 product managers, implementing Agile/Scrum methodologies that increased sprint velocity by 35%, reduced production bugs by 28%, and accelerated feature delivery from 4 weeks to 2.5 weeks average"

BEFORE: "Used machine learning for data analysis"
AFTER: "Developed and deployed machine learning models using Python, scikit-learn, and TensorFlow, improving prediction accuracy from 72% to 89%, processing 2M+ data points daily, and enabling automated decision-making that saved 20 hours/week of manual analysis"

⚠️ CRITICAL: Notice how each "AFTER" example:
- Completely rewrites the content (not just adds keywords)
- Includes specific technologies from job description
- Adds multiple quantitative metrics
- Shows clear business impact
- Uses varied, strong action verbs
- Follows Problem → Action → Result structure

CRITICAL FORMATTING REQUIREMENTS - Follow this EXACT structure:

1. HEADER (First Line):
   [Full Name]
   [Job Title/Position]
   Location: [City, State] | Email: [email] | Phone: [phone] | [Links: LinkedIn, GitHub, Portfolio, etc.]

2. SUMMARY Section:
   SUMMARY
   [2-3 sentences summarizing experience and key qualifications relevant to the job]

3. SKILLS Section:
   SKILLS
   [Category 1]: [skill1], [skill2], [skill3]
   [Category 2]: [skill1], [skill2], [skill3]
   [Category 3]: [skill1], [skill2], [skill3]
   
   Common categories: Methodologies, Languages, IDEs, Packages/Libraries, Visualization Tools, Database, Other Skills, Operating System

4. EXPERIENCE Section:
   EXPERIENCE
   [Company Name], [Location] | [Start Date] - [End Date or Current] | [Job Title]
   • [Bullet point describing achievement with metrics if possible]
   • [Bullet point describing achievement with metrics if possible]
   • [Bullet point describing achievement with metrics if possible]
   
   [Next Company], [Location] | [Start Date] - [End Date] | [Job Title]
   • [Bullet point]
   • [Bullet point]


5. EDUCATION Section:
   EDUCATION
   [Degree Name]: [University Name], [Location]
   [Degree Name]: [University Name], [Location]

6. PROJECTS Section (ONLY if original resume has projects):
   PROJECTS
   [Project Name] | [Technologies Used] | [Date or Duration]
   • [Description of project and achievements]
   • [Key features or results]
   
   [Next Project Name] | [Technologies Used] | [Date or Duration]
   • [Description]
   • [Key features or results]

IMPORTANT INSTRUCTIONS:
- Maintain ALL original information - only enhance and optimize, don't remove truthful content
- Use the EXACT section headers: SUMMARY, SKILLS, EXPERIENCE, EDUCATION (all caps)
- Include PROJECTS section ONLY if the original resume has a projects section - do NOT add projects if they don't exist in the original
- For experience entries, use format: "Company, Location | Date Range | Position"
- For projects, use format: "Project Name | Technologies | Date/Duration"
- Use bullet points (•) for experience and project descriptions

⚠️ REMINDER: For EXPERIENCE section bullets, apply the rules specified at the top of this prompt (Problem → Action → Result format, varied action verbs, specific structures, natural tone, no filler phrases, 4-6 bullets, metrics, etc.)

- Reorder experience to highlight most relevant positions first
- Keep formatting clean and professional
- Do NOT add any explanatory text before or after the resume
- Start directly with the header (name)
- Section order: Header → SUMMARY → SKILLS → EXPERIENCE → EDUCATION → PROJECTS (if exists)

Provide ONLY the complete optimized resume in the format above, nothing else."""

        try:
            # Try multiple model names, use the one that worked before or try all
            model_names = [
                self.model,  # Try the model that worked before
                "claude-3-5-sonnet-20240620",
                "claude-3-5-sonnet",
                "claude-3-opus-20240229",
                "claude-3-sonnet-20240229",
                "claude-3-haiku-20240307"
            ]
            
            system_message = "You are an expert resume writer specializing in tailoring resumes to specific job descriptions. CRITICAL FOR EXPERIENCE SECTION: REWRITE each bullet point using Problem → Action → Result OR Task → Tools → Impact format. Use strong, varied action verbs (Designed, Built, Implemented, Led, Automated, Analyzed, etc.) - DO NOT repeat verbs. Incorporate structures like 'Addressed [problem] by using [technology] to perform [actions], improving [metric] by [%/impact]' and 'Collaborated with [teams] to strengthen [process] and support smoother [workflow]'. Use natural, business-professional tone - NO generic/AI-style language or filler phrases like 'leveraged cutting-edge', 'utilized synergistic', 'dynamic environment'. Make bullets specific, measurable, industry-aligned. Provide 4-6 bullets per position. Include ATS keywords naturally from job description and resume - NO keyword stuffing. Extract and incorporate relevant skills/technologies from both sources. Include quantitative metrics and qualitative achievements when relevant. Maintain truthfulness while making content compelling and job-relevant."
            
            for model_name in model_names:
                try:
                    response = self.client.messages.create(
                        model=model_name,
                        max_tokens=4000,
                        system=system_message,
                        messages=[
                            {"role": "user", "content": prompt}
                        ]
                    )
                    self.model = model_name  # Save working model
                    return response.content[0].text
                except Exception as e:
                    if "not_found" not in str(e).lower() and "404" not in str(e):
                        raise e
                    continue
            
            return "Error: No available Claude model found."
        except Exception as e:
            return f"Error: {str(e)}"


class GeminiProvider(AIProvider):
    """Google Gemini Provider."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        self.client = None
        self.genai = None
        # Use model name without "models/" prefix - try latest stable models first
        self.model = "gemini-2.5-flash"  # Updated to use available model
        
        try:
            import google.generativeai as genai
            if self.api_key:
                genai.configure(api_key=self.api_key)
                self.genai = genai
                # Try multiple model names in order of preference
                model_names = ["gemini-2.5-flash", "gemini-flash-latest", "gemini-2.0-flash", "gemini-pro-latest"]
                for model_name in model_names:
                    try:
                        self.client = genai.GenerativeModel(model_name)
                        self.model = model_name
                        break
                    except:
                        continue
        except ImportError:
            pass
        except Exception as e:
            pass
    
    def is_available(self) -> bool:
        return self.client is not None
    
    def analyze_resume(self, resume_text: str, job_description: str) -> Dict:
        if not self.is_available():
            return {"error": "Gemini API not available. Set GEMINI_API_KEY."}
        
        prompt = f"""You are a resume analyst. Analyze this resume against the job description and provide a strict, accurate match score.

JOB DESCRIPTION:
{job_description}

RESUME:
{resume_text}

SCORING CRITERIA - Evaluate the resume using these specific factors:

1. REQUIRED SKILLS MATCH (50 points - 50% of total score):
   - CRITICAL: This is the most important factor - it accounts for half of the total score
   - Identify ALL required technical skills, tools, technologies, and competencies mentioned in the job description
   - Count how many required skills are present in the resume
   - Score: (skills_found / skills_required) × 50
   - Example: If job requires 10 skills and resume has 6, score = (6/10) × 50 = 30 points
   - Example: If job requires 8 skills and resume has 8, score = (8/8) × 50 = 50 points
   - Be thorough in identifying skills - include programming languages, frameworks, tools, methodologies, soft skills, certifications, etc.

2. EXPERIENCE LEVEL MATCH (20 points):
   - Check if experience level matches (Junior, Mid-level, Senior, Lead, Principal, etc.)
   - Perfect match: 20 points
   - One level off (e.g., Mid applying to Senior): 12 points
   - Two+ levels off (e.g., Junior applying to Senior): 5 points
   - No clear level in resume: 8 points

3. YEARS OF EXPERIENCE (12 points):
   - Compare required years of experience vs. candidate's total experience
   - Meets or exceeds requirement: 12 points
   - Within 1-2 years: 8 points
   - Within 3-4 years: 4 points
   - More than 4 years short: 0 points
   - No requirement specified: 6 points (neutral)

4. JOB TITLE RELEVANCE (10 points):
   - Check if candidate's current/past job titles are relevant to the target role
   - Exact or very similar title: 10 points
   - Related title in same field: 7 points
   - Different field but transferable skills: 3 points
   - Completely unrelated: 0 points

5. EDUCATION REQUIREMENTS (5 points):
   - Check if education level matches (Bachelor's, Master's, PhD, etc.)
   - Meets requirement: 5 points
   - One level below: 3 points
   - Two+ levels below: 0 points
   - No requirement specified: 2.5 points (neutral)

6. INDUSTRY/DOMAIN EXPERIENCE (3 points):
   - Check if candidate has experience in the same or related industry
   - Same industry: 3 points
   - Related industry: 2 points
   - Different industry: 0 points
   - No industry specified in job: 1.5 points (neutral)

TOTAL SCORE CALCULATION:
- Add up all 6 factors (max 100 points)
- Required Skills Match = 50 points (50% of total)
- Other factors = 50 points combined (50% of total)
- Round to nearest whole number
- This is your MATCH_SCORE

SCORING GUIDELINES:
- 0-40%: Missing most required skills, significant experience level mismatch, or major gaps
- 40-70%: Has some required skills and relevant experience, but missing key requirements
- 70-100%: Meets most/all requirements, strong skill match, appropriate experience level

Be STRICT - only give 70+ if the candidate truly meets most requirements.

Provide your analysis in this EXACT format:

MATCH_SCORE: [number between 0-100 - be strict!]
STRENGTHS:
- [strength 1]
- [strength 2]
- ...

IMPROVEMENTS_NEEDED:
- [specific content change 1]
- [specific content change 2]
- ...

CONTENT_SUGGESTIONS:
1. [Section/Area]: [What to change] - [Why] - [How to improve it]
2. [Section/Area]: [What to change] - [Why] - [How to improve it]
...

Start your response with "MATCH_SCORE:" immediately."""

        try:
            # Try with current model, fallback to other models if needed
            try:
                # Use generation config for stricter scoring
                generation_config = {
                    "temperature": 0.2,  # Lower temperature for more strict scoring
                    "top_p": 0.8,
                    "top_k": 40,
                }
                response = self.client.generate_content(
                    prompt,
                    generation_config=generation_config
                )
                return {"raw_analysis": response.text, "provider": "Gemini"}
            except Exception as e:
                # If model not found, try fallback models
                if "not found" in str(e).lower() or "404" in str(e):
                    if self.genai:
                        fallback_models = ["gemini-flash-latest", "gemini-2.0-flash", "gemini-pro-latest"]
                        for model_name in fallback_models:
                            try:
                                fallback_model = self.genai.GenerativeModel(model_name)
                                generation_config = {
                                    "temperature": 0.2,
                                    "top_p": 0.8,
                                    "top_k": 40,
                                }
                                response = fallback_model.generate_content(
                                    prompt,
                                    generation_config=generation_config
                                )
                                self.model = model_name
                                self.client = fallback_model
                                return {"raw_analysis": response.text, "provider": "Gemini"}
                            except:
                                continue
                raise e
        except Exception as e:
            return {"error": f"Gemini API error: {str(e)}"}
    
    def optimize_resume(self, resume_text: str, job_description: str, suggestions: List[str]) -> str:
        if not self.is_available():
            return "Gemini API not available."
        
        prompt = f"""You are an expert resume writer. Create an optimized version of this resume that is specifically tailored to match the job description.

ORIGINAL RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

SUGGESTIONS TO IMPLEMENT:
{chr(10).join(suggestions[:10])}

🚨 CRITICAL MANDATORY REQUIREMENT FOR EXPERIENCE SECTION 🚨
YOU MUST COMPLETELY REWRITE EVERY EXPERIENCE BULLET POINT. DO NOT just add keywords or make minor edits.
EACH BULLET MUST BE TRANSFORMED with actual content improvements, metrics, and job-relevant achievements.

EXPERIENCE SECTION RULES (MANDATORY - APPLY TO EVERY BULLET):
1. MANDATORY REWRITE: You MUST rewrite each bullet point from scratch. DO NOT copy-paste or make minor edits.
   - If original says "Worked on projects" → Rewrite to "Designed and deployed 3 microservices using Python and Docker, reducing API response time by 45% and handling 50K+ requests daily"
   - If original says "Managed team" → Rewrite to "Led cross-functional team of 5 engineers, implementing Agile practices that increased sprint velocity by 30% and reduced bug reports by 25%"
   - Transform vague statements into specific, measurable achievements

2. STRUCTURE (MANDATORY): Every bullet MUST use Problem → Action → Result OR Task → Tools → Impact format
   - Example: "Addressed [specific problem] by implementing [specific solution] using [technologies], resulting in [quantifiable improvement]"
   - Example: "Developed [specific feature/system] using [tools/tech], improving [metric] by [percentage/amount] and [business impact]"

3. ACTION VERBS (MANDATORY): Use strong, varied verbs - DO NOT repeat verbs across bullets
   - Use: Designed, Built, Implemented, Led, Automated, Analyzed, Developed, Optimized, Increased, Reduced, Managed, Created, Deployed, Architected, Streamlined, Accelerated, Transformed, etc.
   - Vary verbs: If first bullet uses "Developed", second should use "Architected" or "Built", not "Developed" again

4. QUANTITATIVE METRICS (MANDATORY): Every bullet MUST include at least ONE measurable metric:
   - Numbers: "3 applications", "50K users", "5 team members"
   - Percentages: "40% faster", "25% reduction", "30% increase"
   - Time: "reduced from 5 hours to 30 minutes", "deployed in 2 weeks"
   - Money: "$50K saved", "revenue increased by $200K"
   - Scale: "serving 1M+ requests", "processing 10TB data daily"
   - If original has no metrics, ADD realistic, job-relevant metrics based on the work described

5. JOB RELEVANCE (MANDATORY): Every bullet MUST connect to job description requirements:
   - Identify key technologies/tools from job description
   - Identify key responsibilities/outcomes from job description
   - Rewrite bullets to demonstrate experience with those technologies/responsibilities
   - Example: If job requires "cloud deployment" and original says "deployed applications", rewrite to "Deployed scalable applications on AWS using EC2, S3, and Lambda, achieving 99.9% uptime and reducing infrastructure costs by 35%"

6. SPECIFIC STRUCTURES (Use when relevant):
   - "Addressed [specific problem] by using [technology/tool] to [specific action], improving [metric] by [%/amount] and [business impact]"
   - "Collaborated with [specific teams/stakeholders] to [specific action], resulting in [quantifiable outcome] and [business value]"
   - "Designed and implemented [specific solution] using [technologies], reducing [metric] by [amount] and enabling [business outcome]"

7. TONE: Natural, business-professional, real resume writing style - NO generic/AI-style language

8. AVOID filler phrases: NO 'leveraged cutting-edge', 'utilized synergistic', 'dynamic environment', 'synergistic solutions', 'passionate about', or vague wording

9. CONTENT: Specific, measurable, aligned with industry expectations and job requirements

10. VARIETY: Do NOT repeat sentence structures - vary your approach across bullets

11. QUANTITY: Provide 4-6 bullet points per position (expand if original has fewer, consolidate if original has too many)

12. KEYWORDS: Include relevant keywords from job description NATURALLY within the rewritten content - NO keyword stuffing

13. LEARNING: Extract and incorporate skills/technologies from BOTH job description AND candidate's resume

14. QUALITATIVE ACHIEVEMENTS: Include leadership, problem-solving, innovation when relevant, but ALWAYS pair with quantitative metrics

EXPERIENCE REWRITING EXAMPLES (MANDATORY TRANSFORMATION):

BEFORE: "Worked on software development projects"
AFTER: "Designed and built 3 enterprise applications using Python, React, and PostgreSQL, reducing API processing time by 40%, serving 10,000+ daily active users, and improving system reliability to 99.9% uptime"

BEFORE: "Managed database operations"
AFTER: "Addressed performance bottlenecks by implementing database indexing strategies and query optimization techniques, improving average query response time by 60% (from 2.5s to 1s), reducing server infrastructure costs by $50K annually, and enabling real-time analytics for 5K+ concurrent users"

BEFORE: "Responsible for team coordination"
AFTER: "Led cross-functional team of 8 engineers and 3 product managers, implementing Agile/Scrum methodologies that increased sprint velocity by 35%, reduced production bugs by 28%, and accelerated feature delivery from 4 weeks to 2.5 weeks average"

BEFORE: "Used machine learning for data analysis"
AFTER: "Developed and deployed machine learning models using Python, scikit-learn, and TensorFlow, improving prediction accuracy from 72% to 89%, processing 2M+ data points daily, and enabling automated decision-making that saved 20 hours/week of manual analysis"

⚠️ CRITICAL: Notice how each "AFTER" example:
- Completely rewrites the content (not just adds keywords)
- Includes specific technologies from job description
- Adds multiple quantitative metrics
- Shows clear business impact
- Uses varied, strong action verbs
- Follows Problem → Action → Result structure

CRITICAL FORMATTING REQUIREMENTS - Follow this EXACT structure:

1. HEADER (First Line):
   [Full Name]
   [Job Title/Position]
   Location: [City, State] | Email: [email] | Phone: [phone] | [Links: LinkedIn, GitHub, Portfolio, etc.]

2. SUMMARY Section:
   SUMMARY
   [2-3 sentences summarizing experience and key qualifications relevant to the job]

3. SKILLS Section:
   SKILLS
   [Category 1]: [skill1], [skill2], [skill3]
   [Category 2]: [skill1], [skill2], [skill3]
   [Category 3]: [skill1], [skill2], [skill3]
   
   Common categories: Methodologies, Languages, IDEs, Packages/Libraries, Visualization Tools, Database, Other Skills, Operating System

4. EXPERIENCE Section:
   EXPERIENCE
   [Company Name], [Location] | [Start Date] - [End Date or Current] | [Job Title]
   • [Bullet point describing achievement with metrics if possible]
   • [Bullet point describing achievement with metrics if possible]
   • [Bullet point describing achievement with metrics if possible]
   
   [Next Company], [Location] | [Start Date] - [End Date] | [Job Title]
   • [Bullet point]
   • [Bullet point]


5. EDUCATION Section:
   EDUCATION
   [Degree Name]: [University Name], [Location]
   [Degree Name]: [University Name], [Location]

6. PROJECTS Section (ONLY if original resume has projects):
   PROJECTS
   [Project Name] | [Technologies Used] | [Date or Duration]
   • [Description of project and achievements]
   • [Key features or results]
   
   [Next Project Name] | [Technologies Used] | [Date or Duration]
   • [Description]
   • [Key features or results]

IMPORTANT INSTRUCTIONS:
- Maintain ALL original information - only enhance and optimize, don't remove truthful content
- Use the EXACT section headers: SUMMARY, SKILLS, EXPERIENCE, EDUCATION (all caps)
- Include PROJECTS section ONLY if the original resume has a projects section - do NOT add projects if they don't exist in the original
- For experience entries, use format: "Company, Location | Date Range | Position"
- For projects, use format: "Project Name | Technologies | Date/Duration"
- Use bullet points (•) for experience and project descriptions

⚠️ REMINDER: For EXPERIENCE section bullets, apply the rules specified at the top of this prompt (Problem → Action → Result format, varied action verbs, specific structures, natural tone, no filler phrases, 4-6 bullets, metrics, etc.)

- Reorder experience to highlight most relevant positions first
- Keep formatting clean and professional
- Do NOT add any explanatory text before or after the resume
- Start directly with the header (name)
- Section order: Header → SUMMARY → SKILLS → EXPERIENCE → EDUCATION → PROJECTS (if exists)

Provide ONLY the complete optimized resume in the format above, nothing else."""

        try:
            # Try with current model, fallback to other models if needed
            try:
                response = self.client.generate_content(prompt)
                return response.text
            except Exception as e:
                # If model not found, try fallback models
                if "not found" in str(e).lower() or "404" in str(e):
                    if self.genai:
                        fallback_models = ["gemini-flash-latest", "gemini-2.0-flash", "gemini-pro-latest"]
                        for model_name in fallback_models:
                            try:
                                fallback_model = self.genai.GenerativeModel(model_name)
                                response = fallback_model.generate_content(prompt)
                                self.model = model_name
                                self.client = fallback_model
                                return response.text
                            except:
                                continue
                raise e
        except Exception as e:
            return f"Error: {str(e)}"


class CohereProvider(AIProvider):
    """Cohere AI Provider."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('COHERE_API_KEY')
        self.client = None
        self.model = "command-r-plus"
        
        try:
            import cohere
            if self.api_key:
                self.client = cohere.Client(api_key=self.api_key)
        except ImportError:
            pass
    
    def is_available(self) -> bool:
        return self.client is not None
    
    def analyze_resume(self, resume_text: str, job_description: str) -> Dict:
        if not self.is_available():
            return {"error": "Cohere API not available. Set COHERE_API_KEY."}
        
        prompt = f"""You are a resume analyst. Analyze this resume against the job description and provide a strict, accurate match score.

JOB DESCRIPTION:
{job_description}

RESUME:
{resume_text}

SCORING CRITERIA - Evaluate the resume using these specific factors:

1. REQUIRED SKILLS MATCH (50 points - 50% of total score):
   - CRITICAL: This is the most important factor - it accounts for half of the total score
   - Identify ALL required technical skills, tools, technologies, and competencies mentioned in the job description
   - Count how many required skills are present in the resume
   - Score: (skills_found / skills_required) × 50
   - Example: If job requires 10 skills and resume has 6, score = (6/10) × 50 = 30 points
   - Example: If job requires 8 skills and resume has 8, score = (8/8) × 50 = 50 points
   - Be thorough in identifying skills - include programming languages, frameworks, tools, methodologies, soft skills, certifications, etc.

2. EXPERIENCE LEVEL MATCH (20 points):
   - Check if experience level matches (Junior, Mid-level, Senior, Lead, Principal, etc.)
   - Perfect match: 20 points
   - One level off (e.g., Mid applying to Senior): 12 points
   - Two+ levels off (e.g., Junior applying to Senior): 5 points
   - No clear level in resume: 8 points

3. YEARS OF EXPERIENCE (12 points):
   - Compare required years of experience vs. candidate's total experience
   - Meets or exceeds requirement: 12 points
   - Within 1-2 years: 8 points
   - Within 3-4 years: 4 points
   - More than 4 years short: 0 points
   - No requirement specified: 6 points (neutral)

4. JOB TITLE RELEVANCE (10 points):
   - Check if candidate's current/past job titles are relevant to the target role
   - Exact or very similar title: 10 points
   - Related title in same field: 7 points
   - Different field but transferable skills: 3 points
   - Completely unrelated: 0 points

5. EDUCATION REQUIREMENTS (5 points):
   - Check if education level matches (Bachelor's, Master's, PhD, etc.)
   - Meets requirement: 5 points
   - One level below: 3 points
   - Two+ levels below: 0 points
   - No requirement specified: 2.5 points (neutral)

6. INDUSTRY/DOMAIN EXPERIENCE (3 points):
   - Check if candidate has experience in the same or related industry
   - Same industry: 3 points
   - Related industry: 2 points
   - Different industry: 0 points
   - No industry specified in job: 1.5 points (neutral)

TOTAL SCORE CALCULATION:
- Add up all 6 factors (max 100 points)
- Required Skills Match = 50 points (50% of total)
- Other factors = 50 points combined (50% of total)
- Round to nearest whole number
- This is your MATCH_SCORE

SCORING GUIDELINES:
- 0-40%: Missing most required skills, significant experience level mismatch, or major gaps
- 40-70%: Has some required skills and relevant experience, but missing key requirements
- 70-100%: Meets most/all requirements, strong skill match, appropriate experience level

Be STRICT - only give 70+ if the candidate truly meets most requirements.

Provide your analysis in this EXACT format:

MATCH_SCORE: [number between 0-100 - be strict!]
STRENGTHS:
- [strength 1]
- [strength 2]
- ...

IMPROVEMENTS_NEEDED:
- [specific content change 1]
- [specific content change 2]
- ...

CONTENT_SUGGESTIONS:
1. [Section/Area]: [What to change] - [Why] - [How to improve it]
2. [Section/Area]: [What to change] - [Why] - [How to improve it]
...

Start your response with "MATCH_SCORE:" immediately."""

        try:
            response = self.client.chat(
                model=self.model,
                message=prompt,
                temperature=0.2,  # Lower temperature for more strict scoring
                max_tokens=3000
            )
            return {"raw_analysis": response.text, "provider": "Cohere"}
        except Exception as e:
            return {"error": f"Cohere API error: {str(e)}"}
    
    def optimize_resume(self, resume_text: str, job_description: str, suggestions: List[str]) -> str:
        if not self.is_available():
            return "Cohere API not available."
        
        prompt = f"""You are an expert resume writer. Create an optimized version of this resume that is specifically tailored to match the job description.

ORIGINAL RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

SUGGESTIONS TO IMPLEMENT:
{chr(10).join(suggestions[:10])}

🚨 CRITICAL MANDATORY REQUIREMENT FOR EXPERIENCE SECTION 🚨
YOU MUST COMPLETELY REWRITE EVERY EXPERIENCE BULLET POINT. DO NOT just add keywords or make minor edits.
EACH BULLET MUST BE TRANSFORMED with actual content improvements, metrics, and job-relevant achievements.

EXPERIENCE SECTION RULES (MANDATORY - APPLY TO EVERY BULLET):
1. MANDATORY REWRITE: You MUST rewrite each bullet point from scratch. DO NOT copy-paste or make minor edits.
   - If original says "Worked on projects" → Rewrite to "Designed and deployed 3 microservices using Python and Docker, reducing API response time by 45% and handling 50K+ requests daily"
   - If original says "Managed team" → Rewrite to "Led cross-functional team of 5 engineers, implementing Agile practices that increased sprint velocity by 30% and reduced bug reports by 25%"
   - Transform vague statements into specific, measurable achievements

2. STRUCTURE (MANDATORY): Every bullet MUST use Problem → Action → Result OR Task → Tools → Impact format
   - Example: "Addressed [specific problem] by implementing [specific solution] using [technologies], resulting in [quantifiable improvement]"
   - Example: "Developed [specific feature/system] using [tools/tech], improving [metric] by [percentage/amount] and [business impact]"

3. ACTION VERBS (MANDATORY): Use strong, varied verbs - DO NOT repeat verbs across bullets
   - Use: Designed, Built, Implemented, Led, Automated, Analyzed, Developed, Optimized, Increased, Reduced, Managed, Created, Deployed, Architected, Streamlined, Accelerated, Transformed, etc.
   - Vary verbs: If first bullet uses "Developed", second should use "Architected" or "Built", not "Developed" again

4. QUANTITATIVE METRICS (MANDATORY): Every bullet MUST include at least ONE measurable metric:
   - Numbers: "3 applications", "50K users", "5 team members"
   - Percentages: "40% faster", "25% reduction", "30% increase"
   - Time: "reduced from 5 hours to 30 minutes", "deployed in 2 weeks"
   - Money: "$50K saved", "revenue increased by $200K"
   - Scale: "serving 1M+ requests", "processing 10TB data daily"
   - If original has no metrics, ADD realistic, job-relevant metrics based on the work described

5. JOB RELEVANCE (MANDATORY): Every bullet MUST connect to job description requirements:
   - Identify key technologies/tools from job description
   - Identify key responsibilities/outcomes from job description
   - Rewrite bullets to demonstrate experience with those technologies/responsibilities
   - Example: If job requires "cloud deployment" and original says "deployed applications", rewrite to "Deployed scalable applications on AWS using EC2, S3, and Lambda, achieving 99.9% uptime and reducing infrastructure costs by 35%"

6. SPECIFIC STRUCTURES (Use when relevant):
   - "Addressed [specific problem] by using [technology/tool] to [specific action], improving [metric] by [%/amount] and [business impact]"
   - "Collaborated with [specific teams/stakeholders] to [specific action], resulting in [quantifiable outcome] and [business value]"
   - "Designed and implemented [specific solution] using [technologies], reducing [metric] by [amount] and enabling [business outcome]"

7. TONE: Natural, business-professional, real resume writing style - NO generic/AI-style language

8. AVOID filler phrases: NO 'leveraged cutting-edge', 'utilized synergistic', 'dynamic environment', 'synergistic solutions', 'passionate about', or vague wording

9. CONTENT: Specific, measurable, aligned with industry expectations and job requirements

10. VARIETY: Do NOT repeat sentence structures - vary your approach across bullets

11. QUANTITY: Provide 4-6 bullet points per position (expand if original has fewer, consolidate if original has too many)

12. KEYWORDS: Include relevant keywords from job description NATURALLY within the rewritten content - NO keyword stuffing

13. LEARNING: Extract and incorporate skills/technologies from BOTH job description AND candidate's resume

14. QUALITATIVE ACHIEVEMENTS: Include leadership, problem-solving, innovation when relevant, but ALWAYS pair with quantitative metrics

EXPERIENCE REWRITING EXAMPLES (MANDATORY TRANSFORMATION):

BEFORE: "Worked on software development projects"
AFTER: "Designed and built 3 enterprise applications using Python, React, and PostgreSQL, reducing API processing time by 40%, serving 10,000+ daily active users, and improving system reliability to 99.9% uptime"

BEFORE: "Managed database operations"
AFTER: "Addressed performance bottlenecks by implementing database indexing strategies and query optimization techniques, improving average query response time by 60% (from 2.5s to 1s), reducing server infrastructure costs by $50K annually, and enabling real-time analytics for 5K+ concurrent users"

BEFORE: "Responsible for team coordination"
AFTER: "Led cross-functional team of 8 engineers and 3 product managers, implementing Agile/Scrum methodologies that increased sprint velocity by 35%, reduced production bugs by 28%, and accelerated feature delivery from 4 weeks to 2.5 weeks average"

BEFORE: "Used machine learning for data analysis"
AFTER: "Developed and deployed machine learning models using Python, scikit-learn, and TensorFlow, improving prediction accuracy from 72% to 89%, processing 2M+ data points daily, and enabling automated decision-making that saved 20 hours/week of manual analysis"

⚠️ CRITICAL: Notice how each "AFTER" example:
- Completely rewrites the content (not just adds keywords)
- Includes specific technologies from job description
- Adds multiple quantitative metrics
- Shows clear business impact
- Uses varied, strong action verbs
- Follows Problem → Action → Result structure

CRITICAL FORMATTING REQUIREMENTS - Follow this EXACT structure:

1. HEADER (First Line):
   [Full Name]
   [Job Title/Position]
   Location: [City, State] | Email: [email] | Phone: [phone] | [Links: LinkedIn, GitHub, Portfolio, etc.]

2. SUMMARY Section:
   SUMMARY
   [2-3 sentences summarizing experience and key qualifications relevant to the job]

3. SKILLS Section:
   SKILLS
   [Category 1]: [skill1], [skill2], [skill3]
   [Category 2]: [skill1], [skill2], [skill3]
   [Category 3]: [skill1], [skill2], [skill3]
   
   Common categories: Methodologies, Languages, IDEs, Packages/Libraries, Visualization Tools, Database, Other Skills, Operating System

4. EXPERIENCE Section:
   EXPERIENCE
   [Company Name], [Location] | [Start Date] - [End Date or Current] | [Job Title]
   • [Bullet point describing achievement with metrics if possible]
   • [Bullet point describing achievement with metrics if possible]
   • [Bullet point describing achievement with metrics if possible]
   
   [Next Company], [Location] | [Start Date] - [End Date] | [Job Title]
   • [Bullet point]
   • [Bullet point]


5. EDUCATION Section:
   EDUCATION
   [Degree Name]: [University Name], [Location]
   [Degree Name]: [University Name], [Location]

6. PROJECTS Section (ONLY if original resume has projects):
   PROJECTS
   [Project Name] | [Technologies Used] | [Date or Duration]
   • [Description of project and achievements]
   • [Key features or results]
   
   [Next Project Name] | [Technologies Used] | [Date or Duration]
   • [Description]
   • [Key features or results]

IMPORTANT INSTRUCTIONS:
- Maintain ALL original information - only enhance and optimize, don't remove truthful content
- Use the EXACT section headers: SUMMARY, SKILLS, EXPERIENCE, EDUCATION (all caps)
- Include PROJECTS section ONLY if the original resume has a projects section - do NOT add projects if they don't exist in the original
- For experience entries, use format: "Company, Location | Date Range | Position"
- For projects, use format: "Project Name | Technologies | Date/Duration"
- Use bullet points (•) for experience and project descriptions

⚠️ REMINDER: For EXPERIENCE section bullets, apply the rules specified at the top of this prompt (Problem → Action → Result format, varied action verbs, specific structures, natural tone, no filler phrases, 4-6 bullets, metrics, etc.)

- Reorder experience to highlight most relevant positions first
- Keep formatting clean and professional
- Do NOT add any explanatory text before or after the resume
- Start directly with the header (name)
- Section order: Header → SUMMARY → SKILLS → EXPERIENCE → EDUCATION → PROJECTS (if exists)

Provide ONLY the complete optimized resume in the format above, nothing else."""

        try:
            response = self.client.chat(
                model=self.model,
                message=prompt,
                temperature=0.7,
                max_tokens=4000
            )
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"


def get_ai_provider(provider_name: str, api_key: Optional[str] = None) -> Optional[AIProvider]:
    """Get AI provider by name."""
    providers = {
        "groq": GroqProvider,
        "openai": OpenAIProvider,
        "claude": ClaudeProvider,
        "gemini": GeminiProvider,
        "cohere": CohereProvider,
    }
    
    provider_class = providers.get(provider_name.lower())
    if provider_class:
        return provider_class(api_key)
    return None


def get_available_providers() -> Dict[str, bool]:
    """Get list of available providers."""
    return {
        "groq": GroqProvider().is_available(),
        "openai": OpenAIProvider().is_available(),
        "claude": ClaudeProvider().is_available(),
        "gemini": GeminiProvider().is_available(),
        "cohere": CohereProvider().is_available(),
    }


def get_provider_info() -> List[Dict]:
    """Get provider information for UI."""
    return [
        {
            "id": "groq",
            "name": "Groq (Llama 3.3)",
            "description": "Fast & Cost-effective",
            "available": GroqProvider().is_available(),
            "api_key_env": "GROQ_API_KEY"
        },
        {
            "id": "openai",
            "name": "OpenAI (GPT-4o Mini)",
            "description": "High Quality",
            "available": OpenAIProvider().is_available(),
            "api_key_env": "OPENAI_API_KEY"
        },
        {
            "id": "claude",
            "name": "Claude (3.5 Sonnet)",
            "description": "Advanced Reasoning",
            "available": ClaudeProvider().is_available(),
            "api_key_env": "ANTHROPIC_API_KEY"
        },
        {
            "id": "gemini",
            "name": "Google Gemini (2.5 Flash)",
            "description": "Fast & Multimodal AI",
            "available": GeminiProvider().is_available(),
            "api_key_env": "GEMINI_API_KEY"
        },
        {
            "id": "cohere",
            "name": "Cohere (Command R+)",
            "description": "Enterprise AI",
            "available": CohereProvider().is_available(),
            "api_key_env": "COHERE_API_KEY"
        },
    ]

