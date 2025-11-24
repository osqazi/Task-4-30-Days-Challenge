import os
import google.generativeai as genai
from dotenv import load_dotenv
import streamlit as st

# Load environment variables
load_dotenv()

# TO RUN LOCALLY
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# TO RUN ON STREAMLIT SERVER
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

# Configure the Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Initialize the generative model
# Use gemini-2.5-flash-preview-09-2025 as specified in GEMINI.md
model = genai.GenerativeModel('gemini-2.5-flash-preview-09-2025')

def summarize_pdf(text_content: str) -> str:
    """
    Generates a concise summary of the provided text content using the Gemini API.
    """
    prompt = f"Please provide a concise, high-quality summary of the following text:\n\n{text_content}"
    response = model.generate_content(prompt)
    return response.text

def generate_quizzes(text_content: str, num_quizzes: int, difficulty: str) -> str:
    """
    Generates multiple-choice quizzes based on the provided text content, number of quizzes,
    and difficulty level using the Gemini API.
    Adheres strictly to the formatting and difficulty control rules.
    """
    difficulty_instructions = {
        "Easy": "Focus on definitions, facts, and directly stated concepts.",
        "Normal": "Focus on key relationships, simple analysis, and application of concepts.",
        "Advanced": "Focus on complex analysis, inference, synthesis, and critical evaluation."
    }
    
    prompt = f"""
    Generate {num_quizzes} multiple-choice quizzes based on the following text.
    Each quiz must have 4 options (A, B, C, D) and clearly state the correct answer at the end.
    The quizzes should adhere to a '{difficulty}' difficulty level. {difficulty_instructions.get(difficulty, '')}
    
    Strictly follow this output format for each quiz item:
    **Quiz 1**: What is the primary function of the hippocampus in memory formation?
    A) Motor coordination
    B) Emotional regulation
    C) Encoding new long-term memories
    D) Sensory processing
    Correct Answer: C

    **Quiz 2**: [Question]
    A) [Option A]
    B) [Option B]
    C) [Option C]
    D) [Option D]
    Correct Answer: [Correct Option Letter]

    Here is the text to generate quizzes from:
    {text_content}
    """
    response = model.generate_content(prompt)
    return response.text

if __name__ == "__main__":
    # This block can be used for testing the functions directly
    sample_text = "The quick brown fox jumps over the lazy dog. The fox is known for its agility."
    
    print("--- Summary ---")
    summary = summarize_pdf(sample_text)
    print(summary)
    
    print("\n--- Easy Quizzes (2) ---")
    easy_quizzes = generate_quizzes(sample_text, 2, "Easy")
    print(easy_quizzes)
    
    print("\n--- Advanced Quizzes (1) ---")
    advanced_quizzes = generate_quizzes(sample_text, 1, "Advanced")
    print(advanced_quizzes)
