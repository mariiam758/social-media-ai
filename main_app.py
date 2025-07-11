# main_app.py

import streamlit as st
from utils.text_gen import generate_custom_posts, query_model
from utils.image_gen import load_pipeline, generate_sd_image
from utils.export_zip import create_zip_output
from utils.quote_section import quote_section
from utils.image_overlay import add_quote_to_image

from io import BytesIO
from PIL import Image
import os

st.set_page_config(page_title="🧠 AI Content Generator", layout="wide")
st.title("📱 AI Destekli Sosyal Medya İçerik Üretimi")

os.makedirs("outputs", exist_ok=True)

# 1. Topic Input
topic = st.text_input("📝 Konu Başlığı", "Yapay zekâ ile içerik üretimi")

# Model seçimi (Hugging Face modelleri ve LM studio üzerinde bulunan bir kaç model)
model_choice = st.selectbox("🤖 Kullanılacak Hugging Face Modeli", [
    "ytu-ce-cosmos/turkish-gpt2",
    "redrussianarmy/gpt2-turkish-cased",
    "gorkemgoknar/gpt2-turkish-writer",
    "erythropygia/gpt2-turkish-base",
    "LM Studio: mistralai/mistral-7b-instruct-v0.3",
    "LM Studio: deepseek/deepseek-r1-0528-qwen3-8b",
    "LM Studio: nous-hermes-2-mistral-7b-dpo"
])

# Uyarı
if model_choice.startswith("LM Studio:"):
    st.warning("💡 Bu modeli kullanabilmek için LM Studio uygulamasında ilgili modeli elle yüklemelisiniz. LM Studio arka planda çalışıyor olmalı.")
else:
    st.warning(f"⚠️ Bu işlem internet bağlantısı ve CPU'da birkaç saniye sürebilir. Seçilen model: {model_choice}")

# 2. Prompt Editing Section 
st.markdown("### ✍️ Platform Bazlı Prompts")
# --- Prompt Editing and Outputs Section ---

# Function to update prompts if topic changed
def update_prompt_if_topic_changed(key, topic, template):
    if key not in st.session_state or st.session_state.get("last_topic") != topic:
        st.session_state[key] = template.format(topic=topic)

# Update prompts if topic changed
update_prompt_if_topic_changed(
    "twitter_prompt",
    topic,
    "{topic} hakkında, 280 karakteri aşmayacak şekilde, dikkat çekici ve hashtag içeren kısa bir türkçe tweet yaz. Sadece tweet'in içeriği döndür."
)
update_prompt_if_topic_changed(
    "linkedin_prompt",
    topic,
    "{topic} konusuyla ilgili, profesyonel ve analitik bir dille, etkileşim yaratacak bir türkçe LinkedIn gönderisi oluştur. Sadece gönderinin içeriği döndür."
)
update_prompt_if_topic_changed(
    "instagram_prompt",
    topic,
    "{topic} temasıyla uyumlu, duygusal, etkileyici bir türkçe Instagram paylaşımı için açıklama yaz. Sadece açıklamanın içeriği döndür."
)

# Save the current topic in session state
st.session_state["last_topic"] = topic

# Prompt editing form
with st.form("prompt_form"):
    twitter_prompt = st.text_area(
        "🐦 Twitter Prompt",
        value=st.session_state.twitter_prompt,
        key="twitter_prompt"
    )
    linkedin_prompt = st.text_area(
        "💼 LinkedIn Prompt",
        value=st.session_state.linkedin_prompt,
        key="linkedin_prompt"
    )
    instagram_prompt = st.text_area(
        "📸 Instagram Prompt",
        value=st.session_state.instagram_prompt,
        key="instagram_prompt"
    )
    submitted = st.form_submit_button("🧠 İçerikleri Üret")

if submitted:
    with st.spinner("🤖 AI ile içerikler oluşturuluyor..."):
        outputs = generate_custom_posts({
            "twitter": twitter_prompt,
            "linkedin": linkedin_prompt,
            "instagram": instagram_prompt
        }, model_choice)

        # Save outputs in session state
        st.session_state["outputs"] = outputs

        # Save outputs to files immediately
        for platform, content in outputs.items():
            with open(f"outputs/{platform}.txt", "w", encoding="utf-8") as f:
                f.write(content)

# Show outputs section only if outputs exist
if "outputs" in st.session_state:
    st.subheader("📰 İçerik Çıktıları")

    for platform in ["twitter", "linkedin", "instagram"]:
        st.markdown(f"#### {platform.capitalize()} İçeriği")

        # Load saved content from file or session
        try:
            with open(f"outputs/{platform}.txt", "r", encoding="utf-8") as f:
                saved_content = f.read()
        except FileNotFoundError:
            saved_content = st.session_state["outputs"].get(platform, "")

        edited_content = st.text_area(
            f"{platform}_content",
            saved_content,
            height=150,
            key=f"{platform}_text_area"
        )

        col1, col2 = st.columns([1, 1])

        with col1:
            if st.button(f"💾 {platform.capitalize()} İçeriğini Güncelle", key=f"{platform}_update_btn"):
                with open(f"outputs/{platform}.txt", "w", encoding="utf-8") as f:
                    f.write(edited_content)
                st.session_state["outputs"][platform] = edited_content
                st.success(f"{platform.capitalize()} içeriği başarıyla güncellendi.")

        with col2:
            if st.button(f"🔄 {platform.capitalize()} İçeriğini Yeniden Üret", key=f"{platform}_regen_btn"):
                # Use current prompt from session_state to regenerate output
                prompt = st.session_state.get(f"{platform}_prompt", "")
                if not prompt:
                    prompt = {
                        "twitter": st.session_state.twitter_prompt,
                        "linkedin": st.session_state.linkedin_prompt,
                        "instagram": st.session_state.instagram_prompt
                    }[platform]

                with st.spinner(f"{platform.capitalize()} içeriği yeniden üretiliyor..."):
                    new_output = query_model(prompt, model_choice)
                    st.session_state["outputs"][platform] = new_output
                    with open(f"outputs/{platform}.txt", "w", encoding="utf-8") as f:
                        f.write(new_output)
                    st.experimental_rerun()  # Refresh to show new content

