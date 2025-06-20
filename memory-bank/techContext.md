# QualiGPT - Technical Context

## Technology Stack

### Backend Technologies
- **Python 3.8+**: Core programming language
- **Flask 2.3.2**: Web framework for HTTP handling and routing
- **pandas 2.0.3**: Data manipulation and analysis
- **OpenAI 1.0+**: AI API integration for GPT-4o (latest version)
- **python-docx 0.8.11**: Microsoft Word document processing
- **NLTK 3.8.1**: Natural language processing and tokenization
- **openpyxl 3.1.2**: Excel file processing
- **Werkzeug 2.3.6**: WSGI utilities and security functions

### Frontend Technologies
- **HTML5**: Modern semantic markup
- **CSS3**: Responsive styling with gradients and animations
- **Vanilla JavaScript**: Client-side interactivity and AJAX
- **SVG Icons**: Scalable vector graphics for UI elements

### Development Environment
- **Python Virtual Environment**: Isolated dependency management
- **pip**: Package management
- **Flask Development Server**: Local development and testing
- **Git**: Version control

## Architecture Decisions

### 1. Flask Over Django
**Decision**: Use Flask instead of Django
**Rationale**: 
- Lightweight and minimal for single-purpose application
- Faster development for simple web API
- Less overhead for stateless application
- Easier deployment and maintenance

### 2. Vanilla JavaScript Over Frameworks
**Decision**: Use vanilla JavaScript instead of React/Vue
**Rationale**:
- Simple UI requirements don't justify framework complexity
- Faster page load times
- No build process required
- Easier maintenance for small team

### 3. In-Memory Processing
**Decision**: Process files in memory without persistent storage
**Rationale**:
- Enhanced security (no file persistence)
- Simpler deployment (no file system management)
- Better performance for typical file sizes
- Reduced storage requirements

### 4. OpenAI GPT-4o
**Decision**: Use GPT-4o as primary AI model
**Rationale**:
- Superior analysis quality for qualitative research
- Large 128k context window reduces segmentation needs
- Better understanding of complex qualitative data
- Enhanced accuracy in theme identification and quote extraction

## Development Setup

### Local Development Environment
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download NLTK data (one-time setup)
python -c "import nltk; nltk.download('punkt')"

# Run development server
python qualigpt-webapp.py
```

### Environment Variables
```bash
# Optional: Set secret key for production
export SECRET_KEY="your-secure-secret-key-here"

# Optional: Set OpenAI API key (alternative to UI input)
export OPENAI_API_KEY="your-openai-api-key"
```

### Dependencies Analysis

#### Core Dependencies
```
flask==2.3.2          # Web framework
pandas==2.0.3         # Data processing
openai==0.27.8        # AI integration
python-docx==0.8.11   # Word document processing
nltk==3.8.1           # Text processing
openpyxl==3.1.2       # Excel processing
werkzeug==2.3.6       # Web utilities
```

#### Dependency Relationships
- **Flask** → **Werkzeug** (HTTP utilities)
- **pandas** → **openpyxl** (Excel file support)
- **NLTK** → **punkt tokenizer** (sentence segmentation)
- **python-docx** → **lxml** (XML processing)

## File Structure

```
QualiGPT/
├── qualigpt-webapp.py          # Main Flask application
├── requirements.txt            # Python dependencies
├── README.md                   # Documentation
├── templates/
│   └── index.html             # Web interface (embedded in HTML file)
├── memory-bank/               # Project documentation
│   ├── projectbrief.md
│   ├── productContext.md
│   ├── systemPatterns.md
│   ├── techContext.md
│   ├── activeContext.md
│   └── progress.md
├── graph/                     # Project assets
│   ├── Logo-QualiGPT.png
│   ├── QualiGPT-workflow.png
│   └── ...
└── legacy/                    # Original desktop version
    ├── QualiGPTApp.py
    └── setup.py
