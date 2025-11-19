"""
INTERMEDIATE LEVEL: Advanced Resume Optimizer
Features:
- PDF/DOCX parsing
- Job description matching
- Resume scoring
- Keyword gap analysis
- Improvement suggestions
"""

import argparse
import sys
from typing import Dict, List, Set, Tuple
from utils.file_parser import parse_resume
from utils.keyword_extractor import KeywordExtractor
from basic_resume_analyzer import BasicResumeAnalyzer


class ResumeOptimizer:
    """Advanced resume optimizer with job description matching."""
    
    def __init__(self, resume_text: str, job_description: str = None):
        self.resume_text = resume_text
        self.job_description = job_description or ""
        self.resume_analyzer = BasicResumeAnalyzer(resume_text)
        self.resume_keywords = KeywordExtractor(resume_text)
        self.job_keywords = KeywordExtractor(job_description) if job_description else None
    
    def calculate_match_score(self) -> Dict:
        """Calculate how well resume matches job description."""
        if not self.job_description:
            return {
                'score': 0,
                'message': 'No job description provided'
            }
        
        # Extract keywords from both
        resume_keyword_set = set([kw[0] for kw in self.resume_keywords.extract_keywords(top_n=100)])
        job_keyword_set = set([kw[0] for kw in self.job_keywords.extract_keywords(top_n=100)])
        
        # Calculate overlap
        matching_keywords = resume_keyword_set.intersection(job_keyword_set)
        missing_keywords = job_keyword_set - resume_keyword_set
        
        # Calculate score (0-100)
        if len(job_keyword_set) == 0:
            score = 0
        else:
            score = (len(matching_keywords) / len(job_keyword_set)) * 100
        
        return {
            'score': round(score, 2),
            'matching_keywords': list(matching_keywords),
            'missing_keywords': list(missing_keywords),
            'match_count': len(matching_keywords),
            'total_job_keywords': len(job_keyword_set)
        }
    
    def analyze_resume_quality(self) -> Dict:
        """Analyze overall resume quality metrics."""
        sections = self.resume_analyzer.get_sections()
        word_count = self.resume_analyzer.get_word_count()
        technical_skills = self.resume_keywords.extract_technical_skills()
        
        # Quality checks
        quality_issues = []
        quality_score = 100
        
        # Check for essential sections
        essential_sections = ['experience', 'education', 'skills']
        missing_sections = [s for s in essential_sections if s not in sections]
        if missing_sections:
            quality_issues.append(f"Missing sections: {', '.join(missing_sections)}")
            quality_score -= 10 * len(missing_sections)
        
        # Check word count (ideal: 400-800 words)
        if word_count < 300:
            quality_issues.append("Resume is too short (recommended: 400-800 words)")
            quality_score -= 15
        elif word_count > 1000:
            quality_issues.append("Resume is too long (recommended: 400-800 words)")
            quality_score -= 10
        
        # Check for technical skills
        if len(technical_skills) < 5:
            quality_issues.append("Consider adding more technical skills")
            quality_score -= 10
        
        # Check for action verbs
        action_verbs = ['developed', 'created', 'implemented', 'designed', 'built',
                       'managed', 'led', 'improved', 'optimized', 'achieved']
        has_action_verbs = any(verb in self.resume_text.lower() for verb in action_verbs)
        if not has_action_verbs:
            quality_issues.append("Use more action verbs (developed, created, implemented, etc.)")
            quality_score -= 10
        
        return {
            'quality_score': max(0, quality_score),
            'word_count': word_count,
            'section_count': len(sections),
            'technical_skills_count': len(technical_skills),
            'technical_skills': list(technical_skills),
            'issues': quality_issues
        }
    
    def generate_suggestions(self) -> List[str]:
        """Generate improvement suggestions."""
        suggestions = []
        
        if not self.job_description:
            return ["Add a job description to get targeted suggestions"]
        
        match_analysis = self.calculate_match_score()
        quality_analysis = self.analyze_resume_quality()
        
        # Match score suggestions
        if match_analysis['score'] < 50:
            suggestions.append(
                f"Low match score ({match_analysis['score']}%). "
                f"Add {len(match_analysis['missing_keywords'][:5])} key missing keywords."
            )
        
        if match_analysis['missing_keywords']:
            top_missing = match_analysis['missing_keywords'][:5]
            suggestions.append(
                f"Consider adding these keywords: {', '.join(top_missing)}"
            )
        
        # Quality suggestions
        suggestions.extend(quality_analysis['issues'])
        
        # Technical skills suggestions
        if self.job_keywords:
            job_tech_skills = self.job_keywords.extract_technical_skills()
            resume_tech_skills = self.resume_keywords.extract_technical_skills()
            missing_tech_skills = job_tech_skills - resume_tech_skills
            
            if missing_tech_skills:
                suggestions.append(
                    f"Add these technical skills mentioned in job description: "
                    f"{', '.join(list(missing_tech_skills)[:5])}"
                )
        
        # Keyword density suggestions
        if self.job_keywords:
            top_job_keywords = [kw[0] for kw in self.job_keywords.extract_keywords(top_n=10)]
            for keyword in top_job_keywords[:3]:
                density = self.resume_keywords.get_keyword_density(keyword)
                if density < 0.1:
                    suggestions.append(
                        f"Increase usage of '{keyword}' (current density: {density:.2f}%)"
                    )
        
        return suggestions
    
    def get_comprehensive_analysis(self) -> Dict:
        """Get comprehensive analysis report."""
        analysis = {
            'resume_quality': self.analyze_resume_quality(),
            'suggestions': self.generate_suggestions(),
            'top_keywords': self.resume_keywords.extract_keywords(top_n=20),
            'technical_skills': list(self.resume_keywords.extract_technical_skills()),
            'sections': self.resume_analyzer.get_sections()
        }
        
        if self.job_description:
            analysis['job_match'] = self.calculate_match_score()
        
        return analysis
    
    def print_report(self):
        """Print a formatted analysis report."""
        analysis = self.get_comprehensive_analysis()
        
        print("\n" + "=" * 70)
        print("RESUME OPTIMIZATION REPORT")
        print("=" * 70)
        
        # Resume Quality
        quality = analysis['resume_quality']
        print(f"\n📊 RESUME QUALITY SCORE: {quality['quality_score']}/100")
        print(f"   Word Count: {quality['word_count']}")
        print(f"   Sections: {quality['section_count']}")
        print(f"   Technical Skills: {quality['technical_skills_count']}")
        
        if quality['issues']:
            print("\n   ⚠️  Issues Found:")
            for issue in quality['issues']:
                print(f"      - {issue}")
        
        # Job Match (if job description provided)
        if 'job_match' in analysis:
            match = analysis['job_match']
            print(f"\n🎯 JOB MATCH SCORE: {match['score']}%")
            print(f"   Matching Keywords: {match['match_count']}/{match['total_job_keywords']}")
            
            if match['matching_keywords']:
                print(f"\n   ✅ Keywords Found in Resume:")
                print(f"      {', '.join(match['matching_keywords'][:10])}")
            
            if match['missing_keywords']:
                print(f"\n   ❌ Missing Keywords (Top 10):")
                print(f"      {', '.join(match['missing_keywords'][:10])}")
        
        # Technical Skills
        if analysis['technical_skills']:
            print(f"\n💻 TECHNICAL SKILLS DETECTED:")
            print(f"   {', '.join(analysis['technical_skills'])}")
        
        # Top Keywords
        print(f"\n🔑 TOP KEYWORDS IN RESUME:")
        for keyword, count in analysis['top_keywords'][:10]:
            print(f"   {keyword}: {count}")
        
        # Suggestions
        if analysis['suggestions']:
            print(f"\n💡 IMPROVEMENT SUGGESTIONS:")
            for i, suggestion in enumerate(analysis['suggestions'], 1):
                print(f"   {i}. {suggestion}")
        
        print("\n" + "=" * 70 + "\n")


def main():
    """Main function for command-line usage."""
    parser = argparse.ArgumentParser(
        description='Resume Optimizer - Analyze and optimize your resume for job applications'
    )
    parser.add_argument(
        '--resume', '-r',
        type=str,
        required=True,
        help='Path to resume file (PDF, DOCX, or TXT)'
    )
    parser.add_argument(
        '--job_description', '-j',
        type=str,
        default=None,
        help='Path to job description file (TXT)'
    )
    
    args = parser.parse_args()
    
    # Parse resume
    print(f"📄 Parsing resume: {args.resume}")
    resume_text = parse_resume(args.resume)
    
    if not resume_text:
        print("❌ Error: Could not parse resume file")
        sys.exit(1)
    
    # Parse job description if provided
    job_description_text = None
    if args.job_description:
        print(f"📋 Parsing job description: {args.job_description}")
        job_description_text = parse_resume(args.job_description)
        if not job_description_text:
            print("⚠️  Warning: Could not parse job description file")
    
    # Analyze
    print("\n🔍 Analyzing resume...")
    optimizer = ResumeOptimizer(resume_text, job_description_text)
    optimizer.print_report()


if __name__ == "__main__":
    main()

