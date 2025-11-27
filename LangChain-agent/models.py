"""
数据模型定义
"""
from datetime import datetime, date
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum


# ==================== 枚举类型 ====================

class IntentType(str, Enum):
    """意图类型"""
    FLIGHT = "flight"  # 机票查询
    HOTEL = "hotel"  # 酒店查询
    ATTRACTION = "attraction"  # 景点推荐
    ITINERARY = "itinerary"  # 行程规划
    PRICE_COMPARE = "price_compare"  # 价格对比
    BOOKING = "booking"  # 预订
    CUSTOMER_SERVICE = "customer_service"  # 客服咨询


class CabinClass(str, Enum):
    """舱位等级"""
    ECONOMY = "economy"  # 经济舱
    BUSINESS = "business"  # 商务舱
    FIRST = "first"  # 头等舱


class HotelStarRating(str, Enum):
    """酒店星级"""
    THREE_STAR = "3star"
    FOUR_STAR = "4star"
    FIVE_STAR = "5star"
    LUXURY = "luxury"


class OrderStatus(str, Enum):
    """订单状态"""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"


# ==================== 请求模型 ====================

class TravelRequest(BaseModel):
    """旅行查询请求"""
    query: str = Field(..., description="用户的自然语言查询")
    user_id: Optional[str] = Field(None, description="用户ID")
    session_id: Optional[str] = Field(None, description="会话ID")


# ==================== 意图解析 ====================

class ParsedIntent(BaseModel):
    """解析后的意图"""
    intent_type: IntentType = Field(..., description="意图类型")
    departure: Optional[str] = Field(None, description="出发地")
    destination: Optional[str] = Field(None, description="目的地")
    departure_date: Optional[date] = Field(None, description="出发日期")
    return_date: Optional[date] = Field(None, description="返程日期")
    passengers: int = Field(1, description="乘客数量")
    budget: Optional[float] = Field(None, description="预算")
    preferences: List[str] = Field(default_factory=list, description="偏好标签")
    extra_info: Dict[str, Any] = Field(default_factory=dict, description="额外信息")


# ==================== 机票相关 ====================

class Flight(BaseModel):
    """航班信息"""
    flight_id: str = Field(..., description="航班ID")
    airline: str = Field(..., description="航空公司")
    flight_number: str = Field(..., description="航班号")
    departure_city: str = Field(..., description="出发城市")
    arrival_city: str = Field(..., description="到达城市")
    departure_airport: str = Field(..., description="出发机场")
    arrival_airport: str = Field(..., description="到达机场")
    departure_time: datetime = Field(..., description="起飞时间")
    arrival_time: datetime = Field(..., description="到达时间")
    duration: str = Field(..., description="飞行时长")
    cabin_class: CabinClass = Field(..., description="舱位等级")
    price: float = Field(..., description="价格")
    available_seats: int = Field(..., description="余票数量")
    stops: int = Field(0, description="经停次数")


class FlightSearchResult(BaseModel):
    """航班搜索结果"""
    flights: List[Flight] = Field(default_factory=list, description="航班列表")
    total_count: int = Field(0, description="总数量")
    search_params: Dict[str, Any] = Field(default_factory=dict, description="搜索参数")


# ==================== 酒店相关 ====================

class Hotel(BaseModel):
    """酒店信息"""
    hotel_id: str = Field(..., description="酒店ID")
    name: str = Field(..., description="酒店名称")
    star_rating: HotelStarRating = Field(..., description="星级")
    address: str = Field(..., description="地址")
    city: str = Field(..., description="城市")
    price_per_night: float = Field(..., description="每晚价格")
    available_rooms: int = Field(..., description="可用房间数")
    room_type: str = Field(..., description="房型")
    facilities: List[str] = Field(default_factory=list, description="设施")
    rating: float = Field(..., description="评分")
    reviews_count: int = Field(0, description="评论数")
    distance_to_center: float = Field(..., description="距离市中心距离(km)")


