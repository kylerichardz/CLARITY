import pytest
import os
from pathlib import Path
import io
from PIL import Image
import numpy as np

@pytest.fixture
def mock_image():
    """Create a simple test image"""
    img = Image.new('RGB', (100, 100), color='red')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG')
    return img_byte_arr.getvalue()

@pytest.fixture
def mock_api_key():
    return "mock_api_key_12345" 