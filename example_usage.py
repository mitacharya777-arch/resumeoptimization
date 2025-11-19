"""
Example usage scripts for different levels of the Resume Optimizer.
"""

# ============================================================================
# BASIC LEVEL: Simple text analysis
# ============================================================================

def basic_example():
    """Example of basic resume analyzer."""
    from basic_resume_analyzer import BasicResumeAnalyzer
    
    resume_text = """
    John Doe
    Software Engineer
    
    SUMMARY
    Experienced software engineer with expertise in Python and web development.
    
    EXPERIENCE
    Senior Developer | Tech Corp | 2020-Present
    - Developed web applications using Python and React
    - Led team of developers
    
    SKILLS
    Python, JavaScript, React, SQL
    """
    
    analyzer = BasicResumeAnalyzer(resume_text)
    results = analyzer.analyze()
    
    print("Basic Analysis Results:")
    print(f"Word Count: {results['word_count']}")
    print(f"Top Keywords: {results['top_keywords'][:5]}")


# ============================================================================
# INTERMEDIATE LEVEL: File parsing and job matching
# ============================================================================

def intermediate_example():
    """Example of intermediate resume optimizer."""
    from resume_optimizer import ResumeOptimizer
    
    resume_text = """
    Software Engineer with 5 years of experience in Python, JavaScript, and cloud technologies.
    """
    
    job_description = """
    We are looking for a Software Engineer with experience in:
    - Python and JavaScript
    - React framework
    - AWS cloud services
    - Docker and Kubernetes
    """
    
    optimizer = ResumeOptimizer(resume_text, job_description)
    analysis = optimizer.get_comprehensive_analysis()
    
    print("\nIntermediate Analysis:")
    print(f"Quality Score: {analysis['resume_quality']['quality_score']}")
    if 'job_match' in analysis:
        print(f"Job Match Score: {analysis['job_match']['score']}%")


# ============================================================================
# ADVANCED LEVEL: With AI suggestions
# ============================================================================

def advanced_example():
    """Example of AI-powered resume optimizer."""
    from resume_optimizer_ai import AIResumeOptimizer
    
    resume_text = """
    Software Engineer with experience in Python and web development.
    """
    
    job_description = """
    Looking for a Software Engineer with Python, React, and AWS experience.
    """
    
    optimizer = AIResumeOptimizer(resume_text, job_description, use_ai=True)
    analysis = optimizer.get_comprehensive_analysis()
    
    print("\nAdvanced Analysis with AI:")
    if 'ai_suggestions' in analysis:
        print("AI Suggestions:")
        for suggestion in analysis['ai_suggestions']:
            print(f"  - {suggestion}")


if __name__ == "__main__":
    print("=" * 70)
    print("RESUME OPTIMIZER - EXAMPLE USAGE")
    print("=" * 70)
    
    print("\n1. Basic Example:")
    basic_example()
    
    print("\n2. Intermediate Example:")
    intermediate_example()
    
    print("\n3. Advanced Example (requires OpenAI API key):")
    advanced_example()

