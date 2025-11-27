"""
LangGraph 工作流编排
多智能体协作流程
"""
from typing import TypedDict, Annotated, Sequence
from langgraph.graph import StateGraph, END
from langchain_community.chat_models import ChatTongyi
from config import settings
from agents import (
    IntentParseAgent,
    FlightQueryAgent,
    HotelQueryAgent,
    AttractionRecommendAgent,
    ItineraryPlanAgent,
    PriceCompareAgent,
    BookingAgent,
    CustomerServiceAgent
)
from models import IntentType
from loguru import logger


# ==================== 状态定义 ====================

class AgentState(TypedDict):
    """智能体工作流状态"""
    # 输入
    query: str  # 用户查询
    user_id: str  # 用户ID
    session_id: str  # 会话ID
    
    # 意图解析结果
    intent: dict  # 解析的意图
    intent_type: str  # 意图类型
    
    # 各智能体的结果
    flight_result: dict  # 机票查询结果
    hotel_result: dict  # 酒店查询结果
    attraction_result: dict  # 景点推荐结果
    itinerary_result: dict  # 行程规划结果
    price_result: dict  # 价格对比结果
    booking_result: dict  # 预订结果
    service_result: dict  # 客服结果
    
    # 最终输出
    final_answer: str  # 最终答案
    recommendations: list  # 建议列表
    error: str  # 错误信息


# ==================== 节点函数 ====================

