"""
机票查询智能体
职责：航班查询、比价、余票校验
"""
from typing import Dict, Any, List
from datetime import datetime, timedelta
from langchain.prompts import ChatPromptTemplate
from langchain_core.language_models import BaseChatModel
from .base_agent import BaseAgent
from models import Flight, FlightSearchResult, CabinClass
import random


class FlightQueryAgent(BaseAgent):
    """机票查询智能体"""
    
    def __init__(self, llm: BaseChatModel):
        super().__init__(llm, "机票查询智能体")
    
    def _create_prompt_template(self) -> ChatPromptTemplate:
        """创建提示词模板"""
        return ChatPromptTemplate.from_messages([
            ("system", """你是一个专业的机票查询助手。根据用户的航班搜索结果，提供专业的选择建议。

请分析航班列表，考虑：
1. 价格因素
2. 飞行时长
3. 起飞/到达时间
4. 是否直飞
5. 余票情况

给出简洁专业的建议。"""),
            ("user", """航班搜索参数：
出发地: {departure}
目的地: {destination}
出发日期: {departure_date}
乘客数量: {passengers}

找到以下航班：
{flights_info}

请给出选择建议。""")
        ])
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        查询航班信息
        
        Args:
            input_data: 包含航班搜索参数
            
        Returns:
            航班搜索结果
        """
        departure = input_data.get("departure", "")
        destination = input_data.get("destination", "")
        departure_date = input_data.get("departure_date", "")
        passengers = input_data.get("passengers", 1)
        
        self.log_info(f"查询航班: {departure} -> {destination}, {departure_date}")
        
        try:
            # 模拟查询航班数据
            flights = self._search_flights(departure, destination, departure_date, passengers)
            
            # 生成航班信息摘要
            flights_info = self._format_flights_info(flights)
            
            # 调用LLM生成建议
            suggestion = await self.invoke_llm(
                departure=departure,
                destination=destination,
                departure_date=departure_date,
                passengers=passengers,
                flights_info=flights_info
            )
            
            result = FlightSearchResult(
                flights=flights,
                total_count=len(flights),
                search_params={
                    "departure": departure,
                    "destination": destination,
                    "departure_date": departure_date,
                    "passengers": passengers
                }
            )
            
            self.log_info(f"找到 {len(flights)} 个航班")
            
            return {
                "success": True,
                "data": result.model_dump(),
                "suggestion": suggestion,
                "message": f"找到 {len(flights)} 个航班"
            }
            
        except Exception as e:
            self.log_error("航班查询失败", e)
            return {
                "success": False,
                "error": f"航班查询失败: {str(e)}"
            }
    
    def _search_flights(self, departure: str, destination: str, 
                       departure_date: str, passengers: int) -> List[Flight]:
        """模拟查询航班数据"""
        flights = []
        airlines = ["中国国际航空", "东方航空", "南方航空", "海南航空", "吉祥航空"]
        
        # 生成3-5个模拟航班
        for i in range(random.randint(3, 5)):
            airline = random.choice(airlines)
            flight_number = f"{airline[:2]}{random.randint(1000, 9999)}"
            
            # 解析日期
            dep_date = datetime.strptime(departure_date, "%Y-%m-%d")
            # 随机起飞时间
            dep_hour = random.randint(6, 22)
            dep_time = dep_date.replace(hour=dep_hour, minute=random.randint(0, 59))
            
            # 飞行时长 2-8小时
            duration_hours = random.randint(2, 8)
            arr_time = dep_time + timedelta(hours=duration_hours, minutes=random.randint(0, 59))
            
            # 随机舱位
            cabin_class = random.choice([CabinClass.ECONOMY, CabinClass.BUSINESS, CabinClass.FIRST])
            
            # 价格根据舱位设定
            base_price = random.randint(800, 2000)
            if cabin_class == CabinClass.BUSINESS:
                base_price *= 2.5
            elif cabin_class == CabinClass.FIRST:
                base_price *= 4
            
            flight = Flight(
                flight_id=f"FL{random.randint(10000, 99999)}",
                airline=airline,
                flight_number=flight_number,
                departure_city=departure,
                arrival_city=destination,
                departure_airport=f"{departure}国际机场",
                arrival_airport=f"{destination}国际机场",
                departure_time=dep_time,
                arrival_time=arr_time,
                duration=f"{duration_hours}小时{random.randint(0, 59)}分钟",
                cabin_class=cabin_class,
                price=round(base_price, 2),
                available_seats=random.randint(5, 200),
                stops=0 if random.random() > 0.3 else 1
            )
            flights.append(flight)
        
        # 按价格排序
        flights.sort(key=lambda x: x.price)
        return flights
    
    def _format_flights_info(self, flights: List[Flight]) -> str:
        """格式化航班信息"""
        info_lines = []
        for i, flight in enumerate(flights, 1):
            stops_text = "直飞" if flight.stops == 0 else f"{flight.stops}次经停"
            info_lines.append(
                f"{i}. {flight.airline} {flight.flight_number} - "
                f"¥{flight.price} - {flight.departure_time.strftime('%H:%M')}-"
                f"{flight.arrival_time.strftime('%H:%M')} - {flight.duration} - "
                f"{stops_text} - {flight.cabin_class.value} - 余票{flight.available_seats}"
            )
        return "\n".join(info_lines)

