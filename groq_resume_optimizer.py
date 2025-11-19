"""
Groq-Powered Resume Optimizer
Complete tool for optimizing resumes for specific job applications using Groq API.
"""

import argparse
import sys
import os
from typing import Dict, Optional
from utils.file_parser import parse_resume
from utils.groq_optimizer import GroqResumeOptimizer
from resume_optimizer import ResumeOptimizer


class GroqResumeEditor:
    """Complete resume editing tool using Groq API."""
    
    def __init__(self, groq_api_key: Optional[str] = None):
        self.groq_optimizer = GroqResumeOptimizer(groq_api_key)
        self.model = "llama-3.1-70b-versatile"  # Fast and capable model
    
    def optimize_for_job(
        self,
        resume_path: str,
        job_description_path: str,
        output_path: Optional[str] = None,
        optimize_sections: bool = True
    ) -> Dict:
        """
        Optimize resume for a specific job and optionally save the result.
        
        Args:
            resume_path: Path to resume file
            job_description_path: Path to job description file
            output_path: Optional path to save optimized resume
            optimize_sections: Whether to optimize each section individually
        
        Returns:
            Dictionary with optimization results
        """
        print("📄 Loading resume...")
        resume_text = parse_resume(resume_path)
        if not resume_text:
            return {"error": "Could not parse resume file"}
        
        print("📋 Loading job description...")
        job_description = parse_resume(job_description_path)
        if not job_description:
            return {"error": "Could not parse job description file"}
        
        if not self.groq_optimizer.is_available():
            return {"error": "Groq API not available. Set GROQ_API_KEY environment variable."}
        
        print("\n🔍 Analyzing resume against job description...")
        # First, get basic analysis
        basic_optimizer = ResumeOptimizer(resume_text, job_description)
        basic_analysis = basic_optimizer.get_comprehensive_analysis()
        
        print("🤖 Generating AI-powered optimizations with Groq...")
        
        results = {
            "basic_analysis": basic_analysis,
            "optimizations": {}
        }
        
        # Get overall optimization suggestions
        print("  → Analyzing overall resume...")
        overall_optimization = self.groq_optimizer.optimize_resume_for_job(
            resume_text, job_description, self.model
        )
        results["optimizations"]["overall"] = overall_optimization
        
        # Get keyword suggestions
        print("  → Generating keyword suggestions...")
        keyword_suggestions = self.groq_optimizer.generate_keyword_suggestions(
            resume_text, job_description, self.model
        )
        results["optimizations"]["keywords"] = keyword_suggestions
        
        # Optimize individual sections if requested
        if optimize_sections:
            print("  → Optimizing individual sections...")
            sections = basic_analysis.get("sections", {})
            
            for section_name, section_content in sections.items():
                if section_content and len(section_content) > 20:
                    print(f"    • Optimizing {section_name}...")
                    section_opt = self.groq_optimizer.optimize_section(
                        section_name, section_content, job_description, self.model
                    )
                    results["optimizations"][f"section_{section_name}"] = section_opt
        
        # Generate complete optimized resume
        print("  → Creating fully optimized resume...")
        optimized_resume = self.groq_optimizer.create_optimized_resume(
            resume_text, job_description, self.model
        )
        results["optimizations"]["complete_resume"] = optimized_resume
        
        # Save optimized resume if output path provided
        if output_path and "optimized_resume" in optimized_resume:
            print(f"\n💾 Saving optimized resume to {output_path}...")
            try:
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(optimized_resume["optimized_resume"])
                results["saved_to"] = output_path
            except Exception as e:
                results["save_error"] = str(e)
        
        return results
    
    def print_optimization_report(self, results: Dict):
        """Print a comprehensive optimization report."""
        print("\n" + "=" * 80)
        print("RESUME OPTIMIZATION REPORT (Groq-Powered)")
        print("=" * 80)
        
        # Basic analysis
        if "basic_analysis" in results:
            basic = results["basic_analysis"]
            print(f"\n📊 BASIC ANALYSIS")
            print(f"   Quality Score: {basic['resume_quality']['quality_score']}/100")
            if "job_match" in basic:
                print(f"   Job Match Score: {basic['job_match']['score']}%")
        
        # Overall optimization
        if "overall" in results.get("optimizations", {}):
            print(f"\n🤖 AI OPTIMIZATION ANALYSIS")
            overall = results["optimizations"]["overall"]
            if "analysis" in overall:
                print(overall["analysis"][:1000] + "..." if len(overall.get("analysis", "")) > 1000 else overall.get("analysis", ""))
        
        # Keyword suggestions
        if "keywords" in results.get("optimizations", {}):
            print(f"\n🔑 KEYWORD SUGGESTIONS")
            keywords = results["optimizations"]["keywords"]
            if "suggestions" in keywords:
                print(keywords["suggestions"])
        
        # Section optimizations
        section_opts = {
            k: v for k, v in results.get("optimizations", {}).items() 
            if k.startswith("section_")
        }
        if section_opts:
            print(f"\n📝 SECTION OPTIMIZATIONS")
            for section_key, section_data in section_opts.items():
                section_name = section_key.replace("section_", "").title()
                print(f"\n   {section_name}:")
                if "optimized_content" in section_data:
                    content = section_data["optimized_content"]
                    # Show first 300 chars
                    preview = content[:300] + "..." if len(content) > 300 else content
                    print(f"   {preview}")
                if "changes" in section_data and section_data["changes"]:
                    print(f"   Changes made:")
                    for change in section_data["changes"][:5]:  # Show first 5
                        print(f"     • {change}")
        
        # Complete optimized resume
        if "complete_resume" in results.get("optimizations", {}):
            complete = results["optimizations"]["complete_resume"]
            if "optimized_resume" in complete:
                print(f"\n✨ FULLY OPTIMIZED RESUME")
                print("   (Preview - first 500 characters)")
                print("-" * 80)
                resume_preview = complete["optimized_resume"][:500]
                print(resume_preview)
                print("...")
                if "saved_to" in results:
                    print(f"\n💾 Saved to: {results['saved_to']}")
        
        print("\n" + "=" * 80 + "\n")


