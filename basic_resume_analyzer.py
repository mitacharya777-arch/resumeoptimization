"""
BASIC LEVEL: Simple Resume Analyzer
This is the starting point - analyzes text-based resumes for keywords and basic metrics.
"""

import re
from collections import Counter
from typing import Dict, List, Tuple


class BasicResumeAnalyzer:
    """Basic resume analyzer for text-based resumes."""
    
    def __init__(self, resume_text: str):
        self.resume_text = resume_text.lower()
        self.words = self._extract_words()
    
    def _extract_words(self) -> List[str]:
        """Extract words from resume text."""
        # Remove special characters and split into words
        words = re.findall(r'\b[a-z]+\b', self.resume_text)
        return words
    
    def get_word_count(self) -> int:
        """Get total word count."""
        return len(self.words)
    
    def get_keywords(self, top_n: int = 20) -> List[Tuple[str, int]]:
        """Get most common keywords."""
        word_freq = Counter(self.words)
        # Filter out common stop words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 
                     'to', 'for', 'of', 'with', 'by', 'from', 'as', 'is', 'was',
                     'are', 'been', 'be', 'have', 'has', 'had', 'do', 'does',
                     'did', 'will', 'would', 'should', 'could', 'may', 'might',
                     'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she',
                     'it', 'we', 'they', 'my', 'your', 'his', 'her', 'its',
                     'our', 'their', 'me', 'him', 'us', 'them'}
        
        filtered_words = {word: count for word, count in word_freq.items() 
                         if word not in stop_words and len(word) > 2}
        
        return Counter(filtered_words).most_common(top_n)
    
    def find_section(self, section_name: str) -> str:
        """Find a specific section in the resume."""
        pattern = rf'{section_name.lower()}\s*:?\s*\n(.*?)(?=\n\w+\s*:|\Z)'
        match = re.search(pattern, self.resume_text, re.IGNORECASE | re.DOTALL)
        return match.group(1).strip() if match else ""
    
    def get_sections(self) -> Dict[str, str]:
        """Extract common resume sections."""
        sections = {}
        section_names = ['experience', 'education', 'skills', 'summary', 
                        'objective', 'projects', 'certifications']
        
        for section in section_names:
            content = self.find_section(section)
            if content:
                sections[section] = content
        
        return sections
    
    def analyze(self) -> Dict:
        """Perform basic analysis."""
        return {
            'word_count': self.get_word_count(),
            'top_keywords': self.get_keywords(),
            'sections': self.get_sections(),
            'section_count': len(self.get_sections())
        }


def main():
    """Example usage of basic resume analyzer."""
    # Sample resume text
    sample_resume = """
    John Doe
    Email: john.doe@email.com
    Phone: (555) 123-4567
    
    SUMMARY
    Experienced software engineer with 5 years of experience in Python, 
    JavaScript, and cloud technologies. Strong background in full-stack 
    development and machine learning.
    
    EXPERIENCE
    Senior Software Engineer | Tech Corp | 2020 - Present
    - Developed scalable web applications using Python and React
    - Led team of 5 developers on multiple projects
    - Implemented CI/CD pipelines using Docker and Kubernetes
    
    Software Engineer | Startup Inc | 2018 - 2020
    - Built RESTful APIs using Flask and Django
    - Worked with PostgreSQL and MongoDB databases
    - Collaborated with cross-functional teams
    
    EDUCATION
    Bachelor of Science in Computer Science
    University of Technology | 2014 - 2018
    
    SKILLS
    Programming Languages: Python, JavaScript, Java, SQL
    Frameworks: React, Django, Flask, Node.js
    Tools: Git, Docker, Kubernetes, AWS, Jenkins
    """
    
    print("=" * 60)
    print("BASIC RESUME ANALYZER")
    print("=" * 60)
    
    analyzer = BasicResumeAnalyzer(sample_resume)
    results = analyzer.analyze()
    
    print(f"\nTotal Word Count: {results['word_count']}")
    print(f"\nSections Found: {results['section_count']}")
    print(f"\nSection Names: {', '.join(results['sections'].keys())}")
    
    print("\nTop Keywords:")
    for keyword, count in results['top_keywords']:
        print(f"  {keyword}: {count}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()

