"""
Resume Analytics Engine
Provides comprehensive insights into resume optimization changes.
"""
import re
from typing import Dict, List, Optional, Tuple
from difflib import SequenceMatcher
import logging

logger = logging.getLogger(__name__)


def generate_comprehensive_analytics(
    original_resume: str,
    optimized_resume: str,
    job_description: str,
    job_analysis: Optional[Dict] = None,
    ats_score: Optional[Dict] = None
) -> Dict:
    """
    Generate comprehensive analytics comparing original and optimized resumes.

    Args:
        original_resume: The original resume text
        optimized_resume: The optimized resume text
        job_description: The target job description
        job_analysis: Optional job analysis data from AI
        ats_score: Optional ATS score data

    Returns:
        Dictionary containing:
        - change_explanations: List of specific changes with reasons
        - keyword_analysis: Added/removed keywords with locations
        - section_scores: Percentage scores for each section
        - improvement_suggestions: Actionable recommendations
        - industry_benchmark: Comparative strength analysis
    """
    analytics = {
        'change_explanations': generate_change_explanations(
            original_resume, optimized_resume, job_description, job_analysis
        ),
        'keyword_analysis': analyze_keywords(
            original_resume, optimized_resume, job_description, job_analysis
        ),
        'section_scores': calculate_section_scores(
            optimized_resume, job_description, job_analysis
        ),
        'improvement_suggestions': generate_improvement_suggestions(
            optimized_resume, job_description, ats_score
        ),
        'industry_benchmark': calculate_industry_benchmark(
            optimized_resume, job_description, job_analysis, ats_score
        )
    }

    return analytics


def generate_change_explanations(
    original: str,
    optimized: str,
    job_description: str,
    job_analysis: Optional[Dict] = None
) -> List[Dict]:
    """
    Generate detailed explanations for each significant change made.

    Returns list of changes with format:
    {
        'type': 'keyword_addition' | 'content_enhancement' | 'formatting' | 'quantification',
        'section': 'SUMMARY' | 'EXPERIENCE' | 'SKILLS' | etc.,
        'change': 'Added "Python" to skills',
        'reason': 'Job requires Python as a primary skill',
        'impact': 'high' | 'medium' | 'low'
    }
    """
    changes = []

    # Extract job requirements
    job_keywords = extract_job_keywords(job_description, job_analysis)

    # Analyze keyword additions
    original_lower = original.lower()
    optimized_lower = optimized.lower()

    for keyword in job_keywords:
        if keyword.lower() not in original_lower and keyword.lower() in optimized_lower:
            section = find_section_for_keyword(optimized, keyword)
            changes.append({
                'type': 'keyword_addition',
                'section': section,
                'change': f'Added "{keyword}"',
                'reason': f'Job requires {keyword} as a key skill/technology',
                'impact': 'high' if job_analysis and keyword.lower() in [s.lower() for s in job_analysis.get('required_skills', [])[:5]] else 'medium'
            })

    # Analyze quantification additions
    original_numbers = re.findall(r'\d+%|\d+\+|increased by \d+|reduced by \d+|\$\d+', original, re.IGNORECASE)
    optimized_numbers = re.findall(r'\d+%|\d+\+|increased by \d+|reduced by \d+|\$\d+', optimized, re.IGNORECASE)

    if len(optimized_numbers) > len(original_numbers):
        changes.append({
            'type': 'quantification',
            'section': 'EXPERIENCE',
            'change': f'Added {len(optimized_numbers) - len(original_numbers)} quantifiable metrics',
            'reason': 'Quantified achievements make your impact more concrete and measurable',
            'impact': 'high'
        })

    # Analyze action verb improvements
    strong_verbs = [
        'engineered', 'architected', 'spearheaded', 'pioneered', 'orchestrated',
        'optimized', 'streamlined', 'accelerated', 'transformed', 'innovated'
    ]

    added_strong_verbs = []
    for verb in strong_verbs:
        if verb not in original_lower and verb in optimized_lower:
            added_strong_verbs.append(verb)

    if added_strong_verbs:
        changes.append({
            'type': 'content_enhancement',
            'section': 'EXPERIENCE',
            'change': f'Enhanced with strong action verbs: {", ".join(added_strong_verbs[:3])}',
            'reason': 'Strong action verbs demonstrate leadership and technical capability',
            'impact': 'medium'
        })

    # Analyze section restructuring
    sections = ['SUMMARY', 'SKILLS', 'EXPERIENCE', 'EDUCATION', 'PROJECTS']
    for section in sections:
        orig_section = extract_section_text(original, section)
        opt_section = extract_section_text(optimized, section)

        if orig_section and opt_section:
            len_diff = len(opt_section) - len(orig_section)
            if len_diff > 100:  # Significant expansion
                changes.append({
                    'type': 'content_enhancement',
                    'section': section,
                    'change': f'Expanded {section.title()} section with more detail',
                    'reason': f'Enhanced to better showcase relevant {section.lower()} for this role',
                    'impact': 'medium'
                })

    # Sort by impact
    impact_order = {'high': 0, 'medium': 1, 'low': 2}
    changes.sort(key=lambda x: impact_order[x['impact']])

    return changes


