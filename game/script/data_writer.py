import requests as r

def write_data(URL: str = "http://localhost:8000/save_score", 
               nickname: str = "player", 
               score: int = 0) -> r.Response:
    """Sends score to server"""
    req = r.post(URL, json={"player": nickname, "score": score})
    return req