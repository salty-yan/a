import json
import os
import random

from app.utils.paths import get_data_file


class InterpretationService:
    """解读服务，根据规则生成占卜解释"""

    def __init__(self):
        self.templates = {}
        self._load_templates()

    def _load_templates(self):
        """加载解读模板"""
        data_path = get_data_file("tarot_cards.json")
        try:
            with open(data_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.templates = data.get("interpretation_templates", {})
        except (FileNotFoundError, json.JSONDecodeError):
            self.templates = {}

    def interpret(self, question, question_type, spread_name, draw_results):
        """生成综合解读"""
        if not draw_results:
            return "暂无解读数据。"

        template = self.templates.get(question_type, {})
        advice_prefix = template.get("advice_prefix", "综合来看，")
        advice_suffix = template.get("advice_suffix", "希望这些指引能为你带来启发。")
        tone = template.get("tone", "")

        lines = []
        lines.append(f"【问题】{question}")
        lines.append(f"【问题类型】{question_type}")
        lines.append(f"【牌阵】{spread_name}")
        lines.append("")

        for i, result in enumerate(draw_results, 1):
            card = result["card"]
            is_reversed = result["is_reversed"]
            position = result["position"]
            direction = "逆位" if is_reversed else "正位"
            meaning = card["reversed_meaning"] if is_reversed else card["upright_meaning"]

            lines.append(f"--- 第{i}张牌：{position} ---")
            lines.append(f"卡牌：{card['name_cn']} ({card['name_en']}) [{direction}]")
            lines.append(f"所属：{card['arcana']}" + (f" · {card['suit']}" if card['suit'] else ""))
            lines.append(f"关键词：{'、'.join(card['keywords'])}")
            lines.append(f"解读：{meaning}")
            lines.append("")

        # 综合建议
        lines.append("=== 综合建议 ===")
        combined_advice = self._generate_combined_advice(
            draw_results, question_type, advice_prefix, advice_suffix
        )
        lines.append(combined_advice)

        return "\n".join(lines)

    def _generate_combined_advice(self, draw_results, question_type, prefix, suffix):
        """根据卡牌组合生成综合建议"""
        upright_count = sum(1 for r in draw_results if not r["is_reversed"])
        reversed_count = sum(1 for r in draw_results if r["is_reversed"])

        advice_parts = [prefix]

        if upright_count > reversed_count:
            advice_parts.append("整体能量偏向积极，")
        elif reversed_count > upright_count:
            advice_parts.append("当前可能面临一些挑战和反思，")
        else:
            advice_parts.append("正逆位能量平衡，")

        # 根据问题类型添加具体建议
        type_advice = {
            "学习事业": [
                "建议制定清晰的学习或工作计划，将大目标分解为可执行的小步骤。",
                "注意劳逸结合，避免过度压力影响效率和创造力。",
                "保持专注和耐心，每一步的积累都会带来成长。",
            ],
            "人际关系": [
                "建议主动沟通，真诚地表达自己的想法和感受。",
                "在关系中保持适当的边界感，尊重他人的同时也照顾好自己。",
                "学会倾听和理解，良好的人际关系需要双方共同维护。",
            ],
            "情绪状态": [
                "允许自己感受各种情绪，不必急于逃避或评判。",
                "尝试通过书写、运动或与信任的人交谈来释放情绪。",
                "建立一个自我照顾的日常习惯，给自己足够的时间和空间。",
            ],
            "未来选择": [
                "列出每个选项的优缺点，冷静评估各种可能性。",
                "不要急于做决定，给自己足够的思考时间。",
                "相信你的直觉，最了解你自己的人始终是你自己。",
            ],
        }

        advices = type_advice.get(question_type, [
            "保持冷静和理性，仔细分析当前的情况。",
            "相信自己的判断力，勇敢做出选择。",
        ])

        advice_parts.append(random.choice(advices))
        advice_parts.append(suffix)

        return "".join(advice_parts)
