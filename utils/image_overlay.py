from PIL import Image, ImageDraw, ImageFont
import textwrap
import os

def add_quote_to_image(
    image_path,
    quote_text,
    output_path="outputs/quote_on_image.png",
    font_path="assets/fonts/arial.ttf",
    font_size=32,
    font_color=(255, 255, 255),
    placement="bottom",  # "top", "center", "bottom"
    show_box_bg=True
):
    # Load the image and convert to RGBA
    img = Image.open(image_path).convert("RGBA")
    draw = ImageDraw.Draw(img)

    # Load font with fallback
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        font = ImageFont.load_default()

    # Wrap the text for max 40 chars per line or width limit
    lines = textwrap.wrap(quote_text, width=40)
    line_height = font_size + 10
    total_text_height = len(lines) * line_height

    # Vertical placement calculation
    if placement == "top":
        y_text = 50
    elif placement == "center":
        y_text = (img.height - total_text_height) // 2
    else:  # bottom
        y_text = img.height - total_text_height - 50

    # Optional semi-transparent background box
    if show_box_bg:
        bg_margin = 20
        box_height = total_text_height + bg_margin * 2
        box_width = max(draw.textlength(line, font=font) for line in lines) + bg_margin * 2
        box_x = (img.width - box_width) // 2
        box_y = y_text - bg_margin
        draw.rectangle(
            [box_x, box_y, box_x + box_width, box_y + box_height],
            fill=(0, 0, 0, 180)
        )

    # Draw each line centered horizontally
    for line in lines:
        text_width = draw.textlength(line, font=font)
        x_text = (img.width - text_width) // 2
        draw.text((x_text, y_text), line, font=font, fill=font_color)
        y_text += line_height

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path)
    return output_path
