import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.broker import check_health, close_broker, connect_broker
from . import models
from .database import engine
from .routers import perfumes, orders, cart, users, uploads
load_dotenv(".env")
URL_FRONTEND_LOCAL = os.getenv('CORS_FRONTEND_LOCAL')
URL_FRONTEND2 = os.getenv('CORS_ORIGINS2')
URL_FRONTEND3 = os.getenv('CORS_ORIGINS3')
URL_FRONTEND4 = os.getenv('CORS_ORIGINS4')

# Lifespan менеджер
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await connect_broker()
    print("✅ RabbitMQ broker connected")

    # Создаем таблицы БД
    models.Base.metadata.create_all(bind=engine)
    print("✅ Database tables created")

    yield  # Здесь работает приложение

    # Shutdown
    await close_broker()
    print("✅ RabbitMQ broker disconnected")


app = FastAPI(
    title="AromaBay API",
    version="1.0.0",
    lifespan=lifespan
)

# Раздаем загруженные изображения
STATIC_UPLOADS_DIR = Path(__file__).resolve().parent / "uploads"
STATIC_UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/upload", StaticFiles(directory=str(STATIC_UPLOADS_DIR)), name="upload")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[URL_FRONTEND_LOCAL, URL_FRONTEND2, URL_FRONTEND3, URL_FRONTEND4,],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Роутеры
prefix = "/api/v1"
app.include_router(perfumes.router, prefix=prefix)
app.include_router(orders.router, prefix=prefix)
app.include_router(cart.router, prefix=prefix)
app.include_router(users.router, prefix=prefix)
app.include_router(uploads.router, prefix=prefix)


@app.get("/")
def read_root():
    return {"message": "Welcome to AromaBay API"}

@app.get("/health")
async def health_check():
    broker_healthy = await check_health()
    return {
        "status": "healthy" if broker_healthy else "degraded",
        "database": "connected",
        "rabbitmq": "connected" if broker_healthy else "disconnected"
    }
