from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from app.database import engine, Base
from app.routes import auth_routes, profile_routes, user_routes, docs_routes, news_routes
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from fastapi.responses import JSONResponse
from fastapi_limiter import FastAPILimiter
import aioredis


# Инициализируем базу данных (создаем таблицы, если их еще нет)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Secure Corporate Portal")

@app.on_event("startup")
async def startup():
    import aioredis
    redis = await aioredis.from_url("redis://redis:6379", encoding="utf8", decode_responses=True)
    await FastAPILimiter.init(redis)


# CORS – разрешаем запросы только с доверенных источников
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

# Rate Limiter (защита от DDoS, брутфорса) с помощью slowapi
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler)

# Middleware для сессий – используется для хранения токенов в HttpOnly cookie
import os
SESSION_SECRET = os.getenv("SESSION_SECRET", "defaultsecret")
app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET)

# Простейшее логирование запросов (для аудита)
@app.middleware("http")
async def log_requests(request: Request, call_next):
    import time, logging
    logger = logging.getLogger("uvicorn.access")
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    logger.info("%s %s %s (%.2fms)", request.method, request.url, response.status_code, process_time)

    return response

async def custom_rate_limit_exceeded_handler(request: Request, exc):
    view_rate_limit = getattr(request.state, "view_rate_limit", None)
    return JSONResponse(
        status_code=429,
        content={"detail": "Превышен лимит запросов", "rate_limit": view_rate_limit},
    )

# Таймауты
# app.add_exception_handler(429, custom_rate_limit_exceeded_handler)

# Роуты
app.include_router(auth_routes.router, prefix="/api", tags=["auth"])
app.include_router(profile_routes.router, prefix="/api", tags=["profile"])
app.include_router(user_routes.router, prefix="/api", tags=["users"])
app.include_router(docs_routes.router, prefix="/api", tags=["documents"])
app.include_router(news_routes.router, prefix="/api/news", tags=["news"])

