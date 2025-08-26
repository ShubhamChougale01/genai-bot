# from langchain.chains import LLMMathChain
# from langchain_groq import ChatGroq
# import os

# llm = ChatGroq(model="gemma2-9b-it", api_key=os.getenv("GROQ_API_KEY"))

# llm_math = LLMMathChain.from_llm(llm=llm, verbose=True)

# def calculator_tool(query: str) -> str:
#     try:
#         result = llm_math.run(query)
#         return f"Result: {result}"
#     except Exception as e:
#         return f"Calculation failed: {str(e)}"

def calculator_tool(query: str) -> str:
    try:
        expr = query.replace("×", "*").replace("÷", "/")
        result = eval(expr, {"__builtins__": {}})
        return f"Result: {result}"

    except ZeroDivisionError:
        return "Error: Division by zero is not allowed."
    except SyntaxError:
        return "Error: Invalid arithmetic expression syntax."
    except Exception as e:
        return f"Error: Could not evaluate expression ({str(e)})"