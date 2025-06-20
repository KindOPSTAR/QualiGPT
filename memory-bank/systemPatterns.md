# QualiGPT - System Patterns & Architecture

## System Architecture Overview

QualiGPT follows a clean separation between frontend presentation, backend processing, and external AI services. The architecture is designed for simplicity, reliability, and maintainability.

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Flask App     │    │   OpenAI API    │
│   (HTML/CSS/JS) │◄──►│   (Python)      │◄──►│   (GPT-3.5)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                       ┌─────────────────┐
                       │   File System   │
                       │   (Temp Files)  │
                       └─────────────────┘
```

## Core Design Patterns

### 1. Request-Response Pattern
All interactions follow a simple HTTP request-response pattern:
- Frontend sends AJAX requests to Flask endpoints
- Flask processes data and returns JSON responses
- Frontend updates UI based on response data

### 2. Pipeline Processing Pattern
Data flows through a consistent processing pipeline:
```
File Upload → Format Detection → Content Extraction → Segmentation → AI Analysis → Response Parsing → Export
```

### 3. Strategy Pattern for File Processing
Different file types use specialized processing strategies:
- **CSV Strategy**: pandas.read_csv() with encoding detection
- **XLSX Strategy**: pandas.read_excel() with openpyxl engine
- **DOCX Strategy**: python-docx with paragraph extraction

### 4. Template Method Pattern for AI Analysis
AI analysis follows a consistent template with customizable components:
- Base prompt structure (consistent across all analysis types)
- Variable components (data type, theme count, custom instructions)
- Role-playing system message (optional expert mode)

## Key Components

### Flask Application Structure
```python
app = Flask(__name__)
├── Routes
│   ├── / (index page)
│   ├── /test_api (API key validation)
│   ├── /upload_file (file processing)
│   ├── /analyze (AI analysis)
│   └── /export_csv (result export)
├── Configuration
│   ├── MAX_CONTENT_LENGTH (16MB)
│   ├── SECRET_KEY (session security)
│   └── ALLOWED_EXTENSIONS (csv, xlsx, docx)
└── Utilities
    ├── File validation
    ├── Data segmentation
    └── Response parsing
```

### Data Processing Pipeline

#### 1. File Upload & Validation
```python
def upload_file():
    # Security validation
    if not allowed_file(filename):
        return error_response
    
    # File type detection and processing
    if file_ext == 'csv':
        data = pd.read_csv(file)
    elif file_ext == 'xlsx':
        data = pd.read_excel(file)
    elif file_ext == 'docx':
        # Extract paragraphs to DataFrame
```

#### 2. Content Extraction Pattern
All file types are normalized to a consistent format:
- Headers: List of column names
- Content: Concatenated text data
- Preview: First 1000 characters for user verification

#### 3. Data Segmentation Algorithm
```python
def split_into_segments(text, max_tokens=3800):
    sentences = sent_tokenize(text)  # NLTK sentence tokenization
    segments = []
    current_segment = ""
    token_count = 0
    
    for sentence in sentences:
        sentence_tokens = len(word_tokenize(sentence))
        if token_count + sentence_tokens > max_tokens:
            segments.append(current_segment)
            current_segment = sentence
            token_count = sentence_tokens
        else:
            current_segment += " " + sentence
            token_count += sentence_tokens
```

### AI Integration Patterns

#### 1. Prompt Engineering Strategy
Three specialized prompt templates for different data types:
- **Interview Analysis**: Focus on participant themes and direct quotes
- **Focus Group Analysis**: Emphasis on group dynamics and consensus themes
- **Social Media Analysis**: Attention to sentiment and trending topics

#### 2. Token Management Pattern
```python
# Reserve tokens for system message and response
max_input_tokens = 128000 - 8000  # Reserve 8k for prompt and response (GPT-4o)
segments = split_into_segments(data, max_input_tokens)
```

#### 3. Multi-Segment Processing
For large datasets:
1. Split data into segments
2. Process each segment individually
3. Collect all responses
4. Merge and re-analyze for final themes

#### 4. Response Parsing Pattern
Structured table extraction using delimiters:
```
**********  (Start delimiter)
| Theme | Description | Quotes | Participant Count |
|-------|-------------|--------|-------------------|
| Data rows with pipe separators |
**********  (End delimiter)
```

## Error Handling Patterns

### 1. Graceful Degradation
- API failures don't crash the application
- File processing errors provide helpful feedback
- Partial results are preserved when possible

### 2. User-Friendly Error Messages
```python
try:
    # OpenAI API call
except openai.error.OpenAIError as e:
    return jsonify({'success': False, 'error': f'OpenAI API Error: {str(e)}'})
except Exception as e:
    return jsonify({'success': False, 'error': f'Processing Error: {str(e)}'})
```

### 3. Input Validation Pattern
All user inputs are validated before processing:
- File type validation
- File size limits (16MB)
- API key format validation
- Parameter range validation (themes: 1-20)

## Security Patterns

### 1. File Security
- Secure filename handling with `werkzeug.utils.secure_filename`
- File type validation beyond extension checking
- Size limits to prevent resource exhaustion
- In-memory processing (no persistent file storage)

### 2. API Key Handling
- API keys stored only in memory during session
- No persistent storage of sensitive data
- Environment variable support for production deployment

### 3. Input Sanitization
- All user inputs sanitized before processing
- SQL injection prevention (though no database used)
- XSS prevention in frontend display

## Performance Patterns

### 1. Lazy Loading
- File content loaded only when needed
- API connections established on demand
- Results cached in memory during session

### 2. Streaming Responses
- Large file processing with progress indicators
- Chunked response handling for better user experience

### 3. Resource Management
- Temporary file cleanup
- Memory-efficient data processing
- Connection pooling for API requests

## Integration Patterns

### 1. OpenAI API Integration
```python
# New v1.0+ API syntax
client = OpenAI(api_key=api_key)
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": system_message},
        {"role": "user", "content": combined_message}
    ],
    temperature=0.7,
    max_tokens=4000
)
# Response access: response.choices[0].message.content
```

### 2. Frontend-Backend Communication
- RESTful API design
- JSON request/response format
- Asynchronous JavaScript for better UX

### 3. Export Integration
- CSV generation compatible with Excel/SPSS
- Text export for documentation
- In-memory file generation and download

## Scalability Considerations

### 1. Stateless Design
- No server-side session storage
- Each request is independent
- Easy horizontal scaling potential

### 2. Resource Limits
- File size limits prevent resource exhaustion
- Token limits prevent excessive API usage
- Request timeouts prevent hanging connections

### 3. Caching Strategy
- Results cached during user session
- API responses cached for duplicate requests
- File processing results cached for re-analysis

## Monitoring & Observability

### 1. Error Tracking
- Comprehensive exception handling
- Error logging for debugging
- User-friendly error messages

### 2. Performance Monitoring
- Request timing tracking
- File processing metrics
- API response time monitoring

### 3. Usage Analytics
- File type distribution
- Analysis type preferences
- Error rate tracking