class TravelAgentWorkflow:
    """旅行智能体工作流"""
    
    def __init__(self):
        """初始化工作流"""
        # 初始化LLM
        self.llm = ChatTongyi(
            model_name=settings.LLM_MODEL,
            temperature=settings.LLM_TEMPERATURE,
            max_tokens=settings.LLM_MAX_TOKENS,
            dashscope_api_key=settings.DASHSCOPE_API_KEY
        )
        
        # 初始化智能体
        self.intent_agent = IntentParseAgent(self.llm)
        self.flight_agent = FlightQueryAgent(self.llm)
        self.hotel_agent = HotelQueryAgent(self.llm)
        self.attraction_agent = AttractionRecommendAgent(self.llm)
        self.itinerary_agent = ItineraryPlanAgent(self.llm)
        self.price_agent = PriceCompareAgent(self.llm)
        self.booking_agent = BookingAgent(self.llm)
        self.service_agent = CustomerServiceAgent(self.llm)
        
        # 构建工作流图
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """构建工作流图"""
        workflow = StateGraph(AgentState)
        
        # 添加节点
        workflow.add_node("parse_intent", self.parse_intent_node)
        workflow.add_node("query_flight", self.query_flight_node)
        workflow.add_node("query_hotel", self.query_hotel_node)
        workflow.add_node("recommend_attraction", self.recommend_attraction_node)
        workflow.add_node("plan_itinerary", self.plan_itinerary_node)
        workflow.add_node("compare_price", self.compare_price_node)
        workflow.add_node("handle_booking", self.handle_booking_node)
        workflow.add_node("customer_service", self.customer_service_node)
        workflow.add_node("generate_answer", self.generate_answer_node)
        
        # 设置入口点
        workflow.set_entry_point("parse_intent")
        
        # 添加条件边：根据意图类型路由
        workflow.add_conditional_edges(
            "parse_intent",
            self.route_by_intent,
            {
                "flight": "query_flight",
                "hotel": "query_hotel",
                "attraction": "recommend_attraction",
                "itinerary": "query_flight",  # 行程规划需要先查询交通和酒店
                "price_compare": "compare_price",
                "booking": "handle_booking",
                "customer_service": "customer_service",
                "end": "generate_answer"
            }
        )
        
        # 机票查询后的路由
        workflow.add_conditional_edges(
            "query_flight",
            self.route_after_flight,
            {
                "itinerary": "query_hotel",  # 继续查询酒店
                "price_compare": "compare_price",
                "end": "generate_answer"
            }
        )
        
        # 酒店查询后的路由
        workflow.add_conditional_edges(
            "query_hotel",
            self.route_after_hotel,
            {
                "itinerary": "recommend_attraction",  # 继续推荐景点
                "price_compare": "compare_price",
                "end": "generate_answer"
            }
        )
        
        # 景点推荐后的路由
        workflow.add_conditional_edges(
            "recommend_attraction",
            self.route_after_attraction,
            {
                "itinerary": "plan_itinerary",
                "end": "generate_answer"
            }
        )
        
        # 其他节点直接到生成答案
        workflow.add_edge("plan_itinerary", "generate_answer")
        workflow.add_edge("compare_price", "generate_answer")
        workflow.add_edge("handle_booking", "generate_answer")
        workflow.add_edge("customer_service", "generate_answer")
        
        # 生成答案后结束
        workflow.add_edge("generate_answer", END)
        
        return workflow.compile()
    
    # ==================== 节点处理函数 ====================
    
    async def parse_intent_node(self, state: AgentState) -> AgentState:
        """意图解析节点"""
        logger.info("执行意图解析节点")
        result = await self.intent_agent.process({"query": state["query"]})
        
        if result["success"]:
            state["intent"] = result["intent"]
            state["intent_type"] = result["intent"]["intent_type"]
        else:
            state["error"] = result.get("error", "意图解析失败")
            state["intent_type"] = "customer_service"  # 失败时转到客服
        
        return state
    
    async def query_flight_node(self, state: AgentState) -> AgentState:
        """机票查询节点"""
        logger.info("执行机票查询节点")
        intent = state.get("intent", {})
        result = await self.flight_agent.process(intent)
        state["flight_result"] = result
        return state
    
    async def query_hotel_node(self, state: AgentState) -> AgentState:
        """酒店查询节点"""
        logger.info("执行酒店查询节点")
        intent = state.get("intent", {})
        result = await self.hotel_agent.process(intent)
        state["hotel_result"] = result
        return state
    
    async def recommend_attraction_node(self, state: AgentState) -> AgentState:
        """景点推荐节点"""
        logger.info("执行景点推荐节点")
        intent = state.get("intent", {})
        result = await self.attraction_agent.process(intent)
        state["attraction_result"] = result
        return state
    
    async def plan_itinerary_node(self, state: AgentState) -> AgentState:
        """行程规划节点"""
        logger.info("执行行程规划节点")
        intent = state.get("intent", {})
        
        # 整合之前的结果
        input_data = intent.copy()
        if state.get("flight_result"):
            input_data["flight_data"] = state["flight_result"].get("data", {})
        if state.get("hotel_result"):
            input_data["hotel_data"] = state["hotel_result"].get("data", {})
        if state.get("attraction_result"):
            input_data["attraction_data"] = state["attraction_result"].get("data", {})
        
        result = await self.itinerary_agent.process(input_data)
        state["itinerary_result"] = result
        return state
    
    async def compare_price_node(self, state: AgentState) -> AgentState:
        """价格对比节点"""
        logger.info("执行价格对比节点")
        
        # 从已有结果中获取产品信息
        product_info = {}
        if state.get("flight_result") and state["flight_result"].get("data"):
            flights = state["flight_result"]["data"].get("flights", [])
            if flights:
                flight = flights[0]
                product_info = {
                    "product_id": flight["flight_id"],
                    "product_name": f"{flight['airline']} {flight['flight_number']}",
                    "product_type": "flight",
                    "base_price": flight["price"]
                }
        elif state.get("hotel_result") and state["hotel_result"].get("data"):
            hotels = state["hotel_result"]["data"].get("hotels", [])
            if hotels:
                hotel = hotels[0]
                product_info = {
                    "product_id": hotel["hotel_id"],
                    "product_name": hotel["name"],
                    "product_type": "hotel",
                    "base_price": hotel["price_per_night"]
                }
        
        if product_info:
            result = await self.price_agent.process(product_info)
            state["price_result"] = result
        
        return state
    
    async def handle_booking_node(self, state: AgentState) -> AgentState:
        """预订处理节点"""
        logger.info("执行预订处理节点")
        intent = state.get("intent", {})
        
        # 从意图中提取预订信息
        booking_data = {
            "action": "create",
            "user_id": state.get("user_id", "guest"),
            "product_type": "travel",
            "product_id": intent.get("extra_info", {}).get("product_id", "UNKNOWN"),
            "product_name": intent.get("extra_info", {}).get("product_name", "旅行产品"),
            "quantity": intent.get("passengers", 1),
            "total_price": intent.get("extra_info", {}).get("price", 1000.0),
            "contact_info": intent.get("extra_info", {}).get("contact_info", {})
        }
        
        result = await self.booking_agent.process(booking_data)
        state["booking_result"] = result
        return state
    
    async def customer_service_node(self, state: AgentState) -> AgentState:
        """客服咨询节点"""
        logger.info("执行客服咨询节点")
        
        service_data = {
            "question": state["query"],
            "user_id": state.get("user_id", "guest"),
            "order_id": state.get("intent", {}).get("extra_info", {}).get("order_id", "无")
        }
        
        result = await self.service_agent.process(service_data)
        state["service_result"] = result
        return state
    
    async def generate_answer_node(self, state: AgentState) -> AgentState:
        """生成最终答案节点"""
        logger.info("执行生成答案节点")
        
        # 收集所有结果
        answer_parts = []
        recommendations = []
        
        intent_type = state.get("intent_type", "")
        
        # 根据意图类型组织答案
        if intent_type == IntentType.FLIGHT and state.get("flight_result"):
            result = state["flight_result"]
            if result.get("success"):
                data = result["data"]
                answer_parts.append(f"为您找到了 {data['total_count']} 个航班选项。")
                answer_parts.append(f"\n建议：{result.get('suggestion', '')}")
                recommendations.append("点击查看详细航班信息")
        
        elif intent_type == IntentType.HOTEL and state.get("hotel_result"):
            result = state["hotel_result"]
            if result.get("success"):
                data = result["data"]
                answer_parts.append(f"为您找到了 {data['total_count']} 家酒店。")
                answer_parts.append(f"\n建议：{result.get('suggestion', '')}")
                recommendations.append("点击查看详细酒店信息")
        
        elif intent_type == IntentType.ATTRACTION and state.get("attraction_result"):
            result = state["attraction_result"]
            if result.get("success"):
                data = result["data"]
                answer_parts.append(f"为您推荐了 {data['total_count']} 个景点。")
                answer_parts.append(f"\n推荐理由：{data.get('recommendation_reason', '')}")
                recommendations.append("点击查看景点详情")
        
        elif intent_type == IntentType.ITINERARY and state.get("itinerary_result"):
            result = state["itinerary_result"]
            if result.get("success"):
                data = result["data"]
                answer_parts.append(f"已为您规划 {data['title']}。")
                answer_parts.append(f"\n总费用约：¥{data['total_cost']}")
                answer_parts.append(f"\n行程总结：{data.get('summary', '')}")
                recommendations.append("点击查看完整行程")
        
        elif intent_type == IntentType.PRICE_COMPARE and state.get("price_result"):
            result = state["price_result"]
            if result.get("success"):
                data = result["data"]
                answer_parts.append(f"已完成价格对比。")
                answer_parts.append(f"\n最低价：¥{data['lowest_price']} ({data['lowest_platform']})")
                answer_parts.append(f"\n价格差：¥{data['price_difference']}")
                answer_parts.append(f"\n建议：{result.get('suggestion', '')}")
        
        elif intent_type == IntentType.BOOKING and state.get("booking_result"):
            result = state["booking_result"]
            if result.get("success"):
                data = result["data"]
                answer_parts.append(f"订单已创建成功！")
                answer_parts.append(f"\n订单号：{data['order_id']}")
                answer_parts.append(f"\n{result.get('confirmation', '')}")
                recommendations.append("查看订单详情")
        
        elif intent_type == IntentType.CUSTOMER_SERVICE and state.get("service_result"):
            result = state["service_result"]
            answer_parts.append(result.get("answer", ""))
        
        else:
            answer_parts.append("抱歉，暂时无法处理您的请求，请尝试换个方式描述。")
        
        state["final_answer"] = "".join(answer_parts)
        state["recommendations"] = recommendations
        
        return state
    
    # ==================== 路由函数 ====================
    
    def route_by_intent(self, state: AgentState) -> str:
        """根据意图类型路由"""
        intent_type = state.get("intent_type", "")
        logger.info(f"根据意图路由: {intent_type}")
        
        if intent_type == IntentType.FLIGHT:
            return "flight"
        elif intent_type == IntentType.HOTEL:
            return "hotel"
        elif intent_type == IntentType.ATTRACTION:
            return "attraction"
        elif intent_type == IntentType.ITINERARY:
            return "itinerary"
        elif intent_type == IntentType.PRICE_COMPARE:
            return "price_compare"
        elif intent_type == IntentType.BOOKING:
            return "booking"
        elif intent_type == IntentType.CUSTOMER_SERVICE:
            return "customer_service"
        else:
            return "end"
    
    def route_after_flight(self, state: AgentState) -> str:
        """机票查询后的路由"""
        intent_type = state.get("intent_type", "")
        if intent_type == IntentType.ITINERARY:
            return "itinerary"
        elif intent_type == IntentType.PRICE_COMPARE:
            return "price_compare"
        return "end"
    
    def route_after_hotel(self, state: AgentState) -> str:
        """酒店查询后的路由"""
        intent_type = state.get("intent_type", "")
        if intent_type == IntentType.ITINERARY:
            return "itinerary"
        elif intent_type == IntentType.PRICE_COMPARE:
            return "price_compare"
        return "end"
    
    def route_after_attraction(self, state: AgentState) -> str:
        """景点推荐后的路由"""
        intent_type = state.get("intent_type", "")
        if intent_type == IntentType.ITINERARY:
            return "itinerary"
        return "end"
    
    # ==================== 执行工作流 ====================
    
    async def run(self, query: str, user_id: str = "guest", 
                  session_id: str = None) -> dict:
        """
        运行工作流
        
        Args:
            query: 用户查询
            user_id: 用户ID
            session_id: 会话ID
            
        Returns:
            工作流执行结果
        """
        logger.info(f"开始执行工作流，查询: {query}")
        
        # 初始化状态
        initial_state = AgentState(
            query=query,
            user_id=user_id,
            session_id=session_id or f"session_{user_id}",
            intent={},
            intent_type="",
            flight_result={},
            hotel_result={},
            attraction_result={},
            itinerary_result={},
            price_result={},
            booking_result={},
            service_result={},
            final_answer="",
            recommendations=[],
            error=""
        )
        
        try:
            # 执行工作流
            final_state = await self.graph.ainvoke(initial_state)
            
            logger.info("工作流执行完成")
            
            return {
                "success": True,
                "query": query,
                "intent": final_state.get("intent"),
                "final_answer": final_state.get("final_answer"),
                "recommendations": final_state.get("recommendations", []),
                "results": {
                    "flight": final_state.get("flight_result"),
                    "hotel": final_state.get("hotel_result"),
                    "attraction": final_state.get("attraction_result"),
                    "itinerary": final_state.get("itinerary_result"),
                    "price": final_state.get("price_result"),
                    "booking": final_state.get("booking_result"),
                    "service": final_state.get("service_result")
                }
            }
        
        except Exception as e:
            logger.error(f"工作流执行失败: {str(e)}")
            return {
                "success": False,
                "error": f"工作流执行失败: {str(e)}",
                "query": query
            }


# ==================== 全局工作流实例 ====================

_workflow_instance = None


def get_workflow() -> TravelAgentWorkflow:
    """获取工作流实例（单例模式）"""
    global _workflow_instance
    if _workflow_instance is None:
        _workflow_instance = TravelAgentWorkflow()
    return _workflow_instance

