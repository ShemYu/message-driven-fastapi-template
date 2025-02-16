from fastapi import FastAPI
from api.routes import create_task, cancel_task

app = FastAPI(title="Message-Driven FastAPI Template")

# Include routers
app.include_router(create_task.router, tags=["tasks"])
app.include_router(cancel_task.router, tags=["tasks"])

@app.get("/", tags=["health"])
async def health_check():
    return {"status": "healthy"}
