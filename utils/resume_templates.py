"""
Resume Template System
Implements comprehensive professional resume templates with customization options.

Templates:
1. Professional Modern - Blue accents, professional style
2. Tech Minimalist - Minimal, ATS-optimized
3. Data Professional - Teal accents, structured layout
4. Creative Portfolio - Portfolio-style for creative/design roles
5. Executive Leadership - Leadership focus for C-level positions
6. Academic Research - Publications-first for academic/research roles
7. Career Changer - Skills-based for career transitions
8. Entry Level - Education-first for students/entry-level
"""

from typing import Dict, List, Optional


def get_template(template_name: str) -> Dict:
    """Get template configuration by name."""
    templates = {
        "professional_modern": {
            "name": "Professional Modern",
            "description": "Best for corporate positions, business roles, traditional companies",
            "accent_color": "#2563eb",
            "section_underline": True,
            "header_border": True,
            "style": "professional",
            "font_family": "Arial, sans-serif",
            "spacing": "normal",
            "section_order": ["SUMMARY", "EXPERIENCE", "SKILLS", "EDUCATION", "PROJECTS"],
            "icon": "briefcase",
            "best_for": ["Business", "Corporate", "Finance", "Management"]
        },
        "tech_minimalist": {
            "name": "Tech Minimalist",
            "description": "Best for tech companies, startups, ATS-optimized",
            "accent_color": "#000000",
            "section_underline": False,
            "header_border": False,
            "style": "minimal",
            "font_family": "Helvetica, sans-serif",
            "spacing": "compact",
            "section_order": ["SUMMARY", "SKILLS", "EXPERIENCE", "PROJECTS", "EDUCATION"],
            "icon": "code",
            "best_for": ["Software Engineering", "Tech", "Startups", "Development"]
        },
        "data_professional": {
            "name": "Data Professional",
            "description": "Best for data analyst/scientist roles, research positions",
            "accent_color": "#14b8a6",
            "section_underline": True,
            "header_border": True,
            "style": "structured",
            "font_family": "Arial, sans-serif",
            "spacing": "normal",
            "section_order": ["SUMMARY", "SKILLS", "EXPERIENCE", "PROJECTS", "EDUCATION"],
            "icon": "chart-line",
            "best_for": ["Data Science", "Analytics", "Research", "Statistics"]
        },
        "creative_portfolio": {
            "name": "Creative Portfolio",
            "description": "Portfolio-style for creative and design roles, showcases projects prominently",
            "accent_color": "#ec4899",
            "section_underline": True,
            "header_border": True,
            "style": "creative",
            "font_family": "Georgia, serif",
            "spacing": "relaxed",
            "section_order": ["SUMMARY", "PROJECTS", "EXPERIENCE", "SKILLS", "EDUCATION"],
            "icon": "palette",
            "best_for": ["Design", "Creative", "UX/UI", "Marketing", "Content"]
        },
        "executive_leadership": {
            "name": "Executive Leadership",
            "description": "Leadership-focused for C-level and executive positions",
            "accent_color": "#1e293b",
            "section_underline": True,
            "header_border": True,
            "style": "executive",
            "font_family": "Times New Roman, serif",
            "spacing": "relaxed",
            "section_order": ["SUMMARY", "EXPERIENCE", "EDUCATION", "SKILLS", "CERTIFICATIONS"],
            "icon": "user-tie",
            "best_for": ["Executive", "C-Level", "Senior Leadership", "Director"]
        },
        "academic_research": {
            "name": "Academic Research",
            "description": "Publications-first for academic and research positions",
            "accent_color": "#7c3aed",
            "section_underline": True,
            "header_border": True,
            "style": "academic",
            "font_family": "Times New Roman, serif",
            "spacing": "normal",
            "section_order": ["SUMMARY", "EDUCATION", "PUBLICATIONS", "EXPERIENCE", "SKILLS"],
            "icon": "graduation-cap",
            "best_for": ["Academia", "Research", "PhD", "Professor", "Scientist"]
        },
        "career_changer": {
            "name": "Career Changer",
            "description": "Skills-based format for career transitions, highlights transferable skills",
            "accent_color": "#f59e0b",
            "section_underline": True,
            "header_border": True,
            "style": "functional",
            "font_family": "Arial, sans-serif",
            "spacing": "normal",
            "section_order": ["SUMMARY", "SKILLS", "PROJECTS", "EXPERIENCE", "EDUCATION"],
            "icon": "route",
            "best_for": ["Career Change", "Transition", "Pivot", "Reskilling"]
        },
        "entry_level": {
            "name": "Entry Level / Student",
            "description": "Education-first for students and entry-level positions",
            "accent_color": "#10b981",
            "section_underline": True,
            "header_border": True,
            "style": "entry_level",
            "font_family": "Arial, sans-serif",
            "spacing": "normal",
            "section_order": ["SUMMARY", "EDUCATION", "SKILLS", "PROJECTS", "EXPERIENCE"],
            "icon": "user-graduate",
            "best_for": ["Student", "Entry Level", "Intern", "New Grad"]
        }
    }
    return templates.get(template_name.lower(), templates["professional_modern"])


