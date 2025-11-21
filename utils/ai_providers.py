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
    def optimize_resume(self, resume_text: str, job_description: str, suggestions: List[str], social_links: Optional[Dict] = None) -> str:
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
    
    def optimize_resume(self, resume_text: str, job_description: str, suggestions: List[str], social_links: Optional[Dict] = None) -> str:
        if not self.is_available():
            return "Groq API not available."
        
        # Prepare social links information for the prompt
        social_links_info = ""
        if social_links:
            if social_links.get('linkedin'):
                social_links_info += f"\nLinkedIn URL from original resume: {social_links['linkedin']}"
            if social_links.get('github'):
                social_links_info += f"\nGitHub URL from original resume: {social_links['github']}"
        
        prompt = f"""You are an expert resume writer. Create an optimized version of this resume that is specifically tailored to match the job description.

ORIGINAL RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

SUGGESTIONS TO IMPLEMENT:
{chr(10).join(suggestions[:10])}
{social_links_info}

CRITICAL: If the original resume contains LinkedIn or GitHub links, you MUST preserve them in the header contact line with their full URLs.

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

4. QUANTITATIVE METRICS (BALANCED APPROACH):
   - AIM for metrics in ~50-60% of bullet points, NOT every single one.
   - QUALITY OVER QUANTITY: Only use metrics where they feel natural and credible.
   - Avoid "data stuffing" (e.g., don't force a % into a task where it doesn't belong).
   - Good metrics: "Reduced latency by 40%", "Managed $50k budget", "Led team of 5"
   - Bad metrics: "Wrote 100% of code", "Attended 5 meetings", "Used 3 keyboards"
   - If a metric feels forced, focus on the QUALITATIVE impact instead (e.g., "Enabled new capabilities," "Solved critical bug").

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

12. BALANCE (CRITICAL): Maintain a natural balance between quantifiable and technical points:
    - ~50% QUANTIFIABLE: Focus on metrics, numbers, percentages, measurable results (where natural)
    - ~50% TECHNICAL/QUALITATIVE: Focus on technical skills, architectures, complex problem solving (without forced numbers)
    - Example of quantifiable: "Designed and deployed 3 microservices using Python and Docker, reducing API response time by 45%"
    - Example of technical/qualitative: "Architected microservices infrastructure using Docker and Kubernetes, implementing service mesh patterns for improved scalability"
    - DO NOT include soft skills (leadership, collaboration) unless tied to a specific technical outcome.

13. KEYWORDS: Include relevant keywords from job description NATURALLY within the rewritten content - NO keyword stuffing

14. LEARNING: Extract and incorporate skills/technologies from BOTH job description AND candidate's resume

15. TECHNICAL NON-QUANTIFIABLE BULLETS: For the 50% technical bullets (without metrics), focus on:
    - Technical implementations and architectures (microservices, APIs, data pipelines, etc.)
    - Technologies and tools from job description (Docker, Kubernetes, AWS services, frameworks, etc.)
    - Technical patterns and best practices (RESTful design, event-driven architecture, etc.)
    - System design and technical solutions
    - Integration with specific technologies or platforms
    - DO NOT include soft skills, leadership, collaboration, or strategic thinking
    - These bullets should demonstrate technical depth and job-relevant technical expertise

EXPERIENCE REWRITING EXAMPLES (MANDATORY TRANSFORMATION):

BEFORE: "Worked on software development projects"
AFTER: "Designed and built 3 enterprise applications using Python, React, and PostgreSQL, reducing API processing time by 40%, serving 10,000+ daily active users, and improving system reliability to 99.9% uptime"

BEFORE: "Managed database operations"
AFTER: "Addressed performance bottlenecks by implementing database indexing strategies and query optimization techniques, improving average query response time by 60% (from 2.5s to 1s), reducing server infrastructure costs by $50K annually, and enabling real-time analytics for 5K+ concurrent users"

BEFORE: "Responsible for team coordination"
AFTER: "Led cross-functional team of 8 engineers and 3 product managers, implementing Agile/Scrum methodologies that increased sprint velocity by 35%, reduced production bugs by 28%, and accelerated feature delivery from 4 weeks to 2.5 weeks average"

BEFORE: "Used machine learning for data analysis"
AFTER: "Developed and deployed machine learning models using Python, scikit-learn, and TensorFlow, improving prediction accuracy from 72% to 89%, processing 2M+ data points daily, and enabling automated decision-making that saved 20 hours/week of manual analysis"

BEFORE: "Worked on backend systems"
AFTER (TECHNICAL NON-QUANTIFIABLE - 50%): "Architected microservices infrastructure using Docker, Kubernetes, and AWS ECS, implementing service mesh patterns with Istio and container orchestration best practices for scalable distributed systems"

BEFORE: "Developed APIs"
AFTER (TECHNICAL NON-QUANTIFIABLE - 50%): "Designed and implemented RESTful APIs following OpenAPI 3.0 specifications, integrating OAuth 2.0 authentication, JWT token management, and rate limiting middleware for secure and scalable API architecture"

⚠️ CRITICAL: Notice how each "AFTER" example:
- Completely rewrites the content (not just adds keywords)
- Includes specific technologies from job description (for quantifiable bullets)
- Adds multiple quantitative metrics (for 70% of bullets)
- Shows clear business impact (for 50% quantifiable bullets) or demonstrates technical depth and job-relevant technologies (for 50% technical bullets)
- Uses varied, strong action verbs
- Follows Problem → Action → Result structure
- Maintains 50/50 balance: Half the bullets are quantifiable with metrics, half focus on technical implementations and technologies without metrics

CRITICAL FORMATTING REQUIREMENTS - Follow this EXACT structure:

1. HEADER (First Line):
   [Full Name]
   [Job Title/Position]
   Location: [City, State] | Email: [email] | Phone: [phone] | LinkedIn: [linkedin_url] | GitHub: [github_url]
   
   IMPORTANT: If the original resume contains LinkedIn or GitHub links, you MUST include them in the contact line with their full URLs.
   - Extract the actual URLs from the original resume (they are provided above if found)
   - Format: "LinkedIn: https://linkedin.com/in/username" or "GitHub: https://github.com/username"
   - Only include links that exist in the original resume
   - If no LinkedIn/GitHub in original, omit them

2. SUMMARY Section:
   SUMMARY
   [2-3 sentences summarizing experience and key qualifications relevant to the job]

3. SKILLS Section:
   SKILLS
   [Category 1]: [skill1], [skill2], [skill3]
   [Category 2]: [skill1], [skill2], [skill3]
   [Category 3]: [skill1], [skill2], [skill3]

   Common categories: Methodologies, Languages, IDEs, Packages/Libraries, Visualization Tools, Database, Other Skills, Operating System

   CRITICAL SKILLS SECTION OPTIMIZATION (MANDATORY):
   - ADD missing job-relevant skills from the job description to the SKILLS section (e.g., programming languages, tools, technologies, frameworks, methodologies)
   - REORGANIZE skills to put most relevant skills for the job first within each category
   - GROUP related skills together using appropriate categories (e.g., "Programming Languages:", "Tools & Technologies:", "Frameworks & Libraries:", "Methodologies:")
   - REMOVE outdated or irrelevant skills that don't match the job requirements
   - Include ALL key technical requirements mentioned in the job description
   - Make the SKILLS section comprehensive and keyword-rich for ATS optimization while keeping it natural and credible
   - DO NOT include skills that the candidate clearly doesn't have based on their experience

4. EXPERIENCE Section:
   EXPERIENCE
   [Company Name], [Location] | [Start Date] - [End Date or Current] | [Job Title]
   • [Bullet point describing achievement with metrics if possible]
   • [Bullet point describing achievement with metrics if possible]
   • [Bullet point describing achievement with metrics if possible]
   
   [Next Company], [Location] | [Start Date] - [End Date] | [Job Title]
   • [Bullet point]
   • [Bullet point]


5. EDUCATION Section (ONLY if original resume has education):
   EDUCATION
   [Degree Name]: [University Name], [Location]
   [Degree Name]: [University Name], [Location]
   
   ⚠️ CRITICAL: ONLY include education entries that exist in the original resume. 
   - DO NOT add any education (Bachelor's, Master's, PhD, etc.) if it is NOT mentioned in the original resume
   - Copy and paste education information exactly as it appears in the original resume
   - If the original resume has no education section, DO NOT create one
   - If the original resume only has a Master's degree, DO NOT add a Bachelor's degree
   - Only include what is explicitly stated in the original resume

6. PROJECTS Section (ONLY if original resume has projects):
   PROJECTS
   [Project Name] | [Technologies Used] | [Date or Duration]
   • [Description of project and achievements]
   • [Key features or results]
   
   [Next Project Name] | [Technologies Used] | [Date or Duration]
   • [Description]
   • [Key features or results]
   
   ⚠️ CRITICAL: Check for project sections using these common names (case-insensitive):
   - "PROJECTS", "ACADEMIC PROJECTS", "SCHOOL PROJECTS", "PERSONAL PROJECTS"
   - "SIDE PROJECTS", "PORTFOLIO PROJECTS", "CAPSTONE PROJECTS", "RESEARCH PROJECTS"
   - "INDIVIDUAL PROJECTS", "TEAM PROJECTS", "GROUP PROJECTS", "COURSE PROJECTS"
   - "UNIVERSITY PROJECTS", "COLLEGE PROJECTS", or any section containing the word "PROJECT"
   - If ANY of these exist in the original resume, include the PROJECTS section
   - If NONE of these exist, do NOT add a PROJECTS section

IMPORTANT INSTRUCTIONS:
- Maintain ALL original information - only enhance and optimize, don't remove truthful content
- Use the EXACT section headers: SUMMARY, SKILLS, EXPERIENCE, EDUCATION (all caps)
- Include EDUCATION section ONLY if the original resume has an education section - do NOT add education if it doesn't exist in the original
- Include PROJECTS section ONLY if the original resume has a projects section (check for: "PROJECTS", "ACADEMIC PROJECTS", "SCHOOL PROJECTS", "PERSONAL PROJECTS", "SIDE PROJECTS", "PORTFOLIO PROJECTS", "CAPSTONE PROJECTS", "RESEARCH PROJECTS", "INDIVIDUAL PROJECTS", "TEAM PROJECTS", "GROUP PROJECTS", "COURSE PROJECTS", "UNIVERSITY PROJECTS", "COLLEGE PROJECTS", or any section containing "PROJECT") - do NOT add projects if they don't exist in the original
- CRITICAL: For EDUCATION section, ONLY copy education entries that are explicitly mentioned in the original resume. DO NOT add Bachelor's, Master's, or any other degree if it is not in the original resume
- For experience entries, use format: "Company, Location | Date Range | Position"
- For projects, use format: "Project Name | Technologies | Date/Duration"
- Use bullet points (•) for experience and project descriptions

⚠️ REMINDER: For EXPERIENCE section bullets, apply the rules specified at the top of this prompt (Problem → Action → Result format, varied action verbs, specific structures, natural tone, no filler phrases, 4-6 bullets, metrics, etc.)

- Reorder experience to highlight most relevant positions first
- Keep formatting clean and professional
- Do NOT add any explanatory text before or after the resume
- Start directly with the header (name)
- Section order: Header → SUMMARY → SKILLS → EXPERIENCE → EDUCATION (if exists) → PROJECTS (if exists)

Provide ONLY the complete optimized resume in the format above, nothing else."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert resume writer specializing in tailoring resumes to specific job descriptions. 🚨 CRITICAL MANDATORY REQUIREMENT: You MUST completely rewrite every experience bullet point from scratch. DO NOT just add keywords or make minor edits. Each bullet must be transformed with: (1) Specific quantitative metrics (numbers, percentages, time, money, scale) for 50% of bullets, (2) Job-relevant technologies/tools from the job description, (3) Problem → Action → Result structure, (4) Strong, varied action verbs (never repeat verbs), (5) Clear business impact. CRITICAL BALANCE: Maintain 50% quantifiable bullets (heavy on metrics) and 50% technical bullets (technical implementations, architectures, technologies matching job description, but WITHOUT metrics). DO NOT include soft skills like leadership, collaboration, or strategic thinking. For 4 bullets: 2 quantifiable, 2 technical. For 5 bullets: 2-3 quantifiable, 2-3 technical. For 6 bullets: 3 quantifiable, 3 technical. If original bullet says 'Worked on projects', rewrite to 'Designed and deployed 3 microservices using Python and Docker, reducing API response time by 45% and handling 50K+ requests daily'. Transform vague statements into specific, measurable achievements that directly connect to job requirements. Use natural, business-professional tone - NO generic/AI-style language. Provide 4-6 bullets per position. Maintain truthfulness while making content significantly more compelling and job-relevant."
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=4000
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"

    # ========== ENHANCED MULTI-STAGE OPTIMIZATION METHODS ==========

    def analyze_job_description(self, job_description: str) -> Dict:
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
                model=self.model,
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
                temperature=0.3,
                max_tokens=1500
            )

            result = response.choices[0].message.content
            return self._parse_job_analysis(result)

        except Exception as e:
            return {"error": f"Error analyzing job description: {str(e)}"}

    def _parse_job_analysis(self, analysis_text: str) -> Dict:
        """Parse job analysis text into structured format."""
        result = {
            'required_skills': [],
            'years_of_experience': '',
            'industry': '',
            'seniority_level': '',
            'critical_keywords': [],
            'ats_keywords': []
        }

        current_section = None
        for line in analysis_text.split('\n'):
            line = line.strip()
            if not line:
                continue

            if 'REQUIRED_SKILLS:' in line:
                current_section = 'required_skills'
            elif 'YEARS_OF_EXPERIENCE:' in line:
                current_section = 'years_of_experience'
            elif 'INDUSTRY:' in line:
                current_section = 'industry'
            elif 'SENIORITY_LEVEL:' in line:
                current_section = 'seniority_level'
            elif 'CRITICAL_KEYWORDS:' in line:
                current_section = 'critical_keywords'
            elif 'ATS_KEYWORDS:' in line:
                current_section = 'ats_keywords'
            elif line.startswith('-') and current_section in ['required_skills', 'critical_keywords', 'ats_keywords']:
                result[current_section].append(line.lstrip('- ').strip())
            elif current_section in ['years_of_experience', 'industry', 'seniority_level'] and not line.endswith(':'):
                result[current_section] = line

        return result

    def multi_stage_optimize(self, resume_text: str, job_description: str, job_analysis: Dict) -> Dict:
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
            stage1_prompt = f"""STAGE 1: CONTENT IMPROVEMENT

