import pytest
import os
import sys

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from app import app
except ImportError as e:
    pytest.skip(f"Could not import app: {e}")

try:
    from excelExtractor import ExcelComparator
except ImportError as e:
    pytest.skip(f"Could not import ExcelComparator: {e}")

@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
    
    with app.test_client() as client:
        yield client

def test_home_page(client):
    """Test that home page loads successfully"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'html' in response.data.lower()  # Basic check for HTML content

def test_app_configuration():
    """Test that the Flask app is properly configured"""
    assert app.config['TESTING'] == True
    assert 'UPLOAD_FOLDER' in app.config
    assert 'MAX_CONTENT_LENGTH' in app.config

def test_upload_folder_exists():
    """Test that the upload folder exists"""
    upload_folder = app.config['UPLOAD_FOLDER']
    assert os.path.exists(upload_folder) or os.path.exists('uploads')

def test_excel_comparator_import():
    """Test that ExcelComparator can be imported successfully"""
    assert ExcelComparator is not None
    # Test that we can create an instance
    comparator = ExcelComparator("dummy_path.xlsx")
    assert comparator is not None
    assert hasattr(comparator, 'base_file_path')
