# 🧠 AI Content Generator & Visual Quote Creator

This is a Streamlit-based AI tool that allows users to generate social media content (Twitter, Instagram, LinkedIn) and design AI-powered quote images and visual artworks based on user prompts. The app supports multiple Hugging Face and LM Studio models, prompt editing, output saving, and regeneration per platform.

---

## 🚀 Features

- ✍️ Custom prompt editing for each platform
- 🧠 AI-generated content via Hugging Face Transformers or local LM Studio API
- 🔁 Per-platform regenerate button to fine-tune results
- 💾 Update and save edited content to file
- 🖼️ AI-generated quote images with styling options
- 🎨 Stable Diffusion image generation with style presets
- 📦 All outputs (text + images) are saved to the `outputs/` folder

---

## 🤖 Supported Models

### Hugging Face (Text Generation)
- `ytu-ce-cosmos/turkish-gpt2`
- `redrussianarmy/gpt2-turkish-cased`
- `gorkemgoknar/gpt2-turkish-writer`
- `erythropygia/gpt2-turkish-base`

### LM Studio (Local API)
- `mistralai/mistral-7b-instruct-v0.3`
- `deepseek/deepseek-r1-0528-qwen3-8b`
- `nous-hermes-2-mistral-7b-dpo`

> 📝 You must select the model from the dropdown. Hugging Face models are loaded dynamically; LM Studio models must be loaded manually via LM Studio and served at `http://localhost:1234`.

---

## 🖼️ Quote Generator

Generate short, inspirational quotes manually or via AI, then create a styled quote image using:
- Minimal Light
- Elegant Dark
- Modern Purple

All images are saved as `outputs/quote.png`.

---

## 🎨 Stable Diffusion Image Generator

Enter a topic, select a style preset (e.g. cinematic, fantasy, anime), and generate images using:
- Customizable prompt & negative prompt
- Style presets
- Width, height, steps, and scheduler selection

---

## 📁 Folder Structure

├── main_app.py

├── utils/

│ ├── text_gen.py

│ ├── quote_image.py

│ ├── image_gen.py

│ ├── image_overlay.py

│ ├── quote_section.py

│ └── export_zip.py

├── outputs/

│ ├── twitter.txt

│ ├── instagram.txt

│ ├── linkedin.txt

│ ├── generated_image.png

│ ├── quote_on_image.png

│ ├── quote.png

│ └── quote.txt

├── requirements.txt

└── README.md


## ▶️ Run the App

```bash
pip install -r requirements.txt
streamlit run app.py
```

## 📦 Requirements
See requirements.txt

## 📝 Notes

- LM Studio models require LM Studio running locally at localhost:1234

- Hugging Face models may take time to load on first use

- All outputs are saved automatically for later access

