import os
import logging
import uuid
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import List, Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, APIRouter, Request, HTTPException, Response, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

# --- MODÜLLER ---
from models import (
    User, Category, CategoryCreate, Word, WordCreate, UserProgress,
    AIExampleRequest, AIExampleResponse, TeacherAssignment
)
from auth import (
    get_session_data, create_or_update_user, create_session,
    get_current_user, require_auth, require_teacher, require_super_admin,
    authenticate_user, create_access_token, get_password_hash, 
    get_current_user_from_token
)
from teacher_management import teacher_router
from progress import router as progress_router
from user_content import router as user_content_router

# --- AYARLAR ---
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')
MONGO_URL = os.getenv('MONGO_URL')

# !!! İŞTE BURAYI DÜZELTTİK: DOĞRU KUTU İSMİ !!!
DB_NAME = "test_database" 

# --- VERİTABANI BAĞLANTISI ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    if MONGO_URL:
        app.mongodb_client = AsyncIOMotorClient(MONGO_URL)
        app.mongodb = app.mongodb_client[DB_NAME]
        logging.info(f"Veritabanına Bağlanıldı: {DB_NAME}")
    yield
    if MONGO_URL:
        app.mongodb_client.close()

app = FastAPI(title="YLM Sozluk API", lifespan=lifespan)

# ========================================================
# --- CORS GÜVENLİK AYARLARI ---
# ========================================================
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO)
async def get_db(): return app.mongodb
api_router = APIRouter(prefix="/api")

# ==================== GİRİŞ VE TAMİR ====================

@api_router.post("/login")
async def login(body: dict, db = Depends(get_db)):
    email = body.get("email")
    password = body.get("password")
    
    # 1. Kullanıcıyı doğrula
    user = await authenticate_user(email, password)
    if not user:
        raise HTTPException(status_code=401, detail="Hatalı şifre")
    
    # 2. Token oluştur
    access_token = create_access_token(data={"sub": email})

    # --- HATA DÜZELTME BÖLÜMÜ ---
    try:
        user_dict = user.model_dump()
    except AttributeError:
        try:
            user_dict = user.dict()
        except AttributeError:
            user_dict = dict(user)

    # 3. Patron Maskesi Tak (Site donmasın diye)
    if user_dict.get("role") == "super_admin":
        user_dict["role"] = "teacher"

    return {
        "token": access_token,
        "user": user_dict
    }

@api_router.post("/register")
async def register(body: dict, db = Depends(get_db)):
    email = body.get("email")
    password = body.get("password")
    
    if await db.users.find_one({"email": email}):
        raise HTTPException(status_code=400, detail="Zaten kayıtlı")
    
    patron_listesi = ["mctelektrik41@gmail.com", "e-turkrut@yandex.ru"]
    role = "super_admin" if email in patron_listesi else "student"
    sub = "premium" if email in patron_listesi else "free"

    user_data = {
        "user_id": f"user_{uuid.uuid4().hex[:12]}",
        "email": email,
        "name": body.get("name", "Kullanıcı"),
        "hashed_password": get_password_hash(password),
        "role": role,
        "subscription": sub,
        "created_at": datetime.now(timezone.utc),
    }
    
    await db.users.insert_one(user_data)
    
    response_user = user_data.copy()
    del response_user["hashed_password"]
    
    return {"token": create_access_token(data={"sub": email}), "user": response_user}

@api_router.get("/me")
async def get_me(user: User = Depends(get_current_user_from_token)):
    return user

# ==================== KELİME & KATEGORİ ====================

@api_router.get("/categories")
async def get_categories(db = Depends(get_db)):
    return await db.categories.find({}, {"_id": 0}).to_list(100)

@api_router.post("/categories")
async def create_category(body: dict, db = Depends(get_db), user = Depends(require_auth)):
    new_cat = {
        "category_id": f"cat_{uuid.uuid4().hex[:8]}",
        "name_tr": body.get("name_tr"),
        "name_ru": body.get("name_ru"),
        "word_count": 0,
        "created_at": datetime.now(timezone.utc)
    }
    await db.categories.insert_one(new_cat)
    return new_cat

@api_router.get("/words", response_model=List[Word])
async def get_words(category_id: Optional[str] = None, limit: int=100, skip: int=0, db=Depends(get_db), user=Depends(require_auth)):
    query = {}
    if category_id: query["category_id"] = category_id
    return await db.words.find(query, {"_id":0}).skip(skip).limit(limit).to_list(limit)

@api_router.post("/words")
async def create_word(word: WordCreate, db=Depends(get_db), user=Depends(require_auth)):
    word_data = {
        **word.model_dump(),
        "word_id": f"word_{uuid.uuid4().hex[:12]}",
        "created_at": datetime.now(timezone.utc),
        "ai_generated": False
    }
    await db.words.insert_one(word_data)
    await db.categories.update_one({"category_id": word.category_id}, {"$inc": {"word_count": 1}})
    return Word(**word_data)

@api_router.post("/words/ai-example")
async def generate_ai(req: AIExampleRequest, user=Depends(require_auth)):
    return AIExampleResponse(
        example_tr=f"Ornek: {req.word_turkish}",
        example_ru=f"Ornek RU: {req.word_russian}"
    )

@api_router.post("/progress/{word_id}/review")
async def review_word(word_id: str, body: dict, db = Depends(get_db), user = Depends(require_auth)):
    return {"message": "Ilerleme kaydedildi", "correct": True}

# --- BAĞLANTILAR ---
app.include_router(api_router)
app.include_router(teacher_router, prefix="/api/teacher", tags=["Teacher"])
app.include_router(progress_router, prefix="/api/progress-stats", tags=["Progress"]) 
app.include_router(user_content_router, prefix="/api/content", tags=["Content"])

# --- SWAGGER ---
def custom_openapi():
    if app.openapi_schema: return app.openapi_schema
    openapi_schema = get_openapi(title="YLM API", version="1.0", routes=app.routes)
    openapi_schema["components"]["securitySchemes"] = {
        "Bearer Auth": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
    }
    openapi_schema["security"] = [{"Bearer Auth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema
app.openapi = custom_openapi