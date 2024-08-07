from flask import jsonify, request
import torch
from diffusers import StableDiffusionPipeline
import logging
import io
import threading
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
        pipe = StableDiffusionPipeline.from_pretrained(
            model_id, 
            # revision="fp16", 
            # torch_dtype=torch.float16, 
            # use_auth_token=os.getenv("AUTH_TOKEN")
        )
        pipe = pipe.to(device)
        
        # Cache the model
        model_cache[model_id] = pipe
        
        return pipe

def validate_and_truncate_prompt(pipe, prompt):
    tokens = pipe.tokenizer.encode(prompt, return_tensors="pt")
    max_length = pipe.tokenizer.model_max_length
    if tokens.size(1) <= max_length:
        return prompt  # Return the original prompt if within the limit
    
    logging.debug(f"Prompt exceeds maximum length of {max_length} tokens, truncating the prompt")
    # Truncate the prompt
    truncated_tokens = tokens[:, :max_length]
    truncated_prompt = pipe.tokenizer.decode(truncated_tokens[0], skip_special_tokens=True)
    return truncated_prompt

def warm_up_model(pipe, prompt):
    try:
        _ = pipe(prompt)
    except Exception as e:
        logging.error(f"Warm-up failed: {str(e)}")


def generate_images(pipe, prompt, num_images):
    try:
        torch.cuda.empty_cache()  # Clear GPU memory
        # warm_up_model(pipe, prompt)
        logging.debug("Warm-up model done")
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
        logging.debug("Image generation done")

        # Save images to directory
        img_files = save_images(images)
        return jsonify({"message": "Multiple images generated", "images": img_files})

    except ValueError as e:
        logging.error(f"ValueError: {str(e)}")
        return f"An error occurred: {str(e)}", 500
    except TypeError as e:
        logging.error(f"TypeError: {str(e)}")
        return f"An error occurred: {str(e)}", 500
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return f"An unexpected error occurred: {str(e)}", 500


def save_images(images):
    """Save generated images to a directory and return their URLs."""
    save_dir = './' + IMG_DIR
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    img_files = []
    for idx, img in enumerate(images):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        image_name = f'image_{idx + 1}_{timestamp}.png'
        img_path = os.path.join(save_dir, image_name)
        img.save(img_path, 'PNG')
        img_files.append(request.host_url + "images/" + image_name)

    return img_files


def generateImage(model_id, prompt, num_images):
    pipe = load_model(model_id)
    valid_prompt = validate_and_truncate_prompt(pipe, prompt)
    return generate_images(pipe, valid_prompt, num_images)
