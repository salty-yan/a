#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成经典韦特风格塔罗牌 - 仿羊皮纸底色、经典布局 (600×880)"""

import json
import os
import math
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

PROJECT_ROOT = Path(__file__).resolve().parent
CARDS_DIR = PROJECT_ROOT / "assets" / "cards"
CARDS_DIR.mkdir(parents=True, exist_ok=True)

# ===== 卡片尺寸 =====
W, H = 600, 880

# ===== 经典配色 =====
PARCHMENT = (255, 248, 230)
PARCHMENT_DARK = (240, 228, 200)
BORDER_OUTER = (80, 60, 30)
BORDER_INNER = (180, 160, 120)
TITLE_BG = (220, 200, 160)
TEXT_DARK = (40, 30, 15)
TEXT_MEDIUM = (100, 80, 50)
GOLD_ACCENT = (180, 150, 60)
WHITE = (255, 255, 255)

ROMAN = {
    0: "0", 1: "I", 2: "II", 3: "III", 4: "IV", 5: "V",
    6: "VI", 7: "VII", 8: "VIII", 9: "IX", 10: "X",
    11: "XI", 12: "XII", 13: "XIII", 14: "XIV", 15: "XV",
    16: "XVI", 17: "XVII", 18: "XVIII", 19: "XIX", 20: "XX", 21: "XXI",
}

RANK_NAMES = {
    1: "ACE", 2: "II", 3: "III", 4: "IV", 5: "V",
    6: "VI", 7: "VII", 8: "VIII", 9: "IX", 10: "X",
    11: "PAGE", 12: "KNIGHT", 13: "QUEEN", 14: "KING",
}

SUIT_SYMBOLS = {"权杖": "♆", "圣杯": "♇", "宝剑": "♅", "星币": "⬡"}

SUIT_COLORS = {
    "权杖": (180, 50, 50),
    "圣杯": (40, 80, 180),
    "宝剑": (180, 160, 40),
    "星币": (50, 140, 70),
}

with open(PROJECT_ROOT / "data" / "tarot_cards.json", "r", encoding="utf-8") as f:
    cards_data = json.load(f)["cards"]


def find_font(size):
    font_paths = [
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/Library/Fonts/Arial Unicode.ttf",
    ]
    for fp in font_paths:
        if os.path.exists(fp):
            try:
                return ImageFont.truetype(fp, size)
            except:
                continue
    return ImageFont.load_default()


def draw_classic_frame(draw):
    """经典塔罗牌边框"""
    draw.rectangle([0, 0, W - 1, H - 1], fill=PARCHMENT)
    m0 = 20
    draw.rectangle([m0, m0, W - m0, H - m0], outline=BORDER_OUTER, width=2)
    m1 = 28
    draw.rectangle([m1, m1, W - m1, H - m1], outline=BORDER_INNER, width=1)
    m2 = 36
    draw.rectangle([m2, m2, W - m2, H - m2], outline=BORDER_OUTER, width=1)
    cs = 10
    for cx, cy in [(m1 + 6, m1 + 6), (W - m1 - 6, m1 + 6),
                    (m1 + 6, H - m1 - 6), (W - m1 - 6, H - m1 - 6)]:
        draw.rectangle([cx - cs, cy - cs, cx + cs, cy + cs], outline=BORDER_OUTER, width=1)
        draw.rectangle([cx - cs + 3, cy - cs + 3, cx + cs - 3, cy + cs - 3], fill=GOLD_ACCENT)


