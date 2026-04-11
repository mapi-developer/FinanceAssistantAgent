import sys
import os
import uvicorn

# Inject project root into sys.path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router as api_router
from api.websockets import router as ws_router

app = FastAPI(title="Finance Assistant AaaS Platform")

# CORS middleware for UI connectivity
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")
app.include_router(ws_router)

if __name__ == "__main__":
    # Start the server
    uvicorn.run("api.server:app", host="0.0.0.0", port=8000, reload=True)