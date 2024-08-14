from flask import jsonify

import torch
import os
from transformers import AutoModelForCausalLM, AutoTokenizer

def generateText(prompt):
    try:
        model_name = "LGAI-EXAONE/EXAONE-3.0-7.8B-Instruct"
        device = "cpu"
        print(model_name)
        model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.bfloat16,
        trust_remote_code=True,
        device_map="auto",
        use_auth_token=os.getenv("AUTH_TOKEN")
    )
        print("model_name")
        tokenizer = AutoTokenizer.from_pretrained(model_name)

        messages = [
        {"role": "system", 
        "content": "You are a helpful assistant"},
        {"role": "user", "content": prompt}
    ]
        input_ids = tokenizer.apply_chat_template(
        messages,
        tokenize=True,
        add_generation_prompt=True,
        return_tensors="pt"
    )
        print("kjhghj")
        output = model.generate(
        input_ids.to(device),
        eos_token_id=tokenizer.eos_token_id,
        max_new_tokens=128
    )

        return tokenizer.decode(output[0])
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500