def main():
    """Main function for command-line usage."""
    parser = argparse.ArgumentParser(
        description='Groq-Powered Resume Optimizer - AI-powered resume optimization for job applications',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic optimization
  python groq_resume_optimizer.py -r resume.pdf -j job.txt
  
  # Save optimized resume
  python groq_resume_optimizer.py -r resume.pdf -j job.txt -o optimized_resume.txt
  
  # Skip section-by-section optimization (faster)
  python groq_resume_optimizer.py -r resume.pdf -j job.txt --no-sections
        """
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
        required=True,
        help='Path to job description file (TXT)'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=str,
        default=None,
        help='Path to save optimized resume (optional)'
    )
    
    parser.add_argument(
        '--no-sections',
        action='store_true',
        help='Skip individual section optimization (faster)'
    )
    
    parser.add_argument(
        '--api-key',
        type=str,
        default=None,
        help='Groq API key (or set GROQ_API_KEY environment variable)'
    )
    
    parser.add_argument(
        '--model',
        type=str,
        default='llama-3.1-70b-versatile',
        help='Groq model to use (default: llama-3.1-70b-versatile)'
    )
    
    args = parser.parse_args()
    
    # Set API key if provided
    if args.api_key:
        os.environ['GROQ_API_KEY'] = args.api_key
    
    # Check for API key
    if not os.getenv('GROQ_API_KEY'):
        print("❌ Error: GROQ_API_KEY not found!")
        print("   Set it as an environment variable or use --api-key flag")
        print("   Get your API key from: https://console.groq.com/keys")
        sys.exit(1)
    
    # Create optimizer
    editor = GroqResumeEditor()
    editor.model = args.model
    
    # Optimize
    results = editor.optimize_for_job(
        args.resume,
        args.job_description,
        args.output,
        optimize_sections=not args.no_sections
    )
    
    # Check for errors
    if "error" in results:
        print(f"❌ Error: {results['error']}")
        sys.exit(1)
    
    # Print report
    editor.print_optimization_report(results)
    
    print("✅ Optimization complete!")


if __name__ == "__main__":
    main()

