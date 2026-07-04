import json
import random
import os

from app.utils.paths import get_data_file


class TarotService:
    """塔罗牌核心服务，负责卡牌数据加载和抽牌"""

    def __init__(self):
        self.cards = []
        self.spreads = []
        self.question_types = []
        self._load_data()

    def _load_data(self):
        """从 JSON 加载卡牌和牌阵数据"""
        data_path = get_data_file("tarot_cards.json")
        try:
            with open(data_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.cards = data.get("cards", [])
                self.spreads = data.get("spreads", [])
                self.question_types = data.get("question_types", [])
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"卡牌数据加载失败: {e}")
            self.cards = []
            self.spreads = []
            self.question_types = []

    def get_all_cards(self):
        """获取所有卡牌"""
        return self.cards

    def get_card_by_id(self, card_id):
        """根据ID获取卡牌"""
        for card in self.cards:
            if card["id"] == card_id:
                return card
        return None

    def get_cards_by_arcana(self, arcana):
        """根据阿卡那类型筛选"""
        if arcana == "全部":
            return self.cards
        return [c for c in self.cards if c["arcana"] == arcana]

    def get_cards_by_suit(self, suit):
        """根据花色筛选"""
        if suit == "全部":
            return self.cards
        return [c for c in self.cards if c["suit"] == suit]

    def search_cards(self, keyword):
        """搜索卡牌"""
        if not keyword:
            return self.cards
        keyword = keyword.lower()
        results = []
        for card in self.cards:
            if (keyword in card["name_cn"].lower() or
                keyword in card["name_en"].lower() or
                any(keyword in kw.lower() for kw in card["keywords"])):
                results.append(card)
        return results

    def get_spreads(self):
        """获取所有牌阵"""
        return self.spreads

    def get_spread_by_name(self, name):
        """根据名称获取牌阵"""
        for spread in self.spreads:
            if spread["name"] == name:
                return spread
        return None

    def get_question_types(self):
        """获取问题类型列表"""
        return self.question_types

    def draw_cards(self, spread_name):
        """根据牌阵抽牌"""
        spread = self.get_spread_by_name(spread_name)
        if not spread:
            return None, "未找到该牌阵"

        card_count = spread["card_count"]
        if card_count > len(self.cards):
            return None, "卡牌数量不足"

        drawn = random.sample(self.cards, card_count)
        results = []
        for i, card in enumerate(drawn):
            is_reversed = random.choice([True, False])
            results.append({
                "card": card,
                "is_reversed": is_reversed,
                "position": spread["positions"][i]["name"],
                "position_meaning": spread["positions"][i]["meaning"],
            })

        return results, None

    def get_daily_card(self):
        """获取今日推荐牌"""
        today = random.choice(self.cards)
        return today
