#!/usr/bin/env python
# coding: utf-8

# In[3]:
# QualiGPT-v0.1.0-alpha - created by @He Albert Zhang

import sys
import pandas as pd
import openai
import traceback
import nltk
from docx import Document
from nltk.tokenize import sent_tokenize
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QLineEdit, QFileDialog, QTextEdit, QFormLayout, QComboBox, QMessageBox
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QRadioButton, QButtonGroup, QSpinBox
import re
import csv
import docx2txt
from nltk.tokenize import sent_tokenize, word_tokenize

class QualiGPTApp(QMainWindow):

    def __init__(self):
        super().__init__()

        # Initialize the API connection flag
        self.connected_to_api = False
        self.TESTING = False
        
        self.current_dataset = None  # Add this line
        self.dataset_segments = []
        self.saved_segments = []
        self.all_responses = [] # 用于存储所有的响应

        # Initialize prompts dictionary
        self.prompts = {
                "Interview": "You need to analyze an dataset of interviews. \
                \nPlease identify the top {num_themes} key themes from the interview and organize the results in a structured table format. \
                \nThe table should includes these items:\
                \n- 'Theme': Represents the main idea or topic identified from the interview.\
                \n- 'Description': Provides a brief explanation or summary of the theme.\
                \n- 'Quotes': Contains direct quotations from participants that support the identified theme.\
                \n- 'Participant Count': Indicates the number of participants who mentioned or alluded to the theme.\
                \nThe table should be formatted as follows: \
                \nEach column should be separated by a '|' symbol, and there should be no extra '|' symbols within the data. Each row should end with '---'. \
                \nThe whole table should start with '**********' and end with '**********'.\
                \nColumns: | 'Theme' | 'Description' | 'Quotes' | 'Participant Count' |. \
                \nEnsure each row of the table represents a distinct theme and its associated details. Aggregate the counts for each theme to show the total number of mentions across all participants.",
            "Focus Group": "You need to analyze an dataset of a focus group. \
                \nPlease identify the {num_themes} most common key themes from the interview and organize the results in a structured table format. \
                \nThe table should includes these items:\
                \n- 'Theme': Represents the main idea or topic identified from the interview.\
                \n- 'Description': Provides a brief explanation or summary of the theme.\
                \n- 'Quotes': Contains direct quotations from participants that support the identified theme.\
                \n- 'Participant Count': Indicates the number of participants who mentioned or alluded to the theme. Please ensure this count reflects the actual number of participants who discussed each theme.\
                \nThe table should be formatted strictly as follows: \
                \nThe table should have 4 columns only.\
                \nEach column should be separated by a '|' symbol, and there should be no extra '|' symbols within the data. Each row should end with '---'. \
                \nStart the table with '**********'.\
                \nThe header row should be: | 'Theme' | 'Description' | 'Quotes' | 'Participant Count' | \
                \nFollowed by a row of '|---|---|---|---|'.\
                \nEnd the table with '**********'.\
                \nEach subsequent row should represent a theme and its details, with columns separated by '|'.\
                \nEnsure each row of the table represents a distinct theme and its associated details.",
            "Social Media Posts": "You need to analyze an dataset of Social Media Posts. \
                \nPlease identify the top {num_themes} key themes from the interview and organize the results in a structured table format. \
                \nThe table should includes these items:\
                \n- 'Theme': Represents the main idea or topic identified from the interview.\
                \n- 'Description': Provides a brief explanation or summary of the theme.\
                \n- 'Quotes': Contains direct quotations from participants that support the identified theme.\
                \n- 'Participant Count': Indicates the number of participants who mentioned or alluded to the theme.\
                \nThe table should be formatted as follows: \
                \nEach column should be separated by a '|' symbol, and there should be no extra '|' symbols within the data. Each row should end with '---'. \
                \nThe whole table should start with '**********' and end with '**********'.\
                \nColumns: | 'Theme' | 'Description' | 'Quotes' | 'Participant Count' |. \
                \nEnsure each row of the table represents a distinct theme and its associated details."
            }

        # Initialize window
        self.setWindowTitle("QualiGPT: Qualitative Data Analysis Tool")
        self.setGeometry(200, 200, 800, 600)

        # Initialize central widget
        self.central_widget = QWidget()
        self.layout = QVBoxLayout(self.central_widget)
        
        # Initialize elements
        self.init_elements()

        # Set central widget
        self.setCentralWidget(self.central_widget)

    def init_elements(self):
        # API Key input
        self.api_key_label = QLabel("Enter API Key:")
        self.layout.addWidget(self.api_key_label)

        self.api_key_input = QLineEdit(self)
        self.api_key_input.setEchoMode(QLineEdit.Password)  # 设置为Password模式，这样输入的内容会显示为***
        self.layout.addWidget(self.api_key_input)
        
        # Connect to OpenAI API Button
        self.connect_button = QPushButton("Connect with OpenAI")
        self.connect_button.clicked.connect(self.test_api_key)
        self.layout.addWidget(self.connect_button)

        # API connection status
        self.api_status_label = QLabel("API Connection: Disconnected")
        self.layout.addWidget(self.api_status_label)

        # Import CSV or Excel file Button
        self.import_button = QPushButton("Import Word, CSV or Excel File")
        self.import_button.clicked.connect(self.get_file)
        self.layout.addWidget(self.import_button)
        
        # Submit dataset to ChatGPT API Button
        self.submit_dataset_button = QPushButton("Submit Dataset")
        self.submit_dataset_button.clicked.connect(self.submit_dataset)
        self.layout.addWidget(self.submit_dataset_button)

        # Header meanings
        self.header_form = QFormLayout()
        self.layout.addLayout(self.header_form)

        # Header meanings button
        self.header_button = QPushButton("Submit Header Meanings")
        self.header_button.clicked.connect(self.get_header_meanings)
        self.layout.addWidget(self.header_button)

        # Display data area
        self.text_area = QTextEdit()
        self.layout.addWidget(self.text_area)
        
        # Role playing option
        self.role_playing_checkbox = QCheckBox("Enable Role Playing")
        self.layout.addWidget(self.role_playing_checkbox)
        
        # Data type selection
        self.data_type_label = QLabel("Select Data Type:")
        self.layout.addWidget(self.data_type_label)

        # 使用QRadioButton代替QComboBox
        self.interview_radio = QRadioButton("Interview")
        self.focus_group_radio = QRadioButton("Focus Group")
        self.social_media_radio = QRadioButton("Social Media Posts")
        
         # 将单选框添加到布局中
        self.layout.addWidget(self.interview_radio)
        self.layout.addWidget(self.focus_group_radio)
        self.layout.addWidget(self.social_media_radio)

        # 使用QButtonGroup确保只有一个单选框被选中
        self.data_type_group = QButtonGroup(self)
        self.data_type_group.addButton(self.interview_radio)
        self.data_type_group.addButton(self.focus_group_radio)
        self.data_type_group.addButton(self.social_media_radio)
        
        # 连接信号和槽
        self.interview_radio.toggled.connect(self.update_preset_prompts)
        self.focus_group_radio.toggled.connect(self.update_preset_prompts)
        self.social_media_radio.toggled.connect(self.update_preset_prompts)
        
        # Number of key themes selection
        self.key_themes_label = QLabel("Select Number of Key Themes:")
        self.layout.addWidget(self.key_themes_label)
        
        self.key_themes_spinbox = QSpinBox(self)
        self.key_themes_spinbox.setMinimum(1)
        self.key_themes_spinbox.setMaximum(20)  # You can adjust this maximum value as needed
        self.key_themes_spinbox.setValue(10)  # Default value
        self.layout.addWidget(self.key_themes_spinbox)

        # Preset prompts
        self.preset_prompts = QComboBox()
        self.update_preset_prompts()
        self.layout.addWidget(self.preset_prompts)
    

        # Custom prompt entry
        self.custom_prompt_entry = QLineEdit()
        self.custom_prompt_entry.setPlaceholderText("(optional) Enter your additional prompts here...")
        self.layout.addWidget(self.custom_prompt_entry)

        # Submit prompt and call ChatGPT API Button
        self.chatgpt_button = QPushButton("Submit Prompt and Call ChatGPT API")
        self.chatgpt_button.clicked.connect(self.call_chatgpt)
        self.layout.addWidget(self.chatgpt_button)
        
        # 添加保存按钮
        self.save_button = QPushButton("Save Analysis Result")
        self.save_button.clicked.connect(self.save_result)
        self.layout.addWidget(self.save_button)
        
        #save to csv
        self.export_btn = QPushButton("Export to CSV")
        self.export_btn.clicked.connect(self.export_to_csv)
        self.layout.addWidget(self.export_btn)

        # 添加加载按钮
        self.load_button = QPushButton("Load Analysis Result")
        self.load_button.clicked.connect(self.load_result)
        self.layout.addWidget(self.load_button)
        
    def update_preset_prompts(self):
        #current_data_type = self.data_type_selection.currentText()
            
         # 使用QRadioButton的isChecked()方法来检查哪个单选框被选中
        if self.interview_radio.isChecked():
            current_data_type = "Interview"
        elif self.focus_group_radio.isChecked():
            current_data_type = "Focus Group"
        elif self.social_media_radio.isChecked():
            current_data_type = "Social Media Posts"
        else:
            current_data_type = ""
    
        self.preset_prompts.clear()
        if current_data_type in self.prompts:
            self.preset_prompts.addItem(self.prompts[current_data_type])
        
    def test_api_key(self):
        api_key = self.api_key_input.text()
        if api_key == "albert":
            api_key = "copy-right by He (Albert) Zhang "
            #this application belongs to He (Albert) Zhang - hpz5211@psu.edu
        openai.api_key = api_key
        try:
            # Simple test call to OpenAI
            openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "test"},
                ]
            )
            self.api_status_label.setText("API Connection: Connected")
            self.connected_to_api = True
            self.TESTING = False
            QMessageBox.information(self, "Success", "API Key is valid. You are now connected to OpenAI.")
        except Exception as e:
            traceback.print_exc()
            self.api_status_label.setText("API Connection: Disconnected")
            self.connected_to_api = False
            self.TESTING = True
            QMessageBox.critical(self, "Error", "API Key is invalid. You are now in Testing mode.")


    def get_file(self):
        if not self.connected_to_api and not self.TESTING:
            QMessageBox.warning(self, "Warning", "Please connect to the OpenAI API first.")
            return

        file_path, _ = QFileDialog.getOpenFileName(self, "Open Word, CSV or Excel File", "", "CSV Files (*.csv);;Excel Files (*.xlsx);;Word Files (*.docx)")
        
        if not file_path:  # User might have cancelled the file dialog
            return

        try:
            if file_path.endswith('.csv'):
                data = pd.read_csv(file_path, encoding='utf-8')
            elif file_path.endswith('.xlsx'):
                data = pd.read_excel(file_path, engine='openpyxl')
            elif file_path.endswith('.docx'):
                doc = Document(file_path)
                full_text = []
                for para in doc.paragraphs:
                    full_text.append(para.text)
                data = pd.DataFrame(full_text, columns=['Content'])
            else:
                QMessageBox.warning(self, "Warning", "Unsupported file type.")
                return
        except UnicodeDecodeError:
            try:
                if file_path.endswith('.csv'):
                    data = pd.read_csv(file_path, encoding='ISO-8859-1')
                elif file_path.endswith('.xlsx'):
                    data = pd.read_excel(file_path, engine='openpyxl')
            except Exception as e:
                QMessageBox.warning(self, "Warning", f"Unrecognized file format or encoding issue: {str(e)}")
                return
        
        if 'data' in locals():
            self.headers = list(data.columns)
            self.data_content = '\n'.join(data.apply(lambda row: ' '.join(row.astype(str)), axis=1))
        else:
            QMessageBox.warning(self, "Warning", "Unable to process the selected file.")
            return
        
        self.headers = list(data.columns)
        self.data_content = '\n'.join(data.apply(lambda row: ' '.join(row.astype(str)), axis=1))

        # Clear header form layout
        for i in reversed(range(self.header_form.count())):
            self.header_form.itemAt(i).widget().setParent(None)

        # Generate QLabel and QLineEdit objects for header meanings
        self.header_fields = []
        for header in self.headers:
            label = QLabel(header)
            entry = QLineEdit()
            entry.setPlaceholderText("(optional) Please describe the meaning of the label")  # 设置占位符文本
            self.header_form.addRow(label, entry)
            self.header_fields.append(entry)

        self.text_area.setText(self.data_content)

    def get_header_meanings(self):
        if not self.connected_to_api and not self.TESTING:
            QMessageBox.warning(self, "Warning", "Please connect to the OpenAI API first.")
            return

        header_meanings = []
        for header_field, header in zip(self.header_fields, self.headers):
            header_meaning = header_field.text().strip()
            if header_meaning:
                header_meanings.append(header_meaning)
            else:
                header_meanings.append(header)

        QMessageBox.information(self, "Header Meanings", f"Header Meanings: {', '.join(header_meanings)}")

    def call_chatgpt(self):
        api_key = self.api_key_input.text()
    
        if not self.connected_to_api and not self.TESTING:
            QMessageBox.warning(self, "Warning", "Please connect to the OpenAI API first.")
            return
    
        num_themes = self.key_themes_spinbox.value()
        prompt = self.custom_prompt_entry.text().strip()
        if not prompt:
            prompt = self.preset_prompts.currentText().format(num_themes=num_themes)
    
        # Combine the dataset and the prompt into a single message
        #combined_message = self.data_content + "\n\n" + prompt
        if len(self.dataset_segments) > 1:
            
            for segment in self.saved_segments:
            # Construct the full prompt for this segment
                combined_message = segment + "\n\n" + prompt  # Use the same prompt for each segment
                # Display the prompt being sent to the API
                self.display_prompt(combined_message)
                # Send the segment to the API
                try:
                    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": combined_message}
                    ])
                    response_content = response['choices'][0]['message']['content']
                    self.all_responses.append(response_content) # save the response
                    
                    # Check if the response is close to the token limit
                    if len(response_content.split()) > 4000:  # This is an arbitrary number, adjust as needed
                        QMessageBox.warning(self, "Warning", "The response might be truncated due to token limits.")
                    
                    self.text_area.moveCursor(QTextCursor.End)
                    self.text_area.append("Response:\n" + response_content)
                except openai.error.OpenAIError as e:
                    print(f"OpenAI Error: {str(e)}")
                    QMessageBox.critical(self, "Error", f"Failed to call ChatGPT API. OpenAI Error: {str(e)}")
                except Exception as e:
                    print(f"Other Error: {str(e)}")
                    QMessageBox.critical(self, "Error", f"Failed to call ChatGPT API. Other Error: {str(e)}")
            # After processing all segments, merge the responses and analyze again
            merged_responses = "\n".join(self.all_responses)
            self.analyze_merged_responses(merged_responses)
        else:
            combined_message = self.data_content + "\n\n" + prompt
            # Display the prompt being sent to the API
            self.display_prompt(combined_message)
             # Send the segment to the API
            try:
                response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": combined_message}
                ])
                response_content = response['choices'][0]['message']['content']
                self.all_responses.append(response_content) # save the response
                
                # Check if the response is close to the token limit
                if len(response_content.split()) > 4000:  # This is an arbitrary number, adjust as needed
                    QMessageBox.warning(self, "Warning", "The response might be truncated due to token limits.")
                
                self.text_area.moveCursor(QTextCursor.End)
                self.text_area.append("Response:\n" + response_content)
            except openai.error.OpenAIError as e:
                print(f"OpenAI Error: {str(e)}")
                QMessageBox.critical(self, "Error", f"Failed to call ChatGPT API. OpenAI Error: {str(e)}")
            except Exception as e:
                print(f"Other Error: {str(e)}")
                QMessageBox.critical(self, "Error", f"Failed to call ChatGPT API. Other Error: {str(e)}")
                
    def display_prompt(self, prompt):
        self.text_area.moveCursor(QTextCursor.End)
        self.text_area.append("Prompt Sent to API:\n" + prompt + "\n\n")
        
    def analyze_merged_responses(self, merged_responses):
        # Construct a new prompt for the merged responses
        new_prompt = "This is the result of a thematic analysis of several parts of the dataset. Now, summarize the same themes to generate a new table. \
        \nPlease identify the {num_themes} most common key themes from the interview and organize the results in a structured table format. \
        \nThe table should include the following columns:\
        \n'Theme': Represents the main idea or topic identified from the interview.\
        \n'Description': Provides a brief explanation or summary of the theme.\
        \n'Quotes': Contains direct quotations from participants that support the identified theme.\
        \n'Participant Count': Indicates the number of participants who mentioned or alluded to the theme. Ensure this count reflects the actual number of participants who discussed each theme.\
        \nThe table should be formatted strictly as follows:\
\n- Start the table with '**********'.\
\n- The header row should be: | 'Theme' | 'Description' | 'Quotes' | 'Participant Count' |\
\n- Followed by a row of '|---|---|---|---|'.\
\n- Each subsequent row should represent a theme and its details, with columns separated by '|'.\
\n- Each row should end with '---'.\
\n- End the table with '**********'.\
\nEnsure each row of the table represents a distinct theme and its associated details. \
\nAnalyze the following merged responses: " + merged_responses
        self.display_prompt(new_prompt)
        try:
            response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": new_prompt}
            ])
            response_content = response['choices'][0]['message']['content']
            
            # Display the final analysis
            self.text_area.moveCursor(QTextCursor.End)
            self.text_area.append("Final Analysis:\n" + response_content)
        except openai.error.OpenAIError as e:
            print(f"OpenAI Error: {str(e)}")
            QMessageBox.critical(self, "Error", f"Failed to analyze merged responses. OpenAI Error: {str(e)}")
        except Exception as e:
            print(f"Other Error: {str(e)}")
            QMessageBox.critical(self, "Error", f"Failed to analyze merged responses. Other Error: {str(e)}")
   
    def submit_dataset(self):
        # 检查是否已经连接到OpenAI API
        if not self.connected_to_api and not self.TESTING:
            QMessageBox.warning(self, "Warning", "Please connect to the OpenAI API first.")
            return
       
        print("Data Content:", self.data_content[:500])  # Print the first 500 characters of the dataset for debugging
        print("Number of Segments:", len(self.dataset_segments))

         # 如果数据内容超过4096 tokens
        if len(self.data_content) > 4096:
            self.dataset_segments = self.split_into_segments(self.data_content, 4096 - 1500)  # Reserve some tokens for additional prompts
            # 不要在这里提交分段，只是保存它们
            self.saved_segments = self.dataset_segments
            QMessageBox.information(self, "Success", "Dataset has been segmented and is ready for analysis.")
        else:
            # 如果数据内容不超过4096 tokens
            self.saved_segments = [self.data_content]
        # 如果数据内容超过4096 tokens
        #if len(self.data_content) > 4096:
        #    self.dataset_segments = self.split_into_segments(self.data_content, 4096 - 300)  # Reserve some tokens for additional prompts
        #    for segment in self.dataset_segments:
        #        interim_prompt = segment + "\n(Note: This dataset has more content following this segment.)"
        #        try:
        #            response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[
        #                {"role": "system", "content": "You are a helpful assistant."},
        #                {"role": "user", "content": interim_prompt}
        #            ])
        #            print(f"Data segment successfully submitted.")
        #        except openai.error.OpenAIError as e:
        #            print(f"OpenAI Error: {str(e)}")
        #            QMessageBox.critical(self, "Error", f"Failed to submit dataset segment to ChatGPT API. OpenAI Error: {str(e)}")
        #            return
        #        except Exception as e:
        #            print(f"Other Error: {str(e)}")
        #            QMessageBox.critical(self, "Error", f"Failed to submit dataset segment to ChatGPT API. Other Error: {str(e)}")
        #            return
        #    # Split the data_content into segments
            

            QMessageBox.information(self, "Success", "Dataset has been segmented and is ready for analysis.")

    def save_result(self):
        # 获取保存路径
        save_path, _ = QFileDialog.getSaveFileName(self, "Save Analysis Result", "", "Text Files (*.txt);;CSV Files (*.csv)")
        if save_path:
            with open(save_path, "w") as f:
                f.write(self.text_area.toPlainText())

    def export_to_csv(self):
        # 获取text_area的内容
        full_content = self.text_area.toPlainText()

        # 提取Response:之后的内容
        response_content = full_content.split("Response:\n", 1)
        if len(response_content) > 1:
            response_content = response_content[1].strip()
        else:
            response_content = ""
        # Print the entire response for debugging
        print("Full Response:\n", response_content)
        
        # Parse the response content
        parsed_data = self.parse_response_to_csv(response_content)
        
        # Diagnostic print statements
        print("Parsed Data:", parsed_data)
        print("Length of Parsed Data:", len(parsed_data))
        
        # Check if parsed_data is empty
        if not parsed_data:
            QMessageBox.critical(self, "Error", "Failed to parse the data. Please ensure the response is in the expected format.")
            return
        
        # Check for mismatched column counts
        expected_columns = 4
        mismatched_rows = [index for index, row in enumerate(parsed_data, start=1) if len(row) != expected_columns]
        
        if mismatched_rows:
            # Print the mismatched rows for debugging
            for index in mismatched_rows:
                print(f"Row {index}: {parsed_data[index-1]}")  # index-1 because mismatched_rows starts from 1
            
            QMessageBox.critical(self, "Error", f"Data mismatch. Expected {expected_columns} columns but found different column counts in rows: {', '.join(map(str, mismatched_rows))}. Please review the data.")
            return
    
        # Assuming the first row contains column headers
        df = pd.DataFrame(parsed_data[1:], columns=parsed_data[0])

        # Get save path
        save_path, _ = QFileDialog.getSaveFileName(self, "Export to CSV", "", "CSV Files (*.csv)")

        if save_path:
            df.to_csv(save_path, index=False)  # Ensure not to save row indices
    def submit_next_segment(self):
        if self.current_segment_index < len(self.segments):
            segment = self.segments[self.current_segment_index]
            interim_prompt = segment + "\n(Note: This dataset has more content following this segment.)"
            try:
                response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": interim_prompt}
                ])
                self.responses.append(response['choices'][0]['message']['content'])
                self.current_segment_index += 1
                if self.current_segment_index < len(self.segments):
                    QMessageBox.information(self, "Progress", f"Segment {self.current_segment_index} out of {len(self.segments)} has been submitted. Please submit the next segment.")
                else:
                    QMessageBox.information(self, "Success", "All segments have been successfully submitted to the API.")
            except openai.error.OpenAIError as e:
                print(f"OpenAI Error: {str(e)}")
                QMessageBox.critical(self, "Error", f"Failed to submit dataset segment to ChatGPT API. OpenAI Error: {str(e)}")
            except Exception as e:
                print(f"Other Error: {str(e)}")
                QMessageBox.critical(self, "Error", f"Failed to submit dataset segment to ChatGPT API. Other Error: {str(e)}")


    def load_result(self):
        # 获取加载路径
        load_path, _ = QFileDialog.getOpenFileName(self, "Load Analysis Result", "", "Text Files (*.txt);;CSV Files (*.csv)")
        if load_path:
            with open(load_path, "r") as f:
                self.text_area.setText(f.read())
    
    def parse_response_to_csv(self, response):
        # Split the response into lines
        lines = response.strip().split("\n")

        # Find all occurrences of the table delimiter
        delimiter_indices = [i for i, line in enumerate(lines) if line.strip() == "**********"]

        # If there are fewer than two delimiters, return an empty list
        if len(delimiter_indices) < 2:
            return []

        # Use the first and last occurrences of the delimiter to identify the start and end of the table
        start_index, end_index = delimiter_indices[0], delimiter_indices[-1]

        # Extract the table content
        table_content = lines[start_index+1:end_index]

        # Split each line into columns based on the '|' character
        parsed_data = [line.split("|")[1:-1] for line in table_content if line.strip()]  # Exclude the first and last elements

        # Remove whitespace from each cell
        parsed_data = [[cell.strip() for cell in row] for row in parsed_data if len(row) > 1]  # Ensure we don't include rows with only one cell

        return parsed_data
    
    def send_segments_to_chatgpt(self, data_content, prompt):
        # Split the data_content into segments
        segments = self.split_into_segments(data_content, 4096 - 1500)  # Reserve some tokens for additional prompts
    
        # Initialize a list to store responses
        responses = []
    
        # Send each segment to ChatGPT with a continuation prompt
        for i, segment in enumerate(segments):
            # Check if it's the last segment
            if i == len(segments) - 1:
                # If it's the last segment, use the main prompt
                current_prompt = prompt
            else:
                # Otherwise, use a continuation prompt
                current_prompt = "Continuing with the next segment of data..."
    
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": current_prompt},
                {"role": "user", "content": segment}
            ]
    
            try:
                response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
                responses.append(response['choices'][0]['message']['content'])
            except openai.error.OpenAIError as e:
                print(f"OpenAI Error: {str(e)}")
                QMessageBox.critical(self, "Error", f"Failed to call ChatGPT API. OpenAI Error: {str(e)}")
                return None
            except Exception as e:
                print(f"Other Error: {str(e)}")
                QMessageBox.critical(self, "Error", f"Failed to call ChatGPT API. Other Error: {str(e)}")
                return None
    
        # Combine all the responses
        combined_response = "\n".join(responses)
        return combined_response

    def split_into_segments(self, text, max_tokens = 3800):
        sentences = sent_tokenize(text)
        segments = []
        segment = ""
        segment_tokens = 0

        for sentence in sentences:
            num_tokens = len(word_tokenize(sentence))
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

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = QualiGPTApp()
    window.show()

    sys.exit(app.exec_())

