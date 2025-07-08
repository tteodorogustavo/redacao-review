from flask import Flask, request, jsonify
from flask_cors import CORS
import pytesseract
from PIL import Image
import io
import base64
import cv2
import numpy as np

app = Flask(__name__)
CORS(app)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "service": "tesseract-ocr"})

@app.route('/extract-text', methods=['POST'])
def extract_text():
    try:
        # Receber imagem em base64 ou arquivo
        if 'image' in request.files:
            file = request.files['image']
            image = Image.open(file.stream)
        elif 'image_base64' in request.json:
            image_data = base64.b64decode(request.json['image_base64'])
            image = Image.open(io.BytesIO(image_data))
        else:
            return jsonify({"error": "Nenhuma imagem fornecida"}), 400
        
        # Configurar Tesseract para português
        custom_config = r'--oem 3 --psm 6 -l por'
        
        # Extrair texto
        text = pytesseract.image_to_string(image, config=custom_config)
        
        return jsonify({
            "success": True,
            "extracted_text": text.strip(),
            "service": "tesseract-ocr"
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "service": "tesseract-ocr"
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)

