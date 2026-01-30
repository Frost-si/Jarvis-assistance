from app.core.nlp_task_parser import parse_task

def interpret_task(text: str):
    return parse_task(text)
