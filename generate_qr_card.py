import os
import qrcode
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def create_qr_card():
    # Target URL
    target_url = "https://santiago-guarnizo2026.github.io/HISTORIA-CONCEPTOS-Y-VARIABLES-ESAP/"
    
    # Generate high quality QR code
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=12,
        border=2,
    )
    qr.add_data(target_url)
    qr.make(fit=True)
    
    qr_img = qr.make_image(fill_color="#0F172A", back_color="#FFFFFF").convert("RGBA")
    
    # Canvas dimensions
    W, H = 1080, 1480
    canvas = Image.new("RGBA", (W, H), (15, 23, 42, 255)) # Dark slate base
    
    # Draw subtle background gradient or glow
    draw = ImageDraw.Draw(canvas)
    for y in range(H):
        ratio = y / H
        r = int(15 * (1 - ratio) + 24 * ratio)
        g = int(23 * (1 - ratio) + 38 * ratio)
        b = int(42 * (1 - ratio) + 68 * ratio)
        draw.line([(0, y), (W, y)], fill=(r, g, b, 255))
        
    # Add a glowing accent circle in background
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    glow_draw.ellipse([W//2 - 350, 480, W//2 + 350, 1180], fill=(20, 222, 222, 45))
    glow_draw.ellipse([W//2 - 250, 150, W//2 + 250, 500], fill=(183, 245, 39, 35))
    glow = glow.filter(ImageFilter.GaussianBlur(80))
    canvas = Image.alpha_composite(canvas, glow)
    draw = ImageDraw.Draw(canvas)
    
    # Draw Inner Card Frame
    card_x0, card_y0 = 80, 80
    card_x1, card_y1 = W - 80, H - 80
    
    # Glassmorphism effect card background
    card_bg = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    card_draw = ImageDraw.Draw(card_bg)
    card_draw.rounded_rectangle([card_x0, card_y0, card_x1, card_y1], radius=36, fill=(255, 255, 255, 14), outline=(255, 255, 255, 50), width=2)
    canvas = Image.alpha_composite(canvas, card_bg)
    draw = ImageDraw.Draw(canvas)
    
    # Fonts
    font_dir = os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Fonts')
    def get_font(name, size):
        try:
            return ImageFont.truetype(os.path.join(font_dir, name), size)
        except:
            return ImageFont.load_default()
            
    font_badge = get_font('segoeui.ttf', 20)
    font_title = get_font('segoeuib.ttf', 44)
    font_sub = get_font('segoeui.ttf', 26)
    font_authors = get_font('segoeui.ttf', 20)
    font_callout = get_font('segoeuib.ttf', 26)
    font_url = get_font('consolas.ttf', 19)
    
    # 1. Logo ESAP
    logo_path = "Logo_Esap.png"
    current_y = 130
    if os.path.exists(logo_path):
        try:
            logo = Image.open(logo_path).convert("RGBA")
            # Resize keeping aspect ratio
            target_w = 210
            ratio = target_w / logo.width
            target_h = int(logo.height * ratio)
            logo = logo.resize((target_w, target_h), Image.Resampling.LANCZOS)
            canvas.paste(logo, ((W - target_w) // 2, current_y), logo)
            current_y += target_h + 30
        except Exception as e:
            print("Logo load error:", e)
            current_y += 40
            
    # 2. Pill Tag / Badge
    badge_text = "ESCUELA SUPERIOR DE ADMINISTRACIÓN PÚBLICA"
    bbox = draw.textbbox((0, 0), badge_text, font=font_badge)
    bw = bbox[2] - bbox[0] + 40
    bh = bbox[3] - bbox[1] + 16
    bx = (W - bw) // 2
    draw.rounded_rectangle([bx, current_y, bx + bw, current_y + bh], radius=bh//2, fill=(20, 222, 222, 40), outline=(20, 222, 222, 180), width=1)
    draw.text(((W - (bbox[2] - bbox[0])) // 2, current_y + 6), badge_text, font=font_badge, fill=(20, 222, 222, 255))
    current_y += bh + 25

    # 3. Main Title
    title1 = "HISTORIA, CONCEPTOS"
    title2 = "Y VARIABLES"
    bbox1 = draw.textbbox((0, 0), title1, font=font_title)
    draw.text(((W - (bbox1[2] - bbox1[0])) // 2, current_y), title1, font=font_title, fill=(255, 255, 255))
    current_y += 50
    bbox2 = draw.textbbox((0, 0), title2, font=font_title)
    draw.text(((W - (bbox2[2] - bbox2[0])) // 2, current_y), title2, font=font_title, fill=(183, 245, 39)) # Neon green accent
    current_y += 55

    # 4. Subtitle
    sub = "Taller 2 • Informe Interactivo Web"
    bbox_sub = draw.textbbox((0, 0), sub, font=font_sub)
    draw.text(((W - (bbox_sub[2] - bbox_sub[0])) // 2, current_y), sub, font=font_sub, fill=(203, 213, 225))
    current_y += 45

    # 5. Authors
    authors = "Pablo S. Triana  •  Carol M. Boton  •  Yessica M. Morales"
    bbox_auth = draw.textbbox((0, 0), authors, font=font_authors)
    draw.text(((W - (bbox_auth[2] - bbox_auth[0])) // 2, current_y), authors, font=font_authors, fill=(148, 163, 184))
    current_y += 45

    # 6. QR Code Container Box
    qr_box_size = 480
    qr_box_x = (W - qr_box_size) // 2
    qr_box_y = current_y
    
    # White rounded square for QR code
    draw.rounded_rectangle([qr_box_x, qr_box_y, qr_box_x + qr_box_size, qr_box_y + qr_box_size], radius=28, fill=(255, 255, 255, 255))
    # Border
    draw.rounded_rectangle([qr_box_x, qr_box_y, qr_box_x + qr_box_size, qr_box_y + qr_box_size], radius=28, outline=(20, 222, 222, 160), width=3)
    
    # Paste QR code in center of box
    qr_scaled = qr_img.resize((qr_box_size - 40, qr_box_size - 40), Image.Resampling.NEAREST)
    canvas.paste(qr_scaled, (qr_box_x + 20, qr_box_y + 20), qr_scaled)
    
    current_y += qr_box_size + 30
    
    # 7. Scan Instruction Pill
    scan_text = "📷 ESCANEA EL CÓDIGO QR PARA INGRESAR"
    bbox_scan = draw.textbbox((0, 0), scan_text, font=font_callout)
    draw.text(((W - (bbox_scan[2] - bbox_scan[0])) // 2, current_y), scan_text, font=font_callout, fill=(255, 255, 255))
    current_y += 42
    
    # 8. Web URL box
    url_display = target_url
    bbox_url = draw.textbbox((0, 0), url_display, font=font_url)
    url_w = bbox_url[2] - bbox_url[0] + 36
    url_h = bbox_url[3] - bbox_url[1] + 18
    url_x = (W - url_w) // 2
    draw.rounded_rectangle([url_x, current_y, url_x + url_w, current_y + url_h], radius=12, fill=(15, 23, 42, 220), outline=(51, 65, 85, 255), width=1)
    draw.text(((W - (bbox_url[2] - bbox_url[0])) // 2, current_y + 7), url_display, font=font_url, fill=(20, 222, 222))

    # Save output
    output_path = "codigo_qr_proyecto.png"
    canvas.convert("RGB").save(output_path, "PNG", quality=95)
    print(f"Generated successfully: {output_path}")

if __name__ == "__main__":
    create_qr_card()
