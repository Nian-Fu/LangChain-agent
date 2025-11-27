"""
预订执行智能体
职责：处理订单创建、确认、取消
"""
from typing import Dict, Any
from datetime import datetime
from langchain.prompts import ChatPromptTemplate
from langchain_core.language_models import BaseChatModel
from .base_agent import BaseAgent
from models import Order, OrderStatus
import random


class BookingAgent(BaseAgent):
    """预订执行智能体"""
    
    def __init__(self, llm: BaseChatModel):
        super().__init__(llm, "预订执行智能体")
    
    def _create_prompt_template(self) -> ChatPromptTemplate:
        """创建提示词模板"""
        return ChatPromptTemplate.from_messages([
            ("system", """你是一个专业的预订助手。根据用户的预订信息，生成确认信息和注意事项。

请提供：
1. 订单确认信息
2. 注意事项
3. 取消政策
4. 联系方式

语气友好专业。"""),
            ("user", """预订信息：
订单号: {order_id}
产品: {product_name}
类型: {product_type}
数量: {quantity}
总价: ¥{total_price}
状态: {status}

请生成确认信息和注意事项。""")
        ])
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理预订
        
        Args:
            input_data: 包含预订信息
            
        Returns:
            预订结果
        """
        action = input_data.get("action", "create")  # create, confirm, cancel
        
        if action == "create":
            return await self._create_order(input_data)
        elif action == "confirm":
            return await self._confirm_order(input_data)
        elif action == "cancel":
            return await self._cancel_order(input_data)
        else:
            return {
                "success": False,
                "error": f"不支持的操作: {action}"
            }
    
    async def _create_order(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """创建订单"""
        user_id = input_data.get("user_id", "guest")
        product_type = input_data.get("product_type", "")
        product_id = input_data.get("product_id", "")
        product_name = input_data.get("product_name", "")
        quantity = input_data.get("quantity", 1)
        total_price = input_data.get("total_price", 0.0)
        contact_info = input_data.get("contact_info", {})
        
        self.log_info(f"创建订单: {product_name}")
        
        try:
            # 生成订单
            order = Order(
                order_id=f"ORD{datetime.now().strftime('%Y%m%d%H%M%S')}{random.randint(1000, 9999)}",
                user_id=user_id,
                product_type=product_type,
                product_id=product_id,
                product_name=product_name,
                quantity=quantity,
                total_price=total_price,
                status=OrderStatus.PENDING,
                contact_info=contact_info
            )
            
            # 调用LLM生成确认信息
            confirmation = await self.invoke_llm(
                order_id=order.order_id,
                product_name=product_name,
                product_type=product_type,
                quantity=quantity,
                total_price=total_price,
                status="待确认"
            )
            
            self.log_info(f"订单创建成功: {order.order_id}")
            
            return {
                "success": True,
                "data": order.model_dump(),
                "confirmation": confirmation,
                "message": f"订单创建成功，订单号: {order.order_id}"
            }
            
        except Exception as e:
            self.log_error("订单创建失败", e)
            return {
                "success": False,
                "error": f"订单创建失败: {str(e)}"
            }
    
    async def _confirm_order(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """确认订单"""
        order_id = input_data.get("order_id", "")
        
        self.log_info(f"确认订单: {order_id}")
        
        try:
            # 模拟订单确认（实际应从数据库查询）
            confirmation = await self.invoke_llm(
                order_id=order_id,
                product_name="已确认的产品",
                product_type="travel",
                quantity=1,
                total_price=1000,
                status="已确认"
            )
            
            self.log_info(f"订单确认成功: {order_id}")
            
            return {
                "success": True,
                "order_id": order_id,
                "status": OrderStatus.CONFIRMED,
                "confirmation": confirmation,
                "message": "订单确认成功"
            }
            
        except Exception as e:
            self.log_error("订单确认失败", e)
            return {
                "success": False,
                "error": f"订单确认失败: {str(e)}"
            }
    
    async def _cancel_order(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """取消订单"""
        order_id = input_data.get("order_id", "")
        reason = input_data.get("reason", "用户取消")
        
        self.log_info(f"取消订单: {order_id}, 原因: {reason}")
        
        try:
            # 模拟订单取消
            self.log_info(f"订单取消成功: {order_id}")
            
            return {
                "success": True,
                "order_id": order_id,
                "status": OrderStatus.CANCELLED,
                "message": f"订单已取消，原因: {reason}"
            }
            
        except Exception as e:
            self.log_error("订单取消失败", e)
            return {
                "success": False,
                "error": f"订单取消失败: {str(e)}"
            }

