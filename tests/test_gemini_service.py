import pytest
from unittest.mock import Mock, patch
from src.gemini_service import GeminiService

@pytest.fixture
def mock_gemini_service():
    return GeminiService("mock_api_key")

def test_gemini_service_init():
    service = GeminiService("test_key")
    assert service.api_key == "test_key"

@patch('google.generativeai.GenerativeModel')
def test_analyze_image_success(mock_model, mock_gemini_service, mock_image):
    # Mock the generate_content response
    mock_response = Mock()
    mock_response.text = "This is a test response"
    mock_model.return_value.generate_content.return_value = mock_response
    
    response = mock_gemini_service.analyze_image(mock_image, "What's in this image?")
    
    assert response['answer'] == "This is a test response"
    assert 'raw_response' in response

@patch('google.generativeai.GenerativeModel')
def test_analyze_image_error(mock_model, mock_gemini_service, mock_image):
    # Mock an API error
    mock_model.return_value.generate_content.side_effect = Exception("API Error")
    
    with pytest.raises(Exception) as exc_info:
        mock_gemini_service.analyze_image(mock_image, "What's in this image?")
    
    assert "Gemini API error" in str(exc_info.value) 