import streamlit as st
from image_processor import preprocess_image
from gemini_service import GeminiService
from utils import load_env_variables
from datetime import datetime

# Configure Streamlit theme
st.set_page_config(
    page_title="Clarity - Image Analysis",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# Force dark theme
st.markdown("""
    <style>
        /* Force dark theme */
        [data-testid="stAppViewContainer"] {
            background-color: #121212;
        }
        
        [data-testid="stSidebar"] {
            background-color: #1E1E1E;
        }
        
        [data-testid="stToolbar"] {
            background-color: #1E1E1E;
        }
        
        [data-testid="stHeader"] {
            background-color: #121212;
        }
        
        .stTextInput > div > div > input {
            background-color: #1E1E1E;
            color: white;
        }
        
        .stSlider > div > div > div {
            background-color: #BB86FC;
        }
        
        .stUploadedFile {
            background-color: #1E1E1E !important;
        }
        
        .stMarkdown {
            color: white;
        }
        
        /* Analysis Results Styling */
        .analysis-container {
            background-color: #1E1E1E;
            border-radius: 15px;
            padding: 25px;
            margin: 20px 0;
            border-left: 5px solid #BB86FC;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        }
        
        .analysis-header {
            color: #BB86FC;
            font-size: 1.5rem;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #333;
        }
        
        .analysis-section {
            margin: 15px 0;
            padding: 15px;
            background-color: #2D2D2D;
            border-radius: 10px;
        }
        
        .section-title {
            color: #03DAC6;
            font-size: 1.1rem;
            margin-bottom: 10px;
            font-weight: 500;
        }
        
        .section-content {
            color: #E1E1E1;
            line-height: 1.6;
            font-size: 1.05rem;
        }
        
        /* Confidence Bar */
        .confidence-bar {
            margin-top: 20px;
            padding: 15px;
            background-color: #2D2D2D;
            border-radius: 10px;
        }
        
        .stProgress > div > div > div {
            background-color: #03DAC6;
        }
        
        /* Additional Details */
        .details-container {
            background-color: #2D2D2D;
            padding: 15px;
            border-radius: 10px;
            margin-top: 15px;
        }
        
        .details-item {
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px solid #333;
        }
        
        .details-label {
            color: #BB86FC;
            font-weight: 500;
        }
        
        .details-value {
            color: #03DAC6;
        }
    </style>
""", unsafe_allow_html=True)

def main():
    # Initialize chat history if not exists
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Title with custom styling
    st.markdown('<h1 class="main-header">Clarity - Intelligent Image Analysis</h1>', unsafe_allow_html=True)
    
    # Initialize Gemini service
    api_key = load_env_variables()["GOOGLE_API_KEY"]
    gemini_service = GeminiService(api_key)
    
    # Move sidebar settings outside of the columns
    with st.sidebar:
        st.markdown('<p class="sub-header">Image Settings</p>', unsafe_allow_html=True)
        analysis_mode = st.selectbox(
            "Analysis Mode",
            ["General Analysis", "Technical Details", "Artistic Analysis", "Object Detection"],
            key="analysis_mode"
        )
        if st.toggle("Compare Images", key="compare_toggle"):
            st.session_state.uploaded_file2 = st.file_uploader("Upload second image", type=["jpg", "jpeg", "png"], key="file2")
    
    # Create two columns for layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
        
        if uploaded_file:
            st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
    
    with col2:
        if uploaded_file:
            # Process image without slider values
            processed_image = preprocess_image(uploaded_file)
            
            if st.session_state.get('uploaded_file2'):
                # Process both images without slider values
                processed_image1 = preprocess_image(uploaded_file)
                processed_image2 = preprocess_image(st.session_state.uploaded_file2)
                
                # Display second image
                st.image(st.session_state.uploaded_file2, caption="Second Image", use_column_width=True)
                
                st.markdown('<p class="sub-header">Compare the images</p>', unsafe_allow_html=True)
                
                # Move quick prompts before the text input
                comparison_prompts = st.multiselect(
                    "Select questions to compare images",
                    [
                        "Compare the overall composition",
                        "What are the main differences?",
                        "Which image has better lighting?",
                        "Compare the colors and contrast",
                        "Compare the objects present",
                        "Which image appears older?",
                        "Compare the styles",
                        "Compare the emotions conveyed",
                        "Which image is more detailed?",
                        "Compare the backgrounds",
                        "Which image is more vibrant?",
                        "Compare the focal points",
                        "Which image tells a better story?",
                        "Compare the time periods",
                        "Which image is more professional?"
                    ],
                    key="comparison_prompts"  # Added key for state management
                )
                
                # Handle the question input
                if comparison_prompts:
                    question = " & ".join(comparison_prompts)
                    st.write(f"Selected questions: {question}")  # Show selected questions
                else:
                    question = st.text_input("Or type your own comparison question:", 
                                           placeholder="What would you like to compare between these images?")
                
                if question and st.button("Compare", type="primary"):
                    with st.spinner("✨ Comparing images..."):
                        try:
                            response = gemini_service.analyze_images_comparison(
                                processed_image1, 
                                processed_image2, 
                                question
                            )
                            
                            # Analysis Results Container
                            st.markdown('<h3 class="analysis-header">Analysis Results</h3>', unsafe_allow_html=True)
                            
                            # Main Analysis
                            st.markdown(
                                f"""
                                <div class="analysis-section">
                                    <div class="section-title">🔍 Comparison Analysis</div>
                                    <div class="section-content">{response["answer"]}</div>
                                </div>
                                """, 
                                unsafe_allow_html=True
                            )
                            
                            # Confidence Level
                            col1, col2 = st.columns([3, 1])
                            with col1:
                                st.markdown('<div class="section-title">✨ Confidence Level</div>', unsafe_allow_html=True)
                                st.progress(0.85, text="High Confidence")
                            
                            # Details
                            st.markdown(
                                """
                                <div class="details-container">
                                    <div class="details-item">
                                        <span class="details-label">Model</span>
                                        <span class="details-value">Gemini 1.5 Flash</span>
                                    </div>
                                    <div class="details-item">
                                        <span class="details-label">Processing Time</span>
                                        <span class="details-value">0.8s</span>
                                    </div>
                                    <div class="details-item">
                                        <span class="details-label">Status</span>
                                        <span class="details-value">Success</span>
                                    </div>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                            
                            if 'raw_response' in response:
                                with st.expander("Additional Details"):
                                    st.markdown("""
                                        <div style='background-color: var(--surface-color); padding: 15px; border-radius: 8px;'>
                                            <p><strong>Model:</strong> Gemini 1.5 Flash</p>
                                            <p><strong>Status:</strong> Success</p>
                                        </div>
                                    """, unsafe_allow_html=True)
                            
                            if 'confidence' in response:
                                confidence = float(response['confidence'])
                                st.progress(confidence, text=f"Confidence: {confidence*100:.0f}%")
                            
                            if response:
                                st.session_state.chat_history.append({
                                    'question': question,
                                    'answer': response['answer'],
                                    'timestamp': datetime.now().strftime("%H:%M:%S")
                                })
                                
                                with st.expander("Chat History"):
                                    for chat in st.session_state.chat_history:
                                        st.markdown(f"""
                                            <div class="chat-item">
                                                <div class="chat-timestamp">{chat['timestamp']}</div>
                                                <div class="chat-question">Q: {chat['question']}</div>
                                                <div class="chat-answer">A: {chat['answer']}</div>
                                            </div>
                                        """, unsafe_allow_html=True)
                                    
                        except Exception as e:
                            st.error(f"An error occurred: {str(e)}")
            else:
                # Process image without slider values
                processed_image = preprocess_image(uploaded_file)
                
                st.markdown('<p class="sub-header">Ask about the image</p>', unsafe_allow_html=True)
                question = st.text_input("", placeholder="What would you like to know about this image?")
                
                quick_prompts = st.multiselect(
                    "Quick Prompts",
                    ["Describe the scene", "List main objects", "Analyze colors", "Detect emotions", "Identify text"],
                    placeholder="Select common questions"
                )
                if quick_prompts:
                    question = " & ".join(quick_prompts)
                
                if question and st.button("Analyze", type="primary"):
                    with st.spinner("✨ Analyzing image..."):
                        try:
                            response = gemini_service.analyze_image(processed_image, question)
                            
                            # Analysis Results Container
                            st.markdown('<h3 class="analysis-header">Analysis Results</h3>', unsafe_allow_html=True)
                            
                            # Main Analysis
                            st.markdown(
                                f"""
                                <div class="analysis-section">
                                    <div class="section-title">🔍 Analysis</div>
                                    <div class="section-content">{response["answer"]}</div>
                                </div>
                                """, 
                                unsafe_allow_html=True
                            )
                            
                            # Confidence Level
                            col1, col2 = st.columns([3, 1])
                            with col1:
                                st.markdown('<div class="section-title">✨ Confidence Level</div>', unsafe_allow_html=True)
                                st.progress(0.85, text="High Confidence")
                            
                            # Details
                            st.markdown(
                                """
                                <div class="details-container">
                                    <div class="details-item">
                                        <span class="details-label">Model</span>
                                        <span class="details-value">Gemini 1.5 Flash</span>
                                    </div>
                                    <div class="details-item">
                                        <span class="details-label">Processing Time</span>
                                        <span class="details-value">0.8s</span>
                                    </div>
                                    <div class="details-item">
                                        <span class="details-label">Status</span>
                                        <span class="details-value">Success</span>
                                    </div>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                            
                            if 'raw_response' in response:
                                with st.expander("Additional Details"):
                                    st.markdown("""
                                        <div style='background-color: var(--surface-color); padding: 15px; border-radius: 8px;'>
                                            <p><strong>Model:</strong> Gemini 1.5 Flash</p>
                                            <p><strong>Status:</strong> Success</p>
                                        </div>
                                    """, unsafe_allow_html=True)
                            
                            if 'confidence' in response:
                                confidence = float(response['confidence'])
                                st.progress(confidence, text=f"Confidence: {confidence*100:.0f}%")
                            
                            if response:
                                st.session_state.chat_history.append({
                                    'question': question,
                                    'answer': response['answer'],
                                    'timestamp': datetime.now().strftime("%H:%M:%S")
                                })
                                
                                with st.expander("Chat History"):
                                    for chat in st.session_state.chat_history:
                                        st.markdown(f"""
                                            <div class="chat-item">
                                                <div class="chat-timestamp">{chat['timestamp']}</div>
                                                <div class="chat-question">Q: {chat['question']}</div>
                                                <div class="chat-answer">A: {chat['answer']}</div>
                                            </div>
                                        """, unsafe_allow_html=True)
                                        
                        except Exception as e:
                            st.error(f"An error occurred: {str(e)}")
        else:
            st.markdown(
                '<div style="text-align: center; color: var(--text-secondary); padding: 2rem;">'
                '📸 Upload an image to start the analysis'
                '</div>',
                unsafe_allow_html=True
            )

    # Footer
    st.markdown("""
        <div class="footer">
            ✨ Powered by Google Gemini 1.5 Flash
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 