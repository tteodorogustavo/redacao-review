from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import base64
import io
from PIL import Image

app = Flask(__name__)
CORS(app)

# URLs dos serviços
TESSERACT_SERVICE_URL = "http://tesseract-ocr:5001"
TRAINED_MODEL_SERVICE_URL = "http://trained-model:5002"
LLAMA_SERVICE_URL = "http://llama:5003"


@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy", "service": "backend-api"})


@app.route("/process-redaction", methods=["POST"])
def process_redaction():
    """Endpoint principal para processar redação (imagem ou texto)"""
    try:
        text = None

        # Verificar se é uma imagem ou texto direto
        if "image" in request.files:
            # Processar imagem com OCR
            text = extract_text_from_image(request.files["image"])
            if not text:
                return (
                    jsonify({"error": "Não foi possível extrair texto da imagem"}),
                    400,
                )
        elif "text" in request.form:
            text = request.form["text"]
        elif request.is_json and "text" in request.get_json():
            text = request.get_json()["text"]
        else:
            return jsonify({"error": "Nenhum texto ou imagem fornecida"}), 400

        if not text or len(text.strip()) < 50:
            return jsonify({"error": "Texto muito curto para análise"}), 400

        # Analisar com o modelo treinado
        analysis_data = analyze_with_trained_model(text)
        if not analysis_data:
            return jsonify({"error": "Erro na análise do texto"}), 500

        # Gerar feedback com Llama
        feedback_data = generate_feedback_with_llama(text, analysis_data)
        if not feedback_data:
            return jsonify({"error": "Erro na geração de feedback"}), 500

        # Combinar resultados
        result = {
            "success": True,
            "extracted_text": text,
            "analysis": analysis_data,
            "feedback": feedback_data,
            "timestamp": None,  # Pode adicionar timestamp se necessário
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


def extract_text_from_image(image_file):
    """Extrai texto de imagem usando o serviço Tesseract OCR"""
    try:
        files = {"image": image_file}
        response = requests.post(f"{TESSERACT_SERVICE_URL}/extract-text", files=files)

        if response.status_code == 200:
            data = response.json()
            return data.get("extracted_text", "")
        else:
            print(f"Erro no OCR: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Erro ao conectar com serviço OCR: {e}")
        return None


def analyze_with_trained_model(text):
    """Analisa texto usando o modelo treinado"""
    try:
        payload = {"text": text}
        response = requests.post(
            f"{TRAINED_MODEL_SERVICE_URL}/analyze-competencies", json=payload
        )

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Erro na análise: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Erro ao conectar com serviço de análise: {e}")
        return None


def generate_feedback_with_llama(text, analysis_data):
    """Gera feedback usando o serviço Llama"""
    try:
        payload = {"text": text, "analysis_data": analysis_data}
        response = requests.post(f"{LLAMA_SERVICE_URL}/generate-feedback", json=payload)

        if response.status_code == 200:
            data = response.json()
            return data.get("feedback", {})
        else:
            print(
                f"Erro na geração de feedback: {response.status_code} - {response.text}"
            )
            return None
    except Exception as e:
        print(f"Erro ao conectar com serviço Llama: {e}")
        return None


@app.route("/services-status", methods=["GET"])
def services_status():
    """Verifica o status de todos os serviços"""
    services = {
        "tesseract-ocr": check_service_health(TESSERACT_SERVICE_URL),
        "trained-model": check_service_health(TRAINED_MODEL_SERVICE_URL),
        "llama": check_service_health(LLAMA_SERVICE_URL),
    }

    return jsonify({"backend": "healthy", "services": services})


def check_service_health(service_url):
    """Verifica se um serviço está saudável"""
    try:
        response = requests.get(f"{service_url}/health", timeout=5)
        return response.status_code == 200
    except:
        return False


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004)
