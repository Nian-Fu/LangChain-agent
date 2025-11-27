"""
行程规划智能体
职责：整合交通/住宿/景点生成行程
"""
from typing import Dict, Any, List
from datetime import date, timedelta
from langchain.prompts import ChatPromptTemplate
from langchain_core.language_models import BaseChatModel
from .base_agent import BaseAgent
from models import Itinerary, ItineraryDay
import random
import json


class ItineraryPlanAgent(BaseAgent):
    """行程规划智能体"""
    
    def __init__(self, llm: BaseChatModel):
        super().__init__(llm, "行程规划智能体")
    
    def _create_prompt_template(self) -> ChatPromptTemplate:
        """创建提示词模板"""
        return ChatPromptTemplate.from_messages([
            ("system", """你是一个专业的旅行行程规划师。根据用户的旅行信息，制定详细的每日行程计划。

请为每一天规划：
1. 上午安排：2-3个活动或景点
2. 下午安排：2-3个活动或景点
3. 晚上安排：1-2个活动
4. 住宿推荐
5. 交通建议
6. 预计花费

注意事项：
- 合理安排景点顺序，考虑地理位置
- 预留用餐和休息时间
- 避免行程过于紧凑
- 考虑景点开放时间

请以JSON格式返回每日行程，格式如下：
{{
  "days": [
    {{
      "day": 1,
      "morning": ["活动1", "活动2"],
      "afternoon": ["活动3", "活动4"],
      "evening": ["活动5"],
      "accommodation": "住宿建议",
      "transportation": "交通建议",
      "estimated_cost": 费用金额
    }}
  ],
  "summary": "行程总结"
}}"""),
            ("user", """行程规划参数：
目的地: {destination}
开始日期: {start_date}
结束日期: {end_date}
天数: {days}
预算: {budget}

可选航班信息：
{flight_info}

可选酒店信息：
{hotel_info}

推荐景点信息：
{attraction_info}

请制定详细的行程计划。""")
        ])
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        规划行程
        
        Args:
            input_data: 包含行程规划参数和其他智能体的结果
            
        Returns:
            行程规划结果
        """
        destination = input_data.get("destination", "")
        start_date_str = input_data.get("departure_date", "")
        return_date_str = input_data.get("return_date", "")
        budget = input_data.get("budget", 0)
        
        # 获取其他智能体的结果
        flight_data = input_data.get("flight_data", {})
        hotel_data = input_data.get("hotel_data", {})
        attraction_data = input_data.get("attraction_data", {})
        
        self.log_info(f"规划行程: {destination}, {start_date_str} 至 {return_date_str}")
        
        try:
            # 计算天数
            if start_date_str and return_date_str:
                start_date = date.fromisoformat(start_date_str)
                end_date = date.fromisoformat(return_date_str)
                days = (end_date - start_date).days + 1
            else:
                days = 3
                start_date = date.today()
                end_date = start_date + timedelta(days=days-1)
            
            # 格式化其他智能体的数据
            flight_info = self._format_flight_info(flight_data)
            hotel_info = self._format_hotel_info(hotel_data)
            attraction_info = self._format_attraction_info(attraction_data)
            
            # 调用LLM生成行程
            response = await self.invoke_llm(
                destination=destination,
                start_date=start_date.isoformat(),
                end_date=end_date.isoformat(),
                days=days,
                budget=f"¥{budget}" if budget else "不限",
                flight_info=flight_info,
                hotel_info=hotel_info,
                attraction_info=attraction_info
            )
            
            # 解析响应
            response = response.strip()
            if response.startswith("```json"):
                response = response[7:]
            if response.startswith("```"):
                response = response[3:]
            if response.endswith("```"):
                response = response[:-3]
            response = response.strip()
            
            itinerary_data = json.loads(response)
            
            # 构建行程对象
            itinerary_days = []
            for day_data in itinerary_data.get("days", []):
                itinerary_day = ItineraryDay(
                    day=day_data["day"],
                    travel_date=start_date + timedelta(days=day_data["day"]-1),
                    morning=day_data.get("morning", []),
                    afternoon=day_data.get("afternoon", []),
                    evening=day_data.get("evening", []),
                    accommodation=day_data.get("accommodation", ""),
                    transportation=day_data.get("transportation", ""),
                    estimated_cost=day_data.get("estimated_cost", 0.0)
                )
                itinerary_days.append(itinerary_day)
            
            total_cost = sum(day.estimated_cost for day in itinerary_days)
            
            itinerary = Itinerary(
                itinerary_id=f"IT{random.randint(10000, 99999)}",
                title=f"{destination}{days}日游",
                destination=destination,
                start_date=start_date,
                end_date=end_date,
                days=itinerary_days,
                total_cost=total_cost,
                summary=itinerary_data.get("summary", "")
            )
            
            self.log_info(f"行程规划完成: {days}天")
            
            return {
                "success": True,
                "data": itinerary.model_dump(),
                "message": f"{days}天行程规划完成"
            }
            
        except Exception as e:
            self.log_error("行程规划失败", e)
            return {
                "success": False,
                "error": f"行程规划失败: {str(e)}"
            }
    
    def _format_flight_info(self, flight_data: Dict[str, Any]) -> str:
        """格式化航班信息"""
        if not flight_data or not flight_data.get("flights"):
            return "暂无航班信息"
        
        flights = flight_data.get("flights", [])[:3]  # 只取前3个
        lines = []
        for f in flights:
            lines.append(f"{f.get('airline', '')} {f.get('flight_number', '')} - ¥{f.get('price', 0)}")
        return "\n".join(lines)
    
    def _format_hotel_info(self, hotel_data: Dict[str, Any]) -> str:
        """格式化酒店信息"""
        if not hotel_data or not hotel_data.get("hotels"):
            return "暂无酒店信息"
        
        hotels = hotel_data.get("hotels", [])[:3]  # 只取前3个
        lines = []
        for h in hotels:
            lines.append(f"{h.get('name', '')} - ¥{h.get('price_per_night', 0)}/晚")
        return "\n".join(lines)
    
    def _format_attraction_info(self, attraction_data: Dict[str, Any]) -> str:
        """格式化景点信息"""
        if not attraction_data or not attraction_data.get("attractions"):
            return "暂无景点信息"
        
        attractions = attraction_data.get("attractions", [])
        lines = []
        for a in attractions:
            lines.append(f"{a.get('name', '')} - {a.get('category', '')} - 门票¥{a.get('ticket_price', 0)}")
        return "\n".join(lines)