def get_all_templates() -> Dict:
    """Get all available templates."""
    return {
        "professional_modern": get_template("professional_modern"),
        "tech_minimalist": get_template("tech_minimalist"),
        "data_professional": get_template("data_professional"),
        "creative_portfolio": get_template("creative_portfolio"),
        "executive_leadership": get_template("executive_leadership"),
        "academic_research": get_template("academic_research"),
        "career_changer": get_template("career_changer"),
        "entry_level": get_template("entry_level")
    }


def recommend_template(job_description: str, resume_text: str, job_analysis: Optional[Dict] = None) -> Dict:
    """
    Recommend the best template based on job description, resume, and analysis.

    Args:
        job_description: The target job description
        resume_text: The candidate's resume
        job_analysis: Optional job analysis data from AI

    Returns:
        Dictionary with recommended template and reasoning
    """
    # Extract key indicators
    job_lower = job_description.lower()
    resume_lower = resume_text.lower()

    # Detect role type from job description
    role_keywords = {
        "executive_leadership": ["ceo", "cto", "cfo", "vp", "vice president", "director", "executive", "c-level", "head of"],
        "tech_minimalist": ["software engineer", "developer", "programmer", "full stack", "backend", "frontend", "devops"],
        "data_professional": ["data scientist", "data analyst", "machine learning", "data engineer", "analytics", "statistician"],
        "creative_portfolio": ["designer", "ux", "ui", "creative", "graphic", "product designer", "art director"],
        "academic_research": ["professor", "researcher", "phd", "postdoc", "academic", "faculty", "scientist"],
        "entry_level": ["entry level", "intern", "junior", "graduate", "recent grad", "associate"],
        "career_changer": []  # Will be detected by experience mismatch
    }

    # Score each template
    scores = {template: 0 for template in role_keywords.keys()}
    scores["professional_modern"] = 0  # Default fallback

    # Check job description keywords
    for template, keywords in role_keywords.items():
        for keyword in keywords:
            if keyword in job_lower:
                scores[template] += 10

    # Check experience level from job analysis
    if job_analysis:
        seniority = job_analysis.get('seniority_level', '').lower()
        years_exp = job_analysis.get('years_of_experience', 0)

        if 'senior' in seniority or years_exp >= 10:
            scores["executive_leadership"] += 5
        elif 'entry' in seniority or years_exp <= 2:
            scores["entry_level"] += 5

    # Check for publications/research indicators
    if "publication" in resume_lower or "research" in resume_lower or "phd" in resume_lower:
        scores["academic_research"] += 8

    # Check for portfolio/creative work
    if "portfolio" in resume_lower or "behance" in resume_lower or "dribbble" in resume_lower:
        scores["creative_portfolio"] += 8

    # Check for career change indicators (mismatched experience)
    job_industries = ["finance", "healthcare", "tech", "education", "marketing"]
    job_industry = None
    for industry in job_industries:
        if industry in job_lower:
            job_industry = industry
            break

    if job_industry:
        # If resume doesn't mention the job industry much, might be career change
        if job_industry not in resume_lower or resume_lower.count(job_industry) < 2:
            scores["career_changer"] += 5

    # Get the template with highest score
    recommended = max(scores.items(), key=lambda x: x[1])
    template_name = recommended[0]
    score = recommended[1]

    # If no clear winner, default to professional_modern
    if score < 5:
        template_name = "professional_modern"

    template = get_template(template_name)

    return {
        "template_id": template_name,
        "template": template,
        "confidence": min(100, score * 10),  # Convert to percentage
        "reason": f"This template is recommended because it's best suited for {', '.join(template['best_for'])} roles."
    }


def customize_template(template_name: str, customizations: Dict) -> Dict:
    """
    Apply customizations to a template.

    Args:
        template_name: Name of the base template
        customizations: Dictionary of customizations to apply
            - accent_color: Custom accent color (hex)
            - font_family: Custom font family
            - spacing: 'compact', 'normal', or 'relaxed'

    Returns:
        Customized template configuration
    """
    template = get_template(template_name).copy()

    # Apply customizations
    if "accent_color" in customizations:
        template["accent_color"] = customizations["accent_color"]

    if "font_family" in customizations:
        template["font_family"] = customizations["font_family"]

    if "spacing" in customizations and customizations["spacing"] in ["compact", "normal", "relaxed"]:
        template["spacing"] = customizations["spacing"]

    if "section_order" in customizations:
        template["section_order"] = customizations["section_order"]

    return template


def get_available_fonts() -> List[str]:
    """Get list of available font families."""
    return [
        "Arial, sans-serif",
        "Helvetica, sans-serif",
        "Times New Roman, serif",
        "Georgia, serif",
        "Calibri, sans-serif",
        "Verdana, sans-serif"
    ]


def get_spacing_options() -> List[Dict]:
    """Get available spacing options."""
    return [
        {"value": "compact", "label": "Compact (1-page optimized)", "description": "Tight spacing for fitting more content"},
        {"value": "normal", "label": "Normal", "description": "Balanced spacing for readability"},
        {"value": "relaxed", "label": "Relaxed (2-page)", "description": "More breathing room, easier to scan"}
    ]