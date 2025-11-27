"""
景点推荐智能体
职责：基于目的地和偏好推荐景点
"""
from typing import Dict, Any, List
from langchain.prompts import ChatPromptTemplate
from langchain_core.language_models import BaseChatModel
from .base_agent import BaseAgent
from models import Attraction, AttractionRecommendation
import random


class AttractionRecommendAgent(BaseAgent):
    """景点推荐智能体"""
    
    def __init__(self, llm: BaseChatModel):
        super().__init__(llm, "景点推荐智能体")
    
    def _create_prompt_template(self) -> ChatPromptTemplate:
        """创建提示词模板"""
        return ChatPromptTemplate.from_messages([
            ("system", """你是一个专业的旅游景点推荐助手。根据用户的目的地和偏好，推荐合适的景点。

请分析景点列表，考虑：
1. 景点类型与用户偏好匹配度
2. 评分和口碑
3. 门票价格
4. 建议游玩时长
5. 景点间的地理位置关系

给出专业的推荐理由和游玩建议。"""),
            ("user", """推荐参数：
目的地: {destination}
旅行天数: {days}
兴趣偏好: {preferences}

景点列表：
{attractions_info}

请给出推荐理由和游玩建议。""")
        ])
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        推荐景点
        
        Args:
            input_data: 包含景点推荐参数
            
        Returns:
            景点推荐结果
        """
        destination = input_data.get("destination", "")
        preferences = input_data.get("preferences", [])
        days = input_data.get("days", 3)
        
        self.log_info(f"推荐景点: {destination}, 偏好: {preferences}")
        
        try:
            # 模拟查询景点数据
            attractions = self._recommend_attractions(destination, preferences, days)
            
            # 生成景点信息摘要
            attractions_info = self._format_attractions_info(attractions)
            
            # 调用LLM生成推荐理由
            recommendation_reason = await self.invoke_llm(
                destination=destination,
                days=days,
                preferences=", ".join(preferences) if preferences else "综合推荐",
                attractions_info=attractions_info
            )
            
            result = AttractionRecommendation(
                attractions=attractions,
                total_count=len(attractions),
                recommendation_reason=recommendation_reason
            )
            
            self.log_info(f"推荐 {len(attractions)} 个景点")
            
            return {
                "success": True,
                "data": result.model_dump(),
                "message": f"推荐 {len(attractions)} 个景点"
            }
            
        except Exception as e:
            self.log_error("景点推荐失败", e)
            return {
                "success": False,
                "error": f"景点推荐失败: {str(e)}"
            }
    
    def _recommend_attractions(self, destination: str, preferences: List[str], 
                              days: int) -> List[Attraction]:
        """模拟推荐景点"""
        attractions = []
        
        # 各城市的著名景点数据库
        famous_attractions = {
            "北京": [
                {"name": "故宫博物院", "category": "历史文化", "desc": "世界上现存规模最大、保存最完整的古代皇宫建筑群", "price": 60, "hours": "08:30-17:00"},
                {"name": "长城", "category": "历史文化", "desc": "世界七大奇迹之一，中华民族的象征", "price": 40, "hours": "07:00-18:00"},
                {"name": "颐和园", "category": "自然风光", "desc": "中国现存规模最大、保存最完整的皇家园林", "price": 30, "hours": "06:30-18:00"},
                {"name": "天坛公园", "category": "历史文化", "desc": "明清两代皇帝祭祀皇天上帝的场所", "price": 15, "hours": "06:00-22:00"},
                {"name": "圆明园", "category": "历史文化", "desc": "被誉为万园之园的皇家园林", "price": 25, "hours": "07:00-19:00"}
            ],
            "上海": [
                {"name": "外滩", "category": "历史文化", "desc": "上海的标志性景点，万国建筑博览群", "price": 0, "hours": "全天开放"},
                {"name": "东方明珠", "category": "现代建筑", "desc": "上海的标志性建筑，亚洲第一高塔", "price": 220, "hours": "08:00-22:00"},
                {"name": "豫园", "category": "历史文化", "desc": "江南古典园林的代表作", "price": 40, "hours": "08:30-17:30"},
                {"name": "上海迪士尼乐园", "category": "主题乐园", "desc": "中国大陆首座迪士尼主题乐园", "price": 399, "hours": "09:00-21:00"},
                {"name": "田子坊", "category": "文化街区", "desc": "上海特色的石库门建筑群", "price": 0, "hours": "10:00-22:00"}
            ],
            "杭州": [
                {"name": "西湖", "category": "自然风光", "desc": "中国著名的风景名胜，世界文化遗产", "price": 0, "hours": "全天开放"},
                {"name": "灵隐寺", "category": "宗教建筑", "desc": "中国佛教著名寺院，江南禅宗五山之一", "price": 75, "hours": "07:00-18:00"},
                {"name": "西溪湿地", "category": "自然风光", "desc": "中国首个国家湿地公园", "price": 80, "hours": "08:30-17:30"},
                {"name": "宋城", "category": "主题乐园", "desc": "展示宋朝文化的大型主题公园", "price": 320, "hours": "10:00-21:00"},
                {"name": "千岛湖", "category": "自然风光", "desc": "中国最美的人工湖泊之一", "price": 150, "hours": "08:00-17:00"}
            ]
        }
        
        # 如果目的地在数据库中，使用真实数据
        if destination in famous_attractions:
            attraction_data = famous_attractions[destination]
            num_attractions = min(days * 2, len(attraction_data))
            selected_attractions = random.sample(attraction_data, num_attractions)
            
            for i, attr_data in enumerate(selected_attractions):
                attraction = Attraction(
                    attraction_id=f"AT{random.randint(10000, 99999)}",
                    name=attr_data["name"],
                    city=destination,
                    category=attr_data["category"],
                    description=attr_data["desc"],
                    address=f"{destination}市{random.choice(['朝阳区', '海淀区', '东城区', '黄浦区', '浦东新区', '西湖区'])}{attr_data['name']}",
                    opening_hours=attr_data["hours"],
                    ticket_price=attr_data["price"],
                    rating=round(random.uniform(4.5, 5.0), 1),
                    visit_duration=f"{random.randint(2, 5)}小时",
                    tags=[attr_data["category"], "热门", "必游", "4A景区"]
                )
                attractions.append(attraction)
        else:
            # 使用通用模拟数据
            categories = ["历史文化", "自然风光", "主题乐园", "博物馆", "购物中心", "美食街区", "宗教建筑"]
            selected_categories = categories if not preferences else [cat for cat in categories if any(pref in cat for pref in preferences)] or categories
            
            num_attractions = min(days * 2 + random.randint(0, days), 8)
            
            for i in range(num_attractions):
                category = random.choice(selected_categories)
                attraction_name = f"{destination}{category}景区"
                
                attraction = Attraction(
                    attraction_id=f"AT{random.randint(10000, 99999)}",
                    name=attraction_name,
                    city=destination,
                    category=category,
                    description=f"这是{destination}著名的{category}景点，融合了当地特色文化，深受游客喜爱。景区设施完善，风景优美，是休闲旅游的好去处。",
                    address=f"{destination}市{random.choice(['中心区', '新区', '开发区'])}{random.choice(['文化路', '旅游路', '风景路'])}{random.randint(1, 999)}号",
                    opening_hours=f"{random.randint(7, 9)}:00-{random.randint(17, 19)}:00",
                    ticket_price=round(random.uniform(0, 180), 2),
                    rating=round(random.uniform(4.0, 5.0), 1),
                    visit_duration=f"{random.randint(1, 4)}小时",
                    tags=[category, "热门推荐"] if random.random() > 0.5 else [category]
                )
                attractions.append(attraction)
        
        # 按评分排序
        attractions.sort(key=lambda x: x.rating, reverse=True)
        return attractions
    
    def _format_attractions_info(self, attractions: List[Attraction]) -> str:
        """格式化景点信息"""
        info_lines = []
        for i, attr in enumerate(attractions, 1):
            info_lines.append(
                f"{i}. {attr.name} - {attr.category} - "
                f"门票¥{attr.ticket_price} - 评分{attr.rating} - "
                f"建议游玩{attr.visit_duration} - {attr.opening_hours}"
            )
        return "\n".join(info_lines)