def draw_bottom_banner(draw, name_cn, name_en, accent):
    """底部横幅"""
    banner_top = H - 150
    banner_bottom = H - 40
    draw.rectangle([40, banner_top, W - 40, banner_bottom], fill=TITLE_BG, outline=BORDER_OUTER, width=2)
    draw.line([(50, banner_top + 8), (W - 50, banner_top + 8)], fill=BORDER_OUTER, width=1)
    draw.line([(50, banner_bottom - 8), (W - 50, banner_bottom - 8)], fill=BORDER_OUTER, width=1)
    font_cn = find_font(36)
    draw.text((W // 2, banner_top + 42), name_cn, fill=TEXT_DARK, anchor="mm", font=font_cn)
    font_en = find_font(18)
    draw.text((W // 2, banner_top + 78), name_en.upper(), fill=TEXT_MEDIUM, anchor="mm", font=font_en)


def draw_top_number(draw, card, accent):
    """顶部编号"""
    arcana = card["arcana"]
    card_id = card["id"]
    if arcana == "大阿卡那":
        roman = ROMAN.get(card_id, str(card_id))
        font_num = find_font(28)
        draw.text((W // 2, 44), roman, fill=TEXT_DARK, anchor="mt", font=font_num)
    else:
        rank = (card_id - 22) % 14 + 1
        rank_name = RANK_NAMES.get(rank, str(rank))
        font_num = find_font(22)
        draw.text((W // 2, 44), rank_name, fill=accent, anchor="mt", font=font_num)


def draw_illustration_major(draw, card_id, name_cn):
    """大阿卡那象征插图"""
    symbols = {
        0: ("★", "☀"), 1: ("∞", "☿"), 2: ("☽", "✦"), 3: ("♛", "♡"),
        4: ("♚", "♆"), 5: ("†", "☩"), 6: ("♡", "⚖"), 7: ("⚔", "♞"),
        8: ("♁", "⚘"), 9: ("☉", "✧"), 10: ("☸", "☯"), 11: ("⚖", "♎"),
        12: ("⏳", "↯"), 13: ("☠", "♄"), 14: ("☤", "⚕"), 15: ("♅", "↯"),
        16: ("⚡", "♃"), 17: ("☆", "☉"), 18: ("☽", "☾"), 19: ("☼", "☀"),
        20: ("♪", "✿"), 21: ("⊕", "♁"),
    }
    symbol, symbol2 = symbols.get(card_id, ("✧", "✦"))
    cx, cy = W // 2, 380
    for r in [120, 100, 80]:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=TEXT_MEDIUM, width=1)
    for angle in range(0, 360, 30):
        rad = math.radians(angle)
        x1, y1 = cx + 70 * math.cos(rad), cy + 70 * math.sin(rad)
        x2, y2 = cx + 115 * math.cos(rad), cy + 115 * math.sin(rad)
        draw.line([(x1, y1), (x2, y2)], fill=GOLD_ACCENT, width=1)
    font_sym = find_font(80)
    draw.text((cx, cy - 5), symbol, fill=TEXT_DARK, anchor="mm", font=font_sym)
    font_sym2 = find_font(36)
    draw.text((cx, cy + 65), symbol2, fill=GOLD_ACCENT, anchor="mm", font=font_sym2)
    draw.ellipse([cx - 50, cy - 50, cx + 50, cy + 50], outline=GOLD_ACCENT, width=2)


def draw_illustration_minor(draw, suit, rank, accent):
    """小阿卡那花色图案"""
    cx, cy = W // 2, 370
    sym = SUIT_SYMBOLS.get(suit, "✦")
    count = min(rank, 10) if rank <= 10 else 1

    if count == 1:
        draw.ellipse([cx - 90, cy - 90, cx + 90, cy + 90], outline=accent, width=2)
        draw.ellipse([cx - 70, cy - 70, cx + 70, cy + 70], outline=accent, width=1)
        draw.text((cx, cy), sym, fill=accent, anchor="mm", font=find_font(100))
    elif count == 2:
        draw.text((cx, cy - 40), sym, fill=accent, anchor="mm", font=find_font(60))
        draw.text((cx, cy + 40), sym, fill=accent, anchor="mm", font=find_font(60))
        draw.line([(cx, cy - 40), (cx, cy + 40)], fill=GOLD_ACCENT, width=1)
    elif count == 3:
        for dy in [-70, 0, 70]:
            draw.text((cx, cy + dy), sym, fill=accent, anchor="mm", font=find_font(60))
    elif count == 4:
        for dx, dy in [(-30, -50), (30, -50), (-30, 50), (30, 50)]:
            draw.text((cx + dx, cy + dy), sym, fill=accent, anchor="mm", font=find_font(40))
    elif count == 5:
        positions = [(-40, -60), (40, -60), (0, -15), (-40, 30), (40, 30)]
        for dx, dy in positions:
            draw.text((cx + dx, cy + dy), sym, fill=accent, anchor="mm", font=find_font(40))
    elif 6 <= count <= 10:
        layout = {
            6: [(3, 2, 50, 60)], 7: [(2, 3, 55, 55), (3, 2, 55, 55)],
            8: [(2, 3, 50, 50), (3, 2, 50, 50)],
            9: [(3, 3, 50, 55)], 10: [(2, 3, 45, 45), (3, 2, 45, 45)]
        }
        rows_data = layout.get(count, [(3, 3, 50, 55)])
        cy_start = cy - 75
        for cols, rows_in, gap_x, gap_y in rows_data:
            for r in range(rows_in):
                for c in range(cols):
                    px = cx + (c - (cols - 1) / 2) * gap_x
                    py = cy_start + r * gap_y + (rows_in - 1) * gap_y / 2
                    if count == 7 and r == 0:
                        px = cx + (c - 1) * gap_x
                    draw.text((int(px), int(py)), sym, fill=accent, anchor="mm", font=find_font(24))

    # 宫廷牌
    if rank > 10:
        court_labels = {11: "侍从", 12: "骑士", 13: "王后", 14: "国王"}
        draw.ellipse([cx - 80, cy - 60, cx + 80, cy + 60], outline=accent, width=2)
        draw.text((cx, cy - 10), sym, fill=accent, anchor="mm", font=find_font(80))
        draw.text((cx, cy + 55), court_labels.get(rank, ""), fill=accent, anchor="mm", font=find_font(24))


def generate_card_image(card):
    card_id = card["id"]
    name_cn = card["name_cn"]
    name_en = card["name_en"]
    arcana = card["arcana"]
    suit = card.get("suit", "")
    accent = SUIT_COLORS.get(suit, TEXT_DARK) if suit else TEXT_DARK

    img = Image.new('RGB', (W, H), PARCHMENT)
    draw = ImageDraw.Draw(img)

    draw_classic_frame(draw)
    draw_top_number(draw, card, accent)

    line_y = 68
    draw.line([(100, line_y), (W - 100, line_y)], fill=BORDER_INNER, width=1)

    if arcana == "大阿卡那":
        draw_illustration_major(draw, card_id, name_cn)
    else:
        rank = (card_id - 22) % 14 + 1
        draw_illustration_minor(draw, suit, rank, accent)

    draw_bottom_banner(draw, name_cn, name_en, accent)

    save_path = CARDS_DIR / f"{card_id}.png"
    img.save(save_path, "PNG", optimize=True)
    return save_path


def main():
    print("=" * 60)
    print("  生成经典韦特风格塔罗牌 (600×880)")
    print("=" * 60)
    for card in cards_data:
        path = generate_card_image(card)
        print(f"  [{card['id']:2d}] {card['name_cn']:8s} -> {path.name}")
    print(f"\n  共生成 {len(cards_data)} 张经典风格塔罗牌")
    print(f"  保存路径: {CARDS_DIR}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
