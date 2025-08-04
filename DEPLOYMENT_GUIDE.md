# Excel File Comparison Tool - Deployment Guide

## 🚀 Streamlit Cloud Deployment (Recommended)

This is the easiest way to deploy your Excel comparison tool and share it with others.

### Step 1: Prepare Your Files
Make sure you have these files in your repository:
- `streamlit_app.py` (main application)
- `requirements_streamlit.txt` (dependencies)

### Step 2: Deploy to Streamlit Cloud
1. **Push to GitHub**: Upload your files to a GitHub repository
2. **Go to Streamlit Cloud**: Visit https://share.streamlit.io/
3. **Connect Repository**: Link your GitHub repository
4. **Configure Deployment**:
   - **Main file path**: `streamlit_app.py`
   - **Python version**: 3.9 or higher
5. **Deploy**: Click "Deploy app"

### Step 3: Share Your App
Once deployed, you'll get a public URL like:
```
https://your-app-name.streamlit.app
```

## 🖥️ Local Deployment

### Option 1: Run with Streamlit
```bash
# Install dependencies
pip install -r requirements_streamlit.txt

# Run the app
streamlit run streamlit_app.py
```

### Option 2: Create Executable (Single File)
```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
pyinstaller --onefile --add-data "templates;templates" app.py --name ExcelComparator

# The executable will be in the 'dist' folder
```

## 📁 File Structure for Deployment

```
your-repo/
├── streamlit_app.py          # Main Streamlit application
├── requirements_streamlit.txt # Dependencies for Streamlit
├── app.py                   # Flask version (for local use)
├── excelExtractor.py        # Core comparison logic
├── templates/               # HTML templates (for Flask version)
│   └── index.html
└── README.md               # Documentation
```

## 🌐 Deployment Options Comparison

| Option | Pros | Cons | Best For |
|--------|------|------|----------|
| **Streamlit Cloud** | ✅ Free hosting<br>✅ Easy deployment<br>✅ Public URL<br>✅ No server management | ❌ Limited customization<br>❌ Streamlit-specific | Sharing with others |
| **Local Flask** | ✅ Full customization<br>✅ Complete control<br>✅ Custom domain | ❌ Requires server<br>❌ Manual deployment<br>❌ Maintenance | Internal use |
| **Executable** | ✅ Single file<br>✅ No installation needed<br>✅ Works offline | ❌ Large file size<br>❌ Platform specific<br>❌ No updates | Distribution |

## 🔧 Troubleshooting

### Streamlit Cloud Issues
1. **"Module not found"**: Check `requirements_streamlit.txt` has all dependencies
2. **"App not loading"**: Ensure `streamlit_app.py` is the main file
3. **"File upload errors"**: Check file size limits (200MB max)

### Local Issues
1. **Port conflicts**: Change port in `app.py` line 121
2. **Permission errors**: Run with appropriate permissions
3. **Dependency issues**: Use virtual environment

## 📊 Features Comparison

| Feature | Streamlit Version | Flask Version |
|---------|------------------|---------------|
| **File Upload** | ✅ Multiple files | ✅ Multiple files |
| **Excel Processing** | ✅ Full support | ✅ Full support |
| **Download Results** | ✅ Direct download | ✅ Direct download |
| **UI Customization** | ⚠️ Limited | ✅ Full control |
| **Deployment** | ✅ One-click | ⚠️ Manual setup |
| **Sharing** | ✅ Public URL | ⚠️ Requires hosting |

## 🎯 Recommended Approach

**For sharing with others**: Use Streamlit Cloud deployment
**For internal use**: Use local Flask deployment
**For distribution**: Create executable file

## 📞 Support

If you encounter issues:
1. Check the error logs in Streamlit Cloud
2. Verify all dependencies are installed
3. Test with smaller files first
4. Ensure Excel files are not corrupted 