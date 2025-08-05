#!/usr/bin/env python3
"""
Diagnostic script to identify import and test issues
"""
import sys
import os

def test_imports():
    """Test all critical imports"""
    print("=== Testing Critical Imports ===")
    
    # Test basic Python packages
    try:
        import pandas
        print("✓ pandas imported successfully")
    except ImportError as e:
        print(f"✗ pandas import failed: {e}")
    
    try:
        import openpyxl
        print("✓ openpyxl imported successfully")
    except ImportError as e:
        print(f"✗ openpyxl import failed: {e}")
    
    try:
        import numpy
        print("✓ numpy imported successfully")
    except ImportError as e:
        print(f"✗ numpy import failed: {e}")
    
    try:
        import flask
        print("✓ flask imported successfully")
    except ImportError as e:
        print(f"✗ flask import failed: {e}")
    
    try:
        import pytest
        print("✓ pytest imported successfully")
    except ImportError as e:
        print(f"✗ pytest import failed: {e}")

def test_app_import():
    """Test app import specifically"""
    print("\n=== Testing App Import ===")
    
    # Add current directory to Python path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    
    try:
        from app import app
        print("✓ app imported successfully")
        print(f"  - App name: {app.name}")
        print(f"  - Config keys: {list(app.config.keys())}")
        return True
    except ImportError as e:
        print(f"✗ app import failed: {e}")
        return False
    except Exception as e:
        print(f"✗ app import failed with unexpected error: {e}")
        return False

def test_excel_extractor():
    """Test excelExtractor import"""
    print("\n=== Testing ExcelExtractor Import ===")
    
    try:
        from excelExtractor import ExcelComparator
        print("✓ ExcelComparator imported successfully")
        
        # Test creating an instance
        comparator = ExcelComparator("dummy.xlsx")
        print("✓ ExcelComparator instance created successfully")
        return True
    except ImportError as e:
        print(f"✗ ExcelComparator import failed: {e}")
        return False
    except Exception as e:
        print(f"✗ ExcelComparator failed with unexpected error: {e}")
        return False

def test_environment():
    """Test environment setup"""
    print("\n=== Environment Information ===")
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Python path: {sys.path}")
    
    # Check if uploads directory exists
    uploads_dir = "uploads"
    if os.path.exists(uploads_dir):
        print(f"✓ Uploads directory exists: {uploads_dir}")
    else:
        print(f"✗ Uploads directory missing: {uploads_dir}")
        try:
            os.makedirs(uploads_dir)
            print(f"✓ Created uploads directory: {uploads_dir}")
        except Exception as e:
            print(f"✗ Failed to create uploads directory: {e}")

def run_tests():
    """Run actual tests"""
    print("\n=== Running Tests ===")
    
    try:
        import pytest
        import subprocess
        
        # Run pytest with verbose output
        result = subprocess.run([
            sys.executable, "-m", "pytest", "tests/", "-v", "-s", "--tb=long"
        ], capture_output=True, text=True)
        
        print("Test output:")
        print(result.stdout)
        
        if result.stderr:
            print("Test errors:")
            print(result.stderr)
        
        print(f"Test exit code: {result.returncode}")
        return result.returncode == 0
        
    except Exception as e:
        print(f"✗ Failed to run tests: {e}")
        return False

if __name__ == "__main__":
    print("Starting diagnostic tests...\n")
    
    test_environment()
    test_imports()
    app_ok = test_app_import()
    excel_ok = test_excel_extractor()
    
    if app_ok and excel_ok:
        print("\n=== All imports successful, running tests ===")
        tests_ok = run_tests()
        if tests_ok:
            print("\n✅ All tests passed!")
        else:
            print("\n❌ Tests failed!")
    else:
        print("\n❌ Import tests failed, skipping test execution")
    
    print("\nDiagnostic complete.") 