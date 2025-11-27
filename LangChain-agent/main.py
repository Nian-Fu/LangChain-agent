"""
FastAPI 主应用
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from loguru import logger
import sys

from config import settings
from database import init_database
from models import TravelRequest, FinalResponse
from workflow import get_workflow

# 配置日志
logger.remove()
logger.add(
    sys.stderr,
    level=settings.LOG_LEVEL,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>"
)
logger.add(
    "logs/app_{time:YYYY-MM-DD}.log",
    rotation="00:00",
    retention="30 days",
    level=settings.LOG_LEVEL,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function} - {message}"
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时执行
    logger.info("启动应用...")
    logger.info("初始化数据库...")
    await init_database()
    logger.info("初始化工作流...")
    get_workflow()
    logger.info("应用启动完成！")
    
    yield
    
    # 关闭时执行
    logger.info("关闭应用...")


# 创建FastAPI应用
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="基于LangChain、LangGraph和通义千问的多智能体旅行平台",
    lifespan=lifespan
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==================== API 端点 ====================

@app.get("/")
async def root():
    """根路径"""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "description": "携程式多智能体旅行平台"
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION
    }


@app.post("/api/v1/travel/query")
async def travel_query(request: TravelRequest):
    """
    旅行查询接口
    
    支持的查询类型：
    - 机票查询
    - 酒店查询
    - 景点推荐
    - 行程规划
    - 价格对比
    - 预订
    - 客服咨询
    """
    try:
        logger.info(f"收到查询请求: {request.query}")
        
        # 获取工作流实例
        workflow = get_workflow()
        
        # 执行工作流
        result = await workflow.run(
            query=request.query,
            user_id=request.user_id or "guest",
            session_id=request.session_id
        )
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result.get("error", "查询失败"))
        
        # 构建完整响应，包含所有智能体的结果
        response = {
            "success": True,
            "query": request.query,
            "intent": result.get("intent"),
            "intent_type": result.get("intent", {}).get("intent_type"),
            "final_answer": result.get("final_answer", ""),
            "recommendations": result.get("recommendations", []),
            "results": result.get("results", {})
        }
        
        logger.info("查询处理完成")
        return response
        
    except Exception as e:
        logger.error(f"查询处理失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/travel/flight")
async def query_flight(request: dict):
    """机票查询接口"""
    try:
        from agents import FlightQueryAgent
        from langchain_community.chat_models import ChatTongyi
        
        llm = ChatTongyi(
            model_name=settings.LLM_MODEL,
            dashscope_api_key=settings.DASHSCOPE_API_KEY
        )
        
        agent = FlightQueryAgent(llm)
        result = await agent.process(request)
        
        return result
        
    except Exception as e:
        logger.error(f"机票查询失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/travel/hotel")
async def query_hotel(request: dict):
    """酒店查询接口"""
    try:
        from agents import HotelQueryAgent
        from langchain_community.chat_models import ChatTongyi
        
        llm = ChatTongyi(
            model_name=settings.LLM_MODEL,
            dashscope_api_key=settings.DASHSCOPE_API_KEY
        )
        
        agent = HotelQueryAgent(llm)
        result = await agent.process(request)
        
        return result
        
    except Exception as e:
        logger.error(f"酒店查询失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/travel/attraction")
async def recommend_attraction(request: dict):
    """景点推荐接口"""
    try:
        from agents import AttractionRecommendAgent
        from langchain_community.chat_models import ChatTongyi
        
        llm = ChatTongyi(
            model_name=settings.LLM_MODEL,
            dashscope_api_key=settings.DASHSCOPE_API_KEY
        )
        
        agent = AttractionRecommendAgent(llm)
        result = await agent.process(request)
        
        return result
        
    except Exception as e:
        logger.error(f"景点推荐失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/travel/booking")
async def handle_booking(request: dict):
    """预订处理接口"""
    try:
        from agents import BookingAgent
        from langchain_community.chat_models import ChatTongyi
        
        llm = ChatTongyi(
            model_name=settings.LLM_MODEL,
            dashscope_api_key=settings.DASHSCOPE_API_KEY
        )
        
        agent = BookingAgent(llm)
        result = await agent.process(request)
        
        return result
        
    except Exception as e:
        logger.error(f"预订处理失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/customer/service")
async def customer_service(request: dict):
    """客服咨询接口"""
    try:
        from agents import CustomerServiceAgent
        from langchain_community.chat_models import ChatTongyi
        
        llm = ChatTongyi(
            model_name=settings.LLM_MODEL,
            dashscope_api_key=settings.DASHSCOPE_API_KEY
        )
        
        agent = CustomerServiceAgent(llm)
        result = await agent.process(request)
        
        return result
        
    except Exception as e:
        logger.error(f"客服咨询失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=True,
        log_level=settings.LOG_LEVEL.lower()
    )

