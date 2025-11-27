"""
测试客户端
用于测试旅行平台的各项功能
"""
import asyncio
import httpx
from typing import Dict, Any


class TravelClient:
    """旅行平台测试客户端"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=60.0)
    
    async def query(self, query: str, user_id: str = "test_user") -> Dict[str, Any]:
        """通用查询接口"""
        url = f"{self.base_url}/api/v1/travel/query"
        data = {
            "query": query,
            "user_id": user_id
        }
        
        response = await self.client.post(url, json=data)
        return response.json()
    
    async def close(self):
        """关闭客户端"""
        await self.client.aclose()


async def test_scenarios():
    """测试各种场景"""
    client = TravelClient()
    
    print("=" * 80)
    print("携程式多智能体旅行平台 - 功能测试")
    print("=" * 80)
    
    # 测试场景列表
    scenarios = [
        {
            "name": "机票查询",
            "query": "我想查询12月1日从北京到上海的机票，1个人"
        },
        {
            "name": "酒店查询",
            "query": "帮我找一下上海的酒店，预算500元左右，想要四星级的"
        },
        {
            "name": "景点推荐",
            "query": "推荐一些杭州的景点，我喜欢自然风光和历史文化"
        },
        {
            "name": "行程规划",
            "query": "帮我规划一个3天的成都之旅，12月10日出发，12月12日返回"
        },
        {
            "name": "客服咨询",
            "query": "请问机票改签需要什么条件？收费标准是怎样的？"
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n{'=' * 80}")
        print(f"测试场景 {i}: {scenario['name']}")
        print(f"{'=' * 80}")
        print(f"用户查询: {scenario['query']}\n")
        
        try:
            result = await client.query(scenario['query'])
            
            if result.get("success"):
                print("✓ 查询成功")
                print(f"\n意图识别: {result.get('intent', {}).get('intent_type', 'N/A')}")
                print(f"\n回答:\n{result.get('final_answer', 'N/A')}")
                
                recommendations = result.get('recommendations', [])
                if recommendations:
                    print(f"\n建议:")
                    for rec in recommendations:
                        print(f"  - {rec}")
            else:
                print(f"✗ 查询失败: {result.get('error', 'Unknown error')}")
        
        except Exception as e:
            print(f"✗ 请求失败: {str(e)}")
        
        # 等待一下，避免请求过快
        await asyncio.sleep(1)
    
    print(f"\n{'=' * 80}")
    print("测试完成！")
    print(f"{'=' * 80}\n")
    
    await client.close()


async def interactive_mode():
    """交互模式"""
    client = TravelClient()
    
    print("\n" + "=" * 80)
    print("携程式多智能体旅行平台 - 交互模式")
    print("=" * 80)
    print("输入 'quit' 或 'exit' 退出")
    print("=" * 80 + "\n")
    
    while True:
        try:
            query = input("\n请输入您的查询: ").strip()
            
            if query.lower() in ['quit', 'exit', 'q']:
                print("\n再见！")
                break
            
            if not query:
                continue
            
            print("\n处理中...\n")
            result = await client.query(query)
            
            if result.get("success"):
                print("=" * 80)
                print(result.get('final_answer', ''))
                print("=" * 80)
                
                recommendations = result.get('recommendations', [])
                if recommendations:
                    print("\n建议:")
                    for rec in recommendations:
                        print(f"  - {rec}")
            else:
                print(f"✗ 查询失败: {result.get('error', 'Unknown error')}")
        
        except KeyboardInterrupt:
            print("\n\n再见！")
            break
        except Exception as e:
            print(f"✗ 错误: {str(e)}")
    
    await client.close()


async def main():
    """主函数"""
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "interactive":
        # 交互模式
        await interactive_mode()
    else:
        # 测试模式
        await test_scenarios()


if __name__ == "__main__":
    asyncio.run(main())

