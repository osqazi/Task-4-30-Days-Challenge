import streamlit as st
from pypdf import PdfReader
from agent.gemini_agent import summarize_pdf, generate_quizzes
import io

# Initialize session state variables
if "summary" not in st.session_state:
    st.session_state.summary = ""
if "quizzes" not in st.session_state:
    st.session_state.quizzes = ""
if "extracted_text" not in st.session_state:
    st.session_state.extracted_text = ""
if "pdf_processed" not in st.session_state:
    st.session_state.pdf_processed = False

st.set_page_config(layout="wide", page_title="AI-Powered Quiz Generator by Owais Qazi - Friday 6pm to 9pm")

st.markdown(
    """
    <style>
    .reportview-container { background: #f0f2f6; }
    .main .block-container { padding-left: 2rem; padding-right: 2rem; padding-top: 1rem; padding-bottom: 1rem; }
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p { font-size: 1.2rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("📚 AI-Powered Quiz Generator by Owais Qazi - Friday 6pm to 9pm")
st.markdown("Upload a PDF, get a summary, and generate custom quizzes instantly!")

# --- PDF Upload and Processing ---
def extract_text_from_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

upload_tab, summary_tab, quiz_tab = st.tabs(["Upload PDF", "Summary", "Generate Quizzes"])

with upload_tab:
    st.header("Upload your PDF Document")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file is not None:
        if not st.session_state.pdf_processed:
            with st.spinner("Extracting text and summarizing..."):
                st.session_state.extracted_text = extract_text_from_pdf(uploaded_file)
                st.session_state.summary = summarize_pdf(st.session_state.extracted_text)
                st.session_state.pdf_processed = True
            st.success("PDF processed successfully!")
            st.rerun() # Rerun to display summary in the summary tab
        st.write("PDF Loaded: ", uploaded_file.name)

with summary_tab:
    st.header("Document Summary")
    if st.session_state.summary:
        st.write(st.session_state.summary)
    else:
        st.info("Upload a PDF in the 'Upload PDF' tab to see its summary here.")

with quiz_tab:
    st.header("Generate Quizzes")

    if not st.session_state.extracted_text:
        st.warning("Please upload a PDF document in the 'Upload PDF' tab first.")
    else:
        st.markdown("Select your quiz generation criteria:")

        col1, col2 = st.columns(2)
        with col1:
            num_quizzes_option = st.radio(
                "Number of Quizzes to Generate per batch:",
                (10, 15, 20, 25),
                index=0,
                key="num_quizzes_radio",
            )
        with col2:
            difficulty_level = st.radio(
                "Difficulty Level:",
                ("Easy", "Normal", "Advanced"),
                index=1,
                key="difficulty_radio",
            )

        if st.button("Generate Quizzes", key="generate_button"):
            with st.spinner(f"Generating {num_quizzes_option} '{difficulty_level}' quizzes..."):
                generated_quiz_set = generate_quizzes(
                    st.session_state.extracted_text, num_quizzes_option, difficulty_level
                )
                st.session_state.quizzes = generated_quiz_set # Overwrite for new generation
            st.success("Quizzes generated successfully!")

        if st.session_state.quizzes:
            st.subheader("Generated Quizzes")
            st.text_area(
                "Quizzes",
                st.session_state.quizzes,
                height=400,
                key="quiz_text_area"
            )

            st.markdown("---")
            st.subheader("Actions")
            col_copy, col_download, col_reset = st.columns(3)

            with col_copy:
                st.query_params["copy"] = True
                if st.query_params.get("copy") == ["True"]:
                    st.code(st.session_state.quizzes) # In a real app, you'd use st.write to send to clipboard via JS
                    st.success("Quizzes copied! (Check console for programmatic copy, or manually copy from text area)")
                    st.query_params["copy"] = False # Reset query param

            with col_download:
                st.download_button(
                    label="Download Quizzes",
                    data=st.session_state.quizzes,
                    file_name="generated_quizzes.txt",
                    mime="text/plain",
                    key="download_button",
                )

            with col_reset:
                if st.button("Reset Session", key="reset_button"):
                    st.session_state.summary = ""
                    st.session_state.quizzes = ""
                    st.session_state.extracted_text = ""
                    st.session_state.pdf_processed = False
                    st.success("Session reset!")
                    st.rerun()

            st.markdown("---")
            st.subheader("Iterative Generation (Add more quizzes)")
            iterative_num_quizzes = st.selectbox(
                "Add more quizzes:",
                (10, 15, 20, 25),
                key="iterative_num_quizzes"
            )
            if st.button(f"Add {iterative_num_quizzes} more quizzes", key="add_more_quizzes"):
                with st.spinner(f"Adding {iterative_num_quizzes} more '{difficulty_level}' quizzes..."):
                    additional_quizzes = generate_quizzes(
                        st.session_state.extracted_text, iterative_num_quizzes, difficulty_level
                    )
                    st.session_state.quizzes += "\n\n" + additional_quizzes # Append
                st.success(f"{iterative_num_quizzes} additional quizzes generated and added!")
                st.rerun() # Rerun to update the text area with appended quizzes
