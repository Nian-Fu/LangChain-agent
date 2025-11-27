"""
客服咨询智能体
职责：解答售后问题、特殊需求处理
"""
from typing import Dict, Any
from langchain.prompts import ChatPromptTemplate
from langchain_core.language_models import BaseChatModel
from .base_agent import BaseAgent


class CustomerServiceAgent(BaseAgent):
    """客服咨询智能体"""
    
    def __init__(self, llm: BaseChatModel):
        super().__init__(llm, "客服咨询智能体")
    
    def _create_prompt_template(self) -> ChatPromptTemplate:
        """创建提示词模板"""
        return ChatPromptTemplate.from_messages([
            ("system", """你是一个专业、友好的旅行客服助手。你的任务是解答用户的问题和处理特殊需求。

服务范围：
1. 订单相关问题（查询、修改、退改）
2. 产品咨询（航班、酒店、景点）
3. 退改政策说明
4. 特殊需求处理（儿童、老人、特殊饮食等）
5. 投诉建议
6. 紧急情况处理

服务原则：
- 态度友好、耐心
- 回答准确、专业
- 提供解决方案
- 维护用户权益

请根据用户问题，提供专业的回答和解决方案。"""),
            ("user", """用户问题：{question}

用户信息：
- 用户ID: {user_id}
- 相关订单: {order_id}

请提供专业的回答和解决方案。""")
        ])
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理客服咨询
        
        Args:
            input_data: 包含用户问题
            
        Returns:
            客服响应
        """
        question = input_data.get("question", "")
        user_id = input_data.get("user_id", "guest")
        order_id = input_data.get("order_id", "无")
        
        self.log_info(f"处理客服咨询: {question[:50]}...")
        
        try:
            # 调用LLM生成回答
            answer = await self.invoke_llm(
                question=question,
                user_id=user_id,
                order_id=order_id
            )
            
            self.log_info("客服咨询处理完成")
            
            return {
                "success": True,
                "answer": answer,
                "message": "问题已处理"
            }
            
        except Exception as e:
            self.log_error("客服咨询处理失败", e)
            return {
                "success": False,
                "error": f"客服咨询处理失败: {str(e)}",
                "answer": "抱歉，当前服务繁忙，请稍后再试或联系人工客服。"
            }

