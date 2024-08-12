from flask import jsonify
import torch
from diffusers import DiffusionPipeline
from diffusers.utils import export_to_video
from utils.helper import VIDEO_DIR
import os
from datetime import datetime
import logging
logging.basicConfig(level=logging.DEBUG)

def generateVideo(prompt):
    try:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        save_dir = './' + VIDEO_DIR
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        pipe = DiffusionPipeline.from_pretrained(
        "THUDM/CogVideoX-2b",
        torch_dtype=torch.float16
    )
        pipe.enable_model_cpu_offload()
        prompt_embeds, _ = pipe.encode_prompt(
        prompt=prompt,
        do_classifier_free_guidance=True,
        num_videos_per_prompt=1,
        max_sequence_length=226,
        device=device,
        dtype=torch.float16,
    )
        video = pipe(
        num_inference_steps=50,
        guidance_scale=6,
        prompt_embeds=prompt_embeds,
    ).frames[0]
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        video_name = f'video_{timestamp}.mp4'
        video_path = os.path.join(save_dir, video_name)
        export_to_video(video, video_path, fps=8)

        return jsonify({"message": "Video generated", "video": video_name})
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return f"An unexpected error occurred: {str(e)}", 500