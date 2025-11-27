"""
智能体基类
"""
from abc import ABC, abstractmethod
from typing import Any, Dict
from langchain_core.language_models import BaseChatModel
from langchain.prompts import ChatPromptTemplate
from loguru import logger


class BaseAgent(ABC):
    """智能体基类"""
    
    def __init__(self, llm: BaseChatModel, agent_name: str):
        """
        初始化智能体
        
        Args:
            llm: 语言模型
            agent_name: 智能体名称
        """
        self.llm = llm
        self.agent_name = agent_name
        self.prompt_template = self._create_prompt_template()
        
    @abstractmethod
    def _create_prompt_template(self) -> ChatPromptTemplate:
        """创建提示词模板"""
        pass
    
    @abstractmethod
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理输入数据
        
        Args:
            input_data: 输入数据
            
        Returns:
            处理结果
        """
        pass
    
    def log_info(self, message: str):
        """记录信息日志"""
        logger.info(f"[{self.agent_name}] {message}")
    
    def log_error(self, message: str, error: Exception = None):
        """记录错误日志"""
        if error:
            logger.error(f"[{self.agent_name}] {message}: {str(error)}")
        else:
            logger.error(f"[{self.agent_name}] {message}")
    
    async def invoke_llm(self, **kwargs) -> str:
        """
        调用LLM
        
        Args:
            **kwargs: 提示词模板参数
            
        Returns:
            LLM响应
        """
        try:
            prompt = self.prompt_template.format_messages(**kwargs)
            response = await self.llm.ainvoke(prompt)
            return response.content
        except Exception as e:
            self.log_error(f"LLM调用失败", e)
            raise

