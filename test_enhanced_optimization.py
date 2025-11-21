#!/usr/bin/env python3
"""
Test script to verify enhanced multi-stage optimization is working.
"""
import requests
import json
import os

# Test data
SAMPLE_RESUME = """
John Doe
Software Engineer
Email: john@example.com | Phone: (555) 123-4567 | Location: San Francisco, CA

SUMMARY
Experienced software engineer with 5 years of experience in full-stack development.

EXPERIENCE
Senior Software Engineer, Tech Corp (2020-Present)
- Developed web applications using React and Node.js
- Led team of 3 engineers
- Improved system performance by 40%

Software Engineer, StartupXYZ (2018-2020)
- Built RESTful APIs using Python and Flask
- Implemented CI/CD pipelines
- Collaborated with cross-functional teams

EDUCATION
Bachelor of Science in Computer Science, State University (2018)

SKILLS
Python, JavaScript, React, Node.js, Flask, Docker, AWS
"""

SAMPLE_JOB_DESCRIPTION = """
Senior Software Engineer - Machine Learning

Company: AI Innovations Inc.
Location: Remote

We are seeking a Senior Software Engineer with strong experience in machine learning
and Python to join our AI team. The ideal candidate will have 5+ years of software
engineering experience with at least 2 years working on ML projects.

Requirements:
- 5+ years of software engineering experience
- Strong proficiency in Python, TensorFlow, PyTorch
- Experience with REST APIs and microservices
- Cloud experience (AWS, GCP, or Azure)
- Machine learning model deployment experience
- Strong communication and leadership skills

Preferred:
- MS or PhD in Computer Science or related field
- Experience with MLOps and model monitoring
- Kubernetes and Docker experience
"""

def test_enhanced_optimization():
    """Test the enhanced multi-stage optimization."""
    base_url = "http://localhost:5011"

    print("=" * 80)
    print("🧪 TESTING ENHANCED MULTI-STAGE OPTIMIZATION")
    print("=" * 80)

    # Step 1: Upload resume
    print("\n📤 Step 1: Uploading resume...")
    files = {'file': ('test_resume.txt', SAMPLE_RESUME, 'text/plain')}
    response = requests.post(f"{base_url}/api/upload-resume", files=files)

    if response.status_code != 200:
        print(f"❌ Upload failed: {response.text}")
        return

    upload_data = response.json()
    print(f"✅ Resume uploaded successfully")
    print(f"   Word count: {upload_data.get('word_count')}")

    # Step 2: Analyze resume
    print("\n🔍 Step 2: Analyzing resume...")
    analyze_payload = {
        'resume_text': SAMPLE_RESUME,
        'job_description': SAMPLE_JOB_DESCRIPTION,
        'provider': 'groq'
    }
    response = requests.post(f"{base_url}/api/analyze", json=analyze_payload)

    if response.status_code != 200:
        print(f"❌ Analysis failed: {response.text}")
        return

    analysis_data = response.json()
    print(f"✅ Analysis completed")
    print(f"   Match score: {analysis_data.get('analysis', {}).get('match_score', 'N/A')}%")

    # Step 3: Optimize resume
    print("\n⚡ Step 3: Running enhanced optimization...")
    optimize_payload = {
        'resume_text': SAMPLE_RESUME,
        'job_description': SAMPLE_JOB_DESCRIPTION,
        'suggestions': analysis_data.get('analysis', {}).get('suggestions', []),
        'provider': 'groq',
        'template': 'professional_modern'
    }
    response = requests.post(f"{base_url}/api/optimize", json=optimize_payload)

    if response.status_code != 200:
        print(f"❌ Optimization failed: {response.text}")
        return

    optimize_data = response.json()

    # Check for enhanced optimization
    print("\n📊 RESULTS:")
    print("=" * 80)

    if 'enhanced_optimization' in optimize_data:
        enhanced = optimize_data['enhanced_optimization']

        print("✅ ENHANCED OPTIMIZATION ENABLED!")
        print()

        # Job Analysis
        if 'job_analysis' in enhanced:
            job_analysis = enhanced['job_analysis']
            print("🎯 JOB ANALYSIS:")
            print(f"   Industry: {job_analysis.get('industry', 'N/A')}")
            print(f"   Seniority Level: {job_analysis.get('seniority_level', 'N/A')}")
            print(f"   Years of Experience: {job_analysis.get('years_of_experience', 'N/A')}")
            print(f"   Required Skills: {len(job_analysis.get('required_skills', []))} skills")
            if job_analysis.get('required_skills'):
                print(f"      Top 5: {', '.join(job_analysis.get('required_skills', [])[:5])}")
            print(f"   Critical Keywords: {len(job_analysis.get('critical_keywords', []))} keywords")
            if job_analysis.get('critical_keywords'):
                print(f"      Top 5: {', '.join(job_analysis.get('critical_keywords', [])[:5])}")

        print()

        # ATS Score
        if 'ats_score' in enhanced:
            ats_score = enhanced['ats_score']
            print("📈 ATS COMPATIBILITY SCORE:")
            print(f"   Overall Score: {ats_score.get('overall_score', 'N/A')}/100")
            print(f"   Keyword Match: {ats_score.get('keyword_match', 'N/A')}/100")
            print(f"   Format Score: {ats_score.get('format_score', 'N/A')}/100")
            print(f"   Section Score: {ats_score.get('section_score', 'N/A')}/100")

            if 'recommendations' in ats_score and ats_score['recommendations']:
                print(f"\n   📋 Recommendations ({len(ats_score['recommendations'])}):")
                for i, rec in enumerate(ats_score['recommendations'][:3], 1):
                    print(f"      {i}. {rec}")

        print()

        # Optimization Stages
        if 'optimization_stages' in enhanced:
            stages = enhanced['optimization_stages']
            print("🔄 OPTIMIZATION STAGES:")
            for stage_key, stage_value in stages.items():
                print(f"   {stage_key}: {stage_value}")

        print()
        print("=" * 80)
        print("✅ ENHANCED OPTIMIZATION TEST PASSED!")
        print("=" * 80)

    else:
        print("❌ ENHANCED OPTIMIZATION NOT ENABLED")
        print("   Standard optimization was used instead")
        print("   This might indicate the enhanced methods are not available")

    # Print resume length comparison
    print(f"\nOptimized resume length: {len(optimize_data.get('optimized_resume', ''))} characters")
    print(f"Original resume length: {len(SAMPLE_RESUME)} characters")

if __name__ == "__main__":
    try:
        test_enhanced_optimization()
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to Flask server at http://localhost:5011")
        print("   Please ensure the server is running")
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