JOB DESCRIPTION:
{job_description[:2000]}

RESUME:
{resume_text[:4000]}

JOB ANALYSIS:
- Seniority: {job_analysis.get('seniority_level', 'Not specified')}
- Industry: {job_analysis.get('industry', 'Not specified')}
- Required Skills: {', '.join(job_analysis.get('required_skills', [])[:10])}

Improve the resume content by:
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

IMPORTANT FORMATTING RULES:
- Keep the EDUCATION section EXACTLY as it appears in the original resume. Copy it word-for-word without any changes.
- PRESERVE the professional title/job title from the header (the line immediately after the name) on its own line. This title should be prominent and clearly visible.
- PRESERVE ALL contact information in the header including Phone Number, Email, LinkedIn, GitHub, Portfolio, and any other links or URLs. Format them on one line separated by " | "
- In EXPERIENCE section: Company names MUST be in ALL CAPS. Job titles MUST be in ALL CAPS. This is NON-NEGOTIABLE.
- In PROJECTS section: Project names MUST be in ALL CAPS. This is NON-NEGOTIABLE.

Provide the complete improved resume."""

            stage1_response = self.client.chat.completions.create(
                model=self.model,
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

IMPORTANT:
- Keep the EDUCATION section EXACTLY as it appears in the resume from Stage 1. Do not modify it.
- PRESERVE the professional title/job title from the header (the line immediately after the name) on its own line. Keep it EXACTLY as it appears in Stage 1.
- PRESERVE ALL contact information in the header including Phone Number, Email, LinkedIn, GitHub, Portfolio, and any other links. Keep them EXACTLY as they appear in Stage 1.
- In EXPERIENCE section: Company names MUST be in ALL CAPS. Job titles MUST be in ALL CAPS. This formatting is MANDATORY.
- In PROJECTS section: Project names MUST be in ALL CAPS. This formatting is MANDATORY.

Provide the complete ATS-optimized resume."""

            stage2_response = self.client.chat.completions.create(
                model=self.model,
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

ABSOLUTE REQUIREMENTS (NON-NEGOTIABLE):
- Company names MUST be in ALL CAPS (e.g., MICROSOFT, GOOGLE, AMAZON)
- Job titles MUST be in ALL CAPS (e.g., SENIOR SOFTWARE ENGINEER, DATA SCIENTIST)
- Project names MUST be in ALL CAPS (e.g., E-COMMERCE PLATFORM, MACHINE LEARNING CLASSIFIER)
- This is the ONLY way to make them stand out in ATS-friendly plain text
- Provide plain text resume only. NO markdown formatting (**bold**, *italic*, etc.). ATS systems cannot parse markdown.
- Keep the EDUCATION section EXACTLY as it appears in the resume from Stage 2. Do not modify it.
- PRESERVE the professional title/job title from the header (the line immediately after the name) on its own line. Keep it EXACTLY as it appears in Stage 2. This title should be prominent and clearly visible.
- PRESERVE ALL contact information in the header including Phone Number, Email, LinkedIn, GitHub, Portfolio, and any other links. Keep them EXACTLY as they appear in Stage 2.
- Keep dates in Title Case (Month YYYY format)

Provide the final, polished resume in plain text format."""

            stage3_response = self.client.chat.completions.create(
                model=self.model,
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
                "clear, concise, and professional manner"
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

    def calculate_ats_score(self, resume_text: str, job_description: str) -> Dict:
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

RECOMMENDATIONS:
- [specific recommendation 1]
- [specific recommendation 2]
..."""

            response = self.client.chat.completions.create(
                model=self.model,
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

    def _parse_ats_score(self, score_text: str) -> Dict:
        """Parse ATS score text into structured format."""
        result = {
            'keyword_match': 0,
            'format_score': 0,
            'section_score': 0,
            'overall_score': 0,
            'recommendations': []
        }

        in_recommendations = False
        for line in score_text.split('\n'):
            line = line.strip()
            if not line:
                continue

            if 'KEYWORD_MATCH:' in line:
                try:
                    result['keyword_match'] = int(line.split(':')[1].strip())
                except:
                    pass
            elif 'FORMAT_SCORE:' in line:
                try:
                    result['format_score'] = int(line.split(':')[1].strip())
                except:
                    pass
            elif 'SECTION_SCORE:' in line:
                try:
                    result['section_score'] = int(line.split(':')[1].strip())
                except:
                    pass
            elif 'OVERALL_SCORE:' in line:
                try:
                    result['overall_score'] = int(line.split(':')[1].strip())
                except:
                    pass
            elif 'RECOMMENDATIONS:' in line:
                in_recommendations = True
            elif in_recommendations and line.startswith('-'):
                result['recommendations'].append(line.lstrip('- ').strip())

        return result


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
    
    def optimize_resume(self, resume_text: str, job_description: str, suggestions: List[str], social_links: Optional[Dict] = None) -> str:
        if not self.is_available():
            return "OpenAI API not available."
        
        # Prepare social links information for the prompt
        social_links_info = ""
        if social_links:
            if social_links.get('linkedin'):
                social_links_info += f"\nLinkedIn URL from original resume: {social_links['linkedin']}"
            if social_links.get('github'):
                social_links_info += f"\nGitHub URL from original resume: {social_links['github']}"
        
        prompt = f"""You are an expert resume writer. Create an optimized version of this resume that is specifically tailored to match the job description.

ORIGINAL RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

SUGGESTIONS TO IMPLEMENT:
{chr(10).join(suggestions[:10])}
{social_links_info}

CRITICAL: If the original resume contains LinkedIn or GitHub links, you MUST preserve them in the header contact line with their full URLs.

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

12. BALANCE (CRITICAL): Maintain a 50/50 balance between quantifiable and technical points:
    - 50% of bullets should be QUANTIFIABLE (heavy on metrics, numbers, percentages, measurable results)
    - 50% of bullets should be TECHNICAL (job-relevant technical skills, technologies, implementations, but WITHOUT metrics/numbers)
    - Example of quantifiable (50%): "Designed and deployed 3 microservices using Python and Docker, reducing API response time by 45% and handling 50K+ requests daily"
    - Example of technical non-quantifiable (50%): "Architected microservices infrastructure using Docker, Kubernetes, and AWS ECS, implementing service mesh patterns and container orchestration best practices"
    - Example of technical non-quantifiable (50%): "Developed RESTful APIs following OpenAPI specifications, implementing OAuth 2.0 authentication and JWT token management for secure access control"
    - Example of technical non-quantifiable (50%): "Built data processing pipelines using Apache Spark and Kafka, implementing stream processing patterns and event-driven architecture for real-time analytics"
    - For 4 bullets: 2 should be quantifiable, 2 should be technical (no metrics)
    - For 5 bullets: 2-3 should be quantifiable, 2-3 should be technical (no metrics)
    - For 6 bullets: 3 should be quantifiable, 3 should be technical (no metrics)
    - DO NOT include soft skills (leadership, collaboration, strategic thinking) - focus ONLY on technical implementations, architectures, and technologies

13. KEYWORDS: Include relevant keywords from job description NATURALLY within the rewritten content - NO keyword stuffing

14. LEARNING: Extract and incorporate skills/technologies from BOTH job description AND candidate's resume

15. TECHNICAL NON-QUANTIFIABLE BULLETS: For the 50% technical bullets (without metrics), focus on:
    - Technical implementations and architectures (microservices, APIs, data pipelines, etc.)
    - Technologies and tools from job description (Docker, Kubernetes, AWS services, frameworks, etc.)
    - Technical patterns and best practices (RESTful design, event-driven architecture, etc.)
    - System design and technical solutions
    - Integration with specific technologies or platforms
    - DO NOT include soft skills, leadership, collaboration, or strategic thinking
    - These bullets should demonstrate technical depth and job-relevant technical expertise

EXPERIENCE REWRITING EXAMPLES (MANDATORY TRANSFORMATION):

BEFORE: "Worked on software development projects"
AFTER: "Designed and built 3 enterprise applications using Python, React, and PostgreSQL, reducing API processing time by 40%, serving 10,000+ daily active users, and improving system reliability to 99.9% uptime"

BEFORE: "Managed database operations"
AFTER: "Addressed performance bottlenecks by implementing database indexing strategies and query optimization techniques, improving average query response time by 60% (from 2.5s to 1s), reducing server infrastructure costs by $50K annually, and enabling real-time analytics for 5K+ concurrent users"

BEFORE: "Responsible for team coordination"
AFTER: "Led cross-functional team of 8 engineers and 3 product managers, implementing Agile/Scrum methodologies that increased sprint velocity by 35%, reduced production bugs by 28%, and accelerated feature delivery from 4 weeks to 2.5 weeks average"

BEFORE: "Used machine learning for data analysis"
AFTER: "Developed and deployed machine learning models using Python, scikit-learn, and TensorFlow, improving prediction accuracy from 72% to 89%, processing 2M+ data points daily, and enabling automated decision-making that saved 20 hours/week of manual analysis"

BEFORE: "Worked on backend systems"
AFTER (TECHNICAL NON-QUANTIFIABLE - 50%): "Architected microservices infrastructure using Docker, Kubernetes, and AWS ECS, implementing service mesh patterns with Istio and container orchestration best practices for scalable distributed systems"

BEFORE: "Developed APIs"
AFTER (TECHNICAL NON-QUANTIFIABLE - 50%): "Designed and implemented RESTful APIs following OpenAPI 3.0 specifications, integrating OAuth 2.0 authentication, JWT token management, and rate limiting middleware for secure and scalable API architecture"

⚠️ CRITICAL: Notice how each "AFTER" example:
- Completely rewrites the content (not just adds keywords)
- Includes specific technologies from job description (for quantifiable bullets)
- Adds multiple quantitative metrics (for 70% of bullets)
- Shows clear business impact (for 50% quantifiable bullets) or demonstrates technical depth and job-relevant technologies (for 50% technical bullets)
- Uses varied, strong action verbs
- Follows Problem → Action → Result structure
- Maintains 50/50 balance: Half the bullets are quantifiable with metrics, half focus on technical implementations and technologies without metrics

CRITICAL FORMATTING REQUIREMENTS - Follow this EXACT structure:

1. HEADER (First Line):
   [Full Name]
   [Job Title/Position]
   Location: [City, State] | Email: [email] | Phone: [phone] | LinkedIn: [linkedin_url] | GitHub: [github_url]
   
   IMPORTANT: If the original resume contains LinkedIn or GitHub links, you MUST include them in the contact line with their full URLs.
   - Extract the actual URLs from the original resume (they are provided above if found)
   - Format: "LinkedIn: https://linkedin.com/in/username" or "GitHub: https://github.com/username"
   - Only include links that exist in the original resume
   - If no LinkedIn/GitHub in original, omit them

2. SUMMARY Section:
   SUMMARY
   [2-3 sentences summarizing experience and key qualifications relevant to the job]

3. SKILLS Section:
   SKILLS
   [Category 1]: [skill1], [skill2], [skill3]
   [Category 2]: [skill1], [skill2], [skill3]
   [Category 3]: [skill1], [skill2], [skill3]

   Common categories: Methodologies, Languages, IDEs, Packages/Libraries, Visualization Tools, Database, Other Skills, Operating System

   CRITICAL SKILLS SECTION OPTIMIZATION (MANDATORY):
   - ADD missing job-relevant skills from the job description to the SKILLS section (e.g., programming languages, tools, technologies, frameworks, methodologies)
   - REORGANIZE skills to put most relevant skills for the job first within each category
   - GROUP related skills together using appropriate categories (e.g., "Programming Languages:", "Tools & Technologies:", "Frameworks & Libraries:", "Methodologies:")
   - REMOVE outdated or irrelevant skills that don't match the job requirements
   - Include ALL key technical requirements mentioned in the job description
   - Make the SKILLS section comprehensive and keyword-rich for ATS optimization while keeping it natural and credible
   - DO NOT include skills that the candidate clearly doesn't have based on their experience

4. EXPERIENCE Section:
   EXPERIENCE
   [Company Name], [Location] | [Start Date] - [End Date or Current] | [Job Title]
   • [Bullet point describing achievement with metrics if possible]
   • [Bullet point describing achievement with metrics if possible]
   • [Bullet point describing achievement with metrics if possible]
   
   [Next Company], [Location] | [Start Date] - [End Date] | [Job Title]
   • [Bullet point]
   • [Bullet point]


5. EDUCATION Section (ONLY if original resume has education):
   EDUCATION
   [Degree Name]: [University Name], [Location]
   [Degree Name]: [University Name], [Location]
   
   ⚠️ CRITICAL: ONLY include education entries that exist in the original resume. 
   - DO NOT add any education (Bachelor's, Master's, PhD, etc.) if it is NOT mentioned in the original resume
   - Copy and paste education information exactly as it appears in the original resume
   - If the original resume has no education section, DO NOT create one
   - If the original resume only has a Master's degree, DO NOT add a Bachelor's degree
   - Only include what is explicitly stated in the original resume

6. PROJECTS Section (ONLY if original resume has projects):
   PROJECTS
   [Project Name] | [Technologies Used] | [Date or Duration]
   • [Description of project and achievements]
   • [Key features or results]
   
   [Next Project Name] | [Technologies Used] | [Date or Duration]
   • [Description]
   • [Key features or results]
   
   ⚠️ CRITICAL: Check for project sections using these common names (case-insensitive):
   - "PROJECTS", "ACADEMIC PROJECTS", "SCHOOL PROJECTS", "PERSONAL PROJECTS"
   - "SIDE PROJECTS", "PORTFOLIO PROJECTS", "CAPSTONE PROJECTS", "RESEARCH PROJECTS"
   - "INDIVIDUAL PROJECTS", "TEAM PROJECTS", "GROUP PROJECTS", "COURSE PROJECTS"
   - "UNIVERSITY PROJECTS", "COLLEGE PROJECTS", or any section containing the word "PROJECT"
   - If ANY of these exist in the original resume, include the PROJECTS section
   - If NONE of these exist, do NOT add a PROJECTS section

IMPORTANT INSTRUCTIONS:
- Maintain ALL original information - only enhance and optimize, don't remove truthful content
- Use the EXACT section headers: SUMMARY, SKILLS, EXPERIENCE, EDUCATION (all caps)
- Include EDUCATION section ONLY if the original resume has an education section - do NOT add education if it doesn't exist in the original
- Include PROJECTS section ONLY if the original resume has a projects section (check for: "PROJECTS", "ACADEMIC PROJECTS", "SCHOOL PROJECTS", "PERSONAL PROJECTS", "SIDE PROJECTS", "PORTFOLIO PROJECTS", "CAPSTONE PROJECTS", "RESEARCH PROJECTS", "INDIVIDUAL PROJECTS", "TEAM PROJECTS", "GROUP PROJECTS", "COURSE PROJECTS", "UNIVERSITY PROJECTS", "COLLEGE PROJECTS", or any section containing "PROJECT") - do NOT add projects if they don't exist in the original
- CRITICAL: For EDUCATION section, ONLY copy education entries that are explicitly mentioned in the original resume. DO NOT add Bachelor's, Master's, or any other degree if it is not in the original resume
- For experience entries, use format: "Company, Location | Date Range | Position"
- For projects, use format: "Project Name | Technologies | Date/Duration"
- Use bullet points (•) for experience and project descriptions

⚠️ REMINDER: For EXPERIENCE section bullets, apply the rules specified at the top of this prompt (Problem → Action → Result format, varied action verbs, specific structures, natural tone, no filler phrases, 4-6 bullets, metrics, etc.)

- Reorder experience to highlight most relevant positions first
- Keep formatting clean and professional
- Do NOT add any explanatory text before or after the resume
- Start directly with the header (name)
- Section order: Header → SUMMARY → SKILLS → EXPERIENCE → EDUCATION (if exists) → PROJECTS (if exists)

Provide ONLY the complete optimized resume in the format above, nothing else."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert resume writer specializing in tailoring resumes to specific job descriptions. 🚨 CRITICAL MANDATORY REQUIREMENT: You MUST completely rewrite every experience bullet point from scratch. DO NOT just add keywords or make minor edits. Each bullet must be transformed with: (1) Specific quantitative metrics (numbers, percentages, time, money, scale) for 50% of bullets, (2) Job-relevant technologies/tools from the job description, (3) Problem → Action → Result structure, (4) Strong, varied action verbs (never repeat verbs), (5) Clear business impact. CRITICAL BALANCE: Maintain 50% quantifiable bullets (heavy on metrics) and 50% technical bullets (technical implementations, architectures, technologies matching job description, but WITHOUT metrics). DO NOT include soft skills like leadership, collaboration, or strategic thinking. For 4 bullets: 2 quantifiable, 2 technical. For 5 bullets: 2-3 quantifiable, 2-3 technical. For 6 bullets: 3 quantifiable, 3 technical. If original bullet says 'Worked on projects', rewrite to 'Designed and deployed 3 microservices using Python and Docker, reducing API response time by 45% and handling 50K+ requests daily'. Transform vague statements into specific, measurable achievements that directly connect to job requirements. Use natural, business-professional tone - NO generic/AI-style language. Provide 4-6 bullets per position. Maintain truthfulness while making content significantly more compelling and job-relevant."
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
    
    def optimize_resume(self, resume_text: str, job_description: str, suggestions: List[str], social_links: Optional[Dict] = None) -> str:
        if not self.is_available():
            return "Claude API not available."
        
        # Prepare social links information for the prompt
        social_links_info = ""
        if social_links:
            if social_links.get('linkedin'):
                social_links_info += f"\nLinkedIn URL from original resume: {social_links['linkedin']}"
            if social_links.get('github'):
                social_links_info += f"\nGitHub URL from original resume: {social_links['github']}"
        
        prompt = f"""You are an expert resume writer. Create an optimized version of this resume that is specifically tailored to match the job description.

ORIGINAL RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

SUGGESTIONS TO IMPLEMENT:
{chr(10).join(suggestions[:10])}
{social_links_info}

CRITICAL: If the original resume contains LinkedIn or GitHub links, you MUST preserve them in the header contact line with their full URLs.

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

12. BALANCE (CRITICAL): Maintain a 50/50 balance between quantifiable and technical points:
    - 50% of bullets should be QUANTIFIABLE (heavy on metrics, numbers, percentages, measurable results)
    - 50% of bullets should be TECHNICAL (job-relevant technical skills, technologies, implementations, but WITHOUT metrics/numbers)
    - Example of quantifiable (50%): "Designed and deployed 3 microservices using Python and Docker, reducing API response time by 45% and handling 50K+ requests daily"
    - Example of technical non-quantifiable (50%): "Architected microservices infrastructure using Docker, Kubernetes, and AWS ECS, implementing service mesh patterns and container orchestration best practices"
    - Example of technical non-quantifiable (50%): "Developed RESTful APIs following OpenAPI specifications, implementing OAuth 2.0 authentication and JWT token management for secure access control"
    - Example of technical non-quantifiable (50%): "Built data processing pipelines using Apache Spark and Kafka, implementing stream processing patterns and event-driven architecture for real-time analytics"
    - For 4 bullets: 2 should be quantifiable, 2 should be technical (no metrics)
    - For 5 bullets: 2-3 should be quantifiable, 2-3 should be technical (no metrics)
    - For 6 bullets: 3 should be quantifiable, 3 should be technical (no metrics)
    - DO NOT include soft skills (leadership, collaboration, strategic thinking) - focus ONLY on technical implementations, architectures, and technologies

13. KEYWORDS: Include relevant keywords from job description NATURALLY within the rewritten content - NO keyword stuffing

14. LEARNING: Extract and incorporate skills/technologies from BOTH job description AND candidate's resume

15. TECHNICAL NON-QUANTIFIABLE BULLETS: For the 50% technical bullets (without metrics), focus on:
    - Technical implementations and architectures (microservices, APIs, data pipelines, etc.)
    - Technologies and tools from job description (Docker, Kubernetes, AWS services, frameworks, etc.)
    - Technical patterns and best practices (RESTful design, event-driven architecture, etc.)
    - System design and technical solutions
    - Integration with specific technologies or platforms
    - DO NOT include soft skills, leadership, collaboration, or strategic thinking
    - These bullets should demonstrate technical depth and job-relevant technical expertise

EXPERIENCE REWRITING EXAMPLES (MANDATORY TRANSFORMATION):

BEFORE: "Worked on software development projects"
AFTER: "Designed and built 3 enterprise applications using Python, React, and PostgreSQL, reducing API processing time by 40%, serving 10,000+ daily active users, and improving system reliability to 99.9% uptime"

BEFORE: "Managed database operations"
AFTER: "Addressed performance bottlenecks by implementing database indexing strategies and query optimization techniques, improving average query response time by 60% (from 2.5s to 1s), reducing server infrastructure costs by $50K annually, and enabling real-time analytics for 5K+ concurrent users"

BEFORE: "Responsible for team coordination"
AFTER: "Led cross-functional team of 8 engineers and 3 product managers, implementing Agile/Scrum methodologies that increased sprint velocity by 35%, reduced production bugs by 28%, and accelerated feature delivery from 4 weeks to 2.5 weeks average"

BEFORE: "Used machine learning for data analysis"
AFTER: "Developed and deployed machine learning models using Python, scikit-learn, and TensorFlow, improving prediction accuracy from 72% to 89%, processing 2M+ data points daily, and enabling automated decision-making that saved 20 hours/week of manual analysis"

BEFORE: "Worked on backend systems"
AFTER (TECHNICAL NON-QUANTIFIABLE - 50%): "Architected microservices infrastructure using Docker, Kubernetes, and AWS ECS, implementing service mesh patterns with Istio and container orchestration best practices for scalable distributed systems"

BEFORE: "Developed APIs"
AFTER (TECHNICAL NON-QUANTIFIABLE - 50%): "Designed and implemented RESTful APIs following OpenAPI 3.0 specifications, integrating OAuth 2.0 authentication, JWT token management, and rate limiting middleware for secure and scalable API architecture"

⚠️ CRITICAL: Notice how each "AFTER" example:
- Completely rewrites the content (not just adds keywords)
- Includes specific technologies from job description (for quantifiable bullets)
- Adds multiple quantitative metrics (for 70% of bullets)
- Shows clear business impact (for 50% quantifiable bullets) or demonstrates technical depth and job-relevant technologies (for 50% technical bullets)
- Uses varied, strong action verbs
- Follows Problem → Action → Result structure
- Maintains 50/50 balance: Half the bullets are quantifiable with metrics, half focus on technical implementations and technologies without metrics

CRITICAL FORMATTING REQUIREMENTS - Follow this EXACT structure:

1. HEADER (First Line):
   [Full Name]
   [Job Title/Position]
   Location: [City, State] | Email: [email] | Phone: [phone] | LinkedIn: [linkedin_url] | GitHub: [github_url]
   
   IMPORTANT: If the original resume contains LinkedIn or GitHub links, you MUST include them in the contact line with their full URLs.
   - Extract the actual URLs from the original resume (they are provided above if found)
   - Format: "LinkedIn: https://linkedin.com/in/username" or "GitHub: https://github.com/username"
   - Only include links that exist in the original resume
   - If no LinkedIn/GitHub in original, omit them

2. SUMMARY Section:
   SUMMARY
   [2-3 sentences summarizing experience and key qualifications relevant to the job]

3. SKILLS Section:
   SKILLS
   [Category 1]: [skill1], [skill2], [skill3]
   [Category 2]: [skill1], [skill2], [skill3]
   [Category 3]: [skill1], [skill2], [skill3]

   Common categories: Methodologies, Languages, IDEs, Packages/Libraries, Visualization Tools, Database, Other Skills, Operating System

   CRITICAL SKILLS SECTION OPTIMIZATION (MANDATORY):
   - ADD missing job-relevant skills from the job description to the SKILLS section (e.g., programming languages, tools, technologies, frameworks, methodologies)
   - REORGANIZE skills to put most relevant skills for the job first within each category
   - GROUP related skills together using appropriate categories (e.g., "Programming Languages:", "Tools & Technologies:", "Frameworks & Libraries:", "Methodologies:")
   - REMOVE outdated or irrelevant skills that don't match the job requirements
   - Include ALL key technical requirements mentioned in the job description
   - Make the SKILLS section comprehensive and keyword-rich for ATS optimization while keeping it natural and credible
   - DO NOT include skills that the candidate clearly doesn't have based on their experience

4. EXPERIENCE Section:
   EXPERIENCE
   [Company Name], [Location] | [Start Date] - [End Date or Current] | [Job Title]
   • [Bullet point describing achievement with metrics if possible]
   • [Bullet point describing achievement with metrics if possible]
   • [Bullet point describing achievement with metrics if possible]
   
   [Next Company], [Location] | [Start Date] - [End Date] | [Job Title]
   • [Bullet point]
   • [Bullet point]


5. EDUCATION Section (ONLY if original resume has education):
   EDUCATION
   [Degree Name]: [University Name], [Location]
   [Degree Name]: [University Name], [Location]
   
   ⚠️ CRITICAL: ONLY include education entries that exist in the original resume. 
   - DO NOT add any education (Bachelor's, Master's, PhD, etc.) if it is NOT mentioned in the original resume
   - Copy and paste education information exactly as it appears in the original resume
   - If the original resume has no education section, DO NOT create one
   - If the original resume only has a Master's degree, DO NOT add a Bachelor's degree
   - Only include what is explicitly stated in the original resume

6. PROJECTS Section (ONLY if original resume has projects):
   PROJECTS
   [Project Name] | [Technologies Used] | [Date or Duration]
   • [Description of project and achievements]
   • [Key features or results]
   
   [Next Project Name] | [Technologies Used] | [Date or Duration]
   • [Description]
   • [Key features or results]
   
   ⚠️ CRITICAL: Check for project sections using these common names (case-insensitive):
   - "PROJECTS", "ACADEMIC PROJECTS", "SCHOOL PROJECTS", "PERSONAL PROJECTS"
   - "SIDE PROJECTS", "PORTFOLIO PROJECTS", "CAPSTONE PROJECTS", "RESEARCH PROJECTS"
   - "INDIVIDUAL PROJECTS", "TEAM PROJECTS", "GROUP PROJECTS", "COURSE PROJECTS"
   - "UNIVERSITY PROJECTS", "COLLEGE PROJECTS", or any section containing the word "PROJECT"
   - If ANY of these exist in the original resume, include the PROJECTS section
   - If NONE of these exist, do NOT add a PROJECTS section

IMPORTANT INSTRUCTIONS:
- Maintain ALL original information - only enhance and optimize, don't remove truthful content
- Use the EXACT section headers: SUMMARY, SKILLS, EXPERIENCE, EDUCATION (all caps)
- Include EDUCATION section ONLY if the original resume has an education section - do NOT add education if it doesn't exist in the original
- Include PROJECTS section ONLY if the original resume has a projects section (check for: "PROJECTS", "ACADEMIC PROJECTS", "SCHOOL PROJECTS", "PERSONAL PROJECTS", "SIDE PROJECTS", "PORTFOLIO PROJECTS", "CAPSTONE PROJECTS", "RESEARCH PROJECTS", "INDIVIDUAL PROJECTS", "TEAM PROJECTS", "GROUP PROJECTS", "COURSE PROJECTS", "UNIVERSITY PROJECTS", "COLLEGE PROJECTS", or any section containing "PROJECT") - do NOT add projects if they don't exist in the original
- CRITICAL: For EDUCATION section, ONLY copy education entries that are explicitly mentioned in the original resume. DO NOT add Bachelor's, Master's, or any other degree if it is not in the original resume
- For experience entries, use format: "Company, Location | Date Range | Position"
- For projects, use format: "Project Name | Technologies | Date/Duration"
- Use bullet points (•) for experience and project descriptions

⚠️ REMINDER: For EXPERIENCE section bullets, apply the rules specified at the top of this prompt (Problem → Action → Result format, varied action verbs, specific structures, natural tone, no filler phrases, 4-6 bullets, metrics, etc.)

- Reorder experience to highlight most relevant positions first
- Keep formatting clean and professional
- Do NOT add any explanatory text before or after the resume
- Start directly with the header (name)
- Section order: Header → SUMMARY → SKILLS → EXPERIENCE → EDUCATION (if exists) → PROJECTS (if exists)

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
    
    def optimize_resume(self, resume_text: str, job_description: str, suggestions: List[str], social_links: Optional[Dict] = None) -> str:
        if not self.is_available():
            return "Gemini API not available."
        
        # Prepare social links information for the prompt
        social_links_info = ""
        if social_links:
            if social_links.get('linkedin'):
                social_links_info += f"\nLinkedIn URL from original resume: {social_links['linkedin']}"
            if social_links.get('github'):
                social_links_info += f"\nGitHub URL from original resume: {social_links['github']}"
        
        prompt = f"""You are an expert resume writer. Create an optimized version of this resume that is specifically tailored to match the job description.

ORIGINAL RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

SUGGESTIONS TO IMPLEMENT:
{chr(10).join(suggestions[:10])}
{social_links_info}

CRITICAL: If the original resume contains LinkedIn or GitHub links, you MUST preserve them in the header contact line with their full URLs.

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

12. BALANCE (CRITICAL): Maintain a 50/50 balance between quantifiable and technical points:
    - 50% of bullets should be QUANTIFIABLE (heavy on metrics, numbers, percentages, measurable results)
    - 50% of bullets should be TECHNICAL (job-relevant technical skills, technologies, implementations, but WITHOUT metrics/numbers)
    - Example of quantifiable (50%): "Designed and deployed 3 microservices using Python and Docker, reducing API response time by 45% and handling 50K+ requests daily"
    - Example of technical non-quantifiable (50%): "Architected microservices infrastructure using Docker, Kubernetes, and AWS ECS, implementing service mesh patterns and container orchestration best practices"
    - Example of technical non-quantifiable (50%): "Developed RESTful APIs following OpenAPI specifications, implementing OAuth 2.0 authentication and JWT token management for secure access control"
    - Example of technical non-quantifiable (50%): "Built data processing pipelines using Apache Spark and Kafka, implementing stream processing patterns and event-driven architecture for real-time analytics"
    - For 4 bullets: 2 should be quantifiable, 2 should be technical (no metrics)
    - For 5 bullets: 2-3 should be quantifiable, 2-3 should be technical (no metrics)
    - For 6 bullets: 3 should be quantifiable, 3 should be technical (no metrics)
    - DO NOT include soft skills (leadership, collaboration, strategic thinking) - focus ONLY on technical implementations, architectures, and technologies

13. KEYWORDS: Include relevant keywords from job description NATURALLY within the rewritten content - NO keyword stuffing

14. LEARNING: Extract and incorporate skills/technologies from BOTH job description AND candidate's resume

15. TECHNICAL NON-QUANTIFIABLE BULLETS: For the 50% technical bullets (without metrics), focus on:
    - Technical implementations and architectures (microservices, APIs, data pipelines, etc.)
    - Technologies and tools from job description (Docker, Kubernetes, AWS services, frameworks, etc.)
    - Technical patterns and best practices (RESTful design, event-driven architecture, etc.)
    - System design and technical solutions
    - Integration with specific technologies or platforms
    - DO NOT include soft skills, leadership, collaboration, or strategic thinking
    - These bullets should demonstrate technical depth and job-relevant technical expertise

EXPERIENCE REWRITING EXAMPLES (MANDATORY TRANSFORMATION):

BEFORE: "Worked on software development projects"
AFTER: "Designed and built 3 enterprise applications using Python, React, and PostgreSQL, reducing API processing time by 40%, serving 10,000+ daily active users, and improving system reliability to 99.9% uptime"

BEFORE: "Managed database operations"
AFTER: "Addressed performance bottlenecks by implementing database indexing strategies and query optimization techniques, improving average query response time by 60% (from 2.5s to 1s), reducing server infrastructure costs by $50K annually, and enabling real-time analytics for 5K+ concurrent users"

BEFORE: "Responsible for team coordination"
AFTER: "Led cross-functional team of 8 engineers and 3 product managers, implementing Agile/Scrum methodologies that increased sprint velocity by 35%, reduced production bugs by 28%, and accelerated feature delivery from 4 weeks to 2.5 weeks average"

BEFORE: "Used machine learning for data analysis"
AFTER: "Developed and deployed machine learning models using Python, scikit-learn, and TensorFlow, improving prediction accuracy from 72% to 89%, processing 2M+ data points daily, and enabling automated decision-making that saved 20 hours/week of manual analysis"

BEFORE: "Worked on backend systems"
AFTER (TECHNICAL NON-QUANTIFIABLE - 50%): "Architected microservices infrastructure using Docker, Kubernetes, and AWS ECS, implementing service mesh patterns with Istio and container orchestration best practices for scalable distributed systems"

BEFORE: "Developed APIs"
AFTER (TECHNICAL NON-QUANTIFIABLE - 50%): "Designed and implemented RESTful APIs following OpenAPI 3.0 specifications, integrating OAuth 2.0 authentication, JWT token management, and rate limiting middleware for secure and scalable API architecture"

⚠️ CRITICAL: Notice how each "AFTER" example:
- Completely rewrites the content (not just adds keywords)
- Includes specific technologies from job description (for quantifiable bullets)
- Adds multiple quantitative metrics (for 70% of bullets)
- Shows clear business impact (for 50% quantifiable bullets) or demonstrates technical depth and job-relevant technologies (for 50% technical bullets)
- Uses varied, strong action verbs
- Follows Problem → Action → Result structure
- Maintains 50/50 balance: Half the bullets are quantifiable with metrics, half focus on technical implementations and technologies without metrics

CRITICAL FORMATTING REQUIREMENTS - Follow this EXACT structure:

1. HEADER (First Line):
   [Full Name]
   [Job Title/Position]
   Location: [City, State] | Email: [email] | Phone: [phone] | LinkedIn: [linkedin_url] | GitHub: [github_url]
   
   IMPORTANT: If the original resume contains LinkedIn or GitHub links, you MUST include them in the contact line with their full URLs.
   - Extract the actual URLs from the original resume (they are provided above if found)
   - Format: "LinkedIn: https://linkedin.com/in/username" or "GitHub: https://github.com/username"
   - Only include links that exist in the original resume
   - If no LinkedIn/GitHub in original, omit them

2. SUMMARY Section:
   SUMMARY
   [2-3 sentences summarizing experience and key qualifications relevant to the job]

3. SKILLS Section:
   SKILLS
   [Category 1]: [skill1], [skill2], [skill3]
   [Category 2]: [skill1], [skill2], [skill3]
   [Category 3]: [skill1], [skill2], [skill3]

   Common categories: Methodologies, Languages, IDEs, Packages/Libraries, Visualization Tools, Database, Other Skills, Operating System

   CRITICAL SKILLS SECTION OPTIMIZATION (MANDATORY):
   - ADD missing job-relevant skills from the job description to the SKILLS section (e.g., programming languages, tools, technologies, frameworks, methodologies)
   - REORGANIZE skills to put most relevant skills for the job first within each category
   - GROUP related skills together using appropriate categories (e.g., "Programming Languages:", "Tools & Technologies:", "Frameworks & Libraries:", "Methodologies:")
   - REMOVE outdated or irrelevant skills that don't match the job requirements
   - Include ALL key technical requirements mentioned in the job description
   - Make the SKILLS section comprehensive and keyword-rich for ATS optimization while keeping it natural and credible
   - DO NOT include skills that the candidate clearly doesn't have based on their experience

4. EXPERIENCE Section:
   EXPERIENCE
   [Company Name], [Location] | [Start Date] - [End Date or Current] | [Job Title]
   • [Bullet point describing achievement with metrics if possible]
   • [Bullet point describing achievement with metrics if possible]
   • [Bullet point describing achievement with metrics if possible]
   
   [Next Company], [Location] | [Start Date] - [End Date] | [Job Title]
   • [Bullet point]
   • [Bullet point]


5. EDUCATION Section (ONLY if original resume has education):
   EDUCATION
   [Degree Name]: [University Name], [Location]
   [Degree Name]: [University Name], [Location]
   
   ⚠️ CRITICAL: ONLY include education entries that exist in the original resume. 
   - DO NOT add any education (Bachelor's, Master's, PhD, etc.) if it is NOT mentioned in the original resume
   - Copy and paste education information exactly as it appears in the original resume
   - If the original resume has no education section, DO NOT create one
   - If the original resume only has a Master's degree, DO NOT add a Bachelor's degree
   - Only include what is explicitly stated in the original resume

6. PROJECTS Section (ONLY if original resume has projects):
   PROJECTS
   [Project Name] | [Technologies Used] | [Date or Duration]
   • [Description of project and achievements]
   • [Key features or results]
   
   [Next Project Name] | [Technologies Used] | [Date or Duration]
   • [Description]
   • [Key features or results]
   
   ⚠️ CRITICAL: Check for project sections using these common names (case-insensitive):
   - "PROJECTS", "ACADEMIC PROJECTS", "SCHOOL PROJECTS", "PERSONAL PROJECTS"
   - "SIDE PROJECTS", "PORTFOLIO PROJECTS", "CAPSTONE PROJECTS", "RESEARCH PROJECTS"
   - "INDIVIDUAL PROJECTS", "TEAM PROJECTS", "GROUP PROJECTS", "COURSE PROJECTS"
   - "UNIVERSITY PROJECTS", "COLLEGE PROJECTS", or any section containing the word "PROJECT"
   - If ANY of these exist in the original resume, include the PROJECTS section
   - If NONE of these exist, do NOT add a PROJECTS section

IMPORTANT INSTRUCTIONS:
- Maintain ALL original information - only enhance and optimize, don't remove truthful content
- Use the EXACT section headers: SUMMARY, SKILLS, EXPERIENCE, EDUCATION (all caps)
- Include EDUCATION section ONLY if the original resume has an education section - do NOT add education if it doesn't exist in the original
- Include PROJECTS section ONLY if the original resume has a projects section (check for: "PROJECTS", "ACADEMIC PROJECTS", "SCHOOL PROJECTS", "PERSONAL PROJECTS", "SIDE PROJECTS", "PORTFOLIO PROJECTS", "CAPSTONE PROJECTS", "RESEARCH PROJECTS", "INDIVIDUAL PROJECTS", "TEAM PROJECTS", "GROUP PROJECTS", "COURSE PROJECTS", "UNIVERSITY PROJECTS", "COLLEGE PROJECTS", or any section containing "PROJECT") - do NOT add projects if they don't exist in the original
- CRITICAL: For EDUCATION section, ONLY copy education entries that are explicitly mentioned in the original resume. DO NOT add Bachelor's, Master's, or any other degree if it is not in the original resume
- For experience entries, use format: "Company, Location | Date Range | Position"
- For projects, use format: "Project Name | Technologies | Date/Duration"
- Use bullet points (•) for experience and project descriptions

⚠️ REMINDER: For EXPERIENCE section bullets, apply the rules specified at the top of this prompt (Problem → Action → Result format, varied action verbs, specific structures, natural tone, no filler phrases, 4-6 bullets, metrics, etc.)

- Reorder experience to highlight most relevant positions first
- Keep formatting clean and professional
- Do NOT add any explanatory text before or after the resume
- Start directly with the header (name)
- Section order: Header → SUMMARY → SKILLS → EXPERIENCE → EDUCATION (if exists) → PROJECTS (if exists)

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
    
    def optimize_resume(self, resume_text: str, job_description: str, suggestions: List[str], social_links: Optional[Dict] = None) -> str:
        if not self.is_available():
            return "Cohere API not available."
        
        # Prepare social links information for the prompt
        social_links_info = ""
        if social_links:
            if social_links.get('linkedin'):
                social_links_info += f"\nLinkedIn URL from original resume: {social_links['linkedin']}"
            if social_links.get('github'):
                social_links_info += f"\nGitHub URL from original resume: {social_links['github']}"
        
        prompt = f"""You are an expert resume writer. Create an optimized version of this resume that is specifically tailored to match the job description.

ORIGINAL RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

SUGGESTIONS TO IMPLEMENT:
{chr(10).join(suggestions[:10])}
{social_links_info}

CRITICAL: If the original resume contains LinkedIn or GitHub links, you MUST preserve them in the header contact line with their full URLs.

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

12. BALANCE (CRITICAL): Maintain a 50/50 balance between quantifiable and technical points:
    - 50% of bullets should be QUANTIFIABLE (heavy on metrics, numbers, percentages, measurable results)
    - 50% of bullets should be TECHNICAL (job-relevant technical skills, technologies, implementations, but WITHOUT metrics/numbers)
    - Example of quantifiable (50%): "Designed and deployed 3 microservices using Python and Docker, reducing API response time by 45% and handling 50K+ requests daily"
    - Example of technical non-quantifiable (50%): "Architected microservices infrastructure using Docker, Kubernetes, and AWS ECS, implementing service mesh patterns and container orchestration best practices"
    - Example of technical non-quantifiable (50%): "Developed RESTful APIs following OpenAPI specifications, implementing OAuth 2.0 authentication and JWT token management for secure access control"
    - Example of technical non-quantifiable (50%): "Built data processing pipelines using Apache Spark and Kafka, implementing stream processing patterns and event-driven architecture for real-time analytics"
    - For 4 bullets: 2 should be quantifiable, 2 should be technical (no metrics)
    - For 5 bullets: 2-3 should be quantifiable, 2-3 should be technical (no metrics)
    - For 6 bullets: 3 should be quantifiable, 3 should be technical (no metrics)
    - DO NOT include soft skills (leadership, collaboration, strategic thinking) - focus ONLY on technical implementations, architectures, and technologies

13. KEYWORDS: Include relevant keywords from job description NATURALLY within the rewritten content - NO keyword stuffing

14. LEARNING: Extract and incorporate skills/technologies from BOTH job description AND candidate's resume

15. TECHNICAL NON-QUANTIFIABLE BULLETS: For the 50% technical bullets (without metrics), focus on:
    - Technical implementations and architectures (microservices, APIs, data pipelines, etc.)
    - Technologies and tools from job description (Docker, Kubernetes, AWS services, frameworks, etc.)
    - Technical patterns and best practices (RESTful design, event-driven architecture, etc.)
    - System design and technical solutions
    - Integration with specific technologies or platforms
    - DO NOT include soft skills, leadership, collaboration, or strategic thinking
    - These bullets should demonstrate technical depth and job-relevant technical expertise

EXPERIENCE REWRITING EXAMPLES (MANDATORY TRANSFORMATION):

BEFORE: "Worked on software development projects"
AFTER: "Designed and built 3 enterprise applications using Python, React, and PostgreSQL, reducing API processing time by 40%, serving 10,000+ daily active users, and improving system reliability to 99.9% uptime"

BEFORE: "Managed database operations"
AFTER: "Addressed performance bottlenecks by implementing database indexing strategies and query optimization techniques, improving average query response time by 60% (from 2.5s to 1s), reducing server infrastructure costs by $50K annually, and enabling real-time analytics for 5K+ concurrent users"

BEFORE: "Responsible for team coordination"
AFTER: "Led cross-functional team of 8 engineers and 3 product managers, implementing Agile/Scrum methodologies that increased sprint velocity by 35%, reduced production bugs by 28%, and accelerated feature delivery from 4 weeks to 2.5 weeks average"

BEFORE: "Used machine learning for data analysis"
AFTER: "Developed and deployed machine learning models using Python, scikit-learn, and TensorFlow, improving prediction accuracy from 72% to 89%, processing 2M+ data points daily, and enabling automated decision-making that saved 20 hours/week of manual analysis"

BEFORE: "Worked on backend systems"
AFTER (TECHNICAL NON-QUANTIFIABLE - 50%): "Architected microservices infrastructure using Docker, Kubernetes, and AWS ECS, implementing service mesh patterns with Istio and container orchestration best practices for scalable distributed systems"

BEFORE: "Developed APIs"
AFTER (TECHNICAL NON-QUANTIFIABLE - 50%): "Designed and implemented RESTful APIs following OpenAPI 3.0 specifications, integrating OAuth 2.0 authentication, JWT token management, and rate limiting middleware for secure and scalable API architecture"

⚠️ CRITICAL: Notice how each "AFTER" example:
- Completely rewrites the content (not just adds keywords)
- Includes specific technologies from job description (for quantifiable bullets)
- Adds multiple quantitative metrics (for 70% of bullets)
- Shows clear business impact (for 50% quantifiable bullets) or demonstrates technical depth and job-relevant technologies (for 50% technical bullets)
- Uses varied, strong action verbs
- Follows Problem → Action → Result structure
- Maintains 50/50 balance: Half the bullets are quantifiable with metrics, half focus on technical implementations and technologies without metrics

CRITICAL FORMATTING REQUIREMENTS - Follow this EXACT structure:

1. HEADER (First Line):
   [Full Name]
   [Job Title/Position]
   Location: [City, State] | Email: [email] | Phone: [phone] | LinkedIn: [linkedin_url] | GitHub: [github_url]
   
   IMPORTANT: If the original resume contains LinkedIn or GitHub links, you MUST include them in the contact line with their full URLs.
   - Extract the actual URLs from the original resume (they are provided above if found)
   - Format: "LinkedIn: https://linkedin.com/in/username" or "GitHub: https://github.com/username"
   - Only include links that exist in the original resume
   - If no LinkedIn/GitHub in original, omit them

2. SUMMARY Section:
   SUMMARY
   [2-3 sentences summarizing experience and key qualifications relevant to the job]

3. SKILLS Section:
   SKILLS
   [Category 1]: [skill1], [skill2], [skill3]
   [Category 2]: [skill1], [skill2], [skill3]
   [Category 3]: [skill1], [skill2], [skill3]

   Common categories: Methodologies, Languages, IDEs, Packages/Libraries, Visualization Tools, Database, Other Skills, Operating System

   CRITICAL SKILLS SECTION OPTIMIZATION (MANDATORY):
   - ADD missing job-relevant skills from the job description to the SKILLS section (e.g., programming languages, tools, technologies, frameworks, methodologies)
   - REORGANIZE skills to put most relevant skills for the job first within each category
   - GROUP related skills together using appropriate categories (e.g., "Programming Languages:", "Tools & Technologies:", "Frameworks & Libraries:", "Methodologies:")
   - REMOVE outdated or irrelevant skills that don't match the job requirements
   - Include ALL key technical requirements mentioned in the job description
   - Make the SKILLS section comprehensive and keyword-rich for ATS optimization while keeping it natural and credible
   - DO NOT include skills that the candidate clearly doesn't have based on their experience

4. EXPERIENCE Section:
   EXPERIENCE
   [Company Name], [Location] | [Start Date] - [End Date or Current] | [Job Title]
   • [Bullet point describing achievement with metrics if possible]
   • [Bullet point describing achievement with metrics if possible]
   • [Bullet point describing achievement with metrics if possible]
   
   [Next Company], [Location] | [Start Date] - [End Date] | [Job Title]
   • [Bullet point]
   • [Bullet point]


5. EDUCATION Section (ONLY if original resume has education):
   EDUCATION
   [Degree Name]: [University Name], [Location]
   [Degree Name]: [University Name], [Location]
   
   ⚠️ CRITICAL: ONLY include education entries that exist in the original resume. 
   - DO NOT add any education (Bachelor's, Master's, PhD, etc.) if it is NOT mentioned in the original resume
   - Copy and paste education information exactly as it appears in the original resume
   - If the original resume has no education section, DO NOT create one
   - If the original resume only has a Master's degree, DO NOT add a Bachelor's degree
   - Only include what is explicitly stated in the original resume

6. PROJECTS Section (ONLY if original resume has projects):
   PROJECTS
   [Project Name] | [Technologies Used] | [Date or Duration]
   • [Description of project and achievements]
   • [Key features or results]
   
   [Next Project Name] | [Technologies Used] | [Date or Duration]
   • [Description]
   • [Key features or results]
   
   ⚠️ CRITICAL: Check for project sections using these common names (case-insensitive):
   - "PROJECTS", "ACADEMIC PROJECTS", "SCHOOL PROJECTS", "PERSONAL PROJECTS"
   - "SIDE PROJECTS", "PORTFOLIO PROJECTS", "CAPSTONE PROJECTS", "RESEARCH PROJECTS"
   - "INDIVIDUAL PROJECTS", "TEAM PROJECTS", "GROUP PROJECTS", "COURSE PROJECTS"
   - "UNIVERSITY PROJECTS", "COLLEGE PROJECTS", or any section containing the word "PROJECT"
   - If ANY of these exist in the original resume, include the PROJECTS section
   - If NONE of these exist, do NOT add a PROJECTS section

IMPORTANT INSTRUCTIONS:
- Maintain ALL original information - only enhance and optimize, don't remove truthful content
- Use the EXACT section headers: SUMMARY, SKILLS, EXPERIENCE, EDUCATION (all caps)
- Include EDUCATION section ONLY if the original resume has an education section - do NOT add education if it doesn't exist in the original
- Include PROJECTS section ONLY if the original resume has a projects section (check for: "PROJECTS", "ACADEMIC PROJECTS", "SCHOOL PROJECTS", "PERSONAL PROJECTS", "SIDE PROJECTS", "PORTFOLIO PROJECTS", "CAPSTONE PROJECTS", "RESEARCH PROJECTS", "INDIVIDUAL PROJECTS", "TEAM PROJECTS", "GROUP PROJECTS", "COURSE PROJECTS", "UNIVERSITY PROJECTS", "COLLEGE PROJECTS", or any section containing "PROJECT") - do NOT add projects if they don't exist in the original
- CRITICAL: For EDUCATION section, ONLY copy education entries that are explicitly mentioned in the original resume. DO NOT add Bachelor's, Master's, or any other degree if it is not in the original resume
- For experience entries, use format: "Company, Location | Date Range | Position"
- For projects, use format: "Project Name | Technologies | Date/Duration"
- Use bullet points (•) for experience and project descriptions

⚠️ REMINDER: For EXPERIENCE section bullets, apply the rules specified at the top of this prompt (Problem → Action → Result format, varied action verbs, specific structures, natural tone, no filler phrases, 4-6 bullets, metrics, etc.)

- Reorder experience to highlight most relevant positions first
- Keep formatting clean and professional
- Do NOT add any explanatory text before or after the resume
- Start directly with the header (name)
- Section order: Header → SUMMARY → SKILLS → EXPERIENCE → EDUCATION (if exists) → PROJECTS (if exists)

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

