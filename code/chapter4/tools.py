from dotenv import load_dotenv
load_dotenv()

import os
import json
import requests
from typing import Dict, Any

def search(query: str) -> str:
    """
    基于 Bocha API 的网页搜索工具。
    """
    print(f"🔍 正在执行 [BochaAPI] 网页搜索: {query}")
    original_query = query  # 保留原始查询用于错误信息

    if not query or not query.strip():
        return "错误：搜索查询不能为空。"

    try:
        api_key = os.getenv("BOCHA_API_KEY")
        if not api_key:
            return "错误：BOCHA_API_KEY 未在 .env 文件中配置。"

        url = "https://api.bochaai.com/v1/web-search"
        payload = json.dumps({
            "query": query,
            "freshness": "oneYear",
            "summary": True,
            "count": 8
        })
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
        }

        response = requests.post(url, headers=headers, data=payload, timeout=10)
        response.raise_for_status()
        raw_data = response.json()

        # 调试：打印完整返回（可选，可注释掉）
        # print("【调试】Bocha API 原始返回：")
        # print(json.dumps(raw_data, indent=2, ensure_ascii=False))

        # 真正的结果在 raw_data['data'] 中
        result_data = raw_data.get("data", {})
        if not result_data:
            return f"对不起，没有找到关于 '{original_query}' 的信息（响应中无 data 字段）。"

        # 1. 优先取直接答案（如果有）
        if "answer" in result_data and result_data["answer"]:
            return result_data["answer"]
        if "directAnswer" in result_data and result_data["directAnswer"]:
            return result_data["directAnswer"]

        # 2. 尝试从 webPages 提取
        web_pages = result_data.get("webPages", {})
        items = web_pages.get("value", [])
        if items:
            snippets = []
            for i, item in enumerate(items[:3]):
                title = item.get("name", "") or item.get("title", "")
                snippet = item.get("snippet", "") or item.get("description", "")
                snippets.append(f"[{i+1}] {title}\n{snippet}")
            return "\n\n".join(snippets)

        # 3. 尝试从 organic_results（某些兼容格式）
        organic = result_data.get("organic_results", [])
        if organic:
            snippets = []
            for i, res in enumerate(organic[:3]):
                title = res.get("title", "")
                snippet = res.get("snippet", "")
                snippets.append(f"[{i+1}] {title}\n{snippet}")
            return "\n\n".join(snippets)

        # 4. 若都为空，返回提示
        return f"对不起，没有找到关于 '{original_query}' 的信息。"

    except requests.exceptions.RequestException as e:
        return f"网络请求错误: {e}"
    except json.JSONDecodeError as e:
        return f"解析响应数据出错: {e}"
    except Exception as e:
        return f"搜索时发生错误: {e}"


class ToolExecutor:
    """工具执行器（保持不变）"""
    def __init__(self):
        self.tools: Dict[str, Dict[str, Any]] = {}

    def registerTool(self, name: str, description: str, func: callable):
        if name in self.tools:
            print(f"警告：工具 '{name}' 已存在，将被覆盖。")
        self.tools[name] = {"description": description, "func": func}
        print(f"工具 '{name}' 已注册。")

    def getTool(self, name: str) -> callable:
        return self.tools.get(name, {}).get("func")

    def getAvailableTools(self) -> str:
        return "\n".join([
            f"- {name}: {info['description']}" 
            for name, info in self.tools.items()
        ])


if __name__ == '__main__':
    toolExecutor = ToolExecutor()
    search_description = "一个网页搜索引擎。当你需要回答关于时事、事实以及在你的知识库中找不到的信息时，应使用此工具。"
    toolExecutor.registerTool("Search", search_description, search)
    print("\n--- 可用的工具 ---")
    print(toolExecutor.getAvailableTools())

    # 测试查询
    test_query = "英伟达最新的GPU型号是什么"
    print(f"\n--- 执行 Action: Search['{test_query}'] ---")
    tool_func = toolExecutor.getTool("Search")
    if tool_func:
        observation = tool_func(test_query)
        print("--- 观察 (Observation) ---")
        print(observation)
    else:
        print("错误：未找到名为 'Search' 的工具。")