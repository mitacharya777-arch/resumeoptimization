"""
Advanced keyword extraction using NLP techniques.
"""

import re
from collections import Counter
from typing import List, Set, Tuple


class KeywordExtractor:
    """Extract and analyze keywords from text."""
    
    # Common stop words
    STOP_WORDS = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'been', 'be',
        'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'should',
        'could', 'may', 'might', 'this', 'that', 'these', 'those', 'i', 'you',
        'he', 'she', 'it', 'we', 'they', 'my', 'your', 'his', 'her', 'its',
        'our', 'their', 'me', 'him', 'us', 'them', 'am', 'is', 'are', 'was',
        'were', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does',
        'did', 'doing', 'will', 'would', 'should', 'could', 'may', 'might',
        'must', 'can', 'cannot', 'shall', 'ought'
    }
    
    # Technical skills keywords (common in tech resumes)
    TECH_KEYWORDS = {
        'python', 'java', 'javascript', 'typescript', 'react', 'angular', 'vue',
        'node', 'django', 'flask', 'spring', 'express', 'sql', 'nosql', 'mongodb',
        'postgresql', 'mysql', 'aws', 'azure', 'gcp', 'docker', 'kubernetes',
        'git', 'jenkins', 'ci/cd', 'agile', 'scrum', 'rest', 'api', 'microservices',
        'machine learning', 'ai', 'data science', 'tensorflow', 'pytorch', 'pandas',
        'numpy', 'linux', 'unix', 'html', 'css', 'sass', 'redux', 'graphql'
    }
    
    def __init__(self, text: str):
        self.text = text.lower()
        self.words = self._extract_words()
    
    def _extract_words(self) -> List[str]:
        """Extract words from text."""
        words = re.findall(r'\b[a-z]+\b', self.text)
        return words
    
    def extract_keywords(self, min_length: int = 3, top_n: int = 50) -> List[Tuple[str, int]]:
        """Extract most common keywords."""
        word_freq = Counter(self.words)
        filtered_words = {
            word: count for word, count in word_freq.items()
            if word not in self.STOP_WORDS and len(word) >= min_length
        }
        return Counter(filtered_words).most_common(top_n)
    
    def extract_technical_skills(self) -> Set[str]:
        """Extract technical skills from resume."""
        found_skills = set()
        text_lower = self.text.lower()
        
        for skill in self.TECH_KEYWORDS:
            if skill in text_lower:
                found_skills.add(skill)
        
        return found_skills
    
    def extract_phrases(self, min_words: int = 2, max_words: int = 3) -> List[Tuple[str, int]]:
        """Extract common phrases (n-grams)."""
        phrases = []
        words = self.words
        
        for n in range(min_words, max_words + 1):
            for i in range(len(words) - n + 1):
                phrase = ' '.join(words[i:i+n])
                # Filter out phrases with stop words
                if not any(word in self.STOP_WORDS for word in phrase.split()):
                    phrases.append(phrase)
        
        return Counter(phrases).most_common(20)
    
    def get_keyword_density(self, keyword: str) -> float:
        """Calculate keyword density in text."""
        keyword_lower = keyword.lower()
        count = self.text.count(keyword_lower)
        total_words = len(self.words)
        return (count / total_words * 100) if total_words > 0 else 0.0

