"""
酒店查询智能体
职责：酒店搜索、筛选、价格对比
"""
from typing import Dict, Any, List
from langchain.prompts import ChatPromptTemplate
from langchain_core.language_models import BaseChatModel
from .base_agent import BaseAgent
from models import Hotel, HotelSearchResult, HotelStarRating
import random


class HotelQueryAgent(BaseAgent):
    """酒店查询智能体"""
    
    def __init__(self, llm: BaseChatModel):
        super().__init__(llm, "酒店查询智能体")
    
    def _create_prompt_template(self) -> ChatPromptTemplate:
        """创建提示词模板"""
        return ChatPromptTemplate.from_messages([
            ("system", """你是一个专业的酒店推荐助手。根据用户的酒店搜索结果，提供专业的选择建议。

请分析酒店列表，考虑：
1. 价格性价比
2. 星级和评分
3. 地理位置（距离市中心）
4. 设施配备
5. 用户评价

给出简洁专业的建议。"""),
            ("user", """酒店搜索参数：
城市: {city}
预算: {budget}
偏好: {preferences}

找到以下酒店：
{hotels_info}

请给出选择建议。""")
        ])
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        查询酒店信息
        
        Args:
            input_data: 包含酒店搜索参数
            
        Returns:
            酒店搜索结果
        """
        city = input_data.get("destination", "")
        budget = input_data.get("budget", 0)
        preferences = input_data.get("preferences", [])
        
        self.log_info(f"查询酒店: {city}, 预算: {budget}")
        
        try:
            # 模拟查询酒店数据
            hotels = self._search_hotels(city, budget, preferences)
            
            # 生成酒店信息摘要
            hotels_info = self._format_hotels_info(hotels)
            
            # 调用LLM生成建议
            suggestion = await self.invoke_llm(
                city=city,
                budget=f"¥{budget}" if budget else "不限",
                preferences=", ".join(preferences) if preferences else "无特殊要求",
                hotels_info=hotels_info
            )
            
            result = HotelSearchResult(
                hotels=hotels,
                total_count=len(hotels),
                search_params={
                    "city": city,
                    "budget": budget,
                    "preferences": preferences
                }
            )
            
            self.log_info(f"找到 {len(hotels)} 家酒店")
            
            return {
                "success": True,
                "data": result.model_dump(),
                "suggestion": suggestion,
                "message": f"找到 {len(hotels)} 家酒店"
            }
            
        except Exception as e:
            self.log_error("酒店查询失败", e)
            return {
                "success": False,
                "error": f"酒店查询失败: {str(e)}"
            }
    
    def _search_hotels(self, city: str, budget: float, 
                      preferences: List[str]) -> List[Hotel]:
        """模拟查询酒店数据"""
        hotels = []
        hotel_chains = ["希尔顿", "万豪", "香格里拉", "洲际", "喜来登", "凯悦", "如家", "汉庭"]
        facilities_pool = ["WiFi", "游泳池", "健身房", "餐厅", "停车场", "会议室", "SPA", "酒吧"]
        room_types = ["标准间", "豪华间", "商务套房", "行政套房", "总统套房"]
        
        # 生成4-6家模拟酒店
        for i in range(random.randint(4, 6)):
            hotel_name = f"{city}{random.choice(hotel_chains)}酒店"
            star_rating = random.choice(list(HotelStarRating))
            
            # 根据星级设定价格范围
            if star_rating == HotelStarRating.THREE_STAR:
                price = random.randint(200, 400)
            elif star_rating == HotelStarRating.FOUR_STAR:
                price = random.randint(400, 800)
            elif star_rating == HotelStarRating.FIVE_STAR:
                price = random.randint(800, 1500)
            else:  # LUXURY
                price = random.randint(1500, 3000)
            
            # 如果有预算限制，调整价格
            if budget > 0 and price > budget:
                price = budget * random.uniform(0.7, 0.95)
            
            # 随机选择设施
            num_facilities = random.randint(3, 6)
            facilities = random.sample(facilities_pool, num_facilities)
            
            hotel = Hotel(
                hotel_id=f"HT{random.randint(10000, 99999)}",
                name=hotel_name,
                star_rating=star_rating,
                address=f"{city}市{random.choice(['中心区', '商务区', '旅游区'])}{random.randint(1, 999)}号",
                city=city,
                price_per_night=round(price, 2),
                available_rooms=random.randint(5, 50),
                room_type=random.choice(room_types),
                facilities=facilities,
                rating=round(random.uniform(4.0, 5.0), 1),
                reviews_count=random.randint(100, 5000),
                distance_to_center=round(random.uniform(0.5, 15.0), 1)
            )
            hotels.append(hotel)
        
        # 按性价比排序（评分/价格）
        hotels.sort(key=lambda x: x.rating / (x.price_per_night / 100), reverse=True)
        return hotels
    
    def _format_hotels_info(self, hotels: List[Hotel]) -> str:
        """格式化酒店信息"""
        info_lines = []
        for i, hotel in enumerate(hotels, 1):
            info_lines.append(
                f"{i}. {hotel.name} - {hotel.star_rating.value} - "
                f"¥{hotel.price_per_night}/晚 - 评分{hotel.rating} - "
                f"距市中心{hotel.distance_to_center}km - "
                f"设施: {', '.join(hotel.facilities[:3])}等"
            )
        return "\n".join(info_lines)

