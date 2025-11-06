from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.broker import check_health, close_broker, connect_broker
from . import models
from .database import engine
from .routers import perfumes, orders

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

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://aromabay.site",
        "http://localhost:3000"  # для локальной разработки
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Роутеры
app.include_router(perfumes.router, prefix="/api/v1")
app.include_router(orders.router, prefix="/api/v1")

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