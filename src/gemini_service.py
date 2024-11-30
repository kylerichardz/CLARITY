import google.generativeai as genai
from typing import Dict, Any
import logging
from functools import lru_cache
import hashlib
from PIL import Image
import io
from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)

class GeminiService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        genai.configure(api_key=api_key)
        
        # Use gemini-1.5-flash model
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        logger.info("GeminiService initialized with Gemini 1.5 Flash")
    
    @staticmethod
    def _generate_cache_key(image: bytes, question: str) -> str:
        """Generate a cache key from image and question"""
        image_hash = hashlib.md5(image).hexdigest()
        return f"{image_hash}:{question}"
    
    def _prepare_image(self, image_bytes: bytes):
        """Convert bytes to PIL Image for Gemini"""
        return Image.open(io.BytesIO(image_bytes))
    
    @lru_cache(maxsize=100)
    def _cached_analyze(self, cache_key: str, image: bytes, question: str) -> Dict[str, Any]:
        """Cached version of the API call"""
        logger.info(f"Making API call for question: {question}")
        
        # Convert bytes to PIL Image for Gemini
        pil_image = self._prepare_image(image)
        
        # Generate the response with Flash model
        response = self.model.generate_content([pil_image, question])
        response.resolve()  # Ensure the response is complete
        
        return {
            'answer': response.text,
            'raw_response': response
        }
    
    def _build_prompt(self, question: str) -> str:
        """Build a structured prompt for better responses"""
        return f"""
        Please analyze this image and answer the following question:
        {question}
        
        Provide your response in this format:
        1. Direct Answer: [Concise answer to the question]
        2. Details: [Additional relevant details]
        3. Confidence: [High/Medium/Low based on clarity of visual elements]
        """
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def analyze_image(self, image: bytes, question: str) -> Dict[str, Any]:
        """
        Analyze an image using Gemini Flash API
        
        Args:
            image: Preprocessed image bytes
            question: User's question about the image
            
        Returns:
            Dict containing the analysis response
        """
        try:
            formatted_question = self._build_prompt(question)
            cache_key = self._generate_cache_key(image, formatted_question)
            logger.debug(f"Generated cache key: {cache_key}")
            
            return self._cached_analyze(cache_key, image, formatted_question)
            
        except Exception as e:
            logger.error(f"Error analyzing image: {str(e)}")
            raise Exception(f"Gemini API error: {str(e)}")
    
    def analyze_images_comparison(self, image1: bytes, image2: bytes, question: str) -> Dict[str, Any]:
        """
        Compare two images using Gemini API
        
        Args:
            image1: First image bytes
            image2: Second image bytes
            question: User's question about the images
        """
        try:
            # Prepare both images
            pil_image1 = self._prepare_image(image1)
            pil_image2 = self._prepare_image(image2)
            
            # Build comparison prompt
            comparison_prompt = f"""
            Please compare these two images and answer the following question:
            {question}
            
            Provide your response in this format:
            1. Image 1: [Description of first image]
            2. Image 2: [Description of second image]
            3. Comparison: [Key differences and similarities]
            4. Answer: [Direct answer to the question]
            """
            
            # Generate response with both images
            response = self.model.generate_content([pil_image1, pil_image2, comparison_prompt])
            response.resolve()
            
            return {
                'answer': response.text,
                'raw_response': response
            }
            
        except Exception as e:
            logger.error(f"Error comparing images: {str(e)}")
            raise Exception(f"Gemini API error: {str(e)}")