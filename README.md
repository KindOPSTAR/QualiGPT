# QualiGPT Web Application

A modern web-based version of QualiGPT - an AI-powered qualitative data analysis tool that uses OpenAI's GPT-4o to perform thematic analysis on interview data, focus groups, and social media posts.

## 🆕 What's New in the Web Version

This is a complete web-based reimplementation of the original QualiGPT desktop application, offering:

- **No Installation Hassles**: Runs in any web browser
- **Modern Interface**: Clean, responsive design with real-time feedback
- **Enhanced AI**: Uses GPT-4o with 128k context window for better analysis
- **Cross-Platform**: Works on Mac, Windows, Linux, tablets
- **Easy Deployment**: Run locally or deploy to cloud platforms
- **Docker Support**: Complete containerization with production-ready Gunicorn deployment
- **Clean Output**: Enhanced GPT-4o prompts for structured results without extra commentary

## Features

- **Easy API Integration**: Simple connection to OpenAI API with key validation
- **Multiple File Formats**: Support for CSV, XLSX, and DOCX files
- **Flexible Analysis Types**: 
  - Interviews
  - Focus Groups
  - Social Media Posts
- **Customizable Analysis**:
  - Adjustable number of themes (1-20)
  - Role-playing mode for expert analysis
  - Custom prompts for specific needs
- **Smart Data Handling**: Automatic segmentation for large datasets (up to 120k tokens)
- **Export Options**: Save results as CSV or TXT files
- **Production Ready**: Docker support with Gunicorn for scalable deployment

## 🍎 Installation for Mac Users

### Prerequisites

1. **Check Python Version** (Python 3.8+ required):
   ```bash
   python3 --version
   ```
   If you don't have Python 3.8+, install it from [python.org](https://www.python.org/downloads/mac-osx/)

