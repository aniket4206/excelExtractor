import PyInstaller.__main__
import os
import sys

def build_executable():
    """Build a single executable file for the Excel comparison tool"""
    
    # Define the PyInstaller arguments
    args = [
        'app.py',  # Main script
        '--onefile',  # Create single executable
        '--windowed',  # Hide console window (optional)
        '--name=ExcelComparator',  # Name of the executable
        '--add-data=templates;templates',  # Include templates folder
        '--hidden-import=flask',
        '--hidden-import=pandas',
        '--hidden-import=numpy',
        '--hidden-import=openpyxl',
        '--hidden-import=werkzeug',
        '--hidden-import=excelExtractor',
        '--icon=NONE',  # No icon for now
        '--clean',  # Clean cache
        '--noconfirm',  # Overwrite existing files
    ]
    
    # Run PyInstaller
    PyInstaller.__main__.run(args)
    
    print("✅ Executable built successfully!")
    print("📁 Check the 'dist' folder for your executable file")
    print("🚀 The executable will be named 'ExcelComparator.exe' (Windows) or 'ExcelComparator' (Linux/Mac)")

if __name__ == "__main__":
    build_executable() 