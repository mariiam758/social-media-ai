# utils/text_gen.py

from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch
import requests

# Model cache for Hugging Face models
_model_cache = {}

def load_hf_model(model_name):
    if model_name in _model_cache:
        return _model_cache[model_name]

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)

    pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, device=-1)  # CPU device
    _model_cache[model_name] = pipe
    return pipe

def query_lmstudio(prompt: str, model_name: str = "mistralai/mistral-7b-instruct-v0.3"):
    """
    Sends prompt to LM Studio local API and returns the generated text.
    model_name should NOT include the "LM Studio:" prefix.
    """
    url = "http://localhost:1234/v1/chat/completions"
    headers = {"Content-Type": "application/json"}

    payload = {
        "model": model_name,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3,
        "max_tokens": 800
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"❌ Hata: LM Studio bağlantısı başarısız → {e}"

def query_model(prompt: str, model_name: str):
    """
    Routes prompt generation to either Hugging Face or LM Studio
    based on the model_name prefix.
    """
    if model_name.startswith("LM Studio:"):
        # Strip prefix and send to LM Studio API
        lm_model_name = model_name.replace("LM Studio:", "").strip()
        return query_lmstudio(prompt, lm_model_name)
    else:
        # Use Hugging Face local pipeline
        try:
            pipe = load_hf_model(model_name)
            output = pipe(prompt, max_new_tokens=200, temperature=0.7)[0]['generated_text']
            # Remove the original prompt from the output to get the generated continuation
            return output[len(prompt):].strip()
        except Exception as e:
            return f"❌ Hata: Model yüklenemedi veya cevap üretilemedi → {e}"


def generate_custom_posts(prompts: dict, model_name: str):
    results = {}
    for platform, prompt in prompts.items():
        results[platform] = query_model(prompt, model_name)
    return results
