import pytest
from src.image_processor import preprocess_image
from PIL import Image
import io

def test_preprocess_image_resize(mock_image):
    # Create a large test image
    large_img = Image.new('RGB', (2000, 2000), color='blue')
    img_byte_arr = io.BytesIO()
    large_img.save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)
    
    # Process the image
    processed = preprocess_image(img_byte_arr)
    
    # Convert processed bytes back to image for testing
    processed_img = Image.open(io.BytesIO(processed))
    
    # Check if image was resized properly
    assert max(processed_img.size) <= 1600

def test_preprocess_image_format(mock_image):
    # Create RGBA image
    rgba_img = Image.new('RGBA', (100, 100), color='blue')
    img_byte_arr = io.BytesIO()
    rgba_img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    
    # Process the image
    processed = preprocess_image(img_byte_arr)
    
    # Check if image was converted to RGB
    processed_img = Image.open(io.BytesIO(processed))
    assert processed_img.mode == 'RGB' 