from fastapi import FastAPI
from .routes.main import router as Api_Router

app = FastAPI()

app.include_router(Api_Router, tags=["mongo"], prefix="/mongo")

@app.get('/')
@app.get('/index')
async def base():
    return {"Status": "UP"}

