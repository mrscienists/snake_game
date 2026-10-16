from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from api import db
from fastapi.middleware.cors import CORSMiddleware

db.init_db()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Score(BaseModel):
    player: str
    score: int

class PlayerName(BaseModel):
    player: str

@app.post("/save_score", status_code=201)
def save_score(item: Score):
    db.save_score(item.player, item.score)
    return item

@app.get("/delete_score")
def delete_score(player: str):
    deleted =  db.delete_score(player)
    if deleted == 0:
        raise HTTPException(status_code=404, detail="player not found")
    return {"deleted": deleted}

@app.get("/score")
def get_score():
    return  db.get_all_scores()

#to start server write in terminal: uvicorn api.main:app --reload