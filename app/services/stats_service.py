from app.services.database_service import DatabaseService


class StatsService:
    """统计服务，提供统计数据"""

    def __init__(self):
        self.db = DatabaseService()

    def get_stats(self):
        """获取完整统计数据"""
        return self.db.get_stats()

    def refresh(self):
        """刷新统计数据"""
        return self.get_stats()
