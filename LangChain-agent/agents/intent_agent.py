"""
意图解析智能体
职责：识别用户旅行需求类型（机票/酒店/行程等）
"""
import json
from typing import Dict, Any
from langchain.prompts import ChatPromptTemplate
from langchain_core.language_models import BaseChatModel
from .base_agent import BaseAgent
from models import ParsedIntent, IntentType


class IntentParseAgent(BaseAgent):
    """意图解析智能体"""
    
    def __init__(self, llm: BaseChatModel):
        super().__init__(llm, "意图解析智能体")
    
    def _create_prompt_template(self) -> ChatPromptTemplate:
        """创建提示词模板"""
        return ChatPromptTemplate.from_messages([
            ("system", """你是一个专业的旅行意图识别助手。你的任务是从用户的自然语言查询中提取关键信息。

意图类型：
- flight: 机票查询
- hotel: 酒店查询
- attraction: 景点推荐
- itinerary: 行程规划
- price_compare: 价格对比
- booking: 预订
- customer_service: 客服咨询

请从用户查询中提取以下信息（如果有）：
- intent_type: 意图类型
- departure: 出发地
- destination: 目的地
- departure_date: 出发日期 (格式: YYYY-MM-DD)
- return_date: 返程日期 (格式: YYYY-MM-DD)
- passengers: 乘客数量
- budget: 预算
- preferences: 偏好标签列表
- extra_info: 其他额外信息

请以JSON格式返回结果，不要包含任何其他文字说明。"""),
            ("user", "用户查询：{query}")
        ])
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        解析用户意图
        
        Args:
            input_data: 包含 'query' 字段的字典
            
        Returns:
            解析后的意图信息
        """
        query = input_data.get("query", "")
        self.log_info(f"开始解析用户意图: {query}")
        
        try:
            # 调用LLM解析意图
            response = await self.invoke_llm(query=query)
            
            # 解析JSON响应
            # 清理可能的markdown代码块标记
            response = response.strip()
            if response.startswith("```json"):
                response = response[7:]
            if response.startswith("```"):
                response = response[3:]
            if response.endswith("```"):
                response = response[:-3]
            response = response.strip()
            
            intent_data = json.loads(response)
            
            # 验证并规范化数据
            parsed_intent = ParsedIntent(**intent_data)
            
            self.log_info(f"意图解析成功: {parsed_intent.intent_type}")
            
            return {
                "success": True,
                "intent": parsed_intent.model_dump(),
                "message": "意图解析成功"
            }
            
        except json.JSONDecodeError as e:
            self.log_error("JSON解析失败", e)
            return {
                "success": False,
                "error": f"意图解析失败: JSON格式错误",
                "raw_response": response
            }
        except Exception as e:
            self.log_error("意图解析失败", e)
            return {
                "success": False,
                "error": f"意图解析失败: {str(e)}"
            }