# 3. Quote Box Image
quote_section(topic, model_choice)

# 4. Stable Diffusion Görsel Üretimi
st.markdown("## 🎨 AI Görsel Üretimi")

style_presets = {
    "🎨 Realism (Default)": "",
    "🖌 Oil Painting": "oil painting, canvas texture, brush strokes",
    "🎬 Cinematic": "cinematic lighting, shallow depth of field, movie still",
    "🌆 Futuristic City": "futuristic skyline, sci-fi architecture, neon lights",
    "🧝 Fantasy Art": "epic fantasy, detailed armor, glowing background",
    "🌀 Anime": "anime style, vibrant colors, clean lines, soft shading",
    "🎭 Surrealism": "dreamlike, abstract, Salvador Dali style"
}

base_prompt = st.text_area("🎯 Ana Görsel Prompt", f'konu : {topic}, ultra-realistic, cinematic lighting, detailed, 4k digital art')
style = st.selectbox("🎨 Stil", list(style_presets.keys()))
negative_prompt = st.text_area("🚫 Negatif Prompt", "blurry, distorted, bad quality")

steps = st.slider("🧠 Adım Sayısı", 10, 50, 25)
width = st.slider("📏 Genişlik", 256, 512, 384, step=64)
height = st.slider("📐 Yükseklik", 256, 512, 384, step=64)
scheduler_choice = st.selectbox("🧪 Scheduler", ["DPMSolver", "EulerA", "DDIM"])

if st.button("🖌️ Görsel Üret"):
    with st.spinner("Görsel oluşturuluyor..."):
        pipe = load_pipeline(scheduler_choice)
        final_prompt = f"{base_prompt}, {style_presets[style]}" if style_presets[style] else base_prompt
        image = generate_sd_image(pipe, final_prompt, negative_prompt, steps, height, width)
        
        st.session_state.generated_image = image  # 🔒 Store in session
        image.save("outputs/generated_image.png")  # 💾 Save to file

# ✅ Show the image if available
if "generated_image" in st.session_state:
    st.image(st.session_state.generated_image, caption="🎉 Üretilen Görsel", use_column_width=True)
        
    buf = BytesIO()
    st.session_state.generated_image.save(buf, format="PNG")
    st.download_button("💾 Görseli İndir", data=buf.getvalue(), file_name="generated_image.png", mime="image/png")

# 5. Alıntıyı Görsele Yaz ve Göster

# Initialize session state for the combined image path
if "quote_on_image_path" not in st.session_state:
    st.session_state.quote_on_image_path = None

st.markdown("## 📌 Alıntıyı Görsele Eklemek")

# Font selection
font_choice = st.selectbox("🖋️ Font Seçimi", ["Arial", "Times New Roman", "Courier New"])
font_files = {
    "Arial": "assets/fonts/arial.ttf",
    "Times New Roman": "assets/fonts/times.ttf",
    "Courier New": "assets/fonts/courier.ttf"
}
font_path = font_files.get(font_choice, "assets/fonts/arial.ttf")

# Style settings
font_size = st.slider("🔠 Font Boyutu", 16, 64, 32, step=2)
font_color = st.color_picker("🎨 Font Rengi", "#FFFFFF")
placement = st.selectbox("📍 Alıntı Yerleşimi", ["bottom", "center", "top"])
show_box = st.checkbox("🎁 Arka plan kutusu göster", value=True)

# Button to apply quote to image
if st.button("🖼️ Alıntıyı Görsele Ekle ve Göster"):
    if not st.session_state.get("quote_input", "").strip():
        st.error("❗ Önce alıntı metni oluşturun veya yazın.")
    else:
        base_image_path = "outputs/generated_image.png"  # Your existing generated image path

        if not os.path.exists(base_image_path):
            st.error("❗ Öncelikle bir görsel üretmelisiniz.")
        else:
            # Generate the image with quote overlay
            output_path = add_quote_to_image(
                image_path=base_image_path,
                quote_text=st.session_state["quote_input"].strip(),
                output_path="outputs/quote_on_image.png",
                font_path=font_path,
                font_size=font_size,
                font_color=tuple(int(font_color.lstrip("#")[i:i+2], 16) for i in (0, 2, 4)),
                placement=placement,
                show_box_bg=show_box
            )
            st.session_state.quote_on_image_path = output_path
            st.success("✅ Alıntı başarıyla görsele eklendi!")

# Show image persistently
if st.session_state.get("quote_on_image_path"):
    st.image(st.session_state.quote_on_image_path, caption="🎉 Alıntı ile Görsel")

    with open(st.session_state.quote_on_image_path, "rb") as f:
        st.download_button("💾 Görseli İndir", data=f, file_name="quote_on_image.png", mime="image/png")


# 6. ZIP download
if st.button("📦 Tüm İçeriği ZIP Olarak İndir"):
    zip_bytes = create_zip_output("outputs")
    st.download_button(
        label="💾 ZIP Dosyasını İndir",
        data=zip_bytes,
        file_name="social_media_content.zip",
        mime="application/zip"
    )