def analyze_keywords(
    original: str,
    optimized: str,
    job_description: str,
    job_analysis: Optional[Dict] = None
) -> Dict:
    """
    Analyze keyword changes and create heatmap data.

    Returns:
    {
        'added_keywords': [...],
        'removed_keywords': [...],
        'keyword_density': {...},
        'heatmap': {
            'SUMMARY': {'python': 2, 'aws': 1, ...},
            'EXPERIENCE': {'python': 5, 'docker': 3, ...},
            ...
        }
    }
    """
    # Extract keywords from job
    job_keywords = extract_job_keywords(job_description, job_analysis)

    # Find added and removed keywords
    original_words = set(re.findall(r'\b\w{3,}\b', original.lower()))
    optimized_words = set(re.findall(r'\b\w{3,}\b', optimized.lower()))

    job_keywords_lower = set(k.lower() for k in job_keywords)

    added_keywords = [k for k in job_keywords if k.lower() in optimized_words and k.lower() not in original_words]
    removed_keywords = [k for k in job_keywords if k.lower() in original_words and k.lower() not in optimized_words]

    # Calculate keyword density by section
    sections = ['SUMMARY', 'SKILLS', 'EXPERIENCE', 'EDUCATION', 'PROJECTS']
    heatmap = {}

    for section in sections:
        section_text = extract_section_text(optimized, section)
        if section_text:
            section_lower = section_text.lower()
            heatmap[section] = {}

            for keyword in job_keywords:
                count = section_lower.count(keyword.lower())
                if count > 0:
                    heatmap[section][keyword] = count

    # Calculate overall keyword density
    total_words = len(optimized.split())
    keyword_density = {}
    for keyword in job_keywords:
        count = optimized.lower().count(keyword.lower())
        if count > 0:
            keyword_density[keyword] = round((count / total_words) * 100, 2)

    return {
        'added_keywords': added_keywords[:10],  # Top 10
        'removed_keywords': removed_keywords[:5],  # Top 5
        'keyword_density': keyword_density,
        'heatmap': heatmap,
        'total_matched_keywords': len([k for k in job_keywords if k.lower() in optimized_words])
    }


def calculate_section_scores(
    resume: str,
    job_description: str,
    job_analysis: Optional[Dict] = None
) -> Dict[str, int]:
    """
    Calculate percentage scores for each resume section.

    Returns:
    {
        'SUMMARY': 85,
        'SKILLS': 70,
        'EXPERIENCE': 90,
        'EDUCATION': 80,
        'PROJECTS': 75
    }
    """
    sections = ['SUMMARY', 'SKILLS', 'EXPERIENCE', 'EDUCATION', 'PROJECTS']
    scores = {}

    job_keywords = extract_job_keywords(job_description, job_analysis)
    job_keywords_lower = set(k.lower() for k in job_keywords)

    for section in sections:
        section_text = extract_section_text(resume, section)

        if not section_text:
            scores[section] = 0
            continue

        score = 50  # Base score for having the section

        # Check keyword presence (up to +30 points)
        section_lower = section_text.lower()
        matched_keywords = sum(1 for kw in job_keywords_lower if kw in section_lower)
        keyword_score = min(30, (matched_keywords / max(len(job_keywords), 1)) * 30)
        score += keyword_score

        # Check for quantifiable metrics in EXPERIENCE (+10 points)
        if section == 'EXPERIENCE':
            metrics = re.findall(r'\d+%|\d+\+|increased by \d+|reduced by \d+|\$\d+', section_text, re.IGNORECASE)
            if len(metrics) >= 3:
                score += 10
            elif len(metrics) >= 1:
                score += 5

        # Check for strong action verbs (+10 points)
        if section in ['EXPERIENCE', 'PROJECTS']:
            strong_verbs = [
                'engineered', 'architected', 'led', 'managed', 'developed',
                'optimized', 'improved', 'increased', 'reduced', 'launched'
            ]
            verb_count = sum(1 for verb in strong_verbs if verb in section_lower)
            score += min(10, verb_count * 2)

        scores[section] = min(100, int(score))

    return scores


