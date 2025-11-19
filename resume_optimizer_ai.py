"""
ADVANCED LEVEL with AI: Resume Optimizer with AI-Powered Suggestions
This version includes OpenAI integration for intelligent recommendations.
"""

import argparse
import sys
from resume_optimizer import ResumeOptimizer
from utils.file_parser import parse_resume
from utils.ai_suggestions import AISuggestions


class AIResumeOptimizer(ResumeOptimizer):
    """Resume optimizer with AI-powered suggestions."""
    
    def __init__(self, resume_text: str, job_description: str = None, use_ai: bool = True):
        super().__init__(resume_text, job_description)
        self.ai_suggestions = AISuggestions() if use_ai else None
        self.use_ai = use_ai and self.ai_suggestions.is_available() if self.ai_suggestions else False
    
    def get_comprehensive_analysis(self):
        """Get comprehensive analysis with AI suggestions."""
        analysis = super().get_comprehensive_analysis()
        
        # Add AI suggestions if available
        if self.use_ai:
            print("🤖 Generating AI-powered suggestions...")
            ai_suggestions = self.ai_suggestions.generate_suggestions(
                self.resume_text,
                self.job_description,
                analysis
            )
            analysis['ai_suggestions'] = ai_suggestions
        
        return analysis
    
    def print_report(self):
        """Print a formatted analysis report with AI suggestions."""
        analysis = self.get_comprehensive_analysis()
        
        # Print standard report
        super().print_report()
        
        # Add AI suggestions if available
        if self.use_ai and 'ai_suggestions' in analysis:
            print("\n🤖 AI-POWERED SUGGESTIONS:")
            print("-" * 70)
            for i, suggestion in enumerate(analysis['ai_suggestions'], 1):
                print(f"   {i}. {suggestion}")
            print("=" * 70 + "\n")


def main():
    """Main function for command-line usage with AI."""
    parser = argparse.ArgumentParser(
        description='AI-Powered Resume Optimizer - Analyze and optimize your resume with AI'
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
    parser.add_argument(
        '--no-ai',
        action='store_true',
        help='Disable AI-powered suggestions'
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
    
    # Analyze with AI
    print("\n🔍 Analyzing resume...")
    optimizer = AIResumeOptimizer(resume_text, job_description_text, use_ai=not args.no_ai)
    optimizer.print_report()


if __name__ == "__main__":
    main()

