from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.tools import TavilySearchResults
from langchain_community.tools.jina_search import JinaSearch
from typing import Optional


duckduckgo = DuckDuckGoSearchRun()
try:
    tavily = TavilySearchResults()
except Exception:
    tavily = None

try:
    jina = JinaSearch()
except Exception:
    jina = None


def web_search_tool(query: str) -> str:
    try:
        result = duckduckgo.run(query)
        if result:
            return f"DuckDuckGo Search:\n{result}"
    except Exception as e:
        print(f"DuckDuckGo error: {e}")

    if tavily:
        try:
            result = tavily.run(query)
            if result:
                return f"Tavily Search:\n{result}"
        except Exception as e:
            print(f"Tavily error: {e}")

    if jina:
        try:
            result = jina.run(query)
            if result:
                return f"Jina Search:\n{result}"
        except Exception as e:
            print(f"Jina error: {e}")

    return "All search providers failed. Please try again later."
