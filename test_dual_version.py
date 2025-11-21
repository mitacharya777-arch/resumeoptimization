#!/usr/bin/env python3
"""
Test script to verify dual-version resume system is working.
This checks that we get both 'optimized_resume' (with AI commentary)
and 'download_resume' (clean version) from the API.
"""
import requests
import json

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

def test_dual_version():
    """Test the dual-version resume system."""
    base_url = "http://localhost:5011"

    print("=" * 80)
    print("🧪 TESTING DUAL-VERSION RESUME SYSTEM")
    print("=" * 80)

    # Step 1: Upload resume
    print("\n📤 Step 1: Uploading resume...")
    files = {'file': ('test_resume.txt', SAMPLE_RESUME, 'text/plain')}
    response = requests.post(f"{base_url}/api/upload-resume", files=files)

    if response.status_code != 200:
        print(f"❌ Upload failed: {response.text}")
        return

    print(f"✅ Resume uploaded successfully")

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

    # Step 3: Optimize resume
    print("\n⚡ Step 3: Running optimization...")
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

    # Check for dual versions
    print("\n📊 DUAL-VERSION CHECK:")
    print("=" * 80)

    has_optimized = 'optimized_resume' in optimize_data
    has_download = 'download_resume' in optimize_data

    print(f"✅ 'optimized_resume' present: {has_optimized}")
    print(f"✅ 'download_resume' present: {has_download}")

    if has_optimized and has_download:
        optimized = optimize_data['optimized_resume']
        download = optimize_data['download_resume']

        print(f"\n📏 Length comparison:")
        print(f"   Optimized (preview) length: {len(optimized)} characters")
        print(f"   Download (clean) length: {len(download)} characters")
        print(f"   Difference: {len(optimized) - len(download)} characters")

        # Check for AI commentary markers
        commentary_markers = [
            "I've made the following adjustments",
            "I have made the following adjustments",
            "The final resume is",
            "This resume is polished",
            "effectively showcases",
            "strong candidate for passing"
        ]

        has_commentary_in_optimized = any(marker.lower() in optimized.lower() for marker in commentary_markers)
        has_commentary_in_download = any(marker.lower() in download.lower() for marker in commentary_markers)

        print(f"\n🔍 Commentary detection:")
        print(f"   Commentary in optimized (preview): {has_commentary_in_optimized}")
        print(f"   Commentary in download (clean): {has_commentary_in_download}")

        # Show last 300 characters of each
        print(f"\n📝 Last 300 characters of OPTIMIZED (preview):")
        print(f"   ...{optimized[-300:]}")

        print(f"\n📝 Last 300 characters of DOWNLOAD (clean):")
        print(f"   ...{download[-300:]}")

        # Verdict
        print("\n" + "=" * 80)
        if has_commentary_in_optimized and not has_commentary_in_download:
            print("✅ DUAL-VERSION SYSTEM WORKING CORRECTLY!")
            print("   Preview has AI commentary, download is clean.")
        elif not has_commentary_in_optimized and not has_commentary_in_download:
            print("⚠️  NO COMMENTARY DETECTED IN EITHER VERSION")
            print("   AI may not have added commentary, or detection failed.")
        elif has_commentary_in_download:
            print("❌ DUAL-VERSION SYSTEM NOT WORKING!")
            print("   Download version still contains AI commentary.")
        print("=" * 80)

    else:
        print("\n❌ DUAL-VERSION SYSTEM NOT WORKING!")
        print("   Missing one or both version fields in response.")
        print(f"   Available keys: {list(optimize_data.keys())}")

if __name__ == "__main__":
    try:
        test_dual_version()
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to Flask server at http://localhost:5011")
        print("   Please ensure the server is running")
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
