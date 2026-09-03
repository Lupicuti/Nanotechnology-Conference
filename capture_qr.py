import asyncio
from playwright.async_api import async_playwright
from reportlab.pdfgen import canvas
import os
from PIL import Image

async def capture_qr():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        # High resolution for print quality
        page = await browser.new_page(device_scale_factor=4)
        
        html_path = f"file:///{os.path.abspath('render_qr.html').replace(os.sep, '/')}"
        await page.goto(html_path)
        
        # Wait for web fonts to load
        await page.evaluate("document.fonts.ready")
        
        # Select the card container
        card_el = await page.query_selector("#qr-card")
        
        png_path = "qr_framed.png"
        # Omit background so the glow and rounded corners are over a transparent background
        await card_el.screenshot(path=png_path, omit_background=True)
        await browser.close()
        
        # Convert to PDF
        pdf_path = "qr_framed.pdf"
        img = Image.open(png_path)
        w, h = img.size
        # Downscale physical size by 4x to match device_scale_factor (creates high DPI PDF)
        scale = 4
        pdf_w, pdf_h = w / scale, h / scale
        c = canvas.Canvas(pdf_path, pagesize=(pdf_w, pdf_h))
        c.drawImage(png_path, 0, 0, pdf_w, pdf_h, mask='auto')
        c.save()
        
        print("Framed QR created: qr_framed.png, qr_framed.pdf")

if __name__ == "__main__":
    asyncio.run(capture_qr())
