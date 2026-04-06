from fastapi import FastAPI, Request, Depends, HTTPException
from app import schemas

from app.api.users import router as users_router

app = FastAPI()
app.include_router(users_router)

@app.post("/")
def post_root(user: schemas.UserCreate):
    print(user)
    return "ok"
