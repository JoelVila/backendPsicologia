
import io
from app.extensions import db
from run import app

def test_ocr():
    # Create a test client
    with app.test_client() as client:
        # Create a dummy file (acts like an image)
        data = {
            'documento': (io.BytesIO(b"fake image content"), 'test.jpg')
        }
        
        # Send POST request
        print("Enviando petición de prueba al OCR...")
        response = client.post('/main/analyze-document', data=data, content_type='multipart/form-data')
        
        # Print results
        print(f"Status Code: {response.status_code}")
        print(f"Response Body: {response.get_json()}")
        
        if response.status_code == 200:
            print("✅ Prueba Exitosa: El endpoint responde correctamente.")
        else:
            print("❌ Prueba Fallida.")

if __name__ == "__main__":
    test_ocr()
