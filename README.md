# Excel File Comparison Tool - Web UI

A modern web interface for comparing multiple Excel files against a base file. This tool helps identify matching records, missing entries, and extra records across different Excel files.

## Features

URL - https://aniketsinu.pythonanywhere.com

- 📊 **Web-based Interface**: Clean, modern UI for easy file upload and comparison
- 🔍 **Multi-file Comparison**: Compare multiple Excel files against a single base file
- 🎯 **Flexible Matching**: Auto-detect common columns or specify custom match columns
- 📋 **Detailed Reports**: Generate comprehensive Excel reports with multiple sheets
- 📱 **Responsive Design**: Works on desktop and mobile devices
- ⚡ **Fast Processing**: Efficient backend processing with progress indicators

## Installation

1. **Clone or download the project files**

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the web application**:
   ```bash
   python app.py
   ```

4. **Open your browser** and go to:
   ```
   http://localhost:5000
   ```

## How to Use

### Step 1: Upload Files
- **Base File**: Upload your reference Excel file (e.g., master employee list)
- **Comparison Files**: Upload one or more Excel files to compare against the base
- **Match Columns** (Optional): Specify column names for matching (comma-separated)

### Step 2: Process and Download
- Click "Compare Files & Download Results"
- The tool will process your files and automatically download the results
- The downloaded Excel file contains detailed comparison reports

### Step 3: Review Results
The generated Excel file includes:
- **Summary Sheet**: Overview of all comparisons
- **Matched Records**: Records found in both base and comparison files
- **Missing Records**: Records in base file but not in comparison files
- **Extra Records**: Records in comparison files but not in base file

## File Structure

```
excelExtractor/
├── app.py                 # Flask web application
├── excelExtractor.py      # Core comparison logic
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Web UI template
├── uploads/              # Temporary file storage
└── README.md            # This file
```

## Supported File Formats

- **Input**: `.xlsx`, `.xls` files
- **Output**: `.xlsx` file with detailed comparison results

## Technical Details

### Backend Features
- **Data Cleaning**: Automatic standardization of data for comparison
- **Flexible Matching**: Support for single or multiple column matching
- **Error Handling**: Comprehensive error handling and user feedback
- **File Security**: Secure file handling with validation

### Web Interface Features
- **Modern Design**: Clean, responsive UI with gradient backgrounds
- **File Validation**: Real-time file type and size validation
- **Progress Indicators**: Loading states and user feedback
- **Mobile Friendly**: Responsive design for all devices

## Command Line Usage

The original command-line tool is still available:

```bash
# Basic usage
python excelExtractor.py base_file.xlsx file1.xlsx file2.xlsx

# With specific match columns
python excelExtractor.py base_file.xlsx file1.xlsx --match-columns EmployeeID Name

# With custom output file
python excelExtractor.py base_file.xlsx file1.xlsx --output my_results.xlsx
```

## Troubleshooting

### Common Issues

1. **"No base file selected"**
   - Make sure you've selected a base file before submitting

2. **"Invalid file type"**
   - Ensure you're uploading Excel files (.xlsx or .xls)

3. **"Error loading base file"**
   - Check that your Excel file is not corrupted and is properly formatted

4. **"No comparison results generated"**
   - Verify that your files have common columns for comparison

### Performance Tips

- For large files (>10MB), processing may take longer
- The tool automatically cleans up uploaded files after processing
- Results are automatically downloaded as an Excel file

## Security Notes

- Uploaded files are temporarily stored and automatically deleted after processing
- File size is limited to 16MB per file
- Only Excel file types are accepted
- The application runs in debug mode by default (change for production)

## License

This tool is provided as-is for educational and business use. 
