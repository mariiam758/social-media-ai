# utils/quote_image.py
from PIL import Image, ImageDraw, ImageFont
import os

def create_quote_image(text, style="🕊️ Minimal Light"):
    width, height = 800, 400
    padding = 40

    # Fallback font
    font_path = "arial.ttf"
    if not os.path.exists(font_path):
        font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    font = ImageFont.truetype(font_path, 30)

    # Style definitions
    if style == "🌙 Elegant Dark":
        bg_color = (20, 20, 30)
        text_color = (240, 240, 240)
    elif style == "🟣 Modern Purple":
        bg_color = (60, 0, 90)
        text_color = (255, 230, 255)
    else:  # Minimal Light
        bg_color = (250, 250, 250)
        text_color = (20, 20, 20)

    img = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    # Quote symbol
    quote_icon = "\u201C"  # Unicode left quote
    quote_font = ImageFont.truetype(font_path, 60)
    draw.text((padding, padding - 20), quote_icon, font=quote_font, fill=text_color)

    # Wrapped text
    import textwrap
    wrapped = textwrap.fill(text, width=40)
    draw.text((padding, padding + 50), wrapped, font=font, fill=text_color)

    # Footer signature
    signature = "— AI Content Studio"
    sig_font = ImageFont.truetype(font_path, 20)
    draw.text((padding, height - padding), signature, font=sig_font, fill=text_color)

    return img