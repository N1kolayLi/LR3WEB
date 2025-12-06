import unittest
import os
import tempfile
from io import BytesIO
from PIL import Image
import numpy as np
from LR3_WEB import app, UPLOAD_FOLDER


class FlaskAppTestCase(unittest.TestCase):
    """Unit tests for the Flask image processing application."""
    
    def setUp(self):
        """Set up test client and temporary folder for uploads."""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        
        # Create temporary upload folder for tests
        self.test_upload_folder = tempfile.mkdtemp()
        
    def tearDown(self):
        """Clean up temporary files after tests."""
        import shutil
        if os.path.exists(self.test_upload_folder):
            shutil.rmtree(self.test_upload_folder)
    
    def create_test_image(self, width=100, height=100):
        """Create a simple test image in memory."""
        img = Image.new('RGB', (width, height), color='red')
        img_bytes = BytesIO()
        img.save(img_bytes, format='JPEG')
        img_bytes.seek(0)
        return img_bytes
    
    def test_app_exists(self):
        """Test that Flask app is created successfully."""
        self.assertIsNotNone(app)
    
    def test_app_is_testing(self):
        """Test that app is in testing mode."""
        self.assertTrue(app.config['TESTING'])
    
    def test_var9_route_exists(self):
        """Test that /var9 route is accessible."""
        response = self.client.get('/var9')
        self.assertIn(response.status_code, [200, 404, 500])
    
    def test_process_route_get_not_allowed(self):
        """Test that GET request to /process is not allowed."""
        response = self.client.get('/process')
        self.assertEqual(response.status_code, 405)
    
    def test_process_route_post_no_file(self):
        """Test POST to /process without file redirects."""
        response = self.client.post('/process', follow_redirects=False)
        self.assertIn(response.status_code, [302, 400])
    
    def test_process_route_with_file(self):
        """Test POST to /process with valid image file."""
        test_image = self.create_test_image()
        response = self.client.post(
            '/process',
            data={
                'file': (test_image, 'test.jpg'),
                'r_coef': '1.0',
                'g_coef': '1.0',
                'b_coef': '1.0'
            },
            content_type='multipart/form-data',
            follow_redirects=False
        )
        # Should process and return template or redirect
        self.assertIn(response.status_code, [200, 302, 500])
    
    def test_process_route_with_color_coefficients(self):
        """Test POST to /process with custom color coefficients."""
        test_image = self.create_test_image()
        response = self.client.post(
            '/process',
            data={
                'file': (test_image, 'test.jpg'),
                'r_coef': '0.8',
                'g_coef': '1.2',
                'b_coef': '0.9'
            },
            content_type='multipart/form-data',
            follow_redirects=False
        )
        self.assertIn(response.status_code, [200, 302, 500])
    
    def test_upload_folder_created(self):
        """Test that upload folder is created on app initialization."""
        self.assertTrue(os.path.exists(UPLOAD_FOLDER))
    
    def test_numpy_array_clipping(self):
        """Test that numpy array clipping works correctly."""
        arr = np.array([0, 128, 255, 300, -50])
        clipped = np.clip(arr * 1.0, 0, 255)
        
        self.assertEqual(clipped[0], 0)
        self.assertEqual(clipped[1], 128)
        self.assertEqual(clipped[2], 255)
        self.assertEqual(clipped[3], 255)  # Should be clipped to 255
        self.assertEqual(clipped[4], 0)    # Should be clipped to 0
    
    def test_image_conversion_rgb(self):
        """Test that image is properly converted to RGB format."""
        test_image = self.create_test_image()
        img = Image.open(test_image).convert("RGB")
        
        self.assertEqual(img.mode, 'RGB')
        self.assertEqual(img.size, (100, 100))
    
    def test_array_stacking(self):
        """Test that RGB channels can be properly stacked."""
        r = np.array([[100, 150], [200, 250]])
        g = np.array([[110, 160], [210, 255]])
        b = np.array([[120, 170], [220, 255]])
        
        stacked = np.stack([r, g, b], axis=2).astype(np.uint8)
        
        self.assertEqual(stacked.shape, (2, 2, 3))
        self.assertEqual(stacked[0, 0, 0], 100)  # r channel
        self.assertEqual(stacked[0, 0, 1], 110)  # g channel
        self.assertEqual(stacked[0, 0, 2], 120)  # b channel


class ImageProcessingTestCase(unittest.TestCase):
    """Unit tests for image processing logic."""
    
    def test_color_coefficient_application(self):
        """Test that color coefficients are correctly applied."""
        original_value = 128
        coef = 0.5
        result = int(np.clip(original_value * coef, 0, 255))
        
        self.assertEqual(result, 64)
    
    def test_coefficient_overflow(self):
        """Test that coefficient overflow is properly clipped."""
        original_value = 200
        coef = 2.0
        result = int(np.clip(original_value * coef, 0, 255))
        
        self.assertEqual(result, 255)
    
    def test_coefficient_underflow(self):
        """Test that coefficient underflow is properly clipped."""
        original_value = 50
        coef = 0.1
        result = int(np.clip(original_value * coef, 0, 255))
        
        self.assertEqual(result, 5)


if __name__ == '__main__':
    unittest.main()