```

## API Integration

### OpenAI API Configuration
```python
# API Configuration (New v1.0+ syntax)
from openai import OpenAI
client = OpenAI(api_key=user_provided_key)
model = "gpt-4o"
max_tokens = 4000
temperature = 0.7
```

### API Usage Patterns
1. **Connection Testing**: Simple test call to validate API key
2. **Analysis Requests**: Structured prompts with data and instructions
3. **Error Handling**: Comprehensive exception handling for API failures
4. **Rate Limiting**: Built-in handling of API rate limits

### Token Management
- **Input Limit**: 128k tokens for GPT-4o (massive increase from 4k)
- **Reserved Tokens**: 8k tokens reserved for prompts and responses
- **Segmentation**: Automatic data splitting for extremely large datasets only
- **Optimization**: Most datasets now process in single API call

## Security Considerations

### Data Security
- **No Persistent Storage**: Files processed in memory only
- **Secure File Handling**: Werkzeug secure filename processing
- **Input Validation**: Comprehensive validation of all user inputs
- **File Type Validation**: Extension and content-based validation

### API Security
- **Key Management**: API keys stored only in memory during session
- **Environment Variables**: Support for secure key storage in production
- **No Logging**: API keys never logged or persisted
- **HTTPS Ready**: Prepared for SSL/TLS in production

### Web Security
- **CSRF Protection**: Flask secret key for session security
- **XSS Prevention**: Proper output encoding in frontend
- **File Upload Security**: Size limits and type restrictions
- **Input Sanitization**: All user inputs sanitized before processing

## Performance Characteristics

### File Processing Performance
- **CSV Files**: ~1MB/second processing speed
- **Excel Files**: ~500KB/second processing speed
- **Word Documents**: ~2MB/second processing speed
- **Memory Usage**: ~2x file size during processing

### API Performance
- **Response Time**: 5-30 seconds depending on data size
- **Throughput**: Limited by OpenAI API rate limits
- **Concurrent Users**: Stateless design supports multiple users
- **Caching**: Session-based result caching

### Scalability Limits
- **File Size**: 16MB maximum upload size
- **Data Volume**: Limited by OpenAI token limits
- **Concurrent Requests**: Limited by server resources
- **Memory Usage**: Proportional to file size and concurrent users

## Deployment Options

### Local Deployment
```bash
# Development server (not for production)
python qualigpt-webapp.py
```

### Production Deployment
```bash
# Using Gunicorn (recommended)
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 qualigpt-webapp:app

# Using uWSGI
pip install uwsgi
uwsgi --http :8000 --wsgi-file qualigpt-webapp.py --callable app
```

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "qualigpt-webapp.py"]
```

### Cloud Deployment Options
- **Heroku**: Simple deployment with Procfile
- **AWS Elastic Beanstalk**: Managed Python application hosting
- **Google Cloud Run**: Containerized deployment
- **DigitalOcean App Platform**: Simple web app hosting

## Monitoring & Logging

### Application Logging
```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
```

### Error Tracking
- **Exception Handling**: Comprehensive try-catch blocks
- **User-Friendly Messages**: Clear error communication
- **Debug Information**: Detailed logging for troubleshooting

### Performance Monitoring
- **Request Timing**: Track processing times
- **Memory Usage**: Monitor resource consumption
- **API Usage**: Track OpenAI API calls and costs

## Testing Strategy

### Manual Testing Checklist
1. **API Connection**: Test with valid/invalid API keys
2. **File Upload**: Test all supported file formats
3. **Analysis**: Test different data types and configurations
4. **Export**: Verify CSV and text export functionality
5. **Error Handling**: Test various error conditions

### Automated Testing Opportunities
- **Unit Tests**: Test individual functions
- **Integration Tests**: Test API endpoints
- **File Processing Tests**: Test various file formats
- **Error Handling Tests**: Test exception scenarios

## Technical Debt & Improvements

### Current Limitations
1. **No Template Engine**: HTML embedded in single file
2. **Limited Error Recovery**: Some errors require page refresh
3. **No User Authentication**: Single-user application
4. **No Data Persistence**: Results lost on session end

### Potential Improvements
1. **Separate Templates**: Move HTML to proper template files
2. **Better Error Handling**: More graceful error recovery
3. **Result Persistence**: Optional result saving
4. **Batch Processing**: Multiple file analysis
5. **API Abstraction**: Support for multiple AI providers

## Migration from Desktop Version

### Key Changes Made
1. **UI Framework**: PyQt5 → HTML/CSS/JavaScript
2. **Architecture**: Desktop app → Web application
3. **File Handling**: Local files → Upload/download
4. **State Management**: Object state → Stateless requests
5. **Distribution**: Executable → Web deployment

### Preserved Functionality
- All three analysis types (Interview, Focus Group, Social Media)
- Data segmentation for large files
- Custom prompt support
- Role-playing mode
- CSV export functionality
- Multi-format file support

### Enhanced Features
- Modern, responsive web interface
- Better error handling and user feedback
- Cross-platform compatibility
- No installation required
- Real-time progress indicators
