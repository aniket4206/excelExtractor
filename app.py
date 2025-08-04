from flask import Flask, render_template, request, send_file, flash, redirect, url_for
import os
from werkzeug.utils import secure_filename
from pathlib import Path
import tempfile
from excelExtractor import ExcelComparator

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this in production

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    try:
        # Check if base file is uploaded
        if 'base_file' not in request.files:
            flash('No base file selected', 'error')
            return redirect(request.url)
        
        base_file = request.files['base_file']
        if base_file.filename == '':
            flash('No base file selected', 'error')
            return redirect(request.url)
        
        if not allowed_file(base_file.filename):
            flash('Invalid file type for base file. Please upload Excel files (.xlsx, .xls)', 'error')
            return redirect(request.url)
        
        # Save base file
        base_filename = secure_filename(base_file.filename)
        base_filepath = os.path.join(app.config['UPLOAD_FOLDER'], base_filename)
        base_file.save(base_filepath)
        
        # Get comparison files
        comparison_files = request.files.getlist('comparison_files')
        comparison_filepaths = []
        
        for comp_file in comparison_files:
            if comp_file.filename != '' and allowed_file(comp_file.filename):
                comp_filename = secure_filename(comp_file.filename)
                comp_filepath = os.path.join(app.config['UPLOAD_FOLDER'], comp_filename)
                comp_file.save(comp_filepath)
                comparison_filepaths.append(comp_filepath)
        
        if not comparison_filepaths:
            flash('No valid comparison files uploaded', 'error')
            return redirect(request.url)
        
        # Get match columns (optional)
        match_columns_input = request.form.get('match_columns', '').strip()
        match_columns = None
        if match_columns_input:
            match_columns = [col.strip() for col in match_columns_input.split(',')]
        
        # Initialize comparator and perform comparison
        comparator = ExcelComparator(base_filepath)
        
        if not comparator.load_base_file():
            flash('Error loading base file', 'error')
            return redirect(request.url)
        
        # Perform comparison
        comparator.compare_files(comparison_filepaths, match_columns)
        
        if not comparator.comparison_results:
            flash('No comparison results generated', 'error')
            return redirect(request.url)
        
        # Generate output filename
        output_filename = f"comparison_results_{len(comparison_filepaths)}_files.xlsx"
        output_filepath = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        
        # Export results
        comparator.export_results(output_filepath)
        
        # Clean up uploaded files
        for filepath in [base_filepath] + comparison_filepaths:
            try:
                os.remove(filepath)
            except:
                pass
        
        # Return the results file
        return send_file(
            output_filepath,
            as_attachment=True,
            download_name=output_filename,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        
    except Exception as e:
        flash(f'Error processing files: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/download/<filename>')
def download_file(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    else:
        flash('File not found', 'error')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 