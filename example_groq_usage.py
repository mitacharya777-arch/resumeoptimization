"""
Example: Using Groq-Powered Resume Optimizer
Demonstrates how to optimize resumes for job applications.
"""

import os
from resume_editor import ResumeEditor
from groq_resume_optimizer import GroqResumeEditor

# Example 1: Single Job Optimization
def example_single_job():
    """Optimize resume for a single job application."""
    print("=" * 70)
    print("Example 1: Single Job Optimization")
    print("=" * 70)
    
    # Make sure GROQ_API_KEY is set
    if not os.getenv('GROQ_API_KEY'):
        print("⚠️  Set GROQ_API_KEY environment variable first!")
        return
    
    editor = ResumeEditor()
    
    result = editor.create_job_specific_resume(
        original_resume_path="sample_resume.txt",  # Your resume file
        job_description_path="sample_job_description.txt",  # Job description
        output_path="optimized_resume_example.txt",
        job_title="Software Engineer",
        company_name="Tech Corp"
    )
    
    if "error" in result:
        print(f"❌ Error: {result['error']}")
    else:
        print(f"✅ Optimized resume saved to: {result['output_path']}")
        print(f"📄 Metadata saved to: {result['metadata_path']}")


# Example 2: Section-by-Section Optimization
def example_section_optimization():
    """Optimize a specific section of the resume."""
    print("\n" + "=" * 70)
    print("Example 2: Section Optimization")
    print("=" * 70)
    
    from utils.groq_optimizer import GroqResumeOptimizer
    
    if not os.getenv('GROQ_API_KEY'):
        print("⚠️  Set GROQ_API_KEY environment variable first!")
        return
    
    optimizer = GroqResumeOptimizer()
    
    # Example: Optimize the Experience section
    experience_section = """
    Software Engineer | Tech Corp | 2020 - Present
    - Developed web applications using Python and React
    - Led team of 5 developers
    - Implemented CI/CD pipelines
    """
    
    job_description = """
    We are looking for a Software Engineer with experience in:
    - Python and JavaScript
    - React framework
    - Cloud technologies (AWS)
    - Team leadership
    - CI/CD pipelines
    """
    
    result = optimizer.optimize_section(
        section_name="Experience",
        section_content=experience_section,
        job_description=job_description
    )
    
    if "error" in result:
        print(f"❌ Error: {result['error']}")
    else:
        print("✨ Optimized Section:")
        print(result["optimized_content"])
        print("\n📝 Changes Made:")
        for change in result["changes"]:
            print(f"  • {change}")


# Example 3: Keyword Suggestions
def example_keyword_suggestions():
    """Get keyword suggestions for a resume."""
    print("\n" + "=" * 70)
    print("Example 3: Keyword Suggestions")
    print("=" * 70)
    
    from utils.groq_optimizer import GroqResumeOptimizer
    
    if not os.getenv('GROQ_API_KEY'):
        print("⚠️  Set GROQ_API_KEY environment variable first!")
        return
    
    optimizer = GroqResumeOptimizer()
    
    resume_text = """
    Software Engineer with 5 years of experience.
    Proficient in Python and web development.
    """
    
    job_description = """
    Looking for Software Engineer with:
    - Python, JavaScript, React
    - AWS cloud experience
    - Docker and Kubernetes
    - Microservices architecture
    """
    
    result = optimizer.generate_keyword_suggestions(
        resume_text=resume_text,
        job_description=job_description
    )
    
    if "error" in result:
        print(f"❌ Error: {result['error']}")
    else:
        print("🔑 Keyword Suggestions:")
        print(result["suggestions"])


# Example 4: Complete Resume Optimization
def example_complete_optimization():
    """Generate a completely optimized resume."""
    print("\n" + "=" * 70)
    print("Example 4: Complete Resume Optimization")
    print("=" * 70)
    
    from utils.groq_optimizer import GroqResumeOptimizer
    from utils.file_parser import parse_resume
    
    if not os.getenv('GROQ_API_KEY'):
        print("⚠️  Set GROQ_API_KEY environment variable first!")
        return
    
    optimizer = GroqResumeOptimizer()
    
    # Load resume and job description
    resume_text = parse_resume("sample_resume.txt")  # Your resume
    job_description = parse_resume("sample_job_description.txt")  # Job description
    
    if not resume_text or not job_description:
        print("⚠️  Make sure sample_resume.txt and sample_job_description.txt exist!")
        return
    
    result = optimizer.create_optimized_resume(
        resume_text=resume_text,
        job_description=job_description
    )
    
    if "error" in result:
        print(f"❌ Error: {result['error']}")
    else:
        print("✨ Optimized Resume (first 500 characters):")
        print("-" * 70)
        print(result["optimized_resume"][:500])
        print("...")
        print("\n💾 Save this to a file to use for your application!")


# Example 5: Batch Processing
def example_batch_processing():
    """Process multiple job applications at once."""
    print("\n" + "=" * 70)
    print("Example 5: Batch Processing")
    print("=" * 70)
    
    if not os.getenv('GROQ_API_KEY'):
        print("⚠️  Set GROQ_API_KEY environment variable first!")
        return
    
    editor = ResumeEditor()
    
    # Create example directory structure
    import os
    os.makedirs("example_jobs", exist_ok=True)
    os.makedirs("example_output", exist_ok=True)
    
    # Create sample job description files
    with open("example_jobs/job1.txt", "w") as f:
        f.write("Software Engineer position at Tech Corp...")
    
    with open("example_jobs/job2.txt", "w") as f:
        f.write("Full Stack Developer at Startup Inc...")
    
    result = editor.batch_optimize(
        original_resume_path="sample_resume.txt",
        job_descriptions_dir="example_jobs",
        output_dir="example_output"
    )
    
    if "error" in result:
        print(f"❌ Error: {result['error']}")
    else:
        print(f"✅ Processed {result['total_jobs']} jobs")
        print(f"   Successful: {result['successful']}")
        print(f"   Failed: {result['failed']}")
        print(f"\n📁 Check the 'example_output' directory for optimized resumes!")


if __name__ == "__main__":
    print("\n🚀 Groq Resume Optimizer - Usage Examples")
    print("=" * 70)
    print("\nNote: These examples require:")
    print("  1. GROQ_API_KEY environment variable set")
    print("  2. Sample files (sample_resume.txt, sample_job_description.txt)")
    print("\n" + "=" * 70)
    
    # Uncomment the example you want to run:
    
    # example_single_job()
    # example_section_optimization()
    # example_keyword_suggestions()
    # example_complete_optimization()
    # example_batch_processing()
    
    print("\n💡 Uncomment the examples in the script to run them!")
    print("📖 See GROQ_GUIDE.md for detailed documentation")

