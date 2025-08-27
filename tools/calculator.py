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