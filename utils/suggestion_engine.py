"""
Intelligent Suggestion Engine - Silent AI Assistant
Makes smart assumptions, provides confidence-scored suggestions, and learns from user feedback.
Optimized for single comprehensive AI call strategy.
"""

import re
from typing import Dict, List, Tuple, Set, Optional
from collections import Counter, defaultdict
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class SuggestionType(Enum):
    """Types of suggestions based on confidence level."""
    HIGH_CONFIDENCE = "high"  # Auto-apply (90%+ confidence)
    MEDIUM_CONFIDENCE = "medium"  # User approval needed (50-90% confidence)
    NEEDS_INFO = "needs_info"  # Inline micro-questions (<50% confidence)


class SuggestionCategory(Enum):
    """Categories of improvements."""
    VERB_UPGRADE = "verb_upgrade"
    QUANTIFICATION = "quantification"
    STAR_TRANSFORMATION = "star_transformation"
    INDUSTRY_TERMINOLOGY = "industry_terminology"
    REDUNDANCY_FIX = "redundancy_fix"
    IMPACT_AMPLIFICATION = "impact_amplification"
    ACHIEVEMENT_EXTRACTION = "achievement_extraction"
    GRAMMAR_FIX = "grammar_fix"
    FORMATTING = "formatting"


@dataclass
class Suggestion:
    """Represents a single suggestion for improvement."""
    id: str
    category: SuggestionCategory
    type: SuggestionType
    original_text: str
    suggested_text: str
    confidence: float  # 0.0 to 1.0
    reasoning: str
    impact_score: int  # 1-5 stars
    line_number: Optional[int] = None
    section: Optional[str] = None
    context_before: Optional[str] = None
    context_after: Optional[str] = None
    alternatives: Optional[List[str]] = None  # For NEEDS_INFO type
    estimated_value: Optional[str] = None  # For quantification suggestions


