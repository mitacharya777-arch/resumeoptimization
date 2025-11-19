#!/usr/bin/env python3
"""
Quick test script to verify the app works
"""

import sys
import json
from app_resume_analyzer import app

def test_app():
    print("Testing Resume Analyzer API...")
    print("=" * 50)
    
    with app.test_client() as client:
        # Test 1: Health check
        print("\n1. Testing /api/health...")
        response = client.get('/api/health')
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.get_json()
            print(f"   ✅ Health check passed: {data.get('status')}")
        else:
            print(f"   ❌ Health check failed")
            return False
        
        # Test 2: Analyze endpoint
        print("\n2. Testing /api/analyze...")
        test_data = {
            "resume_text": "John Doe\nSoftware Engineer\n5 years Python and JavaScript",
            "job_description": "Senior Software Engineer with React, Node.js, AWS"
        }
        response = client.post('/api/analyze', json=test_data)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.get_json()
            print(f"   ✅ Analyze passed")
            print(f"   Match Score: {data.get('match_score')}%")
            print(f"   Show Optimization: {data.get('show_optimization')}")
        else:
            print(f"   ❌ Analyze failed: {response.get_json()}")
            return False
        
        # Test 3: Optimize endpoint
        print("\n3. Testing /api/optimize...")
        response = client.post('/api/optimize', json=test_data)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.get_json()
            print(f"   ✅ Optimize passed")
            print(f"   Has optimized resume: {bool(data.get('optimized_resume'))}")
        else:
            print(f"   ❌ Optimize failed: {response.get_json()}")
            return False
    
    print("\n" + "=" * 50)
    print("✅ All tests passed! App is working correctly.")
    return True

if __name__ == '__main__':
    success = test_app()
    sys.exit(0 if success else 1)

