from fastapi import FastAPI
from routers import bot_router


app = FastAPI()

app.include_router(bot_router.router, prefix="/api", tags=["CHAT"])


@app.get("/")
@app.get("/echo")
async def echo():
    return {"message": "Up and running"}
