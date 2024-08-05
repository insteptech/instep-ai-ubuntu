from flask import jsonify, request
import torch
from diffusers import StableDiffusionPipeline
import logging
import io
import threading
from base64 import b64encode
from utils.helper import IMG_DIR
import os
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.DEBUG)

model_cache = {}
model_lock = threading.Lock()

def load_model(model_id):
    """Load and cache the model."""
    with model_lock:
        if model_id in model_cache:
            logging.debug(f"Using cached model for {model_id}")
            return model_cache[model_id]
        
        logging.debug(f"Loading new model for {model_id}")
        
        # Check if GPU is available and set device accordingly
        device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Load the model
        pipe = StableDiffusionPipeline.from_pretrained(model_id, revision="fp16", torch_dtype= torch.float16, use_auth_token="auth_token")
        pipe = pipe.to(device)
        
        # Cache the model
        model_cache[model_id] = pipe
        
        return pipe


def warm_up_model(pipe, prompt):
    try:
        _ = pipe(prompt)
    except Exception as e:
        print(f"Warm-up failed: {str(e)}")

def generate_images(pipe, prompt, num_images):
    try:
        warm_up_model(pipe, prompt)
        logging.debug(f"warm_up_model done")
        device = pipe.device
        images = []

        for _ in range(num_images):
            if device == "cuda":
                with torch.autocast("cuda"):
                    result = pipe(prompt)
            else:
                result = pipe(prompt)

            if result is None or result.images is None:
                raise ValueError("Model returned None or invalid images")

            images.append(result.images[0])
        logging.debug(f"generate_images done")
        # if isinstance(images, tuple) and images[1] == 500:
        #     return images

        save_dir = './' + IMG_DIR
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)


        # Create a directory to save images
        img_files = []
        for idx, img in enumerate(images):
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            image_name = f'image_{idx + 1}_{timestamp}.png'
            img_path = os.path.join(save_dir, image_name)
            img.save(img_path, 'PNG')
            img_files.append(request.host_url + "images/" + image_name)

            # img_io = io.BytesIO()
            # img.save(img_io, 'PNG')
            # img_io.seek(0)
            # img_files.append(b64encode(img_io.getvalue()).decode('utf-8'))
        return jsonify({"message": "Multiple images generated", "images": img_files})

        # return jsonify({"message": "Multiple images generated", "images": [image.getvalue().hex() for image in images]})

    except ValueError as e:
        return f"An error occurred: {str(e)}", 500
    except TypeError as e:
        return f"An error occurred: {str(e)}", 500
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}", 500


def generateImage(model_id, prompt, num_images):
        pipe = load_model(model_id)
    
        return generate_images(pipe, prompt, num_images)