"""
ATS (Applicant Tracking System) Compliance Engine
Analyzes resumes for ATS compatibility and provides specific recommendations.
Optimized for high concurrency (1000+ requests).
"""

import re
from typing import Dict, List, Tuple, Set
from collections import Counter
import logging

logger = logging.getLogger(__name__)


class ATSComplianceEngine:
    """
    ATS Compliance Engine for analyzing resume compatibility with ATS systems.
    Optimized for performance and scalability.
    """
    
    def __init__(self):
        """Initialize the ATS compliance engine."""
        # Common ATS-incompatible formatting elements
        self.ats_incompatible_patterns = [
            r'<table[^>]*>',  # Tables
            r'<div[^>]*>',    # Divs
            r'<span[^>]*>',   # Spans
            r'<img[^>]*>',    # Images
            r'<object[^>]*>', # Objects
            r'<embed[^>]*>',  # Embeds
            r'<header[^>]*>', # Headers
            r'<footer[^>]*>', # Footers
            r'<nav[^>]*>',    # Navigation
            r'<section[^>]*>',# Sections
        ]
        
        # ATS-friendly section headers (case-insensitive)
        self.ats_friendly_sections = {
            'summary', 'professional summary', 'objective', 'profile',
            'experience', 'work experience', 'employment history', 'professional experience',
            'education', 'academic background', 'qualifications',
            'skills', 'technical skills', 'core competencies', 'competencies',
            'certifications', 'certificates', 'licenses',
            'projects', 'project experience',
            'achievements', 'awards', 'honors',
            'publications', 'research',
            'languages', 'language skills',
            'references', 'professional references'
        }
        
        # Common ATS-incompatible characters
        self.ats_incompatible_chars = [
            '•', '–', '—', '…', '©', '®', '™',  # Special characters
            '→', '←', '↑', '↓', '↔',  # Arrows
            '✓', '✗', '✘', '★', '☆',  # Symbols
        ]
    
    def extract_qualifications(self, job_description: str) -> Dict[str, List[str]]:
        """
        Extract required and preferred qualifications from job description.
        
        Args:
            job_description: Job description text
            
        Returns:
            Dictionary with 'required' and 'preferred' qualification lists
        """
        job_lower = job_description.lower()
        qualifications = {
            'required': [],
            'preferred': []
        }
        
        # Common patterns for required qualifications
        required_patterns = [
            r'required[:\s]+(?:skills|qualifications|experience|education)[:\s]*([^\.]+)',
            r'must have[:\s]+([^\.]+)',
            r'essential[:\s]+(?:skills|qualifications)[:\s]*([^\.]+)',
            r'minimum requirements[:\s]*([^\.]+)',
            r'required[:\s]*([^\.]+?)(?:preferred|nice to have|bonus)',
        ]
        
        # Common patterns for preferred qualifications
        preferred_patterns = [
            r'preferred[:\s]+(?:skills|qualifications|experience)[:\s]*([^\.]+)',
            r'nice to have[:\s]+([^\.]+)',
            r'bonus[:\s]+([^\.]+)',
            r'plus[:\s]+([^\.]+)',
            r'preferred[:\s]*([^\.]+)',
        ]
        
        # Extract required qualifications
        for pattern in required_patterns:
            matches = re.finditer(pattern, job_lower, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                text = match.group(1).strip()
                # Extract keywords (words with 2+ characters, excluding common words)
                keywords = self._extract_keywords(text)
                qualifications['required'].extend(keywords)
        
        # Extract preferred qualifications
        for pattern in preferred_patterns:
            matches = re.finditer(pattern, job_lower, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                text = match.group(1).strip()
                keywords = self._extract_keywords(text)
                qualifications['preferred'].extend(keywords)
        
        # If no explicit required/preferred found, extract all technical terms
        if not qualifications['required'] and not qualifications['preferred']:
            all_keywords = self._extract_technical_keywords(job_description)
            qualifications['required'] = all_keywords[:20]  # Top 20 as required
            qualifications['preferred'] = all_keywords[20:40]  # Next 20 as preferred
        
        # Remove duplicates and normalize
        qualifications['required'] = list(set(qualifications['required']))
        qualifications['preferred'] = list(set(qualifications['preferred']))
        
        return qualifications
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract meaningful keywords from text."""
        # Remove punctuation and split into words
        words = re.findall(r'\b[a-zA-Z]{2,}\b', text.lower())
        
        # Common stop words to exclude
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be',
            'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
            'would', 'should', 'could', 'may', 'might', 'must', 'can', 'this',
            'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they',
            'years', 'year', 'experience', 'required', 'preferred', 'skills',
            'ability', 'abilities', 'knowledge', 'understanding'
        }
        
        # Filter out stop words and return unique keywords
        keywords = [w for w in words if w not in stop_words and len(w) > 2]
        return list(set(keywords))
    
    def _extract_technical_keywords(self, text: str) -> List[str]:
        """Extract technical keywords from job description."""
        # Common technical terms patterns
        technical_patterns = [
            r'\b[A-Z]{2,}\b',  # Acronyms (AWS, API, SQL, etc.)
            r'\b\w+\.(js|py|java|ts|jsx|tsx|html|css|sql|sh|yml|yaml|json)\b',  # File extensions
            r'\b\w+\s*(?:framework|library|tool|platform|service|system|language|database|server)\b',  # Tech terms
        ]
        
        keywords = []
        text_lower = text.lower()
        
        # Extract acronyms
        acronyms = re.findall(r'\b[A-Z]{2,}\b', text)
        keywords.extend([a.lower() for a in acronyms])
        
        # Extract technology names (common tech stack)
        common_tech = [
            'python', 'java', 'javascript', 'typescript', 'react', 'angular', 'vue',
            'node', 'express', 'django', 'flask', 'spring', 'laravel', 'rails',
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform', 'ansible',
            'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch',
            'git', 'jenkins', 'ci/cd', 'agile', 'scrum', 'devops',
            'machine learning', 'ai', 'data science', 'big data', 'analytics',
            'rest', 'api', 'graphql', 'microservices', 'serverless',
            'html', 'css', 'sass', 'less', 'bootstrap', 'tailwind',
            'linux', 'unix', 'windows', 'macos',
            'sql', 'nosql', 'etl', 'data pipeline', 'data warehouse'
        ]
        
        for tech in common_tech:
            if tech in text_lower:
                keywords.append(tech)
        
        # Extract from patterns
        for pattern in technical_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            keywords.extend([m.lower() if isinstance(m, str) else m[0].lower() for m in matches])
        
        return list(set(keywords))
    
    def analyze_keyword_matches(self, resume_text: str, qualifications: Dict[str, List[str]]) -> Dict:
        """
        Analyze keyword matches in resume.
        
        Args:
            resume_text: Resume text
            qualifications: Dictionary with 'required' and 'preferred' keywords
            
        Returns:
            Dictionary with match analysis
        """
        resume_lower = resume_text.lower()
        
        required_matches = []
        preferred_matches = []
        missing_required = []
        missing_preferred = []
        
        # Check required keywords
        for keyword in qualifications.get('required', []):
            # Case-insensitive search
            if keyword.lower() in resume_lower:
                # Check if keyword appears in context (not just isolated)
                matches = list(re.finditer(re.escape(keyword.lower()), resume_lower))
                for match in matches:
                    start = max(0, match.start() - 20)
                    end = min(len(resume_lower), match.end() + 20)
                    context = resume_lower[start:end]
                    required_matches.append({
                        'keyword': keyword,
                        'context': context.strip(),
                        'position': match.start()
                    })
            else:
                missing_required.append(keyword)
        
        # Check preferred keywords
        for keyword in qualifications.get('preferred', []):
            if keyword.lower() in resume_lower:
                matches = list(re.finditer(re.escape(keyword.lower()), resume_lower))
                for match in matches:
                    start = max(0, match.start() - 20)
                    end = min(len(resume_lower), match.end() + 20)
                    context = resume_lower[start:end]
                    preferred_matches.append({
                        'keyword': keyword,
                        'context': context.strip(),
                        'position': match.start()
                    })
            else:
                missing_preferred.append(keyword)
        
        # Calculate match percentages
        total_required = len(qualifications.get('required', []))
        total_preferred = len(qualifications.get('preferred', []))
        
        required_match_pct = (len(required_matches) / total_required * 100) if total_required > 0 else 0
        preferred_match_pct = (len(preferred_matches) / total_preferred * 100) if total_preferred > 0 else 0
        
        return {
            'required_matches': required_matches,
            'preferred_matches': preferred_matches,
            'missing_required': missing_required,
            'missing_preferred': missing_preferred,
            'required_match_percentage': round(required_match_pct, 1),
            'preferred_match_percentage': round(preferred_match_pct, 1),
            'total_required': total_required,
            'total_preferred': total_preferred,
            'matched_required': len(required_matches),
            'matched_preferred': len(preferred_matches)
        }
    
    def check_keyword_placement(self, resume_text: str, keyword_matches: Dict) -> Dict:
        """
        Check if keywords are placed naturally (not keyword-stuffed).
        
        Args:
            resume_text: Resume text
            keyword_matches: Result from analyze_keyword_matches
            
        Returns:
            Dictionary with placement analysis
        """
        issues = []
        recommendations = []
        
        resume_lower = resume_text.lower()
        
        # Check for keyword stuffing (same keyword repeated too many times)
        all_keywords = [m['keyword'] for m in keyword_matches.get('required_matches', [])]
        all_keywords.extend([m['keyword'] for m in keyword_matches.get('preferred_matches', [])])
        
        keyword_counts = Counter(all_keywords)
        
        for keyword, count in keyword_counts.items():
            if count > 5:  # More than 5 occurrences might be stuffing
                issues.append({
                    'type': 'keyword_stuffing',
                    'keyword': keyword,
                    'count': count,
                    'severity': 'medium' if count <= 10 else 'high'
                })
                recommendations.append(
                    f"Keyword '{keyword}' appears {count} times. Consider using it more naturally in context."
                )
        
        # Check if keywords appear in meaningful sections
        section_keywords = {
            'skills': ['python', 'java', 'javascript', 'sql', 'aws', 'docker'],
            'experience': ['developed', 'implemented', 'managed', 'led', 'created'],
            'education': ['degree', 'bachelor', 'master', 'phd', 'university', 'college']
        }
        
        # Check keyword density (should be reasonable, not too high)
        total_words = len(resume_lower.split())
        keyword_density = (len(all_keywords) / total_words * 100) if total_words > 0 else 0
        
        if keyword_density > 15:  # More than 15% keyword density
            issues.append({
                'type': 'high_keyword_density',
                'density': round(keyword_density, 1),
                'severity': 'high'
            })
            recommendations.append(
                f"Keyword density is {keyword_density:.1f}%, which is quite high. "
                "Ensure keywords appear naturally in context, not just listed."
            )
        
        return {
            'issues': issues,
            'recommendations': recommendations,
            'keyword_density': round(keyword_density, 1),
            'is_natural': len(issues) == 0
        }
    
    def analyze_formatting(self, resume_text: str) -> Dict:
        """
        Analyze formatting elements that reduce ATS compatibility.
        
        Args:
            resume_text: Resume text
            
        Returns:
            Dictionary with formatting analysis
        """
        issues = []
        recommendations = []
        score_deductions = 0
        
        # Check for HTML tags
        html_tags = re.findall(r'<[^>]+>', resume_text)
        if html_tags:
            issues.append({
                'type': 'html_tags',
                'count': len(html_tags),
                'severity': 'high'
            })
            recommendations.append(
                f"Found {len(html_tags)} HTML tags. ATS systems may not parse these correctly. "
                "Use plain text formatting instead."
            )
            score_deductions += 10
        
        # Check for special characters
        special_char_count = sum(1 for char in resume_text if char in self.ats_incompatible_chars)
        if special_char_count > 10:
            issues.append({
                'type': 'special_characters',
                'count': special_char_count,
                'severity': 'medium'
            })
            recommendations.append(
                f"Found {special_char_count} special characters that may not be ATS-compatible. "
                "Replace with standard characters (e.g., use '-' instead of '–')."
            )
            score_deductions += 5
        
        # Check for tables (in text format, look for patterns)
        table_patterns = [
            r'\|\s*\w+\s*\|\s*\w+\s*\|',  # Pipe-separated tables
            r'\s{3,}\w+\s{3,}\w+',  # Multiple spaces (tab-like)
        ]
        
        for pattern in table_patterns:
            if re.search(pattern, resume_text):
                issues.append({
                    'type': 'table_formatting',
                    'severity': 'medium'
                })
                recommendations.append(
                    "Table-like formatting detected. ATS systems prefer simple, linear text. "
                    "Use bullet points or simple lists instead."
                )
                score_deductions += 5
                break
        
        # Check for section headers (should be ATS-friendly)
        lines = resume_text.split('\n')
        section_headers = []
        for line in lines:
            line_stripped = line.strip().lower()
            if line_stripped and not line_stripped.startswith(('•', '-', '*', '·')):
                # Check if it looks like a section header (all caps, short, ends with colon or is standalone)
                if (line_stripped.isupper() and len(line_stripped.split()) <= 4) or \
                   (line_stripped.endswith(':') and len(line_stripped.split()) <= 4):
                    section_headers.append(line_stripped.rstrip(':'))
        
        non_ats_sections = []
        for header in section_headers:
            if header not in self.ats_friendly_sections:
                non_ats_sections.append(header)
        
        if non_ats_sections:
            issues.append({
                'type': 'non_ats_sections',
                'sections': non_ats_sections,
                'severity': 'low'
            })
            recommendations.append(
                f"Consider using standard section headers like 'EXPERIENCE', 'EDUCATION', 'SKILLS' "
                f"instead of: {', '.join(non_ats_sections[:3])}"
            )
            score_deductions += 2
        
        # Check for headers/footers (often problematic)
        if 'header' in resume_text.lower()[:200] or 'footer' in resume_text.lower()[-200:]:
            issues.append({
                'type': 'header_footer',
                'severity': 'low'
            })
            recommendations.append(
                "Headers and footers may not be parsed correctly by ATS systems. "
                "Include contact information in the main body instead."
            )
            score_deductions += 3
        
        return {
            'issues': issues,
            'recommendations': recommendations,
            'score_deductions': score_deductions,
            'total_issues': len(issues)
        }
    
    def calculate_ats_score(self, keyword_analysis: Dict, placement_analysis: Dict, formatting_analysis: Dict) -> Dict:
        """
        Calculate overall ATS-readiness score.
        
        Args:
            keyword_analysis: Result from analyze_keyword_matches
            placement_analysis: Result from check_keyword_placement
            formatting_analysis: Result from analyze_formatting
            
        Returns:
            Dictionary with ATS score and breakdown
        """
        # Base score components
        required_match_score = keyword_analysis.get('required_match_percentage', 0) * 0.5  # 50% weight
        preferred_match_score = keyword_analysis.get('preferred_match_percentage', 0) * 0.2  # 20% weight
        placement_score = 20 if placement_analysis.get('is_natural', False) else 10  # 20% weight
        formatting_score = max(0, 10 - formatting_analysis.get('score_deductions', 0))  # 10% weight
        
        # Calculate total score
        total_score = required_match_score + preferred_match_score + placement_score + formatting_score
        
        # Determine grade
        if total_score >= 90:
            grade = 'A+'
            status = 'Excellent'
        elif total_score >= 80:
            grade = 'A'
            status = 'Very Good'
        elif total_score >= 70:
            grade = 'B'
            status = 'Good'
        elif total_score >= 60:
            grade = 'C'
            status = 'Fair'
        elif total_score >= 50:
            grade = 'D'
            status = 'Needs Improvement'
        else:
            grade = 'F'
            status = 'Poor'
        
        return {
            'overall_score': round(total_score, 1),
            'grade': grade,
            'status': status,
            'breakdown': {
                'required_keywords': round(required_match_score, 1),
                'preferred_keywords': round(preferred_match_score, 1),
                'keyword_placement': round(placement_score, 1),
                'formatting': round(formatting_score, 1)
            },
            'max_score': 100
        }
    
    def analyze_ats_compliance(self, resume_text: str, job_description: str) -> Dict:
        """
        Complete ATS compliance analysis.
        
        Args:
            resume_text: Resume text
            job_description: Job description text
            
        Returns:
            Complete ATS compliance analysis
        """
        try:
            # Step 1: Extract qualifications
            qualifications = self.extract_qualifications(job_description)
            
            # Step 2: Analyze keyword matches
            keyword_analysis = self.analyze_keyword_matches(resume_text, qualifications)
            
            # Step 3: Check keyword placement
            placement_analysis = self.check_keyword_placement(resume_text, keyword_analysis)
            
            # Step 4: Analyze formatting
            formatting_analysis = self.analyze_formatting(resume_text)
            
            # Step 5: Calculate ATS score
            ats_score = self.calculate_ats_score(keyword_analysis, placement_analysis, formatting_analysis)
            
            # Compile all recommendations
            all_recommendations = []
            
            # Keyword recommendations
            if keyword_analysis.get('missing_required'):
                missing = keyword_analysis['missing_required'][:5]  # Top 5
                all_recommendations.append({
                    'category': 'Missing Keywords',
                    'priority': 'high',
                    'message': f"Add these required keywords naturally: {', '.join(missing)}"
                })
            
            if keyword_analysis.get('required_match_percentage', 0) < 70:
                all_recommendations.append({
                    'category': 'Keyword Coverage',
                    'priority': 'high',
                    'message': f"Only {keyword_analysis['required_match_percentage']:.1f}% of required keywords found. "
                              "Review job description and add missing skills/technologies."
                })
            
            # Placement recommendations
            all_recommendations.extend([
                {
                    'category': 'Keyword Placement',
                    'priority': 'medium' if issue.get('severity') == 'medium' else 'high',
                    'message': rec
                }
                for issue, rec in zip(placement_analysis.get('issues', []), placement_analysis.get('recommendations', []))
            ])
            
            # Formatting recommendations
            all_recommendations.extend([
                {
                    'category': 'Formatting',
                    'priority': issue.get('severity', 'medium'),
                    'message': rec
                }
                for issue, rec in zip(formatting_analysis.get('issues', []), formatting_analysis.get('recommendations', []))
            ])
            
            return {
                'success': True,
                'ats_score': ats_score,
                'qualifications': qualifications,
                'keyword_analysis': keyword_analysis,
                'placement_analysis': placement_analysis,
                'formatting_analysis': formatting_analysis,
                'recommendations': all_recommendations[:10],  # Top 10 recommendations
                'summary': {
                    'required_keywords_found': keyword_analysis.get('matched_required', 0),
                    'required_keywords_total': keyword_analysis.get('total_required', 0),
                    'preferred_keywords_found': keyword_analysis.get('matched_preferred', 0),
                    'preferred_keywords_total': keyword_analysis.get('total_preferred', 0),
                    'formatting_issues': formatting_analysis.get('total_issues', 0),
                    'placement_issues': len(placement_analysis.get('issues', []))
                }
            }
            
        except Exception as e:
            logger.error(f"Error in ATS compliance analysis: {str(e)}")
            return {
                'success': False,
                'error': f"ATS analysis failed: {str(e)}"
            }


# Singleton instance for reuse (optimized for concurrency)
_ats_engine = None

def get_ats_engine() -> ATSComplianceEngine:
    """Get singleton ATS engine instance."""
    global _ats_engine
    if _ats_engine is None:
        _ats_engine = ATSComplianceEngine()
    return _ats_engine

