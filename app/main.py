import logging
import time
import os
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from fastapi.responses import JSONResponse
from fastapi_limiter import FastAPILimiter
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from app.database import engine, Base, SessionLocal
from app.routes import auth_routes, profile_routes, user_routes, docs_routes, news_routes
import aioredis
from sqlalchemy.orm import Session
from sentence_transformers import SentenceTransformer, util
from app.models import Department, EmployeeProfile, News, Document
from app.schemas import SmartSearchResponse, EmployeeResponse, DepartmentResponse, NewsResponse, DocumentResponse

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log", mode="a", encoding="utf-8")
    ]
)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Secure Corporate Portal")

# Загрузка модели SentenceTransformer
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
async def startup():
    logging.info("Запуск приложения.")
    redis = await aioredis.from_url("redis://redis:6379", encoding="utf8", decode_responses=True)
    await FastAPILimiter.init(redis)

@app.on_event("shutdown")
async def shutdown():
    logging.info("Остановка приложения.")

origins = [
    "http://localhost",
    'http://localhost:3000',
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
#app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET)

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

#Функция умного поиска
@app.get("/search", response_model=SmartSearchResponse)
def smart_search(query: str, db: Session = Depends(get_db)):
    try:
        query_lower = query.lower()
        # 1. Ищем название отдела в запросе
        department = extract_department_from_query(query_lower, db)
        # 2. Ищем, какой тип данных запрашивается (документы, новости, сотрудники)
        data_type = extract_data_type_from_query(query_lower)
        # 3. Если есть отдел и указан вид данных — ищем конкретные данные по отделу
        if department and data_type:
            return get_data_by_department_and_type(db, query, department, data_type)
        # 4. Если есть отдел, но не указан вид данных — возвращаем информацию об отделе
        elif department:
            return get_department_info(db, query, department)
        # 5. Если отдела нет, но указан вид данных — ищем по общим данным
        elif data_type:
            return get_general_data_by_type(db, query, data_type)
        # 6. Если ничего не найдено явно — ищем наиболее подходящие данные по всем категориям
        else:
            return get_best_matching_data(db, query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при выполнении поиска: {str(e)}")
    # Разделяем запрос по пробелам и проверяем, есть ли в запросе имя сотрудника
    query_parts = query.split()
    if len(query_parts) == 2:  # Если запрос состоит из двух слов (например, имя и фамилия)
        first_name, last_name = query_parts
        employee = db.query(EmployeeProfile).filter(
            EmployeeProfile.first_name.ilike(f"%{first_name}%"),
            EmployeeProfile.last_name.ilike(f"%{last_name}%")
        ).first()
        return employee
    elif len(query_parts) == 1:  # Если запрос состоит из одного слова (например, имя или фамилия)
        employee = db.query(EmployeeProfile).filter(
            EmployeeProfile.first_name.ilike(f"%{query_parts[0]}%") |
            EmployeeProfile.last_name.ilike(f"%{query_parts[0]}%")
        ).first()
        return employee
    return None

# Функция для получения информации по типа данных опредленного отдела
def get_data_by_department_and_type(db, query, department, data_type):
    # Фильтруем по отделу и типу данных
    if data_type == "сотрудники":
        employees = db.query(EmployeeProfile).filter(EmployeeProfile.department_id == department.id).all()
        # Проверяем, есть ли в запросе имя или фамилия сотрудника
        query_lower = query.lower()
        filtered_employees = []
        for employee in employees:
            full_name = f"{employee.first_name.lower()} {employee.last_name.lower()}"
            # Проверяем совпадение имени/фамилии с запросом
            if any(keyword in full_name for keyword in query_lower.split()):
                filtered_employees.append(employee)
        # Если найдены сотрудники, удовлетворяющие запросу, возвращаем их
        if filtered_employees:
            return SmartSearchResponse(
                query=query,
                department=None,
                employees=serialize_employees(filtered_employees),
                news=[],
                documents=[]
            )
        # Если нет совпадений, возвращаем всех сотрудников отдела
        return SmartSearchResponse(
            query=query,
            department=None,
            employees=serialize_employees(employees),
            news=[],
            documents=[]
        )
    if data_type == "новости":
        news = db.query(News).filter(News.department_id == department.id).all()  # Новости фильтруются по department_id
        return SmartSearchResponse(query=query, department=None, employees=[], news=serialize_news(news), documents=[])

    return SmartSearchResponse(query=query, department=None, employees=[], news=[], documents=[])

# Функция для получения общей информации об отделе
def get_department_info(db, query, department):
    # Получаем всех сотрудников отдела
    employees = db.query(EmployeeProfile).filter(EmployeeProfile.department_id == department.id).all()
    
    # Получаем все новости отдела
    news = db.query(News).filter(News.department_id == department.id).all()
    
    
    # Возвращаем полную информацию об отделе
    return SmartSearchResponse(
        query=query,
        department=DepartmentResponse(
            id=department.id,
            name=department.name,
            description=department.description
        ),
        employees=serialize_employees(employees),
        news=serialize_news(news),
        documents=[]
    )

# Функция для поиска общих данных по виду
def get_general_data_by_type(db, query, data_type):
    if data_type == "сотрудники":
        employees = db.query(EmployeeProfile).all()
        return SmartSearchResponse(query=query, department=None, employees=serialize_employees(employees), news=[], documents=[])

    if data_type == "новости":
        news = db.query(News).all()
        return SmartSearchResponse(query=query, department=None, employees=[], news=serialize_news(news), documents=[])

    if data_type == "документы":
        documents = db.query(Document).all()
        return SmartSearchResponse(query=query, department=None, employees=[], news=[], documents=serialize_documents(documents))

    return SmartSearchResponse(query=query, department=None, employees=[], news=[], documents=[])

# Функция для поиска наиболее подходящих данных по запросу
def get_best_matching_data(db, query):
    
    # Преобразуем запрос в нижний регистр
    query_lower = query.lower()
    query_embedding = model.encode(query, convert_to_tensor=True)
    
    # 1. Поиск сотрудников
    employees = db.query(EmployeeProfile).all()
    filtered_employees = []
    for employee in employees:
        full_name = f"{employee.first_name} {employee.last_name} {employee.business_role}".lower()
        if any(keyword in full_name for keyword in query_lower.split()):
            filtered_employees.append(employee)
    
    # Семантическая фильтрация сотрудников
    ranked_employees = []
    for employee in filtered_employees:
        employee_info = f"{employee.first_name} {employee.last_name} {employee.business_role}"
        employee_embedding = model.encode(employee_info, convert_to_tensor=True)
        similarity = util.cos_sim(query_embedding, employee_embedding).item()
        ranked_employees.append((similarity, employee))
    ranked_employees.sort(reverse=True, key=lambda x: x[0])  # Сортировка по релевантности
    
    # 2. Поиск новостей
    news = db.query(News).all()
    filtered_news = []
    for n in news:
        if any(keyword in n.title.lower() or keyword in n.content.lower() for keyword in query_lower.split()):
            filtered_news.append(n)
    
    # Семантическая фильтрация новостей
    ranked_news = []
    for n in filtered_news:
        news_info = f"{n.title} {n.content}"
        news_embedding = model.encode(news_info, convert_to_tensor=True)
        similarity = util.cos_sim(query_embedding, news_embedding).item()
        ranked_news.append((similarity, n))
    ranked_news.sort(reverse=True, key=lambda x: x[0])  # Сортировка по релевантности
    
    # 3. Поиск документов
    documents = db.query(Document).all()
    filtered_documents = []
    for doc in documents:
        if any(keyword in doc.title.lower() or keyword in doc.description.lower() for keyword in query_lower.split()):
            filtered_documents.append(doc)
    
    # Семантическая фильтрация документов
    ranked_documents = []
    for doc in filtered_documents:
        doc_info = f"{doc.title} {doc.description}"
        doc_embedding = model.encode(doc_info, convert_to_tensor=True)
        similarity = util.cos_sim(query_embedding, doc_embedding).item()
        ranked_documents.append((similarity, doc))
    ranked_documents.sort(reverse=True, key=lambda x: x[0])  # Сортировка по релевантности
    
    
    # Возвращаем топ-N результатов
    top_n = 5  # Количество результатов для каждого типа данных
    return SmartSearchResponse(
        query=query,
        department=None,
        employees=serialize_employees([emp for _, emp in ranked_employees[:top_n]]),
        news=serialize_news([n for _, n in ranked_news[:top_n]]),
        documents=serialize_documents([doc for _, doc in ranked_documents[:top_n]])
    )

# Функция для распознования отдела
def extract_department_from_query(query, db):

    known_departments = db.query(Department).all()  # Все отделы
    
    # Преобразуем запрос в нижний регистр
    query_lower = query.lower()
    
    # 1. Проверяем полное совпадение названия отдела
    for dept in known_departments:
        department_name_lower = dept.name.lower()
        if department_name_lower in query_lower:
            return dept
    
    # 2. Проверяем частичное совпадение ключевых слов
    best_match = None
    best_match_keywords = 0
    for dept in known_departments:
        department_keywords = dept.name.lower().split()  # Разбиваем название отдела на слова
        
        # Считаем количество совпадений ключевых слов
        matched_keywords = sum(1 for keyword in department_keywords if keyword in query_lower)
        
        # Выбираем отдел с наибольшим количеством совпадений
        if matched_keywords > best_match_keywords:
            best_match = dept
            best_match_keywords = matched_keywords
    
    if best_match:
        return best_match
    
    return None

# Функция для распознования типа данных
def extract_data_type_from_query(query):
    
    # Преобразуем запрос в нижний регистр для унификации
    query_lower = query.lower()
    
    # Список ключевых фраз для каждого типа данных
    data_type_keywords = {
        "сотрудники": [
            "сотрудники", "список сотрудников", "работники", "персонал", 
            "члены команды", "работающие", "работники отдела", "персонал отдела", "сотрудник"
        ],
        "новости": [
            "новости", "новость", "объявления", "новостная лента", "свежие новости", 
            "новости отдела", "корпоративные новости", "новости компании", "список новостей"
        ],
        "документы": [
            "документы", "файлы", "документ", "папки", "архивы", "отчёты", 
            "соглашения", "платежные документы", "контракты", "материалы", 
            "инструкции", "документы отдела", "книги", "планы", "формы", "образцы документов",
            "доки"
        ]
    }
    
    # Считаем количество совпадений для каждого типа данных
    best_match = None
    best_match_keywords = 0
    for data_type, keywords in data_type_keywords.items():
        # Считаем количество совпадений для каждого типа данных
        matched_keywords = sum(1 for keyword in keywords if keyword in query_lower)
        
        # Выбираем тип данных с наибольшим количеством совпадений
        if matched_keywords > best_match_keywords:
            best_match = data_type
            best_match_keywords = matched_keywords
    
    if best_match:
        return best_match
    
    # Если ничего не найдено
    return None

# Функции для сериализации данных
def serialize_employee(employee):
    return EmployeeResponse(
        id=employee.id, first_name=employee.first_name, last_name=employee.last_name,
        business_role=employee.business_role, corporate_email=employee.corporate_email,
        photo_url=employee.photo_url, additional_info=employee.additional_info
    )

def serialize_employees(employees):
    return [
        EmployeeResponse(
            id=e.id, first_name=e.first_name, last_name=e.last_name,
            business_role=e.business_role, corporate_email=e.corporate_email,
            photo_url=e.photo_url, additional_info=e.additional_info
        ) for e in employees
    ]

def serialize_news(news):
    return [
        NewsResponse(
            id=n.id, title=n.title, content=n.content, news_type=n.news_type,
            is_approved=n.is_approved, created_at=n.created_at, updated_at=n.updated_at,
            author_id=n.author_id, department_id=n.department_id
        ) for n in news
    ]

def serialize_documents(documents):
    return [
        DocumentResponse(
            id=d.id, title=d.title, file_path=d.file_path, doc_type=d.doc_type,
            description=d.description, uploaded_at=d.uploaded_at, uploaded_by=d.uploaded_by
        ) for d in documents
    ]


app.add_exception_handler(429, custom_rate_limit_exceeded_handler)

# Роуты
app.include_router(auth_routes.router, prefix="/api", tags=["auth"])
app.include_router(profile_routes.router, prefix="/api", tags=["profile"])
app.include_router(user_routes.router, prefix="/api", tags=["users"])
app.include_router(docs_routes.router, prefix="/api", tags=["documents"])
app.include_router(news_routes.router, prefix="/api/news", tags=["news"])
