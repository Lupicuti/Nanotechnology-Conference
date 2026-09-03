import asyncio
from playwright.async_api import async_playwright
from reportlab.pdfgen import canvas
import os
from PIL import Image

def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip('#')
    return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))

def create_gradient_image(width, height):
    # 135 deg: Top-Left to Bottom-Right
    img = Image.new('RGB', (width, height))
    pixels = img.load()
    
    cx, cy = 0.7071, 0.7071
    
    proj = [
        0 * cx + 0 * cy,
        width * cx + 0 * cy,
        0 * cx + height * cy,
        width * cx + height * cy
    ]
    min_p, max_p = min(proj), max(proj)
    span = max_p - min_p
    
    # 0%: #00F0FF (Cyan)
    # 50%: #6366F1 (Indigo)
    # 100%: #3B82F6 (Blue)
    stops = [
        (0.0, hex_to_rgb('#2EB192')),
        (1.0, hex_to_rgb('#5F288E'))
    ]
    
    for y in range(height):
        for x in range(width):
            p = x * cx + y * cy
            t = (p - min_p) / span if span > 0 else 0
            t = max(0.0, min(1.0, t))
            
            if t <= stops[0][0]:
                r, g, b = stops[0][1]
            elif t >= stops[-1][0]:
                r, g, b = stops[-1][1]
            else:
                for i in range(len(stops) - 1):
                    t1, col1 = stops[i]
                    t2, col2 = stops[i+1]
                    if t1 <= t <= t2:
                        frac = (t - t1) / (t2 - t1)
                        r = int(col1[0] + frac * (col2[0] - col1[0]))
                        g = int(col1[1] + frac * (col2[1] - col1[1]))
                        b = int(col1[2] + frac * (col2[2] - col1[2]))
                        break
            
            pixels[x, y] = (r, g, b)
    return img

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(device_scale_factor=8)
        
        html_path = f"file:///{os.path.abspath('render_logo.html').replace(os.sep, '/')}"
        await page.goto(html_path)
        await page.evaluate("document.fonts.ready")
        
        logo_el = await page.query_selector("#logo")
        png_path = "temp_mask.png"
        await logo_el.screenshot(path=png_path, omit_background=True)
        await browser.close()
        
        mask_img = Image.open(png_path).convert("RGBA")
        alpha_mask = mask_img.split()[-1]
        w, h = mask_img.size
        
        gradient_img = create_gradient_image(w, h).convert("RGBA")
        transparent_img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        final_img = Image.composite(gradient_img, transparent_img, alpha_mask)
        
        final_png = "logo_nanos_exact.png"
        final_img.save(final_png)
        os.remove(png_path)
        
        pdf_path = "logo_nanos_exact.pdf"
        scale = 8
        pdf_w, pdf_h = w / scale, h / scale
        c = canvas.Canvas(pdf_path, pagesize=(pdf_w, pdf_h))
        c.drawImage(final_png, 0, 0, pdf_w, pdf_h, mask='auto')
        c.save()
        
        print("Logo created: logo_nanos_exact.png, logo_nanos_exact.pdf")

if __name__ == "__main__":
    asyncio.run(main())
