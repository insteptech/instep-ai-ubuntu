from flask import Flask, request, jsonify, send_from_directory
from transformers import pipeline
import logging
from services.textToImage import generateImage, load_model
from services.textToVideo import generateVideo
from utils.helper import BASE_DIR, IMG_DIR, VIDEO_DIR
import os
from dotenv import load_dotenv 
import torch
app = Flask(__name__)

load_dotenv() 

# Set up logging
logging.basicConfig(level=logging.DEBUG)


@app.route('/')
def home():
    if torch.cuda.is_available():
        device = torch.device('cuda')
        print('Using CUDA')
    else:
        device = torch.device('cpu')
        print('Using CPU')
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
        return jsonify({"message":"File not found", "success": False}), 500
    
    return send_from_directory(os.path.join(BASE_DIR, IMG_DIR),filename)


@app.route('/video/<filename>')
def serve_video(filename):
    file_path = os.path.join(VIDEO_DIR, filename)
    logging.info(f"File found: {file_path}")
    logging.info(f"BASE_DIR: {BASE_DIR}")
    logging.info(f"IMG_DIR: {VIDEO_DIR}")
    if not os.path.isfile(file_path):
        logging.error(f"File not found: {file_path}")
        return jsonify({"message":"File not found", "success": False}), 500
    
    return send_from_directory(os.path.join(BASE_DIR, VIDEO_DIR),filename)

@app.route("/generate-video", methods=["POST"])
def textToVideo():
    try:
            if request.content_type != 'application/json':
                return jsonify({"error": "Content-Type must be application/json"}), 400
            
            requestBody = request.get_json()
            if requestBody is None:
                return jsonify({"error": "Invalid JSON payload"}), 400
            
            logging.debug(f"prompt {requestBody}") 
            prompt = requestBody.get('prompt')
           
            if not prompt:
                return jsonify({"message": "Prompt are required", "success":False})
            
            return generateVideo(prompt)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    load_model("CompVis/stable-diffusion-v1-4")
    app.run(debug=True)
