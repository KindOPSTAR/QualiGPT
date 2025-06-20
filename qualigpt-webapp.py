from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
from openai import OpenAI
import os
import io
import json
from werkzeug.utils import secure_filename
from docx import Document
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
import re
from datetime import datetime
import tempfile

# Download NLTK data if not already present
import nltk.data
# Set local NLTK data path
local_nltk_path = os.path.join(os.path.dirname(__file__), 'nltk_data')
if local_nltk_path not in nltk.data.path:
    nltk.data.path.append(local_nltk_path)

try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    # Download to local directory
    nltk.download('punkt_tab', download_dir=local_nltk_path)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Allowed file extensions
ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Prompt templates
PROMPTS = {
    "Interview": """You need to analyze an dataset of interviews.
Please identify the top {num_themes} key themes from the interview and organize the results in a structured table format.
The table should includes these items:
- 'Theme': Represents the main idea or topic identified from the interview.
- 'Description': Provides a brief explanation or summary of the theme.
- 'Quotes': Contains direct quotations from participants that support the identified theme.
- 'Participant Count': Indicates the number of participants who mentioned or alluded to the theme.
The table should be formatted as follows:
Each column should be separated by a '|' symbol, and there should be no extra '|' symbols within the data. Each row should end with '---'.
The whole table should start with '**********' and end with '**********'.
Columns: | 'Theme' | 'Description' | 'Quotes' | 'Participant Count' |.
Ensure each row of the table represents a distinct theme and its associated details. Aggregate the counts for each theme to show the total number of mentions across all participants.

IMPORTANT: Output ONLY the table with no additional text, commentary, or explanations. Do not include phrases like 'Here is the table', 'Below is the analysis', or 'Certainly!'. Start your response immediately with '**********' and end with '**********'. Do not use markdown formatting or code blocks.""",
    
    "Focus Group": """You need to analyze an dataset of a focus group.
Please identify the {num_themes} most common key themes from the interview and organize the results in a structured table format.
The table should includes these items:
- 'Theme': Represents the main idea or topic identified from the interview.
- 'Description': Provides a brief explanation or summary of the theme.
- 'Quotes': Contains direct quotations from participants that support the identified theme.
- 'Participant Count': Indicates the number of participants who mentioned or alluded to the theme. Please ensure this count reflects the actual number of participants who discussed each theme.
The table should be formatted strictly as follows:
The table should have 4 columns only.
Each column should be separated by a '|' symbol, and there should be no extra '|' symbols within the data. Each row should end with '---'.
Start the table with '**********'.
The header row should be: | 'Theme' | 'Description' | 'Quotes' | 'Participant Count' |
Followed by a row of '|---|---|---|---|'.
End the table with '**********'.
Each subsequent row should represent a theme and its details, with columns separated by '|'.
Ensure each row of the table represents a distinct theme and its associated details.

IMPORTANT: Output ONLY the table with no additional text, commentary, or explanations. Do not include phrases like 'Here is the table', 'Below is the analysis', or 'Certainly!'. Start your response immediately with '**********' and end with '**********'. Do not use markdown formatting or code blocks.""",
    
    "Social Media Posts": """You need to analyze an dataset of Social Media Posts.
Please identify the top {num_themes} key themes from the interview and organize the results in a structured table format.
The table should includes these items:
- 'Theme': Represents the main idea or topic identified from the interview.
- 'Description': Provides a brief explanation or summary of the theme.
- 'Quotes': Contains direct quotations from participants that support the identified theme.
- 'Participant Count': Indicates the number of participants who mentioned or alluded to the theme.
The table should be formatted as follows:
Each column should be separated by a '|' symbol, and there should be no extra '|' symbols within the data. Each row should end with '---'.
The whole table should start with '**********' and end with '**********'.
Columns: | 'Theme' | 'Description' | 'Quotes' | 'Participant Count' |.
Ensure each row of the table represents a distinct theme and its associated details.

IMPORTANT: Output ONLY the table with no additional text, commentary, or explanations. Do not include phrases like 'Here is the table', 'Below is the analysis', or 'Certainly!'. Start your response immediately with '**********' and end with '**********'. Do not use markdown formatting or code blocks."""
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test_api', methods=['POST'])
def test_api():
    try:
        data = request.json
        api_key = data.get('api_key')
        
        if not api_key:
            return jsonify({'success': False, 'error': 'API key is required'})
        
        # Test the API key with new OpenAI client
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "test"}
            ],
            max_tokens=10
        )
        
        return jsonify({'success': True, 'message': 'API key is valid'})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/upload_file', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file uploaded'})
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'})
        
        if not allowed_file(file.filename):
            return jsonify({'success': False, 'error': 'Invalid file type'})
        
        # Process the file based on its type
        filename = secure_filename(file.filename)
        file_ext = filename.rsplit('.', 1)[1].lower()
        
        if file_ext == 'csv':
            data = pd.read_csv(file)
        elif file_ext == 'xlsx':
            data = pd.read_excel(file)
        elif file_ext == 'docx':
            doc = Document(file)
            full_text = []
            for para in doc.paragraphs:
                if para.text.strip():
                    full_text.append(para.text)
            data = pd.DataFrame(full_text, columns=['Content'])
        
        # Convert data to string format
        headers = list(data.columns)
        data_content = '\n'.join(data.apply(lambda row: ' '.join(row.astype(str)), axis=1))
        
        return jsonify({
            'success': True,
            'headers': headers,
            'data_content': data_content,
            'preview': data_content[:1000] + '...' if len(data_content) > 1000 else data_content
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.json
        api_key = data.get('api_key')
        data_content = data.get('data_content')
        data_type = data.get('data_type')
        num_themes = data.get('num_themes', 10)
        custom_prompt = data.get('custom_prompt', '')
        enable_role_playing = data.get('enable_role_playing', False)
        
        if not api_key or not data_content:
            return jsonify({'success': False, 'error': 'API key and data content are required'})
        
        # Create OpenAI client with API key
        client = OpenAI(api_key=api_key)
        
        # Get the appropriate prompt
        if custom_prompt:
            prompt = custom_prompt
        else:
            prompt = PROMPTS.get(data_type, PROMPTS['Interview']).format(num_themes=num_themes)
        
        # Add role playing if enabled
        if enable_role_playing:
            system_message = "You are an excellent qualitative data analyst and qualitative research expert. Follow the output format instructions exactly with no additional commentary."
        else:
            system_message = "You are a helpful assistant. Follow the output format instructions exactly with no additional commentary."
        
        # Split data into segments if it's too large
        segments = split_into_segments(data_content)
        all_responses = []
        
        for i, segment in enumerate(segments):
            combined_message = segment + "\n\n" + prompt
            
            messages = [
                {"role": "system", "content": system_message},
                {"role": "user", "content": combined_message}
            ]
            
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                temperature=0.7,
                max_tokens=4000
            )
            
            all_responses.append(response.choices[0].message.content)
        
        # If multiple segments, merge and re-analyze
        if len(segments) > 1:
            merged_responses = "\n".join(all_responses)
            final_response = analyze_merged_responses(merged_responses, num_themes, system_message, client)
        else:
            final_response = all_responses[0]
        
        return jsonify({
            'success': True,
            'response': final_response,
            'segments_processed': len(segments)
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

def split_into_segments(text, max_tokens=120000):
    """Split text into segments that fit within GPT-4o's token limits
    
    GPT-4o has 128k context window, so we use 120k for data and reserve 8k for prompts/responses.
    This is a ~30x increase from the previous 3800 token limit for GPT-3.5-turbo.
    Most datasets will now process in a single call.
    """
    try:
        sentences = sent_tokenize(text)
    except:
        # Fallback to simple splitting if NLTK fails
        sentences = text.split('.')
        sentences = [s + '.' for s in sentences if s.strip()]
    
    segments = []
    segment = ""
    segment_tokens = 0
    
    for sentence in sentences:
        num_tokens = len(word_tokenize(sentence)) if 'word_tokenize' in globals() else len(sentence.split())
        
        if segment_tokens + num_tokens > max_tokens:
            segments.append(segment.strip())
            segment = sentence
            segment_tokens = num_tokens
        else:
            segment += " " + sentence
            segment_tokens += num_tokens
    
    if segment:
        segments.append(segment.strip())
    
    return segments

def analyze_merged_responses(merged_responses, num_themes, system_message, client):
    """Analyze merged responses to create a final summary"""
    prompt = f"""This is the result of a thematic analysis of several parts of the dataset. Now, summarize the same themes to generate a new table.
Please identify the {num_themes} most common key themes from the interview and organize the results in a structured table format.
The table should include the following columns:
'Theme': Represents the main idea or topic identified from the interview.
'Description': Provides a brief explanation or summary of the theme.
'Quotes': Contains direct quotations from participants that support the identified theme.
'Participant Count': Indicates the number of participants who mentioned or alluded to the theme.
The table should be formatted strictly as follows:
- Start the table with '**********'.
- The header row should be: | 'Theme' | 'Description' | 'Quotes' | 'Participant Count' |
- Followed by a row of '|---|---|---|---|'.
- Each subsequent row should represent a theme and its details, with columns separated by '|'.
- Each row should end with '---'.
- End the table with '**********'.
Ensure each row of the table represents a distinct theme and its associated details.

IMPORTANT: Output ONLY the table with no additional text, commentary, or explanations. Do not include phrases like 'Here is the table', 'Below is the analysis', or 'Certainly!'. Start your response immediately with '**********' and end with '**********'. Do not use markdown formatting or code blocks.

Analyze the following merged responses: {merged_responses}"""
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=4000
    )
    
    return response.choices[0].message.content

@app.route('/export_csv', methods=['POST'])
def export_csv():
    try:
        data = request.json
        response_content = data.get('response', '')
        
        # Parse the response to extract table data
        parsed_data = parse_response_to_csv(response_content)
        
        if not parsed_data:
            return jsonify({'success': False, 'error': 'Failed to parse the response'})
        
        # Create DataFrame
        df = pd.DataFrame(parsed_data[1:], columns=parsed_data[0])
        
        # Create CSV in memory
        output = io.StringIO()
        df.to_csv(output, index=False)
        output.seek(0)
        
        # Create response
        return send_file(
            io.BytesIO(output.getvalue().encode()),
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'qualigpt_analysis_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        )
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

def parse_response_to_csv(response):
    """Parse the GPT response to extract table data"""
    lines = response.strip().split("\n")
    
    # Find table delimiters
    delimiter_indices = [i for i, line in enumerate(lines) if line.strip() == "**********"]
    
    if len(delimiter_indices) < 2:
        return []
    
    start_index, end_index = delimiter_indices[0], delimiter_indices[-1]
    table_content = lines[start_index+1:end_index]
    
    # Parse table rows
    parsed_data = []
    for line in table_content:
        if line.strip() and '|' in line and not line.strip().startswith('|---'):
            # Split by | and clean up
            cells = [cell.strip() for cell in line.split('|')]
            # Remove empty cells at start and end
            cells = [cell for cell in cells if cell]
            if cells:
                parsed_data.append(cells)
    
    return parsed_data

if __name__ == '__main__':
    app.run(debug=True, port=5000)
