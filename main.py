import os
import sys
import asyncio

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from .config import SSD_PATH, UPSCAYL_CLI_PATH, MODELS_PATH, BASE_DIR
from .utils.logger import log
from .database import engine
from . import models

# Import routers
from .routers import clients, orders, contents, upscaler, ws, ecommerce

@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info("🚀 Server Initializing...")
    
    # Init Database Tables
    log.info("Checking database and creating tables if missing...")
    models.Base.metadata.create_all(bind=engine)

    # Verify Environment
    if not os.path.exists(SSD_PATH):
        os.makedirs(SSD_PATH)
    if not os.path.exists(UPSCAYL_CLI_PATH):
        log.error(f"CRITICAL: Upscayl CLI not found at {UPSCAYL_CLI_PATH}")
    if not os.path.exists(MODELS_PATH):
        log.error(f"CRITICAL: Models path not found at {MODELS_PATH}")

    yield 
    
    log.info("🛑 Server Shutting Down...")
    await log.complete()

# Initialize FastAPI app
app = FastAPI(lifespan=lifespan, title="Funnel Creative Engine by Flownix")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve generated images from assets/
app.mount("/assets", StaticFiles(directory=os.path.join(BASE_DIR, "assets")), name="assets")

# Wire up the routers
app.include_router(clients.router)
app.include_router(orders.router)
app.include_router(contents.router)
app.include_router(upscaler.router)
app.include_router(ecommerce.router)
# websocket router
app.include_router(ws.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)