def generate_improvement_suggestions(
    resume: str,
    job_description: str,
    ats_score: Optional[Dict] = None
) -> List[Dict]:
    """
    Generate actionable improvement suggestions.

    Returns list of suggestions:
    {
        'category': 'keywords' | 'formatting' | 'content' | 'ats',
        'priority': 'high' | 'medium' | 'low',
        'suggestion': 'Consider adding more quantified achievements',
        'example': 'e.g., "Increased sales by 30%"'
    }
    """
    suggestions = []

    # Check for quantifiable metrics
    metrics = re.findall(r'\d+%|\d+\+|increased by \d+|reduced by \d+|\$\d+', resume, re.IGNORECASE)
    if len(metrics) < 5:
        suggestions.append({
            'category': 'content',
            'priority': 'high',
            'suggestion': 'Add more quantified achievements to demonstrate impact',
            'example': 'e.g., "Increased system performance by 40%" or "Reduced costs by $50K annually"'
        })

    # Check for technical skills keywords
    job_keywords = extract_job_keywords(job_description, None)
    resume_lower = resume.lower()
    missing_keywords = [kw for kw in job_keywords if kw.lower() not in resume_lower]

    if len(missing_keywords) > 3:
        suggestions.append({
            'category': 'keywords',
            'priority': 'high',
            'suggestion': f'Consider incorporating these job-relevant keywords: {", ".join(missing_keywords[:5])}',
            'example': 'Integrate naturally into your experience descriptions'
        })

    # Check experience section detail
    exp_section = extract_section_text(resume, 'EXPERIENCE')
    if exp_section:
        bullet_points = len(re.findall(r'^\s*[-•]\s', exp_section, re.MULTILINE))
        if bullet_points < 8:
            suggestions.append({
                'category': 'content',
                'priority': 'medium',
                'suggestion': 'Expand experience section with more detailed accomplishments',
                'example': 'Aim for 3-5 bullet points per role, focusing on achievements and impact'
            })

    # Check for leadership indicators
    leadership_terms = ['led', 'managed', 'mentored', 'supervised', 'coordinated', 'directed']
    leadership_count = sum(1 for term in leadership_terms if term in resume_lower)
    if leadership_count < 2:
        suggestions.append({
            'category': 'content',
            'priority': 'medium',
            'suggestion': 'Highlight leadership experience and team collaboration',
            'example': 'e.g., "Led team of 5 engineers" or "Mentored junior developers"'
        })

    # ATS-specific suggestions
    if ats_score and ats_score.get('overall_score', 100) < 70:
        suggestions.append({
            'category': 'ats',
            'priority': 'high',
            'suggestion': 'Improve ATS compatibility by using standard section headers and simple formatting',
            'example': 'Use headers like EXPERIENCE, EDUCATION, SKILLS without special characters'
        })

    # Check for summary/objective
    if 'SUMMARY' not in resume.upper() and 'OBJECTIVE' not in resume.upper():
        suggestions.append({
            'category': 'content',
            'priority': 'low',
            'suggestion': 'Consider adding a professional summary at the top',
            'example': 'Brief 2-3 sentence overview of your expertise and career goals'
        })

    # Sort by priority
    priority_order = {'high': 0, 'medium': 1, 'low': 2}
    suggestions.sort(key=lambda x: priority_order[x['priority']])

    return suggestions[:7]  # Return top 7 suggestions


