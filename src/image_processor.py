import cv2
import numpy as np
from PIL import Image
import io

def preprocess_image(uploaded_file: bytes) -> bytes:
    """
    Preprocess the uploaded image for Gemini API
    
    Args:
        uploaded_file: Raw uploaded file bytes
        
    Returns:
        Preprocessed image bytes
    """
    # Convert uploaded file to PIL Image
    image = Image.open(uploaded_file)
    
    # Convert to RGB if needed
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Use fixed values for size and quality
    max_size = 1600
    if max(image.size) > max_size:
        ratio = max_size / max(image.size)
        new_size = tuple([int(dim * ratio) for dim in image.size])
        image = image.resize(new_size, Image.Resampling.LANCZOS)
    
    # Convert back to bytes with fixed quality
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='JPEG', quality=85)
    return img_byte_arr.getvalue() 