#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从 Wikipedia 下载 Rider-Waite 塔罗牌高清图片"""

import requests
import json
import os
import sys
import time
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).resolve().parent
CARDS_DIR = PROJECT_ROOT / "assets" / "cards"
CARDS_DIR.mkdir(parents=True, exist_ok=True)

# Wikipedia API
API_URL = "https://en.wikipedia.org/w/api.php"

# 塔罗牌 ID -> Wikipedia 页面标题映射
# Major Arcana (0-21)
MAJOR_ARCANA = {
    0: "The Fool (tarot card)",
    1: "The Magician (tarot card)",
    2: "The High Priestess",
    3: "The Empress (tarot card)",
    4: "The Emperor (tarot card)",
    5: "The Hierophant",
    6: "The Lovers",
    7: "The Chariot (tarot card)",
    8: "Strength (tarot card)",
    9: "The Hermit (tarot card)",
    10: "Wheel of Fortune (tarot card)",
    11: "Justice (tarot card)",
    12: "The Hanged Man (tarot card)",
    13: "Death (tarot card)",
    14: "Temperance (tarot card)",
    15: "The Devil (tarot card)",
    16: "The Tower (tarot card)",
    17: "The Star (tarot card)",
    18: "The Moon (tarot card)",
    19: "The Sun (tarot card)",
    20: "Judgement (tarot card)",
    21: "The World (tarot card)",
}

# Minor Arcana - Wands (权杖) 22-35
# Each Rank card: "Page of Wands", "Ace of Wands", etc.
# Court cards: "Page of Wands", "Knight of Wands", "Queen of Wands", "King of Wands"
SUIT_WANDS = {
    22: "Ace of Wands",       # 权杖王牌
    23: "Two of Wands",       # 权杖二
    24: "Three of Wands",     # 权杖三
    25: "Four of Wands",      # 权杖四
    26: "Five of Wands",      # 权杖五
    27: "Six of Wands",       # 权杖六
    28: "Seven of Wands",     # 权杖七
    29: "Eight of Wands",     # 权杖八
    30: "Nine of Wands",      # 权杖九
    31: "Ten of Wands",       # 权杖十
    32: "Page of Wands",      # 权杖侍从
    33: "Knight of Wands",    # 权杖骑士
    34: "Queen of Wands",     # 权杖王后
    35: "King of Wands",      # 权杖国王
}

# Minor Arcana - Cups (圣杯) 36-49
SUIT_CUPS = {
    36: "Ace of Cups",
    37: "Two of Cups",
    38: "Three of Cups",
    39: "Four of Cups",
    40: "Five of Cups",
    41: "Six of Cups",
    42: "Seven of Cups",
    43: "Eight of Cups",
    44: "Nine of Cups",
    45: "Ten of Cups",
    46: "Page of Cups",
    47: "Knight of Cups",
    48: "Queen of Cups",
    49: "King of Cups",
}

# Minor Arcana - Swords (宝剑) 50-63
SUIT_SWORDS = {
    50: "Ace of Swords",
    51: "Two of Swords",
    52: "Three of Swords",
    53: "Four of Swords",
    54: "Five of Swords",
    55: "Six of Swords",
    56: "Seven of Swords",
    57: "Eight of Swords",
    58: "Nine of Swords",
    59: "Ten of Swords",
    60: "Page of Swords",
    61: "Knight of Swords",
    62: "Queen of Swords",
    63: "King of Swords",
}

# Minor Arcana - Pentacles (星币/钱币) 64-77
SUIT_PENTACLES = {
    64: "Ace of Pentacles",
    65: "Two of Pentacles",
    66: "Three of Pentacles",
    67: "Four of Pentacles",
    68: "Five of Pentacles",
    69: "Six of Pentacles",
    70: "Seven of Pentacles",
    71: "Eight of Pentacles",
    72: "Nine of Pentacles",
    73: "Ten of Pentacles",
    74: "Page of Pentacles",
    75: "Knight of Pentacles",
    76: "Queen of Pentacles",
    77: "King of Pentacles",
}

# 合并所有映射
ALL_CARDS = {}
ALL_CARDS.update(MAJOR_ARCANA)
ALL_CARDS.update(SUIT_WANDS)
ALL_CARDS.update(SUIT_CUPS)
ALL_CARDS.update(SUIT_SWORDS)
ALL_CARDS.update(SUIT_PENTACLES)


