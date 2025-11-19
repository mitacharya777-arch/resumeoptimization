"""
Utility to extract LinkedIn and GitHub links from resume text.
"""
import re
from typing import Dict, Optional


def extract_social_links(resume_text: str) -> Dict[str, Optional[str]]:
    """
    Extract LinkedIn and GitHub links from resume text.
    
    Args:
        resume_text: The resume text to search
        
    Returns:
        Dictionary with 'linkedin' and 'github' keys containing URLs or None
    """
    links = {
        'linkedin': None,
        'github': None
    }
    
    # Common patterns for LinkedIn and GitHub links
    # Look for URLs in various formats:
    # - https://linkedin.com/in/username
    # - https://www.linkedin.com/in/username
    # - linkedin.com/in/username
    # - LinkedIn: https://linkedin.com/in/username
    # - LinkedIn: linkedin.com/in/username
    # - https://github.com/username
    # - github.com/username
    # - GitHub: https://github.com/username
    
    # LinkedIn patterns
    linkedin_patterns = [
        r'(?:linkedin|LinkedIn|LINKEDIN)[\s:]*([^\s|,;]+linkedin\.com[^\s|,;]*)',
        r'(https?://(?:www\.)?linkedin\.com/[^\s|,;]+)',
        r'(linkedin\.com/[^\s|,;]+)',
    ]
    
    # GitHub patterns
    github_patterns = [
        r'(?:github|GitHub|GITHUB)[\s:]*([^\s|,;]+github\.com[^\s|,;]*)',
        r'(https?://(?:www\.)?github\.com/[^\s|,;]+)',
        r'(github\.com/[^\s|,;]+)',
    ]
    
    # Search for LinkedIn
    for pattern in linkedin_patterns:
        match = re.search(pattern, resume_text, re.IGNORECASE)
        if match:
            link = match.group(1) if match.lastindex else match.group(0)
            # Clean up the link
            link = link.strip().rstrip('.,;|')
            # Ensure it has http:// or https://
            if not link.startswith('http'):
                link = 'https://' + link
            links['linkedin'] = link
            break
    
    # Search for GitHub
    for pattern in github_patterns:
        match = re.search(pattern, resume_text, re.IGNORECASE)
        if match:
            link = match.group(1) if match.lastindex else match.group(0)
            # Clean up the link
            link = link.strip().rstrip('.,;|')
            # Ensure it has http:// or https://
            if not link.startswith('http'):
                link = 'https://' + link
            links['github'] = link
            break
    
    return links


def format_contact_with_links(location: str, email: str, phone: str, 
                              linkedin: Optional[str] = None, 
                              github: Optional[str] = None) -> str:
    """
    Format contact information with LinkedIn and GitHub links.
    
    Args:
        location: Location string
        email: Email address
        phone: Phone number
        linkedin: LinkedIn URL (optional)
        github: GitHub URL (optional)
        
    Returns:
        Formatted contact string with links
    """
    parts = []
    
    if location:
        parts.append(f"Location: {location}")
    
    if email:
        parts.append(f"Email: {email}")
    
    if phone:
        parts.append(f"Phone: {phone}")
    
    if linkedin:
        parts.append(f"LinkedIn: {linkedin}")
    
    if github:
        parts.append(f"GitHub: {github}")
    
    return " | ".join(parts)

