# QualiGPT Web Application - Project Brief

## Project Overview

QualiGPT is a modern web-based qualitative data analysis tool that leverages OpenAI's GPT models to perform automated thematic analysis on qualitative research data. This is the web version of an original PyQt5 desktop application, redesigned to provide researchers with a more accessible, browser-based interface for analyzing interviews, focus groups, and social media posts.

## Core Purpose

Transform the time-intensive process of manual qualitative data analysis by providing researchers with an AI-powered tool that can:
- Identify key themes from qualitative data
- Generate structured analysis tables with themes, descriptions, quotes, and participant counts
- Handle large datasets through intelligent segmentation
- Export results in multiple formats for further analysis

## Target Users

- **Primary**: Qualitative researchers in academia, market research, and social sciences
- **Secondary**: Graduate students conducting thesis research
- **Tertiary**: UX researchers and product teams analyzing user feedback

## Key Requirements

### Functional Requirements
1. **Data Input**: Support CSV, XLSX, and DOCX file formats
2. **AI Analysis**: Integration with OpenAI GPT-3.5-turbo for thematic analysis
3. **Data Types**: Specialized analysis for Interviews, Focus Groups, and Social Media Posts
4. **Customization**: Configurable number of themes (1-20) and custom prompts
5. **Export**: CSV and text file export capabilities
6. **Large Data Handling**: Automatic segmentation for datasets exceeding token limits

### Technical Requirements
1. **Web-based**: Accessible through modern web browsers
2. **Secure**: API key handling and file processing security
3. **Responsive**: Works on desktop and tablet devices
4. **Real-time Feedback**: Progress indicators and status updates
5. **Error Handling**: Graceful handling of API failures and file processing errors

## Success Criteria

1. **Usability**: Researchers can complete analysis workflow in under 10 minutes
2. **Accuracy**: AI-generated themes are relevant and well-structured
3. **Reliability**: Handles files up to 16MB without errors
4. **Accessibility**: No technical setup required beyond API key
5. **Export Quality**: Generated CSV files are immediately usable in Excel/SPSS

## Project Scope

### In Scope
- Web interface for file upload and analysis configuration
- OpenAI API integration for thematic analysis
- Multi-format file processing (CSV, XLSX, DOCX)
- Structured output generation and export
- Data segmentation for large datasets
- Role-playing mode for expert analysis

### Out of Scope
- Real-time collaboration features
- Advanced statistical analysis
- Integration with other AI models beyond OpenAI
- User authentication and data persistence
- Batch processing of multiple files

## Key Differentiators from Desktop Version

1. **Accessibility**: No installation required, runs in any modern browser
2. **Modern UI**: Clean, responsive interface with better user experience
3. **Simplified Workflow**: Streamlined process from upload to export
4. **Better Error Handling**: More informative error messages and recovery options
5. **Cross-Platform**: Works on any operating system with a web browser

## Technical Architecture Overview

- **Backend**: Flask web application with REST API endpoints
- **Frontend**: Modern HTML5/CSS3/JavaScript interface
- **AI Integration**: OpenAI GPT-3.5-turbo via official API
- **File Processing**: pandas, python-docx, and openpyxl for data extraction
- **Text Processing**: NLTK for intelligent text segmentation

## Project Status

This is a functional web application that successfully migrates and enhances the core functionality of the original desktop version while providing a more accessible and user-friendly interface for qualitative researchers.
