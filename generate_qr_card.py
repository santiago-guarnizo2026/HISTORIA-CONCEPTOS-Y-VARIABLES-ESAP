import os
import qrcode
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def create_qr_card():
    # Target URL
    target_url = "https://santiago-guarnizo2026.github.io/HISTORIA-CONCEPTOS-Y-VARIABLES-ESAP/"
    
    # Generate high quality QR code with High Error Correction
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
    W, H = 1080, 1500
    canvas = Image.new("RGBA", (W, H), (15, 23, 42, 255)) # Deep navy slate base
    
    # Gradient background
    draw = ImageDraw.Draw(canvas)
    for y in range(H):
        ratio = y / H
        r = int(14 * (1 - ratio) + 24 * ratio)
        g = int(21 * (1 - ratio) + 36 * ratio)
        b = int(38 * (1 - ratio) + 64 * ratio)
        draw.line([(0, y), (W, y)], fill=(r, g, b, 255))
        
    # Ambient glows (matching the banner color #98B6ED and accent #22D3EE)
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    # Top glow (banner soft blue #98B6ED)
    glow_draw.ellipse([W//2 - 380, 80, W//2 + 380, 520], fill=(152, 182, 237, 50))
    # Bottom glow (cyan #22D3EE)
    glow_draw.ellipse([W//2 - 320, 680, W//2 + 320, 1320], fill=(34, 211, 238, 35))
    glow = glow.filter(ImageFilter.GaussianBlur(90))
    canvas = Image.alpha_composite(canvas, glow)
    draw = ImageDraw.Draw(canvas)
    
    # Outer Card Frame (Glassmorphism card)
    card_x0, card_y0 = 70, 70
    card_x1, card_y1 = W - 70, H - 70
    
    card_bg = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    card_draw = ImageDraw.Draw(card_bg)
    card_draw.rounded_rectangle(
        [card_x0, card_y0, card_x1, card_y1],
        radius=40,
        fill=(255, 255, 255, 12),
        outline=(152, 182, 237, 75),
        width=2
    )
    canvas = Image.alpha_composite(canvas, card_bg)
    draw = ImageDraw.Draw(canvas)
    
    # Fonts setup
    font_dir = os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Fonts')
    def get_font(name, size):
        try:
            return ImageFont.truetype(os.path.join(font_dir, name), size)
        except:
            return ImageFont.load_default()
            
    font_badge = get_font('segoeui.ttf', 20)
    font_title = get_font('segoeuib.ttf', 48)
    font_subtitle = get_font('segoeuib.ttf', 26)
    font_authors = get_font('segoeui.ttf', 20)
    font_callout = get_font('segoeuib.ttf', 25)
    font_url = get_font('consolas.ttf', 18)
    
    # 1. Logo ESAP
    logo_path = "Logo_Esap.png"
    current_y = 120
    if os.path.exists(logo_path):
        try:
            logo = Image.open(logo_path).convert("RGBA")
            target_w = 200
            ratio = target_w / logo.width
            target_h = int(logo.height * ratio)
            logo = logo.resize((target_w, target_h), Image.Resampling.LANCZOS)
            canvas.paste(logo, ((W - target_w) // 2, current_y), logo)
            current_y += target_h + 26
        except Exception as e:
            print("Logo load error:", e)
            current_y += 30

    # 2. Institutional Pill Badge
    badge_text = "ESCUELA SUPERIOR DE ADMINISTRACIÓN PÚBLICA • ESAP"
    bbox = draw.textbbox((0, 0), badge_text, font=font_badge)
    bw = bbox[2] - bbox[0] + 44
    bh = bbox[3] - bbox[1] + 16
    bx = (W - bw) // 2
    draw.rounded_rectangle([bx, current_y, bx + bw, current_y + bh], radius=bh//2, fill=(152, 182, 237, 35), outline=(152, 182, 237, 180), width=1)
    draw.text(((W - (bbox[2] - bbox[0])) // 2, current_y + 6), badge_text, font=font_badge, fill=(152, 182, 237, 255))
    current_y += bh + 26

    # 3. Main Title: "Distribucion de frecuencias"
    title_text = "Distribucion de frecuencias"
    bbox_t = draw.textbbox((0, 0), title_text, font=font_title)
    draw.text(((W - (bbox_t[2] - bbox_t[0])) // 2, current_y), title_text, font=font_title, fill=(255, 255, 255))
    current_y += 58

    # 4. Subtitle: "TALLER 2 Tablas y graficas" (highlighted with banner soft blue)
    subtitle_text = "TALLER 2 Tablas y graficas"
    bbox_sub = draw.textbbox((0, 0), subtitle_text, font=font_subtitle)
    draw.text(((W - (bbox_sub[2] - bbox_sub[0])) // 2, current_y), subtitle_text, font=font_subtitle, fill=(152, 182, 237)) # #98b6ed
    current_y += 42

    # 5. Authors
    authors_text = "Pablo Santiago Triana • Carol Mariana Boton • Yessica Melisa Morales"
    bbox_auth = draw.textbbox((0, 0), authors_text, font=font_authors)
    draw.text(((W - (bbox_auth[2] - bbox_auth[0])) // 2, current_y), authors_text, font=font_authors, fill=(148, 163, 184))
    current_y += 44

    # 6. QR Code Container Box
    qr_box_size = 480
    qr_box_x = (W - qr_box_size) // 2
    qr_box_y = current_y
    
    # White rounded square for QR code
    draw.rounded_rectangle([qr_box_x, qr_box_y, qr_box_x + qr_box_size, qr_box_y + qr_box_size], radius=30, fill=(255, 255, 255, 255))
    # Elegant double-effect border
    draw.rounded_rectangle([qr_box_x, qr_box_y, qr_box_x + qr_box_size, qr_box_y + qr_box_size], radius=30, outline=(152, 182, 237, 200), width=3)
    
    # Paste QR code inside
    qr_scaled = qr_img.resize((qr_box_size - 40, qr_box_size - 40), Image.Resampling.NEAREST)
    canvas.paste(qr_scaled, (qr_box_x + 20, qr_box_y + 20), qr_scaled)
    
    current_y += qr_box_size + 30
    
    # 7. Scan Instruction Pill
    scan_text = "📷 ESCANEA PARA INGRESAR AL INFORME WEB"
    bbox_scan = draw.textbbox((0, 0), scan_text, font=font_callout)
    draw.text(((W - (bbox_scan[2] - bbox_scan[0])) // 2, current_y), scan_text, font=font_callout, fill=(255, 255, 255))
    current_y += 42
    
    # 8. Web URL Badge
    url_display = target_url
    bbox_url = draw.textbbox((0, 0), url_display, font=font_url)
    url_w = bbox_url[2] - bbox_url[0] + 36
    url_h = bbox_url[3] - bbox_url[1] + 18
    url_x = (W - url_w) // 2
    draw.rounded_rectangle([url_x, current_y, url_x + url_w, current_y + url_h], radius=12, fill=(15, 23, 42, 230), outline=(51, 65, 85, 255), width=1)
    draw.text(((W - (bbox_url[2] - bbox_url[0])) // 2, current_y + 7), url_display, font=font_url, fill=(152, 182, 237))

    # Save output
    output_path = "codigo_qr_proyecto.png"
    canvas.convert("RGB").save(output_path, "PNG", quality=95)
    print(f"Generated successfully: {output_path}")

if __name__ == "__main__":
    create_qr_card()
