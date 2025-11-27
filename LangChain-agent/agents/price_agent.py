"""
价格对比智能体
职责：跨平台（模拟）价格比对
"""
from typing import Dict, Any
from langchain.prompts import ChatPromptTemplate
from langchain_core.language_models import BaseChatModel
from .base_agent import BaseAgent
from models import PriceComparison
import random


class PriceCompareAgent(BaseAgent):
    """价格对比智能体"""
    
    def __init__(self, llm: BaseChatModel):
        super().__init__(llm, "价格对比智能体")
    
    def _create_prompt_template(self) -> ChatPromptTemplate:
        """创建提示词模板"""
        return ChatPromptTemplate.from_messages([
            ("system", """你是一个专业的价格分析助手。根据不同平台的价格对比，给出购买建议。

请分析：
1. 各平台价格差异
2. 最优价格平台
3. 价格差异原因（可能）
4. 购买建议

给出简洁专业的建议。"""),
            ("user", """价格对比信息：
产品: {product_name}
类型: {product_type}

各平台价格：
{prices_info}

最低价: ¥{lowest_price} ({lowest_platform})
价格差: ¥{price_difference}

请给出购买建议。""")
        ])
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        对比价格
        
        Args:
            input_data: 包含产品信息
            
        Returns:
            价格对比结果
        """
        product_id = input_data.get("product_id", "")
        product_name = input_data.get("product_name", "")
        product_type = input_data.get("product_type", "")
        base_price = input_data.get("base_price", 1000.0)
        
        self.log_info(f"对比价格: {product_name} ({product_type})")
        
        try:
            # 模拟跨平台价格对比
            comparison = self._compare_prices(product_id, product_name, product_type, base_price)
            
            # 格式化价格信息
            prices_info = "\n".join([f"{platform}: ¥{price}" 
                                    for platform, price in comparison.prices.items()])
            
            # 调用LLM生成建议
            suggestion = await self.invoke_llm(
                product_name=product_name,
                product_type=product_type,
                prices_info=prices_info,
                lowest_price=comparison.lowest_price,
                lowest_platform=comparison.lowest_platform,
                price_difference=comparison.price_difference
            )
            
            self.log_info(f"价格对比完成，最低价: ¥{comparison.lowest_price}")
            
            return {
                "success": True,
                "data": comparison.model_dump(),
                "suggestion": suggestion,
                "message": "价格对比完成"
            }
            
        except Exception as e:
            self.log_error("价格对比失败", e)
            return {
                "success": False,
                "error": f"价格对比失败: {str(e)}"
            }
    
    def _compare_prices(self, product_id: str, product_name: str, 
                       product_type: str, base_price: float) -> PriceComparison:
        """模拟跨平台价格对比"""
        platforms = ["携程", "飞猪", "去哪儿", "马蜂窝", "同程"]
        prices = {}
        
        # 生成各平台价格（基于基础价格浮动）
        for platform in platforms:
            price_variation = random.uniform(-0.15, 0.15)  # ±15%浮动
            price = round(base_price * (1 + price_variation), 2)
            prices[platform] = price
        
        # 找出最低价
        lowest_platform = min(prices, key=prices.get)
        lowest_price = prices[lowest_platform]
        highest_price = max(prices.values())
        price_difference = round(highest_price - lowest_price, 2)
        
        return PriceComparison(
            product_id=product_id,
            product_name=product_name,
            product_type=product_type,
            prices=prices,
            lowest_price=lowest_price,
            lowest_platform=lowest_platform,
            price_difference=price_difference
        )

