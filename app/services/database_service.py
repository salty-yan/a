import sqlite3
import os
from datetime import datetime
import json

from app.utils.paths import get_data_dir
from app.utils.constants import DATABASE_NAME


class DatabaseService:
    """数据库服务，管理历史记录和收藏"""

    def __init__(self):
        db_dir = get_data_dir()
        os.makedirs(db_dir, exist_ok=True)
        self.db_path = os.path.join(db_dir, DATABASE_NAME)
        self._init_db()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        """初始化数据库表"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS readings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question TEXT NOT NULL,
                    question_type TEXT NOT NULL,
                    spread_type TEXT NOT NULL,
                    cards_json TEXT NOT NULL,
                    interpretation TEXT NOT NULL,
                    is_favorite INTEGER DEFAULT 0,
                    note TEXT DEFAULT '',
                    created_at TEXT NOT NULL
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS favorite_cards (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    card_id INTEGER NOT NULL UNIQUE,
                    created_at TEXT NOT NULL
                )
            """)
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            print(f"数据库初始化失败: {e}")

    def save_reading(self, question, question_type, spread_type, cards, interpretation, note=""):
        """保存占卜记录"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO readings (question, question_type, spread_type, cards_json, interpretation, note, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (question, question_type, spread_type, json.dumps(cards, ensure_ascii=False),
                  interpretation, note, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            conn.commit()
            reading_id = cursor.lastrowid
            conn.close()
            return reading_id
        except sqlite3.Error as e:
            print(f"保存记录失败: {e}")
            return None

    def get_all_readings(self):
        """获取所有占卜记录"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM readings ORDER BY created_at DESC")
            rows = cursor.fetchall()
            conn.close()
            return rows
        except sqlite3.Error as e:
            print(f"获取记录失败: {e}")
            return []

    def get_reading_by_id(self, reading_id):
        """根据ID获取单条记录"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM readings WHERE id = ?", (reading_id,))
            row = cursor.fetchone()
            conn.close()
            return row
        except sqlite3.Error as e:
            print(f"获取记录失败: {e}")
            return None

    def delete_reading(self, reading_id):
        """删除占卜记录"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM readings WHERE id = ?", (reading_id,))
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"删除记录失败: {e}")
            return False

    def toggle_favorite(self, reading_id):
        """切换收藏状态"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT is_favorite FROM readings WHERE id = ?", (reading_id,))
            row = cursor.fetchone()
            if row is None:
                conn.close()
                return False
            new_status = 0 if row[0] else 1
            cursor.execute("UPDATE readings SET is_favorite = ? WHERE id = ?", (new_status, reading_id))
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"更新收藏失败: {e}")
            return False

    def search_readings(self, question_type=None, date_from=None, date_to=None, favorite_only=False):
        """筛选历史记录"""
        try:
            conn = self._get_connection()
            query = "SELECT * FROM readings WHERE 1=1"
            params = []
            if question_type and question_type != "全部":
                query += " AND question_type = ?"
                params.append(question_type)
            if date_from:
                query += " AND created_at >= ?"
                params.append(date_from)
            if date_to:
                query += " AND created_at <= ?"
                params.append(date_to)
            if favorite_only:
                query += " AND is_favorite = 1"
            query += " ORDER BY created_at DESC"
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            conn.close()
            return rows
        except sqlite3.Error as e:
            print(f"搜索记录失败: {e}")
            return []

    def get_stats(self):
        """获取统计数据"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            # 总占卜次数
            cursor.execute("SELECT COUNT(*) FROM readings")
            total = cursor.fetchone()[0]

            # 收藏数量
            cursor.execute("SELECT COUNT(*) FROM readings WHERE is_favorite = 1")
            favorites_count = cursor.fetchone()[0]

            # 问题类型分布
            cursor.execute("SELECT question_type, COUNT(*) FROM readings GROUP BY question_type")
            type_dist = cursor.fetchall()

            # 常抽卡牌 Top 5
            cursor.execute("SELECT cards_json FROM readings")
            all_rows = cursor.fetchall()
            card_counter = {}
            for row in all_rows:
                try:
                    cards = json.loads(row[0])
                    for card in cards:
                        name = card.get("name_cn", "")
                        card_counter[name] = card_counter.get(name, 0) + 1
                except (json.JSONDecodeError, KeyError):
                    pass
            top_cards = sorted(card_counter.items(), key=lambda x: x[1], reverse=True)[:5]

            # 正逆位比例
            total_cards = 0
            reversed_count = 0
            for row in all_rows:
                try:
                    cards = json.loads(row[0])
                    for card in cards:
                        total_cards += 1
                        if card.get("is_reversed", False):
                            reversed_count += 1
                except (json.JSONDecodeError, KeyError):
                    pass
            upright_count = total_cards - reversed_count

            # 每日占卜趋势
            cursor.execute("SELECT substr(created_at, 1, 10) as date, COUNT(*) FROM readings GROUP BY date ORDER BY date")
            daily_trend = cursor.fetchall()

            # 牌阵使用分布
            cursor.execute("SELECT spread_type, COUNT(*) FROM readings GROUP BY spread_type")
            spread_dist = cursor.fetchall()

            conn.close()

            return {
                "total": total,
                "favorites_count": favorites_count,
                "type_distribution": type_dist,
                "top_cards": top_cards,
                "upright_count": upright_count,
                "reversed_count": reversed_count,
                "daily_trend": daily_trend,
                "spread_distribution": spread_dist,
            }
        except sqlite3.Error as e:
            print(f"获取统计失败: {e}")
            return {
                "total": 0, "favorites_count": 0, "type_distribution": [],
                "top_cards": [], "upright_count": 0, "reversed_count": 0,
                "daily_trend": [], "spread_distribution": [],
            }
