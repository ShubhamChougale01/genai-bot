from langchain_community.tools import DuckDuckGoSearchRun

try:
    duckduckgo = DuckDuckGoSearchRun()
except Exception as e:
    print(f"DuckDuckGo initialization failed: {e}")
    duckduckgo = None

def web_search_tool(query: str) -> str:
    if not duckduckgo:
        return "DuckDuckGo search is unavailable."
    try:
        result = duckduckgo.run(query)
        if result:
            return f"DuckDuckGo Search:\n{result}"
        return "No results found."
    except Exception as e:
        print(f"DuckDuckGo search failed: {e}")
