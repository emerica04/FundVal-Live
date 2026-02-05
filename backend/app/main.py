from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
import os
import sys

from .routers import funds, ai, account
from .db import init_db
from .services.scheduler import start_scheduler

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    init_db()
    start_scheduler()
    yield
    # Shutdown
    pass

app = FastAPI(title="Fund Intraday Valuation API", lifespan=lifespan)

# CORS: allow all for MVP
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routes
app.include_router(funds.router, prefix="/api")
app.include_router(ai.router, prefix="/api")
app.include_router(account.router, prefix="/api")

# 静态文件服务（前端）
# 判断是否为打包后的应用
if getattr(sys, 'frozen', False):
    # 打包后：fundval-live 在 _internal 目录下
    base_path = sys._MEIPASS
    frontend_dir = os.path.join(base_path, "fundval-live")
else:
    # 开发模式：frontend/dist
    frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "frontend", "dist")

print(f"Frontend directory: {frontend_dir}")
print(f"Frontend exists: {os.path.exists(frontend_dir)}")

if os.path.exists(frontend_dir):
    # 挂载 assets 目录
    assets_dir = os.path.join(frontend_dir, "assets")
    if os.path.exists(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    @app.get("/")
    async def serve_frontend():
        index_path = os.path.join(frontend_dir, "index.html")
        if os.path.exists(index_path):
            return FileResponse(index_path)
        return {"error": "Frontend not found"}

    @app.get("/{full_path:path}")
    async def serve_frontend_routes(full_path: str):
        # 如果是 API 路由，跳过
        if full_path.startswith("api/"):
            return {"error": "Not found"}

        # 尝试返回文件
        file_path = os.path.join(frontend_dir, full_path)
        if os.path.isfile(file_path):
            return FileResponse(file_path)

        # 否则返回 index.html（SPA 路由）
        index_path = os.path.join(frontend_dir, "index.html")
        if os.path.exists(index_path):
            return FileResponse(index_path)
        return {"error": "Frontend not found"}
else:
    print(f"Warning: Frontend directory not found at {frontend_dir}")