class IntelligentSuggestionEngine:
    """
    Intelligent suggestion engine that makes smart assumptions and provides
    confidence-scored suggestions without asking too many questions.
    """
    
    def __init__(self):
        """Initialize the suggestion engine."""
        # Weak verbs that should be upgraded
        self.weak_verbs = {
            'worked on', 'handled', 'did', 'made', 'helped', 'assisted',
            'participated', 'involved', 'responsible for', 'duties included',
            'tasked with', 'assigned to', 'contributed to'
        }
        
        # Strong action verbs by category
        self.strong_verbs = {
            'development': ['developed', 'engineered', 'architected', 'built', 'created', 'designed', 'implemented'],
            'leadership': ['led', 'managed', 'directed', 'orchestrated', 'spearheaded', 'headed', 'oversaw'],
            'improvement': ['optimized', 'enhanced', 'improved', 'streamlined', 'refined', 'upgraded', 'accelerated'],
            'analysis': ['analyzed', 'evaluated', 'assessed', 'diagnosed', 'investigated', 'researched'],
            'collaboration': ['collaborated', 'partnered', 'coordinated', 'facilitated', 'unified'],
            'results': ['achieved', 'delivered', 'generated', 'increased', 'reduced', 'saved', 'boosted']
        }
        
        # Industry standard metrics by role type
        self.role_metrics = {
            'engineer': {
                'team_size': {'junior': 0, 'mid': 2, 'senior': 5, 'lead': 8, 'principal': 12},
                'project_duration': {'junior': 3, 'mid': 6, 'senior': 9, 'lead': 12},
                'performance_improvement': {'junior': 15, 'mid': 25, 'senior': 35, 'lead': 50},
                'scale': {'junior': '1K', 'mid': '10K', 'senior': '100K', 'lead': '1M'}
            },
            'manager': {
                'team_size': {'junior': 3, 'mid': 5, 'senior': 8, 'director': 15},
                'revenue_impact': {'junior': '50K', 'mid': '200K', 'senior': '500K', 'director': '2M'},
                'efficiency_gain': {'junior': 10, 'mid': 20, 'senior': 30, 'director': 40}
            },
            'analyst': {
                'data_volume': {'junior': '1M', 'mid': '10M', 'senior': '100M', 'lead': '1B'},
                'accuracy_improvement': {'junior': 5, 'mid': 10, 'senior': 15, 'lead': 25},
                'time_saved': {'junior': 5, 'mid': 10, 'senior': 20, 'lead': 40}
            }
        }
        
        # Filler phrases to remove
        self.filler_phrases = [
            'responsible for', 'duties included', 'tasked with', 'assigned to',
            'in charge of', 'involved in', 'participated in', 'helped with',
            'worked on', 'contributed to', 'part of', 'member of'
        ]
    
    def analyze_resume_comprehensively(
        self, 
        resume_text: str, 
        job_description: str,
        provider_name: str = "groq",
        api_key: Optional[str] = None
    ) -> Dict:
        """
        Perform comprehensive analysis and generate all suggestions in one AI call.
        
        Args:
            resume_text: Original resume text
            job_description: Job description
            provider_name: AI provider to use
            api_key: Optional API key override
            
        Returns:
            Dictionary with all suggestions categorized by type and confidence
        """
        try:
            # Import here to avoid circular dependencies
            from utils.ai_providers import get_ai_provider
            
            provider = get_ai_provider(provider_name, api_key)
            if not provider or not provider.is_available():
                return {
                    'success': False,
                    'error': f'{provider_name} API not available',
                    'suggestions': []
                }
            
            # Create comprehensive prompt for single AI call
            prompt = self._create_comprehensive_prompt(resume_text, job_description)
            
            # Get AI response - try to use AI for comprehensive suggestions
            # If AI fails, we'll use local suggestions only
            ai_suggestions = []
            try:
                # Use optimize_resume as a fallback - it will generate suggestions in the response
                response = provider.optimize_resume(
                    resume_text, 
                    job_description, 
                    ["Generate comprehensive suggestions with confidence scores"],
                    {}  # No social links needed for suggestions
                )
                
                # Parse AI response and extract suggestions
                ai_suggestions = self._parse_ai_suggestions(response, resume_text, job_description)
            except Exception as e:
                logger.warning(f"AI suggestion generation failed: {e}, using local suggestions only")
                ai_suggestions = []
            
            # Apply local intelligence (verb upgrades, redundancy detection, etc.)
            # This always works and provides fast, reliable suggestions
            local_suggestions = self._generate_local_suggestions(resume_text, job_description)
            
            # Merge AI and local suggestions
            all_suggestions = local_suggestions + ai_suggestions
            
            # Categorize all suggestions (adds type field to each)
            typed_suggestions = self._categorize_suggestions(all_suggestions)
            
            # Rank by impact and confidence
            ranked_suggestions = self._rank_suggestions(typed_suggestions)
            
            return {
                'success': True,
                'suggestions': ranked_suggestions,
                'summary': {
                    'total': len(ranked_suggestions),
                    'high_confidence': len([s for s in ranked_suggestions if s['type'] == 'high']),
                    'medium_confidence': len([s for s in ranked_suggestions if s['type'] == 'medium']),
                    'needs_info': len([s for s in ranked_suggestions if s['type'] == 'needs_info']),
                    'auto_applied': len([s for s in ranked_suggestions if s['type'] == 'high'])
                }
            }
            
        except Exception as e:
            logger.error(f"Error in comprehensive analysis: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'suggestions': []
            }
    
    def _create_comprehensive_prompt(self, resume_text: str, job_description: str) -> str:
        """Create comprehensive prompt for single AI call."""
        return f"""Analyze this resume against the job description and generate ALL possible improvements as structured suggestions.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

INSTRUCTIONS:
1. Identify EVERY improvement opportunity (verbs, quantification, STAR format, terminology, redundancy, impact)
2. For EACH suggestion, provide:
   - Original text (exact phrase)
   - Suggested text (improved version)
   - Confidence level (0.0-1.0): How sure are you this is accurate?
   - Reasoning: Why this change helps
   - Impact score (1-5): How much does this improve the resume?
   - Category: verb_upgrade, quantification, star_transformation, industry_terminology, redundancy_fix, impact_amplification, achievement_extraction

3. CONFIDENCE GUIDELINES:
   - HIGH (0.9-1.0): Safe changes (verb upgrades, grammar, exact terminology matches)
   - MEDIUM (0.5-0.9): Smart guesses (adding numbers, STAR conversions, inferred achievements)
   - NEEDS_INFO (0.0-0.5): Cannot infer (specific metrics, exact team sizes, precise revenue)

4. For QUANTIFICATION suggestions, provide 3 options (conservative, moderate, ambitious) if confidence < 0.7

5. For REDUNDANCY, identify repeated verbs/structures and suggest alternatives

6. For STAR transformations, convert task-focused bullets to Situation-Task-Action-Result format

7. Return as structured JSON with all suggestions.

Format your response as JSON with this structure:
{{
  "suggestions": [
    {{
      "id": "suggestion_1",
      "category": "verb_upgrade",
      "type": "high",
      "original_text": "worked on",
      "suggested_text": "developed",
      "confidence": 0.95,
      "reasoning": "Stronger action verb",
      "impact_score": 3,
      "line_number": 15,
      "section": "EXPERIENCE"
    }}
  ]
}}
"""
    
    def _parse_ai_suggestions(self, ai_response: str, resume_text: str, job_description: str) -> List[Dict]:
        """Parse AI response and extract structured suggestions."""
        suggestions = []
        
        try:
            # Try to extract JSON from response
            import json
            
            # Look for JSON block in response
            json_match = re.search(r'\{[^{}]*"suggestions"[^{}]*\[.*?\]', ai_response, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                data = json.loads(json_str)
                suggestions = data.get('suggestions', [])
            else:
                # Fallback: parse text-based suggestions
                suggestions = self._parse_text_suggestions(ai_response, resume_text)
        except Exception as e:
            logger.warning(f"Could not parse AI suggestions as JSON: {e}")
            suggestions = self._parse_text_suggestions(ai_response, resume_text)
        
        return suggestions
    
    def _parse_text_suggestions(self, text: str, resume_text: str) -> List[Dict]:
        """Fallback: Parse suggestions from text format."""
        suggestions = []
        lines = resume_text.split('\n')
        
        # Look for common patterns in AI response
        # This is a fallback if JSON parsing fails
        # In practice, the AI should return JSON, but we handle text too
        
        return suggestions
    
    def _generate_local_suggestions(self, resume_text: str, job_description: str) -> List[Dict]:
        """Generate suggestions using local intelligence (fast, no API calls)."""
        suggestions = []
        lines = resume_text.split('\n')
        job_lower = job_description.lower()
        resume_lower = resume_text.lower()
        
        # 1. Verb upgrade detection
        verb_suggestions = self._detect_weak_verbs(lines, resume_lower)
        suggestions.extend(verb_suggestions)
        
        # 2. Redundancy detection
        redundancy_suggestions = self._detect_redundancy(lines, resume_lower)
        suggestions.extend(redundancy_suggestions)
        
        # 3. Filler phrase removal
        filler_suggestions = self._detect_filler_phrases(lines, resume_lower)
        suggestions.extend(filler_suggestions)
        
        # 4. Missing quantification detection
        quant_suggestions = self._detect_missing_quantification(lines, resume_lower, job_lower)
        suggestions.extend(quant_suggestions)
        
        return suggestions
    
    def _detect_weak_verbs(self, lines: List[str], resume_lower: str) -> List[Dict]:
        """Detect weak verbs and suggest upgrades."""
        suggestions = []
        verb_counter = Counter()
        
        for idx, line in enumerate(lines):
            line_lower = line.lower()
            for weak_verb in self.weak_verbs:
                if weak_verb in line_lower:
                    # Find appropriate strong verb based on context
                    strong_verb = self._suggest_strong_verb(weak_verb, line_lower)
                    if strong_verb:
                        verb_counter[weak_verb] += 1
                        suggestions.append({
                            'id': f'verb_{idx}_{weak_verb}',
                            'category': 'verb_upgrade',
                            'type': 'high',
                            'original_text': weak_verb,
                            'suggested_text': strong_verb,
                            'confidence': 0.95,
                            'reasoning': f'Replace weak verb "{weak_verb}" with stronger "{strong_verb}"',
                            'impact_score': 3,
                            'line_number': idx,
                            'section': self._detect_section(lines, idx)
                        })
        
        return suggestions
    
    def _suggest_strong_verb(self, weak_verb: str, context: str) -> Optional[str]:
        """Suggest a strong verb based on context."""
        context_lower = context.lower()
        
        # Map weak verbs to strong alternatives
        verb_map = {
            'worked on': 'developed' if 'code' in context_lower or 'software' in context_lower else 'implemented',
            'handled': 'managed' if 'team' in context_lower else 'processed',
            'did': 'executed' if 'project' in context_lower else 'completed',
            'made': 'created' if 'feature' in context_lower else 'developed',
            'helped': 'supported' if 'team' in context_lower else 'facilitated',
            'assisted': 'collaborated' if 'team' in context_lower else 'supported',
            'responsible for': 'managed' if 'team' in context_lower else 'led',
            'duties included': '',  # Remove entirely
            'tasked with': 'assigned to develop' if 'feature' in context_lower else 'responsible for',
        }
        
        return verb_map.get(weak_verb)
    
    def _detect_redundancy(self, lines: List[str], resume_lower: str) -> List[Dict]:
        """Detect repeated verbs and suggest alternatives."""
        suggestions = []
        
        # Extract all verbs from bullet points
        verbs_used = []
        for line in lines:
            if line.strip().startswith(('•', '-', '*')):
                # Extract first verb
                words = line.lower().split()
                if len(words) > 1:
                    first_word = words[1] if words[0] in ['•', '-', '*'] else words[0]
                    if first_word.endswith('ed') or first_word.endswith('ing'):
                        verbs_used.append(first_word)
        
        # Count verb frequency
        verb_counts = Counter(verbs_used)
        
        # Suggest alternatives for overused verbs
        for verb, count in verb_counts.items():
            if count > 3:  # Used more than 3 times
                alternatives = self._get_verb_alternatives(verb)
                if alternatives:
                    suggestions.append({
                        'id': f'redundancy_{verb}',
                        'category': 'redundancy_fix',
                        'type': 'medium',
                        'original_text': verb,
                        'suggested_text': alternatives[0],
                        'confidence': 0.75,
                        'reasoning': f'Verb "{verb}" used {count} times. Consider varying with: {", ".join(alternatives[:3])}',
                        'impact_score': 2,
                        'alternatives': alternatives[:5],
                        'section': 'EXPERIENCE'
                    })
        
        return suggestions
    
    def _get_verb_alternatives(self, verb: str) -> List[str]:
        """Get alternative verbs to avoid repetition."""
        # Common verb alternatives
        alternatives_map = {
            'developed': ['engineered', 'architected', 'built', 'created', 'designed'],
            'managed': ['led', 'directed', 'orchestrated', 'spearheaded', 'oversaw'],
            'improved': ['optimized', 'enhanced', 'streamlined', 'refined', 'upgraded'],
            'created': ['developed', 'built', 'designed', 'engineered', 'established'],
            'implemented': ['deployed', 'executed', 'integrated', 'introduced', 'launched'],
            'analyzed': ['evaluated', 'assessed', 'diagnosed', 'investigated', 'examined']
        }
        
        # Check all categories
        for category, verbs in self.strong_verbs.items():
            if verb in verbs:
                return [v for v in verbs if v != verb]
        
        return alternatives_map.get(verb, [])
    
    def _detect_filler_phrases(self, lines: List[str], resume_lower: str) -> List[Dict]:
        """Detect and suggest removal of filler phrases."""
        suggestions = []
        
        for idx, line in enumerate(lines):
            line_lower = line.lower()
            for filler in self.filler_phrases:
                if filler in line_lower:
                    # Remove filler and clean up
                    cleaned = re.sub(rf'\b{re.escape(filler)}\b\s*', '', line, flags=re.IGNORECASE)
                    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
                    
                    if cleaned != line:
                        suggestions.append({
                            'id': f'filler_{idx}_{filler}',
                            'category': 'grammar_fix',
                            'type': 'high',
                            'original_text': line,
                            'suggested_text': cleaned,
                            'confidence': 0.98,
                            'reasoning': f'Remove filler phrase "{filler}" for more direct language',
                            'impact_score': 2,
                            'line_number': idx,
                            'section': self._detect_section(lines, idx)
                        })
        
        return suggestions
    
    def _detect_missing_quantification(self, lines: List[str], resume_lower: str, job_lower: str) -> List[Dict]:
        """Detect bullets missing quantification and suggest additions."""
        suggestions = []
        
        # Patterns that suggest missing numbers
        quant_patterns = [
            (r'\bimproved\b.*?(?!\d)', 'performance improvement'),
            (r'\bmanaged\b.*?(?!\d)', 'team size'),
            (r'\bincreased\b.*?(?!\d)', 'percentage/amount'),
            (r'\breduced\b.*?(?!\d)', 'percentage/time'),
            (r'\bdelivered\b.*?(?!\d)', 'project count'),
            (r'\bserved\b.*?(?!\d)', 'user count'),
        ]
        
        for idx, line in enumerate(lines):
            if line.strip().startswith(('•', '-', '*')):
                line_lower = line.lower()
                for pattern, quant_type in quant_patterns:
                    if re.search(pattern, line_lower) and not re.search(r'\d+', line):
                        # Suggest quantification
                        suggestion = self._suggest_quantification(line, quant_type, job_lower)
                        if suggestion:
                            suggestions.append(suggestion)
                            break
        
        return suggestions
    
    def _suggest_quantification(self, line: str, quant_type: str, job_lower: str) -> Optional[Dict]:
        """Suggest quantification for a line."""
        # Infer role level from context
        role_level = self._infer_role_level(job_lower)
        
        # Generate conservative, moderate, and ambitious options
        options = []
        
        if 'team' in quant_type.lower():
            sizes = {'junior': [2, 3], 'mid': [4, 5], 'senior': [6, 8], 'lead': [10, 12]}
            team_sizes = sizes.get(role_level, [5, 6])
            options = [f"{team_sizes[0]}", f"{team_sizes[1]}", f"{team_sizes[1]}+"]
        elif 'improvement' in quant_type.lower():
            improvements = {'junior': [15, 20], 'mid': [25, 30], 'senior': [35, 40], 'lead': [45, 50]}
            percents = improvements.get(role_level, [25, 30])
            options = [f"{percents[0]}%", f"{percents[1]}%", f"{percents[1]}+%"]
        elif 'user' in quant_type.lower() or 'served' in quant_type.lower():
            scales = {'junior': ['1K', '5K'], 'mid': ['10K', '50K'], 'senior': ['100K', '500K'], 'lead': ['1M', '5M']}
            user_counts = scales.get(role_level, ['10K', '50K'])
            options = [f"{user_counts[0]}", f"{user_counts[1]}", f"{user_counts[1]}+"]
        else:
            return None
        
        return {
            'id': f'quant_{hash(line)}',
            'category': 'quantification',
            'type': 'needs_info',
            'original_text': line,
            'suggested_text': line,  # Will be updated based on user choice
            'confidence': 0.4,
            'reasoning': f'Add {quant_type} to strengthen this bullet point',
            'impact_score': 5,
            'alternatives': options,
            'estimated_value': options[1]  # Moderate option as default
        }
    
    def _infer_role_level(self, job_lower: str) -> str:
        """Infer role level from job description."""
        if any(word in job_lower for word in ['junior', 'entry', 'associate', 'intern']):
            return 'junior'
        elif any(word in job_lower for word in ['senior', 'sr.', 'lead', 'principal', 'staff']):
            return 'senior'
        elif any(word in job_lower for word in ['manager', 'director', 'head', 'chief']):
            return 'lead'
        else:
            return 'mid'
    
    def _detect_section(self, lines: List[str], line_idx: int) -> str:
        """Detect which section a line belongs to."""
        sections = ['SUMMARY', 'EXPERIENCE', 'EDUCATION', 'SKILLS', 'PROJECTS']
        
        # Look backwards for section header
        for i in range(line_idx, max(0, line_idx - 10), -1):
            line_upper = lines[i].upper().strip()
            for section in sections:
                if section in line_upper:
                    return section
        
        return 'UNKNOWN'
    
    def _categorize_suggestions(self, suggestions: List[Dict]) -> List[Dict]:
        """Categorize suggestions by type - adds type field to each suggestion."""
        typed_suggestions = []
        
        for suggestion in suggestions:
            if not isinstance(suggestion, dict):
                continue
                
            conf = suggestion.get('confidence', 0.5)
            sug_type = suggestion.get('type', 'medium')
            
            # Override type based on confidence if not explicitly set
            if 'type' not in suggestion or not suggestion.get('type'):
                if conf >= 0.9:
                    sug_type = 'high'
                elif conf >= 0.5:
                    sug_type = 'medium'
                else:
                    sug_type = 'needs_info'
            
            suggestion['type'] = sug_type
            typed_suggestions.append(suggestion)
        
        return typed_suggestions
    
    def _merge_suggestions(self, ai_suggestions: List[Dict], local_suggestions: List[Dict]) -> List[Dict]:
        """Merge AI and local suggestions, removing duplicates."""
        all_suggestions = []
        seen = set()
        
        # Add all suggestions, removing duplicates
        for sug in ai_suggestions + local_suggestions:
            if isinstance(sug, dict):
                key = (sug.get('original_text', ''), sug.get('line_number'))
                if key not in seen:
                    all_suggestions.append(sug)
                    seen.add(key)
        
        return all_suggestions
    
    def _rank_suggestions(self, suggestions: List[Dict]) -> List[Dict]:
        """Rank suggestions by impact score and confidence."""
        # Sort by impact_score (descending), then confidence (descending)
        ranked = sorted(
            suggestions,
            key=lambda x: (x.get('impact_score', 0), x.get('confidence', 0)),
            reverse=True
        )
        
        # Add sequential IDs
        for idx, sug in enumerate(ranked):
            if 'id' not in sug or not sug['id']:
                sug['id'] = f'suggestion_{idx + 1}'
        
        return ranked
    
    def apply_suggestions(
        self, 
        resume_text: str, 
        accepted_suggestions: List[str],
        suggestion_map: Dict[str, Dict]
    ) -> str:
        """
        Apply accepted suggestions to resume text.
        
        Args:
            resume_text: Original resume text
            accepted_suggestions: List of suggestion IDs to apply
            suggestion_map: Dictionary mapping suggestion IDs to suggestion data
            
        Returns:
            Updated resume text with suggestions applied
        """
        lines = resume_text.split('\n')
        applied_count = 0
        
        for sug_id in accepted_suggestions:
            if sug_id in suggestion_map:
                suggestion = suggestion_map[sug_id]
                line_num = suggestion.get('line_number')
                original = suggestion.get('original_text', '')
                suggested = suggestion.get('suggested_text', '')
                
                if line_num is not None and line_num < len(lines):
                    # Apply suggestion to specific line
                    if original in lines[line_num]:
                        lines[line_num] = lines[line_num].replace(original, suggested, 1)
                        applied_count += 1
                else:
                    # Apply globally (for redundancy fixes, etc.)
                    for idx, line in enumerate(lines):
                        if original.lower() in line.lower():
                            lines[idx] = re.sub(
                                re.escape(original),
                                suggested,
                                line,
                                flags=re.IGNORECASE,
                                count=1
                            )
                            applied_count += 1
                            break
        
        return '\n'.join(lines)


# Singleton instance
_suggestion_engine = None

def get_suggestion_engine() -> IntelligentSuggestionEngine:
    """Get singleton suggestion engine instance."""
    global _suggestion_engine
    if _suggestion_engine is None:
        _suggestion_engine = IntelligentSuggestionEngine()
    return _suggestion_engine

