import streamlit as st
from utils.text_gen import query_model
from utils.quote_image import create_quote_image
from io import BytesIO

def quote_section(topic: str, model_choice: str):
    st.markdown("## 🖼️ Alıntı Görseli")

    # Initialize session state
    if "quote_text" not in st.session_state:
        st.session_state.quote_text = ""
    if "quote_prompt" not in st.session_state:
        st.session_state.quote_prompt = ""

    quote_source = st.radio("💡 Alıntı Kaynağı", ["✍️ Kendim Yazacağım", "🤖 AI Oluştursun"])
    quote_style = st.selectbox("🎨 Stil Seçimi", ["🕊️ Minimal Light", "🌙 Elegant Dark", "🟣 Modern Purple"])

    if quote_source == "✍️ Kendim Yazacağım":
        st.session_state.quote_text = st.text_area(
            "📝 Alıntı Metni", 
            st.session_state.quote_text or "AI ile içerik üretimi artık saniyeler sürüyor!",
            key="quote_input"
        )
    else:
        # AI mode: editable prompt
        quote_vibe = st.selectbox("💭 Alıntı Vibe'ı", ["ilham verici", "şiirsel", "vizyoner", "felsefi"])
        
        # Track previous values
        if "prev_vibe" not in st.session_state:
            st.session_state.prev_vibe = ""
        if "prev_topic" not in st.session_state:
            st.session_state.prev_topic = ""

        # Check if topic or vibe changed → reset prompt
        if (quote_vibe != st.session_state.prev_vibe) or (topic != st.session_state.prev_topic):
            st.session_state.quote_prompt = f"Çok kısa (max 15 kelime) bir türkçe alıntı (quote) yaz ve sadece metni döndür. Konu: {topic}, vibe: {quote_vibe}"
            st.session_state.prev_vibe = quote_vibe
            st.session_state.prev_topic = topic

        # Set default prompt just once if not already in session state
        if "quote_prompt" not in st.session_state or not st.session_state.quote_prompt:
            st.session_state.quote_prompt = f"Çok kısa (max 15 kelime) bir türkçe alıntı (quote) yaz ve sadece metni döndür. Konu: {topic}, vibe: {quote_vibe}"

        # Show editable prompt field
        st.session_state.quote_prompt = st.text_area("🧠 AI Prompt'u Düzenle", st.session_state.quote_prompt, key="quote_prompt_input")

        if st.button("✨ AI ile Alıntı Oluştur"):
            with st.spinner("AI alıntıyı oluşturuyor..."):
                result = query_model(st.session_state.quote_prompt, model_choice)
                st.session_state.quote_text = result.strip()
                st.success("✅ Alıntı üretildi!")

        st.session_state.quote_text = st.text_area(
            "🧠 AI Ürettiği veya Düzenlenmiş Alıntı", 
            st.session_state.quote_text, 
            key="quote_input"
        )

    # Image generation
    if st.button("📸 Alıntı Görseli Oluştur"):
        final_quote = st.session_state.get("quote_input", "").strip()
        if final_quote:
            img = create_quote_image(final_quote, style=quote_style)
            st.image(img, caption="🎨 Alıntı Görseli")

            img.save("outputs/quote.png")
            buf = BytesIO()
            img.save(buf, format="PNG")
            st.download_button("💾 Görseli İndir", data=buf.getvalue(), file_name="quote.png", mime="image/png")

            # Save quote to file
            with open("outputs/quote.txt", "w", encoding="utf-8") as f:
                f.write(final_quote)
        else:
            st.error("❗ Lütfen önce bir alıntı girin veya üretin.")
