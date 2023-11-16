import uvicorn
from fastapi import FastAPI

import settings

from common.db.session import init_db
from router.api import api_router

app = FastAPI()
app.include_router(api_router)


@app.on_event("startup")
async def on_startup():
    await init_db()


if __name__ == "__main__":
    uvicorn.run(app=app, host=settings.HOST, port=settings.PORT)
