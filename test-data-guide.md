# QualiGPT Test Data Guide

I've created three sample datasets for you to test the QualiGPT webapp:

## 1. Focus Group Data (CSV)
**File:** `remote_work_focus_group.csv`
- 15 participants discussing transition to remote work
- Good for testing "Focus Group" analysis type
- Tests the app's ability to identify themes across multiple participants

## 2. Interview Transcript (DOCX)
**File:** `education_interview.docx`
- Single in-depth interview about digital transformation in education  
- Good for testing "Interview" analysis type
- Tests processing of unstructured text documents

## 3. Social Media Posts (XLSX)
**File:** `social_media_education.xlsx`
- 10 social media posts about online learning
- Good for testing "Social Media Posts" analysis type
- Tests handling of short-form content with metadata

## How to Save the Files:

### For CSV files:
1. Copy the content from the artifact
2. Paste into a text editor (Notepad, TextEdit, VS Code)
3. Save as `.csv` file

### For DOCX files:
1. Copy the interview transcript content
2. Paste into Microsoft Word or Google Docs
3. Save as `.docx` file

### For XLSX files:
1. Copy the CSV content
2. Paste into Excel or Google Sheets
3. Save as `.xlsx` file

## Testing Suggestions:

1. **Start with the Focus Group CSV** - It's the most straightforward and will show you how the tool identifies multiple themes

2. **Try different numbers of themes** - Set it to extract 5, 10, or 15 themes to see how the analysis changes

3. **Enable "Role Playing" mode** - This activates expert analysis mode for more detailed insights

4. **Test large file handling** - The focus group data is large enough to test the segmentation feature

5. **Compare analysis types** - Try analyzing the same file with different data type settings to see how it affects results

## Expected Results:

- **Focus Group**: Should identify themes like "work-life balance," "communication challenges," "flexibility benefits," "technology adaptation"
- **Interview**: Should extract themes about "digital transformation challenges," "student engagement," "assessment methods"
- **Social Media**: Should capture themes like "screen time concerns," "digital equity," "parent challenges," "student experiences"

These datasets are designed to showcase QualiGPT's ability to extract meaningful themes from different types of qualitative data!