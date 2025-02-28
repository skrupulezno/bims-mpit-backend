import logging
import time
import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from fastapi.responses import JSONResponse
from fastapi_limiter import FastAPILimiter
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from app.database import engine, Base
from app.routes import auth_routes, profile_routes, user_routes, docs_routes, news_routes
import aioredis

# Настройка логирования: все логи будут записываться в файл app.log
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log", mode="a", encoding="utf-8")
    ]
)

# Создание таблиц в базе данных
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Secure Corporate Portal")

@app.on_event("startup")
async def startup():
    logging.info("Запуск приложения.")
    redis = await aioredis.from_url("redis://redis:6379", encoding="utf8", decode_responses=True)
    await FastAPILimiter.init(redis)

@app.on_event("shutdown")
async def shutdown():
    logging.info("Остановка приложения.")

# CORS настройка
origins = [
    "http://localhost",
    "http://138.124.20.90",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate Limiter (защита от DDoS и брутфорса)
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler)

# Middleware для сессий
SESSION_SECRET = os.getenv("SESSION_SECRET", "defaultsecret")
app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET)

# Middleware для логирования всех запросов и ответов
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logging.info(f"Получен запрос: {request.method} {request.url}")
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    logging.info(f"Обработан запрос: {request.method} {request.url} - статус {response.status_code} ({process_time:.2f}ms)")
    return response

# Кастомный обработчик превышения лимита запросов с логированием
async def custom_rate_limit_exceeded_handler(request: Request, exc):
    view_rate_limit = getattr(request.state, "view_rate_limit", None)
    logging.warning(f"Превышен лимит запросов от {request.client.host}: {request.method} {request.url}")
    return JSONResponse(
        status_code=429,
        content={"detail": "Превышен лимит запросов", "rate_limit": view_rate_limit},
    )

app.add_exception_handler(429, custom_rate_limit_exceeded_handler)

# Роуты
app.include_router(auth_routes.router, prefix="/api", tags=["auth"])
app.include_router(profile_routes.router, prefix="/api", tags=["profile"])
app.include_router(user_routes.router, prefix="/api", tags=["users"])
app.include_router(docs_routes.router, prefix="/api", tags=["documents"])
app.include_router(news_routes.router, prefix="/api/news", tags=["news"])