def get_page_image_url(page_title):
    """通过 Wikipedia API 获取页面的主图片 URL"""
    params = {
        "action": "query",
        "titles": page_title,
        "prop": "pageimages",
        "format": "json",
        "pithumbsize": 500,  # 500px 宽
    }

    try:
        resp = requests.get(API_URL, params=params, timeout=15,
                          headers={"User-Agent": "TarotInsight/1.0 (educational project)"})
        data = resp.json()
        pages = data.get("query", {}).get("pages", {})

        for page_id, page_info in pages.items():
            if page_id == "-1":
                return None  # 页面不存在
            thumbnail = page_info.get("thumbnail", {})
            source_url = thumbnail.get("source", "")
            if source_url:
                return source_url
        return None
    except Exception as e:
        print(f"  API 请求失败: {e}")
        return None


def get_image_url_from_file(page_title):
    """获取页面上第一张图片（通过 images 属性），用更高分辨率"""
    # 第一步：获取页面上的图片文件名
    params = {
        "action": "query",
        "titles": page_title,
        "prop": "images",
        "format": "json",
        "imlimit": 5,
    }
    try:
        resp = requests.get(API_URL, params=params, timeout=15,
                          headers={"User-Agent": "TarotInsight/1.0"})
        data = resp.json()
        pages = data.get("query", {}).get("pages", {})
        for page_id, page_info in pages.items():
            images = page_info.get("images", [])
            if not images:
                return None
            # 取第一个非 SVG 图片（通常是主图）
            for img in images:
                title = img["title"]
                if title.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                    # 第二步：获取该图片的 URL（更大尺寸）
                    return get_file_url(title)
            # 如果全是 SVG，也取第一个
            return get_file_url(images[0]["title"])
        return None
    except Exception as e:
        print(f"  获取图片列表失败: {e}")
        return None


def get_file_url(file_title):
    """获取 Wikimedia 文件的实际下载 URL"""
    params = {
        "action": "query",
        "titles": file_title,
        "prop": "imageinfo",
        "iiprop": "url",
        "format": "json",
        "iiurlwidth": 400,  # 400px 宽
    }
    try:
        resp = requests.get(API_URL, params=params, timeout=15,
                          headers={"User-Agent": "TarotInsight/1.0"})
        data = resp.json()
        pages = data.get("query", {}).get("pages", {})
        for page_id, page_info in pages.items():
            imageinfo = page_info.get("imageinfo", [])
            if imageinfo:
                thumb_url = imageinfo[0].get("thumburl", "")
                if thumb_url:
                    return thumb_url
                return imageinfo[0].get("url", "")
        return None
    except Exception as e:
        print(f"  获取图片 URL 失败: {e}")
        return None


def download_image(url, save_path):
    """下载图片到指定路径"""
    try:
        resp = requests.get(url, timeout=30,
                          headers={"User-Agent": "TarotInsight/1.0"})
        if resp.status_code == 200:
            with open(save_path, 'wb') as f:
                f.write(resp.content)
            size_kb = len(resp.content) / 1024
            return True, size_kb
        return False, 0
    except Exception as e:
        return False, 0


def main():
    print("=" * 60)
    print("  塔罗牌图片下载工具 - 从 Wikipedia 获取 Rider-Waite 图片")
    print("=" * 60)
    print()

    success_count = 0
    fail_count = 0
    skipped_count = 0

    for card_id in sorted(ALL_CARDS.keys()):
        page_title = ALL_CARDS[card_id]
        save_path = CARDS_DIR / f"{card_id}.png"

        # 检查是否已有有效图片（大于 5KB 说明不是占位图）
        if save_path.exists() and save_path.stat().st_size > 5000:
            # 检查是否是 PIL 生成的占位图（通过读取前几个字节判断）
            with open(save_path, 'rb') as f:
                header = f.read(8)
            if header[:3] != b'\x89PNG':
                pass  # 不是 PNG，重新下载
            else:
                skipped_count += 1
                print(f"  [{card_id:2d}] ✓ 已存在 (跳过)")
                continue

        print(f"  [{card_id:2d}] {page_title} ...", end=" ", flush=True)

        # 方法1：通过 pageimages API 获取缩略图
        url = get_page_image_url(page_title)
        if not url:
            # 方法2：通过 images + imageinfo API 获取更大图
            url = get_image_url_from_file(page_title)

        if url:
            ok, size_kb = download_image(url, save_path)
            if ok and size_kb > 2:
                success_count += 1
                print(f"✓ ({size_kb:.0f} KB)")
            else:
                fail_count += 1
                print(f"✗ 下载失败或文件太小")
                # 删除空文件
                if save_path.exists():
                    save_path.unlink()
        else:
            fail_count += 1
            print("✗ 未找到图片")

        # 礼貌延迟，避免 API 限制
        time.sleep(0.3)

    print()
    print("=" * 60)
    print(f"  结果: 成功 {success_count} | 跳过 {skipped_count} | 失败 {fail_count}")
    print("=" * 60)

    if fail_count > 0:
        print("\n  部分图片下载失败。可重新运行本脚本重试。")
        print("  失败的卡片将使用程序内置的占位图片。")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
