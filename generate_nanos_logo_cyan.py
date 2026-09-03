import urllib.request
import os
from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas

def download_font():
    font_url = "https://github.com/google/fonts/raw/main/ofl/outfit/Outfit%5Bwght%5D.ttf"
    font_path = "Outfit.ttf"
    if not os.path.exists(font_path):
        print("Downloading Outfit font...")
        try:
            urllib.request.urlretrieve(font_url, font_path)
        except Exception as e:
            print("Could not download font, using default:", e)
    return font_path

def create_cyan_logo(output_png, output_pdf):
    font_path = download_font()
    
    width, height = 600, 200
    # Transparent background
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    try:
        # We try to use the downloaded Outfit font
        font = ImageFont.truetype(font_path, 120)
    except Exception:
        font = ImageFont.load_default()
    
    # The text we want to render: Νᾶνος or Ναˆνος. 
    # Let's try "Νᾶνος" which is small alpha with perispomeni.
    text = "Νᾶνος"
    color = (0, 240, 255, 255) # #00F0FF with full alpha
    
    # Calculate text size using bbox
    bbox = draw.textbbox((0,0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    
    # Position
    text_x = width // 2 - text_w // 2
    text_y = height // 2 - text_h // 2 - bbox[1]
    
    draw.text((text_x, text_y), text, font=font, fill=color)
    
    # Save PNG (Transparent background)
    img.save(output_png, format="PNG")
    
    # Save PDF (Transparent background)
    # ReportLab supports PNGs with alpha channels directly, so we just draw the PNG onto the canvas.
    c = canvas.Canvas(output_pdf, pagesize=(width, height))
    # We do NOT draw a white rectangle, so background remains transparent.
    c.drawImage(output_png, 0, 0, width, height, mask='auto')
    c.save()

if __name__ == "__main__":
    create_cyan_logo("logo_nanos_cyan.png", "logo_nanos_cyan.pdf")
    print("Files created: logo_nanos_cyan.png, logo_nanos_cyan.pdf")
