<div align="center">
  <h1>🔍 Clarity</h1>
  <p><i>Intelligent Image Analysis Powered by Google Gemini 1.5 Flash</i></p>
  
  ![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
  ![Streamlit](https://img.shields.io/badge/Streamlit-1.32.0-red)
  ![Google Gemini](https://img.shields.io/badge/Gemini-1.5_Flash-orange)
  ![License](https://img.shields.io/badge/License-MIT-green)
</div>

---

## 🌟 Features

- **🖼️ Single Image Analysis**: Deep insights into any image
- **🔄 Image Comparison**: Compare two images with detailed analysis
- **🤖 Advanced AI**: Powered by Google's Gemini 1.5 Flash model
- **💡 Smart Prompts**: Pre-built questions for quick analysis
- **📊 Confidence Scoring**: Understand the AI's certainty level
- **💾 Response Caching**: Fast responses for repeated queries
- **🌙 Dark Mode**: Beautiful dark theme interface
- **📱 Responsive Design**: Works on desktop and mobile

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- Google Gemini API key

### Installation

1. Clone the repository: 
bash
git clone https://github.com/yourusername/clarity.git
cd clarity
```


2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
env
GOOGLE_API_KEY=your_gemini_api_key_here
```
Run the app:
```bash
streamlit run src/app.py
```

## 🎯 Usage

1. **Single Image Analysis**
   - Upload an image
   - Choose from quick prompts or type your question
   - Get detailed AI analysis

2. **Image Comparison**
   - Toggle "Compare Images" in sidebar
   - Upload two images
   - Select comparison questions
   - Get side-by-side analysis

## 🛠️ Technical Details

- **Frontend**: Streamlit
- **AI Model**: Google Gemini 1.5 Flash
- **Image Processing**: PIL & OpenCV
- **Caching**: LRU Cache & File-based
- **Error Handling**: Retry mechanism with exponential backoff
- **Testing**: Pytest with mock fixtures

## 📊 Architecture
clarity/
├── src/
│ ├── app.py # Main Streamlit application
│ ├── gemini_service.py # AI service integration
│ ├── image_processor.py # Image preprocessing
│ └── utils.py # Utility functions
└── tests/ # Comprehensive test suite


## 🧪 Testing

Run the test suite:
```bash
pytest
```


## 🔒 Security

- Environment variables for sensitive data
- API key validation
- Response caching for efficiency
- Error handling and logging

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Contact

For questions and support, please open an issue in the GitHub repository.

---

<div align="center">
  <p>Made with ❤️ by Quinn</p>
</div>