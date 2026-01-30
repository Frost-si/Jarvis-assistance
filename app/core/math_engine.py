import re

def calculate(text: str):
    try:
        # extract math expression safely
        expr = re.sub(r"[^0-9+\-*/(). ]", "", text)
        result = eval(expr)
        return {"expression": expr, "result": result}
    except:
        return {"error": "Invalid math expression"}