class HotelSearchResult(BaseModel):
    """酒店搜索结果"""
    hotels: List[Hotel] = Field(default_factory=list, description="酒店列表")
    total_count: int = Field(0, description="总数量")
    search_params: Dict[str, Any] = Field(default_factory=dict, description="搜索参数")


# ==================== 景点相关 ====================

class Attraction(BaseModel):
    """景点信息"""
    attraction_id: str = Field(..., description="景点ID")
    name: str = Field(..., description="景点名称")
    city: str = Field(..., description="城市")
    category: str = Field(..., description="类别")
    description: str = Field(..., description="描述")
    address: str = Field(default="", description="地址")
    opening_hours: str = Field(..., description="开放时间")
    ticket_price: float = Field(..., description="门票价格")
    rating: float = Field(..., description="评分")
    visit_duration: str = Field(..., description="建议游玩时长")
    tags: List[str] = Field(default_factory=list, description="标签")


class AttractionRecommendation(BaseModel):
    """景点推荐结果"""
    attractions: List[Attraction] = Field(default_factory=list, description="景点列表")
    total_count: int = Field(0, description="总数量")
    recommendation_reason: str = Field("", description="推荐理由")


# ==================== 行程规划 ====================

class ItineraryDay(BaseModel):
    """单日行程"""
    day: int = Field(..., description="第几天")
    travel_date: date = Field(..., description="日期")
    morning: List[str] = Field(default_factory=list, description="上午安排")
    afternoon: List[str] = Field(default_factory=list, description="下午安排")
    evening: List[str] = Field(default_factory=list, description="晚上安排")
    accommodation: Optional[str] = Field(None, description="住宿信息")
    transportation: Optional[str] = Field(None, description="交通信息")
    estimated_cost: float = Field(0.0, description="预计花费")


class Itinerary(BaseModel):
    """完整行程"""
    itinerary_id: str = Field(..., description="行程ID")
    title: str = Field(..., description="行程标题")
    destination: str = Field(..., description="目的地")
    start_date: date = Field(..., description="开始日期")
    end_date: date = Field(..., description="结束日期")
    days: List[ItineraryDay] = Field(default_factory=list, description="每日行程")
    total_cost: float = Field(0.0, description="总费用")
    summary: str = Field("", description="行程总结")


# ==================== 价格对比 ====================

class PriceComparison(BaseModel):
    """价格对比"""
    product_id: str = Field(..., description="产品ID")
    product_name: str = Field(..., description="产品名称")
    product_type: str = Field(..., description="产品类型")
    prices: Dict[str, float] = Field(default_factory=dict, description="各平台价格")
    lowest_price: float = Field(..., description="最低价格")
    lowest_platform: str = Field(..., description="最低价平台")
    price_difference: float = Field(0.0, description="价格差")


# ==================== 订单相关 ====================

class Order(BaseModel):
    """订单信息"""
    order_id: str = Field(..., description="订单ID")
    user_id: str = Field(..., description="用户ID")
    product_type: str = Field(..., description="产品类型")
    product_id: str = Field(..., description="产品ID")
    product_name: str = Field(..., description="产品名称")
    quantity: int = Field(1, description="数量")
    total_price: float = Field(..., description="总价")
    status: OrderStatus = Field(OrderStatus.PENDING, description="订单状态")
    created_at: datetime = Field(default_factory=datetime.now, description="创建时间")
    contact_info: Dict[str, str] = Field(default_factory=dict, description="联系信息")


# ==================== 智能体响应 ====================

class AgentResponse(BaseModel):
    """智能体响应"""
    agent_name: str = Field(..., description="智能体名称")
    success: bool = Field(True, description="是否成功")
    data: Any = Field(None, description="响应数据")
    message: str = Field("", description="消息")
    error: Optional[str] = Field(None, description="错误信息")


class FinalResponse(BaseModel):
    """最终响应"""
    success: bool = Field(True, description="是否成功")
    intent: Optional[ParsedIntent] = Field(None, description="解析的意图")
    results: List[AgentResponse] = Field(default_factory=list, description="各智能体结果")
    final_answer: str = Field("", description="最终答案")
    recommendations: List[str] = Field(default_factory=list, description="建议")

