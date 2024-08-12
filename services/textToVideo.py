from flask import jsonify
import torch
from diffusers import DiffusionPipeline
from diffusers.utils import export_to_video
from utils.helper import VIDEO_DIR
import os
from datetime import datetime
import logging
import threading
logging.basicConfig(level=logging.DEBUG)

model_cache = {}
model_lock = threading.Lock()

def load_model(model_id):
    """Load and cache the model."""
    logging.debug(f'{os.getenv("AUTH_TOKEN")}-opopopopo')
    with model_lock:
        if model_id in model_cache:
            logging.debug(f"Using cached model for {model_id}")
            return model_cache[model_id]
        
        logging.debug(f"Loading new model for {model_id}")
        
        # Check if GPU is available and set device accordingly
        device = "cuda" if torch.cuda.is_available() else "cpu"
        logging.info(f'device----{device}')
        # Load the model
        pipe = DiffusionPipeline.from_pretrained(
            model_id, 
            # revision="fp16", 
            # torch_dtype=torch.float16, 
            # use_auth_token=os.getenv("AUTH_TOKEN")
        )
        # pipe.enable_model_cpu_offload()
        pipe = pipe.to(device)
        
        # Cache the model
        model_cache[model_id] = pipe
        
        return pipe


def generateVideo(prompt):
    try:
        model_id= "THUDM/CogVideoX-2b"
        device = "cuda" if torch.cuda.is_available() else "cpu"
        save_dir = './' + VIDEO_DIR
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

    #     pipe = DiffusionPipeline.from_pretrained(
    #     "THUDM/CogVideoX-2b",
    #     torch_dtype=torch.float16
    # )
    #     pipe.enable_model_cpu_offload()
        pipe = load_model(model_id)
        logging.info(f'pipe----')
        prompt_embeds, _ = pipe.encode_prompt(
        prompt=prompt,
        do_classifier_free_guidance=True,
        num_videos_per_prompt=1,
        max_sequence_length=226,
        device=device,
        dtype=torch.float16,
    )
        logging.info(f'prompt_embeds----')
        video = pipe(
        num_inference_steps=50,
        guidance_scale=6,
        prompt_embeds=prompt_embeds,
    ).frames[0]
        logging.info(f'video----')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        video_name = f'video_{timestamp}.mp4'
        video_path = os.path.join(save_dir, video_name)
        export_to_video(video, video_path, fps=8)

        return jsonify({"message": "Video generated", "video": video_name})
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return f"An unexpected error occurred: {str(e)}", 500