"""
Basic tests that don't require the full Flask app import
"""
import pytest
import os
import sys

def test_python_environment():
    """Test basic Python environment"""
    assert True, "Python environment is working"

def test_import_flask():
    """Test Flask import"""
    import flask
    assert flask is not None
    print("✓ Flask imported successfully")

def test_import_pandas():
    """Test pandas import"""
    try:
        import pandas
        assert pandas is not None
        print("✓ pandas imported successfully")
    except ImportError as e:
        pytest.skip(f"pandas not available: {e}")

def test_import_openpyxl():
    """Test openpyxl import"""
    try:
        import openpyxl
        assert openpyxl is not None
        print("✓ openpyxl imported successfully")
    except ImportError as e:
        pytest.skip(f"openpyxl not available: {e}")

def test_import_numpy():
    """Test numpy import"""
    try:
        import numpy
        assert numpy is not None
        print("✓ numpy imported successfully")
    except ImportError as e:
        pytest.skip(f"numpy not available: {e}")

def test_uploads_directory():
    """Test that uploads directory exists or can be created"""
    uploads_dir = "uploads"
    if not os.path.exists(uploads_dir):
        try:
            os.makedirs(uploads_dir)
            print(f"✓ Created uploads directory: {uploads_dir}")
        except Exception as e:
            pytest.fail(f"Failed to create uploads directory: {e}")
    else:
        print(f"✓ Uploads directory exists: {uploads_dir}")
    
    assert os.path.exists(uploads_dir)

def test_file_structure():
    """Test that required files exist"""
    required_files = [
        "app.py",
        "excelExtractor.py",
        "requirements.txt"
    ]
    
    for file_path in required_files:
        assert os.path.exists(file_path), f"Required file missing: {file_path}"
        print(f"✓ Found required file: {file_path}")

def test_requirements_file():
    """Test that requirements.txt contains required packages"""
    with open("requirements.txt", "r") as f:
        content = f.read()
    
    required_packages = ["Flask", "pandas", "openpyxl", "numpy", "pytest"]
    for package in required_packages:
        assert package in content, f"Required package missing from requirements.txt: {package}"
        print(f"✓ Found required package in requirements.txt: {package}") 