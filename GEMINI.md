# **AI-Powered Quiz Generator**

## **Project Overview**

This application provides a secure, web-based tool for instantly generating educational content. Users upload a PDF document, receive a summary of its contents, and then leverage a Gemini AI agent to create customizable multiple-choice quizzes based on the source text. The application uses a sleek Streamlit UI for an appealing and responsive user experience.

## **Core Features**

1. **Secure File Upload**: Dedicated tab for uploading PDF documents.  
2. **PDF Text Extraction**: Uses PyPDF to robustly extract all textual content from the uploaded file.  
3. **Content Summarization**: The Gemini Agent generates a concise, high-quality summary of the PDF content, displayed in a dedicated tab.  
4. **Custom Quiz Generation**: Users select the desired **Number of Quizzes** (10, 15, 20, 25\) and **Difficulty Level** (Easy, Normal, Advanced).  
5. **Quiz Formatting**: Generated quizzes follow a strict, easy-to-read format (Bold Quiz, 4 options, Correct Answer listed last).  
6. **Actionable Output**: Options to copy or download all generated quizzes.  
7. **Iterative Generation**: Buttons to generate additional quiz sets (10, 15, 20, 25 more) or reset the session.

## **Tech Stack**

* **Language**: Python 3.11+  
* **UI Framework**: Streamlit (for beautiful, interactive web UI)  
* **AI Agent**: Gemini API (google-genai library)  
* **Model**: gemini-2.5-flash-preview-09-2025 (Selected for speed and reasoning quality)  
* **PDF Handling**: PyPDF  
* **Environment/Package Manager**: UV (for high-speed dependency management and virtual environments)  
* **Environment Variables**: .env file for secure API key handling.

## **Project Structure**

The structure is organized to separate the UI, LLM interaction, and configuration files.

quiz-app/  
├── .env                       \# Stores GEMINI\_API\_KEY  
├── requirements.txt           \# Python dependencies (streamlit, google-genai, pypdf)  
├── app.py                     \# Main Streamlit application (UI layout, state management, and orchestration)  
└── agent/  
    ├── gemini\_agent.py        \# Contains core functions for Gemini API calls (summarize\_pdf, generate\_quizzes)  
    └── \_\_init\_\_.py            \# Makes 'agent' a proper Python package

## **AI Agent Directives (agent/gemini\_agent.py)**

### **1\. Model & Key**

* **Model**: Use gemini-2.5-flash-preview-09-2025 for all text generation tasks.  
* **API Key**: Initialize the client using the API key loaded from the environment variable named GEMINI\_API\_KEY.

### **2\. Quiz Generation Rules (CRITICAL)**

* **Source Material**: The quiz generation prompt **MUST** explicitly instruct the agent to use the **full extracted PDF text**, not the generated summary, to ensure fidelity and complexity.  
* **Formatting Constraint**: The Agent must strictly adhere to the following output format for each quiz item:  
  \*\*Quiz 1\*\*: What is the primary function of the hippocampus in memory formation?  
  A) Motor coordination  
  B) Emotional regulation  
  C) Encoding new long-term memories  
  D) Sensory processing  
  Correct Answer: C

* **Difficulty Control**: The prompt must dynamically adjust the required complexity based on the user's radio button selection:  
  * **Easy**: Focus on definitions, facts, and directly stated concepts.  
  * **Normal**: Focus on key relationships, simple analysis, and application of concepts.  
  * **Advanced**: Focus on complex analysis, inference, synthesis, and critical evaluation.

## **Development and Debugging Loop**

**If, during the application build and test phase, the application encounters an error (e.g., failed API call, incorrect quiz formatting, Streamlit crash), the immediate action is to debug the issue, apply the fix, and then rerun the application from the corrected state until all features are fully functional and meet the requirements.**

This iterative debugging process is mandatory to ensure application stability and compliance with all formatting rules.

## **Setup Instructions**

### **1\. Environment and Dependencies**

\# Create a virtual environment using UV  
uv venv

\# Activate the environment  
source .venv/bin/activate  \# Or .venv\\Scripts\\activate on Windows

\# Install dependencies  
uv pip install \-r requirements.txt

### **2\. Streamlit UI Design Notes (app.py)**

* Use Streamlit's built-in components and markdown for an attractive design.  
* Implement a multi-tab layout using st.tabs().  
* Use a vibrant color palette and responsive widths (st.container(width=True)).  
* Use st.expander for collapsible sections like "Quiz Generation Criteria" or "Download Options."  
* Ensure the quiz text area is scrollable and readable.

### **3\. API Key Management (.env)**

The .env file must contain your key. The application will load this automatically in Python using a library like python-dotenv.

GEMINI\_API\_KEY="YOUR\_API\_KEY\_HERE"  
