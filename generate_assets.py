import qrcode
from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
import os

def create_qr_code(url, output_pdf_path):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    temp_png = "temp_qr.png"
    img.save(temp_png)
    
    # img.pixel_size is property of PilImage created by qrcode
    w, h = img.pixel_size, img.pixel_size
    c = canvas.Canvas(output_pdf_path, pagesize=(w, h))
    c.drawImage(temp_png, 0, 0, width=w, height=h)
    c.save()
    os.remove(temp_png)

def create_logo(output_png, output_pdf):
    width, height = 800, 300
    # Transparent background
    img = Image.new('RGBA', (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # Try Arial which usually supports Greek characters on Windows
    try:
        font = ImageFont.truetype("arial.ttf", 120)
        font_small = ImageFont.truetype("arial.ttf", 40)
    except IOError:
        font = ImageFont.load_default()
        font_small = font
    
    text = "ΝΑΝΟΣ"
    subtext = "SAPIENZA CONFERENCE 2026"
    
    # Calculate text size using bbox
    bbox = draw.textbbox((0,0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    
    s_bbox = draw.textbbox((0,0), subtext, font=font_small)
    s_w = s_bbox[2] - s_bbox[0]
    
    # Colors
    primary_color = (0, 71, 143) # Sapienza-like Blue
    secondary_color = (130, 36, 51) # Sapienza-like Red
    
    # Draw simple graphic (Abstract atom / node)
    circle_radius = 45
    circle_x = width // 2 - text_w // 2 - circle_radius * 2 - 20
    circle_y = height // 2 - 20
    
    draw.ellipse(
        [circle_x - circle_radius, circle_y - circle_radius, circle_x + circle_radius, circle_y + circle_radius],
        fill=secondary_color
    )
    draw.ellipse(
        [circle_x - circle_radius + 15, circle_y - circle_radius + 15, circle_x + circle_radius - 15, circle_y + circle_radius - 15],
        fill=(255, 255, 255)
    )
    
    # Draw Text
    text_x = width // 2 - text_w // 2 + circle_radius
    text_y = height // 2 - text_h // 2 - bbox[1] - 30
    draw.text((text_x, text_y), text, font=font, fill=primary_color)
    
    # Draw Subtext
    s_x = width // 2 - s_w // 2 + circle_radius
    s_y = text_y + text_h + 20
    draw.text((s_x, s_y), subtext, font=font_small, fill=(80, 80, 80))
    
    img.save(output_png)
    
    # Add a white background for PDF to avoid transparent black issue
    img_bg = Image.new('RGB', (width, height), (255, 255, 255))
    img_bg.paste(img, (0,0), mask=img)
    temp_png_pdf = "temp_logo_bg.png"
    img_bg.save(temp_png_pdf)
    
    c = canvas.Canvas(output_pdf, pagesize=(width, height))
    c.drawImage(temp_png_pdf, 0, 0, width, height)
    c.save()
    os.remove(temp_png_pdf)

if __name__ == "__main__":
    # URL placeholder, the user will be told they can change it.
    url = "https://francesco.github.io/Conferenza"
    create_qr_code(url, "qrcode_sito.pdf")
    create_logo("logo_nanos.png", "logo_nanos.pdf")
    print("Files created: qrcode_sito.pdf, logo_nanos.png, logo_nanos.pdf")
