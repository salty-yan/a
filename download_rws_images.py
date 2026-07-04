"""
从 Wikimedia Commons 下载经典 Rider-Waite-Smith 塔罗牌图片
RWS 牌组 (1909) 已进入公共领域
"""
import os
import sys
import json
import time
import requests
from io import BytesIO
from PIL import Image

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
CARDS_DIR = os.path.join(PROJECT_ROOT, "assets", "cards")
DATA_FILE = os.path.join(PROJECT_ROOT, "data", "tarot_cards.json")

# Wikimedia Commons 命名映射 (Rider-Waite-Smith 牌组)
MAJOR_ARCANA_NAMES = [
    "Fool", "Magician", "High_Priestess", "Empress", "Emperor",
    "Hierophant", "Lovers", "Chariot", "Strength", "Hermit",
    "Wheel_of_Fortune", "Justice", "Hanged_Man", "Death", "Temperance",
    "Devil", "Tower", "Star", "Moon", "Sun",
    "Judgement", "World"
]

SUITS = ["Wands", "Cups", "Swords", "Pentacles"]
RANKS = [
    "01", "02", "03", "04", "05", "06", "07", "08", "09", "10",
    "11", "12", "13", "14"  # Page, Knight, Queen, King
]


def get_commons_filename(card_id):
    """根据 card_id (0-77) 获取 Wikimedia Commons 文件名"""
    if 0 <= card_id <= 21:
        # 大阿卡那
        name = MAJOR_ARCANA_NAMES[card_id]
        return f"RWS_Tarot_{card_id:02d}_{name}.jpg"
    else:
        # 小阿卡那: 22-35 Wands, 36-49 Cups, 50-63 Swords, 64-77 Pentacles
        local_id = card_id - 22
        suit_idx = local_id // 14
        rank_idx = local_id % 14
        suit = SUITS[suit_idx]
        rank = RANKS[rank_idx]
        return f"{suit}{rank}.jpg"


def get_image_url(filename):
    """通过 Wikimedia API 获取图片直链 URL"""
    api_url = "https://commons.wikimedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "titles": f"File:{filename}",
        "prop": "imageinfo",
        "iiprop": "url",
    }
    headers = {"User-Agent": "TarotInsight/1.0 (educational project; mac@example.com)"}
    try:
        resp = requests.get(api_url, params=params, headers=headers, timeout=15)
        data = resp.json()
        pages = data.get("query", {}).get("pages", {})
        for page_id, page_info in pages.items():
            if page_id == "-1":
                return None
            imageinfo = page_info.get("imageinfo", [])
            if imageinfo:
                return imageinfo[0].get("url")
        return None
    except Exception as e:
        print(f"  API 错误: {e}")
        return None


def download_card_image(card_id, url, retries=3):
    """下载并保存为 PNG"""
    output_path = os.path.join(CARDS_DIR, f"{card_id}.png")
    
    for attempt in range(retries):
        try:
            headers = {"User-Agent": "TarotInsight/1.0 (educational project)"}
            resp = requests.get(url, headers=headers, timeout=30)
            if resp.status_code == 200:
                img = Image.open(BytesIO(resp.content))
                # 统一转 PNG，保持高质量
                img.save(output_path, "PNG", optimize=True)
                return True, img.size
            else:
                print(f"    HTTP {resp.status_code}, 重试 {attempt+1}/{retries}")
        except Exception as e:
            print(f"    错误: {e}, 重试 {attempt+1}/{retries}")
        time.sleep(1)
    return False, None


def main():
    os.makedirs(CARDS_DIR, exist_ok=True)
    
    total = 78
    success = 0
    failed = []
    
    print("=" * 60)
    print("  下载经典 Rider-Waite-Smith 塔罗牌图片")
    print("  来源: Wikimedia Commons (公共领域)")
    print("=" * 60)
    
    for card_id in range(total):
        filename = get_commons_filename(card_id)
        print(f"\n[{card_id+1}/{total}] ID={card_id}: {filename}")
        
        # 先检查是否已有
        output_path = os.path.join(CARDS_DIR, f"{card_id}.png")
        
        url = get_image_url(filename)
        if not url:
            print(f"  ✗ 未找到图片: {filename}")
            failed.append(card_id)
            continue
        
        print(f"  下载: {url[:80]}...")
        ok, size = download_card_image(card_id, url)
        if ok:
            print(f"  ✓ 已保存 ({size[0]}x{size[1]})")
            success += 1
        else:
            print(f"  ✗ 下载失败")
            failed.append(card_id)
        
        # 礼貌延迟，避免过度请求
        time.sleep(0.3)
    
    print("\n" + "=" * 60)
    print(f"  完成: 成功 {success}/{total}")
    if failed:
        print(f"  失败 IDs: {failed}")
    print("=" * 60)


if __name__ == "__main__":
    main()