2. **Get an OpenAI API Key**:
   - Visit [OpenAI Platform](https://platform.openai.com/api-keys)
   - Create an account and generate an API key
   - Set usage limits to control costs

### Option 1: Run with Python (Recommended for Development)

#### Step 1: Download QualiGPT
```bash
# Clone the repository
git clone <repository-url>
cd QualiGPT

# Or download and extract the ZIP file
```

#### Step 2: Create Virtual Environment
```bash
# Create a virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# You should see (venv) in your terminal prompt
```

#### Step 3: Install Dependencies
```bash
# Upgrade pip first
pip install --upgrade pip

# Install all required packages
pip install -r requirements.txt

# Download NLTK data (one-time setup)
python -c "import nltk; nltk.download('punkt_tab')"
```

#### Step 4: Run the Application
```bash
# Start the web server
python qualigpt-webapp.py
```

You should see:
```
* Running on http://127.0.0.1:5000
* Debug mode: on
```

#### Step 5: Access the Application
Open your web browser and go to: **http://localhost:5000**

### Option 2: Run with Docker (Recommended for Production)

#### Prerequisites for Docker
1. **Install Docker Desktop for Mac**:
   - Download from [docker.com](https://www.docker.com/products/docker-desktop/)
   - Install and start Docker Desktop
   - Verify installation: `docker --version`

#### Step 1: Download QualiGPT
```bash
# Clone the repository
git clone <repository-url>
cd QualiGPT
```

#### Step 2: Build and Run with Docker
```bash
# Build and start the application
docker-compose up --build

# Or run in background (detached mode)
docker-compose up -d --build
```

#### Step 3: Access the Application
Open your web browser and go to: **http://localhost:5005**

#### Docker Management Commands
```bash
# View running containers
docker-compose ps

# View logs
docker-compose logs -f qualigpt

# Stop the application
docker-compose down

# Restart the application
docker-compose restart
```

## 📖 How to Use QualiGPT

### Step 1: Connect to OpenAI
1. Enter your OpenAI API key in the "API Connection" section
2. Click "🔗 Connect" to validate your key
3. Wait for the green "Connected" status

### Step 2: Upload Your Data
1. Click the upload area or drag-and-drop your file
2. **Supported formats**:
   - **CSV**: Comma-separated values with headers
   - **XLSX**: Excel spreadsheet files
   - **DOCX**: Microsoft Word documents
3. **File size limit**: 16MB maximum
4. Preview your data to ensure it loaded correctly

### Step 3: Configure Analysis
1. **Select Data Type**:
   - **Interview**: For one-on-one interview transcripts
   - **Focus Group**: For group discussion data
   - **Social Media Posts**: For social media content analysis

2. **Set Number of Themes**: Choose 1-20 themes to extract

3. **Optional Settings**:
   - **Role-Playing Mode**: Enable for expert-level analysis
   - **Custom Prompt**: Add specific instructions for your analysis
   - **Header Descriptions**: Explain what each column contains

### Step 4: Run Analysis
1. Click "🔍 Analyze Data"
2. Wait for processing (5-30 seconds for most files)
3. Large files are automatically segmented and processed in parts
4. View the structured results with themes, descriptions, quotes, and participant counts

### Step 5: Export Results
- **CSV Export**: Download for Excel/SPSS analysis
- **Text Export**: Save for documentation or reports

## 📁 Sample Data Files

The repository includes sample files for testing:
- `qualigpt-test-data.csv` - Sample CSV interview data
- `sample-social-media.xlsx` - Sample Excel social media data
- `sample-interview.docx` - Sample Word document

## 🔧 File Format Guidelines

### CSV/XLSX Files
```csv
Participant,Age,Response
P1,25,"I think remote work has improved my work-life balance"
P2,32,"The biggest challenge is staying connected with the team"
P3,28,"I miss the spontaneous conversations in the office"
```

### DOCX Files
- Each paragraph becomes a separate data entry
- Best for unstructured interview transcripts
- Automatically extracts text content

## 🚀 Advanced Usage

### Development Mode
For development with live code reloading:
```bash
# Create docker-compose.override.yml
cat > docker-compose.override.yml << EOF
version: '3.8'
services:
  qualigpt:
    environment:
      - FLASK_ENV=development
      - FLASK_DEBUG=1
    volumes:
      - ./qualigpt-webapp.py:/app/qualigpt-webapp.py
      - ./templates:/app/templates
    command: ["python", "qualigpt-webapp.py"]
EOF

# Run in development mode
docker-compose up
```

### Production Deployment
```bash
# Using Gunicorn directly
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 qualigpt-webapp:app

# Or use Docker (recommended)
docker-compose up -d
```

### Environment Variables
```bash
# Optional: Set Flask environment
export FLASK_ENV=production

# For development
export FLASK_ENV=development
export FLASK_DEBUG=1
```

## 🔍 Troubleshooting

### Common Issues on Mac

**Python Command Not Found**:
```bash
# Try python3 instead of python
python3 qualigpt-webapp.py
```

**Permission Denied**:
```bash
# Make sure you're in the virtual environment
source venv/bin/activate
```

**Port Already in Use**:
```bash
# Kill processes using port 5000
sudo lsof -ti:5000 | xargs kill -9

# Or use Docker on port 5005
docker-compose up
```

**NLTK Download Issues**:
```bash
# Manual NLTK download
python -c "import nltk; nltk.download('punkt_tab', download_dir='./nltk_data')"
```

### API Connection Issues
- **Invalid API Key**: Verify your key at [OpenAI Platform](https://platform.openai.com/api-keys)
- **No Credits**: Check your OpenAI account billing
- **Rate Limits**: Wait a moment and try again

### File Upload Problems
- **File Too Large**: Maximum 16MB - compress or split your file
- **Wrong Format**: Ensure file extension matches content (.csv for CSV files)
- **Encoding Issues**: Save CSV files with UTF-8 encoding

### Docker Issues
- **Docker Not Running**: Start Docker Desktop application
- **Port Conflicts**: Use `docker-compose down` then `docker-compose up`
- **Build Errors**: Try `docker-compose build --no-cache`

## 📊 Understanding Results

QualiGPT generates structured analysis with:

- **Theme**: Main concepts identified in your data
- **Description**: Detailed explanation of each theme
- **Quotes**: Supporting evidence from your data
- **Participant Count**: Number of participants mentioning each theme

Results are formatted for easy import into:
- Excel/Google Sheets (CSV export)
- SPSS/R (CSV export)
- Word/Google Docs (TXT export)
- Academic papers (structured format)

## 🔒 Security & Privacy

- **API Keys**: Stored only in memory during your session
- **Data Processing**: Files processed in memory, not saved to disk
- **No Data Retention**: Your data is never stored on our servers
- **HTTPS Ready**: Use reverse proxy for secure production deployment

## 🆚 Comparison: Desktop vs Web Version

| Feature | Desktop Version | Web Version |
|---------|----------------|-------------|
| Installation | Complex setup required | No installation needed |
| Platform | Windows/Mac/Linux apps | Any web browser |
| Updates | Manual download | Automatic |
| Deployment | Single user | Multi-user capable |
| AI Model | GPT-3.5-turbo | GPT-4o (enhanced) |
| Context Window | 4k tokens | 128k tokens |
| Interface | PyQt5 desktop | Modern web UI |
| File Sharing | Local files only | Web-based sharing |
| Collaboration | Not supported | Multi-user ready |

## 🔮 Future Enhancements

- Support for additional AI models (Claude, Gemini)
- Batch processing for multiple files
- Real-time collaborative analysis
- Advanced visualization dashboards
- Integration with survey platforms
- API for programmatic access

## 📄 License

This project is released under the MIT License.

## 🙏 Credits

- **Original QualiGPT**: He Zhang et al. - Desktop application research
- **Web Version**: Modern reimplementation for accessible qualitative research
- **AI Integration**: OpenAI GPT-4o for enhanced analysis capabilities

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review sample files for format examples
3. Verify your OpenAI API key and credits
4. Ensure your data meets format requirements

---

**Ready to analyze your qualitative data? Start with the installation instructions above! 🚀**
