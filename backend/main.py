from fastapi import FastAPI, Request, Depends, HTTPException
from app import schemas

app = FastAPI()

@app.post("/")
def post_root(user: schemas.UserCreate):
    print(user)
    return "ok"