def calculate_industry_benchmark(
    resume: str,
    job_description: str,
    job_analysis: Optional[Dict] = None,
    ats_score: Optional[Dict] = None
) -> Dict:
    """
    Calculate how the resume compares to industry benchmarks.

    Returns:
    {
        'role': 'Software Engineer',
        'improvement_percentage': 25,
        'comparison': 'above_average' | 'average' | 'below_average',
        'percentile': 75,
        'strengths': [...],
        'areas_to_improve': [...]
    }
    """
    # Determine role from job description
    role = 'Professional'
    if job_analysis and job_analysis.get('seniority_level'):
        seniority = job_analysis['seniority_level']
        role = f"{seniority.title()} Level Position"

    # Calculate resume strength score
    strength_score = 50  # Base

    # Factor 1: Keyword match (up to +20 points)
    job_keywords = extract_job_keywords(job_description, job_analysis)
    resume_lower = resume.lower()
    matched = sum(1 for kw in job_keywords if kw.lower() in resume_lower)
    keyword_score = min(20, (matched / max(len(job_keywords), 1)) * 20)
    strength_score += keyword_score

    # Factor 2: Quantified achievements (up to +15 points)
    metrics = re.findall(r'\d+%|\d+\+|increased by \d+|reduced by \d+|\$\d+', resume, re.IGNORECASE)
    quantification_score = min(15, len(metrics) * 3)
    strength_score += quantification_score

    # Factor 3: ATS compatibility (up to +15 points)
    if ats_score:
        ats_points = (ats_score.get('overall_score', 70) / 100) * 15
        strength_score += ats_points
    else:
        strength_score += 10  # Default moderate score

    # Convert to percentile (assume average resume scores 60-70)
    # This is a simplified benchmark model
    if strength_score >= 80:
        comparison = 'above_average'
        percentile = 75 + (strength_score - 80)
        improvement_pct = 30
    elif strength_score >= 65:
        comparison = 'average'
        percentile = 50 + (strength_score - 65) / 15 * 25
        improvement_pct = 15
    else:
        comparison = 'below_average'
        percentile = max(20, strength_score - 45)
        improvement_pct = 5

    # Identify strengths
    strengths = []
    if len(metrics) >= 5:
        strengths.append('Strong quantification of achievements')
    if keyword_score >= 15:
        strengths.append('Excellent keyword alignment with job requirements')
    if ats_score and ats_score.get('overall_score', 0) >= 80:
        strengths.append('High ATS compatibility')

    # Identify areas to improve
    areas_to_improve = []
    if len(metrics) < 3:
        areas_to_improve.append('Add more quantifiable metrics')
    if keyword_score < 10:
        areas_to_improve.append('Incorporate more job-relevant keywords')
    if ats_score and ats_score.get('overall_score', 100) < 70:
        areas_to_improve.append('Improve ATS-friendly formatting')

    return {
        'role': role,
        'improvement_percentage': int(improvement_pct),
        'comparison': comparison,
        'percentile': int(min(99, percentile)),
        'strengths': strengths if strengths else ['Resume has good foundation'],
        'areas_to_improve': areas_to_improve if areas_to_improve else ['Continue refining content']
    }


# Helper functions

def extract_job_keywords(job_description: str, job_analysis: Optional[Dict] = None) -> List[str]:
    """Extract key technical and professional keywords from job description."""
    keywords = set()

    # Use job analysis if available
    if job_analysis:
        keywords.update(job_analysis.get('required_skills', []))
        keywords.update(job_analysis.get('critical_keywords', []))

    # Common technical skills patterns
    tech_patterns = [
        r'\b(?:Python|Java|JavaScript|C\+\+|React|Node\.js|Docker|Kubernetes|AWS|Azure|GCP)\b',
        r'\b(?:SQL|MongoDB|PostgreSQL|MySQL|Redis)\b',
        r'\b(?:Machine Learning|AI|Deep Learning|NLP|Computer Vision)\b',
        r'\b(?:REST|API|Microservices|CI/CD|DevOps|Agile|Scrum)\b',
        r'\b(?:TensorFlow|PyTorch|Scikit-learn|Pandas|NumPy)\b'
    ]

    for pattern in tech_patterns:
        matches = re.findall(pattern, job_description, re.IGNORECASE)
        keywords.update(matches)

    # Extract important noun phrases (3-15 characters)
    words = re.findall(r'\b[A-Z][a-z]{2,14}\b|\b[a-z]{4,15}\b', job_description)

    # Filter common words
    common_words = {
        'experience', 'knowledge', 'ability', 'skills', 'team', 'work',
        'required', 'preferred', 'must', 'should', 'will', 'have', 'with'
    }

    keywords.update([w for w in words if w.lower() not in common_words])

    return list(keywords)[:30]  # Return top 30 keywords


def extract_section_text(resume: str, section_name: str) -> str:
    """Extract text for a specific section from resume."""
    sections = ['SUMMARY', 'SKILLS', 'EXPERIENCE', 'EDUCATION', 'PROJECTS', 'CERTIFICATIONS']

    # Build pattern to match section
    pattern = rf'{section_name}[:\s]*\n(.*?)(?=\n(?:{"|".join(sections)})[:\s]*\n|\Z)'
    match = re.search(pattern, resume, re.IGNORECASE | re.DOTALL)

    if match:
        return match.group(1).strip()

    return ''


def find_section_for_keyword(resume: str, keyword: str) -> str:
    """Find which section a keyword appears in."""
    sections = ['SUMMARY', 'SKILLS', 'EXPERIENCE', 'EDUCATION', 'PROJECTS']

    for section in sections:
        section_text = extract_section_text(resume, section)
        if section_text and keyword.lower() in section_text.lower():
            return section

    return 'GENERAL'
