from flask import Flask, request, jsonify, send_from_directory
from transformers import pipeline
import logging
from services.textToImage import generateImage
from utils.helper import BASE_DIR, IMG_DIR
import os

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.DEBUG)


@app.route('/')
def home():
    return "Welcome to My Fun Flask App!"

@app.route('/test')
def test():
    return "test route"

@app.route('/generate-image', methods=['POST'])
def textToImage():
    try:
            if request.content_type != 'application/json':
                return jsonify({"error": "Content-Type must be application/json"}), 400
            
            requestBody = request.get_json()
            if requestBody is None:
                return jsonify({"error": "Invalid JSON payload"}), 400
            
            logging.debug(f"prompt {requestBody}")
            model_id = requestBody.get('model_id')
            prompt = requestBody.get('prompt')
            num_images = int(requestBody.get('num_images', 1))  # Default to 1 image if not specified
          
            logging.debug(f"model_id {model_id}")
            logging.debug(f"num_images {num_images}")
            if not model_id or not prompt:
                return jsonify({"message": "Both Model ID and Prompt are required", "success":False})
            
            # future = executor.submit(generateImage, model_id, prompt, num_images)
            # return future.result()
            return generateImage(model_id, prompt, num_images)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
 


@app.route('/images/<filename>')
def serve_image(filename):
    file_path = os.path.join(IMG_DIR, filename)
    logging.info(f"File found: {file_path}")
    logging.info(f"BASE_DIR: {BASE_DIR}")
    logging.info(f"IMG_DIR: {IMG_DIR}")
    if not os.path.isfile(file_path):
        logging.error(f"File not found: {file_path}")
        return jsonify({"message":"File not found", "success": False}), 404
    
    return send_from_directory(os.path.join(BASE_DIR, IMG_DIR),filename)

if __name__ == '__main__':
    app.run(debug=True)
