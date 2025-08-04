import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import tempfile
import os
from datetime import datetime
import openpyxl
from openpyxl.styles import PatternFill, Font
from openpyxl.utils.dataframe import dataframe_to_rows
import io
import base64

# Page configuration
st.set_page_config(
    page_title="Excel File Comparison Tool",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .info-box {
        background: #e3f2fd;
        border: 1px solid #2196f3;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .success-box {
        background: #e8f5e8;
        border: 1px solid #4caf50;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .error-box {
        background: #ffebee;
        border: 1px solid #f44336;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

class ExcelComparator:
    def __init__(self, base_file_path):
        """
        Initialize the Excel Comparator with a base employee file
        
        Args:
            base_file_path (str): Path to the base Excel file containing employee data
        """
        self.base_file_path = base_file_path
        self.base_data = None
        self.comparison_results = {}
        
    def load_base_file(self):
        """Load the base Excel file"""
        try:
            self.base_data = pd.read_excel(self.base_file_path)
            return True
        except Exception as e:
            st.error(f"Error loading base file: {e}")
            return False
    
    def clean_data(self, df):
        """Clean and standardize data for comparison"""
        df_clean = df.copy()
        
        # Convert all columns to string and strip whitespace
        for col in df_clean.columns:
            if df_clean[col].dtype == 'object':
                df_clean[col] = df_clean[col].astype(str).str.strip().str.upper()
        
        return df_clean
    
    def find_common_columns(self, df1, df2):
        """Find common columns between two dataframes"""
        cols1 = set(df1.columns)
        cols2 = set(df2.columns)
        common_cols = list(cols1.intersection(cols2))
        return common_cols
    
    def compare_files(self, comparison_files, match_columns=None):
        """
        Compare multiple files against the base file
        
        Args:
            comparison_files (list): List of file paths to compare
            match_columns (list): Specific columns to use for matching (optional)
        """
        if self.base_data is None:
            st.error("Please load the base file first")
            return
        
        base_clean = self.clean_data(self.base_data)
        
        for file_path in comparison_files:
            try:
                st.info(f"Processing: {Path(file_path).name}")
                
                # Load comparison file
                comp_data = pd.read_excel(file_path)
                comp_clean = self.clean_data(comp_data)
                
                st.success(f"Loaded {len(comp_data)} records from {Path(file_path).name}")
                
                # Find common columns
                common_cols = self.find_common_columns(base_clean, comp_clean)
                if not common_cols:
                    st.error(f"No common columns found with base file")
                    continue
                
                # Use specified match columns or all common columns
                if match_columns:
                    match_cols = [col for col in match_columns if col in common_cols]
                    if not match_cols:
                        st.error(f"None of the specified match columns found")
                        continue
                else:
                    match_cols = common_cols
                
                st.info(f"Using columns for matching: {match_cols}")
                
                # Perform comparison
                result = self.perform_comparison(
                    base_clean, comp_clean, match_cols, Path(file_path).name
                )
                
                self.comparison_results[Path(file_path).name] = result
                
            except Exception as e:
                st.error(f"Error processing {file_path}: {e}")
    
    def perform_comparison(self, base_df, comp_df, match_cols, file_name):
        """Perform detailed comparison between base and comparison dataframes"""
        
        # Create a composite key for matching
        if len(match_cols) == 1:
            base_df['_match_key'] = base_df[match_cols[0]]
            comp_df['_match_key'] = comp_df[match_cols[0]]
        else:
            base_df['_match_key'] = base_df[match_cols].apply(
                lambda x: '|'.join(x.astype(str)), axis=1
            )
            comp_df['_match_key'] = comp_df[match_cols].apply(
                lambda x: '|'.join(x.astype(str)), axis=1
            )
        
        # Find matches and misses
        base_keys = set(base_df['_match_key'].dropna())
        comp_keys = set(comp_df['_match_key'].dropna())
        
        matched_keys = base_keys.intersection(comp_keys)
        missing_in_comp = base_keys - comp_keys
        extra_in_comp = comp_keys - base_keys
        
        # Create result dataframes
        matched_base = base_df[base_df['_match_key'].isin(matched_keys)].copy()
        matched_comp = comp_df[comp_df['_match_key'].isin(matched_keys)].copy()
        missing_records = base_df[base_df['_match_key'].isin(missing_in_comp)].copy()
        extra_records = comp_df[comp_df['_match_key'].isin(extra_in_comp)].copy()
        
        # Remove the temporary match key
        for df in [matched_base, matched_comp, missing_records, extra_records]:
            if '_match_key' in df.columns:
                df.drop('_match_key', axis=1, inplace=True)
        
        result = {
            'file_name': file_name,
            'match_columns': match_cols,
            'total_base_records': len(base_df),
            'total_comp_records': len(comp_df),
            'matched_records': len(matched_keys),
            'missing_in_comparison': len(missing_in_comp),
            'extra_in_comparison': len(extra_in_comp),
            'matched_data_base': matched_base,
            'matched_data_comp': matched_comp,
            'missing_records': missing_records,
            'extra_records': extra_records
        }
        
        return result
    
    def export_results(self):
        """Export comparison results to Excel with multiple sheets"""
        
        if not self.comparison_results:
            st.error("No comparison results to export")
            return None
        
        # Create Excel file in memory
        output = io.BytesIO()
        
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            
            # Create summary sheet
            summary_data = []
            for file_name, result in self.comparison_results.items():
                summary_data.append({
                    'File Name': result['file_name'],
                    'Match Columns': ', '.join(result['match_columns']),
                    'Base Records': result['total_base_records'],
                    'Comparison Records': result['total_comp_records'],
                    'Matched': result['matched_records'],
                    'Missing in Comparison': result['missing_in_comparison'],
                    'Extra in Comparison': result['extra_in_comparison'],
                    'Match Rate %': round((result['matched_records'] / result['total_base_records']) * 100, 2) if result['total_base_records'] > 0 else 0
                })
            
            summary_df = pd.DataFrame(summary_data)
            summary_df.to_excel(writer, sheet_name='Summary', index=False)
            
            # Create detailed sheets for each comparison
            for file_name, result in self.comparison_results.items():
                safe_name = file_name.replace('.xlsx', '').replace('.xls', '')[:31]  # Excel sheet name limit
                
                # Matched records sheet
                if not result['matched_data_base'].empty:
                    result['matched_data_base'].to_excel(
                        writer, sheet_name=f'{safe_name}_Matched', index=False
                    )
                
                # Missing records sheet
                if not result['missing_records'].empty:
                    result['missing_records'].to_excel(
                        writer, sheet_name=f'{safe_name}_Missing', index=False
                    )
                
                # Extra records sheet
                if not result['extra_records'].empty:
                    result['extra_records'].to_excel(
                        writer, sheet_name=f'{safe_name}_Extra', index=False
                    )
        
        output.seek(0)
        return output

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>📊 Excel File Comparison Tool</h1>
        <p>Compare multiple Excel files against a base file and download detailed results</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Info box
    st.markdown("""
    <div class="info-box">
        <h3>📋 How to use:</h3>
        <ul>
            <li><strong>Base File:</strong> Upload the reference Excel file (e.g., master employee list)</li>
            <li><strong>Comparison Files:</strong> Upload one or more Excel files to compare against the base</li>
            <li><strong>Match Columns (Optional):</strong> Specify column names for matching (comma-separated)</li>
            <li>The tool will generate a detailed Excel report with comparison results</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # File upload section
    st.subheader("📁 Upload Files")
    
    # Base file upload
    base_file = st.file_uploader(
        "Choose base Excel file (.xlsx, .xls)",
        type=['xlsx', 'xls'],
        key="base_file"
    )
    
    # Comparison files upload
    comparison_files = st.file_uploader(
        "Choose comparison Excel files (.xlsx, .xls)",
        type=['xlsx', 'xls'],
        accept_multiple_files=True,
        key="comparison_files"
    )
    
    # Match columns input
    match_columns_input = st.text_input(
        "Match Columns (Optional)",
        placeholder="e.g., EmployeeID, Name, Email (comma-separated)",
        help="Leave empty to auto-detect common columns"
    )
    
    # Process button
    if st.button("🔍 Compare Files & Generate Report", type="primary"):
        if base_file is None:
            st.error("Please upload a base file")
        elif not comparison_files:
            st.error("Please upload at least one comparison file")
        else:
            with st.spinner("Processing files..."):
                try:
                    # Save base file temporarily
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_base:
                        tmp_base.write(base_file.getvalue())
                        base_filepath = tmp_base.name
                    
                    # Save comparison files temporarily
                    comparison_filepaths = []
                    for comp_file in comparison_files:
                        with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_comp:
                            tmp_comp.write(comp_file.getvalue())
                            comparison_filepaths.append(tmp_comp.name)
                    
                    # Parse match columns
                    match_columns = None
                    if match_columns_input.strip():
                        match_columns = [col.strip() for col in match_columns_input.split(',')]
                    
                    # Initialize comparator
                    comparator = ExcelComparator(base_filepath)
                    
                    if comparator.load_base_file():
                        st.success(f"✓ Base file loaded successfully: {len(comparator.base_data)} records")
                        st.info(f"✓ Columns in base file: {list(comparator.base_data.columns)}")
                        
                        # Perform comparison
                        comparator.compare_files(comparison_filepaths, match_columns)
                        
                        if comparator.comparison_results:
                            # Generate Excel report
                            excel_output = comparator.export_results()
                            
                            if excel_output:
                                # Create download button
                                st.markdown("""
                                <div class="success-box">
                                    <h3>✅ Comparison Complete!</h3>
                                    <p>Your Excel report is ready for download.</p>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                # Display summary
                                st.subheader("📊 Comparison Summary")
                                for file_name, result in comparator.comparison_results.items():
                                    col1, col2, col3, col4, col5 = st.columns(5)
                                    with col1:
                                        st.metric("Base Records", result['total_base_records'])
                                    with col2:
                                        st.metric("Comparison Records", result['total_comp_records'])
                                    with col3:
                                        st.metric("Matched", result['matched_records'])
                                    with col4:
                                        st.metric("Missing", result['missing_in_comparison'])
                                    with col5:
                                        st.metric("Extra", result['extra_in_comparison'])
                                
                                # Download button
                                st.download_button(
                                    label="📥 Download Excel Report",
                                    data=excel_output.getvalue(),
                                    file_name=f"comparison_results_{len(comparison_files)}_files.xlsx",
                                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                                )
                            else:
                                st.error("Failed to generate Excel report")
                        else:
                            st.error("No comparison results generated")
                    else:
                        st.error("Failed to load base file")
                    
                    # Clean up temporary files
                    try:
                        os.unlink(base_filepath)
                        for filepath in comparison_filepaths:
                            os.unlink(filepath)
                    except:
                        pass
                        
                except Exception as e:
                    st.error(f"Error processing files: {str(e)}")

if __name__ == "__main__":
    main() 