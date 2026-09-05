import os
import json
from PIL import Image, ImageDraw, ImageFont

output_dir = "sites/site-2/public/images/spaces"
os.makedirs(output_dir, exist_ok=True)

with open("sites/site-2/src/data/properties.json", "r", encoding="utf-8") as f:
    properties = json.load(f)

font_title = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 44)
font_sub = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 22)
font_badge = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 15)
font_card_val = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 32)
font_card_lbl = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 13)
font_card_sub = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 13)
font_mono = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 14)

W, H = 1200, 675

print(f"Generating {len(properties)} luxury WebP property covers for WorkationRadar...\n")

for p in properties:
    img = Image.new("RGB", (W, H), color=(18, 15, 12))  # Warm dark stone-950
    draw = ImageDraw.Draw(img)

    # Ambient amber glow
    for r in range(400, 0, -20):
        box = [(W//2 - r*1.2, -r//2), (W//2 + r*1.2, r*1.5)]
        draw.ellipse(box, outline=(45, 25, 10))

    # Outer border
    draw.rounded_rectangle([(16, 16), (W-16, H-16)], radius=16, outline=(44, 38, 34), width=2)
    # Top accent bar
    draw.rounded_rectangle([(16, 16), (W-16, 24)], radius=8, fill=(217, 119, 6))  # amber-600

    # Dot grid
    for x in range(60, W - 60, 48):
        for y in range(40, 180, 24):
            draw.point((x, y), fill=(35, 30, 26))

    # Location Pill Badge
    loc_text = f"VERIFIED REMOTE WORK HUB  •  {p['city'].upper()}, {p['country'].upper()}"
    badge_w = draw.textlength(loc_text, font=font_badge) + 36
    draw.rounded_rectangle([(60, 50), (60 + badge_w, 88)], radius=8, fill=(35, 25, 15), outline=(217, 119, 6), width=2)
    draw.text((78, 60), loc_text, fill=(245, 158, 11), font=font_badge)

    # Score Pill on Top Right
    score_text = f"Productivity Score: {p['productivity_score']}/100"
    score_w = draw.textlength(score_text, font=font_badge) + 36
    draw.rounded_rectangle([(W - 60 - score_w, 50), (W - 60, 88)], radius=8, fill=(16, 40, 25), outline=(34, 197, 94), width=2)
    draw.text((W - 60 - score_w + 18, 60), score_text, fill=(74, 222, 128), font=font_badge)

    # Title & Subtitle
    draw.text((60, 115), p['name'], fill=(255, 255, 255), font=font_title)
    sub = f"Sub-{p['ping_ms']}ms Ping Fiber • {p['chair_model']} • {p['phone_booths_count']} Soundproof Call Booths"
    draw.text((60, 180), sub, fill=(168, 162, 158), font=font_sub)

    # Divider
    draw.line([(60, 230), (W - 60, 230)], fill=(44, 38, 34), width=2)

    # 3 Empirical Metric Cards
    cards = [
        {"label": "VERIFIED DOWNLOAD SPEED", "val": f"{p['download_mbps']} Mbps", "sub": f"{p['upload_mbps']} Mbps Upload • {p['ping_ms']}ms Ping", "col": (52, 211, 153)},
        {"label": "ERGONOMIC SEATING", "val": p['chair_model'].split()[0] + " " + p['chair_model'].split()[1] if len(p['chair_model'].split()) > 1 else p['chair_model'], "sub": f"Standing Desks: {'Yes' if p['standing_desks_available'] else 'No'} • {p['phone_booths_count']} Booths", "col": (251, 191, 36)},
        {"label": "VERIFIED MONTHLY RATE", "val": f"€{p['monthly_rate_eur']} / mo", "sub": f"Min Stay: {p['minimum_stay_days']} Days • All-Inclusive", "col": (245, 158, 11)}
    ]

    card_w = (W - 120 - 40) // 3
    for i, card in enumerate(cards):
        cx1 = 60 + i * (card_w + 20)
        cy1 = 260
        cx2 = cx1 + card_w
        cy2 = 560

        draw.rounded_rectangle([(cx1, cy1), (cx2, cy2)], radius=16, fill=(28, 25, 23), outline=(68, 64, 60), width=2)
        draw.rounded_rectangle([(cx1 + 10, cy1 + 10), (cx2 - 10, cy1 + 14)], radius=2, fill=card["col"])

        draw.text((cx1 + 24, cy1 + 35), card["label"], fill=(168, 162, 158), font=font_card_lbl)
        draw.text((cx1 + 24, cy1 + 90), card["val"], fill=card["col"], font=font_card_val)
        draw.text((cx1 + 24, cy1 + 175), card["sub"], fill=(214, 211, 209), font=font_card_sub)

        draw.rounded_rectangle([(cx1 + 24, cy2 - 50), (cx2 - 24, cy2 - 22)], radius=6, fill=(41, 37, 36))
        draw.text((cx1 + 36, cy2 - 42), f"TESTED: {p['verified_date']}", fill=(120, 113, 108), font=font_mono)

    # Footer
    draw.text((60, 615), "WorkationRadar.com  •  16-Field Empirical Workspace Verification Matrix", fill=(120, 113, 108), font=font_mono)
    draw.text((W - 320, 615), "Verified Coliving Index 2026", fill=(87, 83, 78), font=font_mono)

    out_file = os.path.join(output_dir, f"{p['slug']}.webp")
    img.save(out_file, "WEBP", quality=90)
    print(f"Generated WebP: {out_file} ({os.path.getsize(out_file)} bytes)")

print("\nALL 10 PROPERTY COVERS GENERATED!")
