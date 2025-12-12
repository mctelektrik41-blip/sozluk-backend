from fastapi import FastAPI, APIRouter, Request, HTTPException, Response
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from typing import List, Optional
import uuid
from datetime import datetime, timezone, timedelta

from models import (
    User, Category, CategoryCreate, Word, WordCreate, UserProgress,
    AIExampleRequest, AIExampleResponse, UserManagementRequest, TeacherAssignment,
    SUPER_ADMIN_EMAILS, is_super_admin
)
from auth import (
    get_session_data, create_or_update_user, create_session,
    get_current_user, require_auth, require_teacher, require_super_admin,
    authenticate_user, create_access_token, get_password_hash, get_current_user_from_token
)
from teacher_management import teacher_router
from progress import router as progress_router
from user_content import router as user_content_router

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app
app = FastAPI(title="YLM Sözlük API")

# --- CORS AYARLARI (DÜZELTİLDİ) ---
origins = [
    "http://localhost:3001",
    "http://127.0.0.1:3001"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ----------------------------------

# Create API router
api_router = APIRouter(prefix="/api")

# ==================== AUTH ENDPOINTS ====================

@api_router.post("/register")
async def register(body: dict):
    email = body.get("email")
    password = body.get("password")
    name = body.get("name", email.split("@")[0])
    
    if not email or not password:
        raise HTTPException(status_code=400, detail="Email and password required")
    
    existing = await db.users.find_one({"email": email})
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")
    
    user_id = f"user_{uuid.uuid4().hex[:12]}"
    role = "super_admin" if is_super_admin(email) else "student"
    subscription = "premium" if role == "super_admin" else "free"
    
    user_data = {
        "user_id": user_id,
        "email": email,
        "name": name,
        "hashed_password": get_password_hash(password),
        "role": role,
        "subscription": subscription,
        "language_preference": "tr-ru",
        "created_at": datetime.now(timezone.utc),
        "words_learned": 0,
        "streak": 0,
        "progress": 0.0
    }
    
    await db.users.insert_one(user_data)
    access_token = create_access_token(data={"sub": email})
    
    return {
        "token": access_token,
        "user": {
            "user_id": user_id,
            "email": email,
            "name": name,
            "role": role,
            "subscription": subscription
        }
    }

@api_router.post("/login")
async def login(body: dict):
    email = body.get("email")
    password = body.get("password")
    
    if not email or not password:
        raise HTTPException(status_code=400, detail="Email and password required")
    
    user = await authenticate_user(email, password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    access_token = create_access_token(data={"sub": email})
    
    return {
        "token": access_token,
        "user": {
            "user_id": user.user_id,
            "email": user.email,
            "name": user.name,
            "role": user.role,
            "subscription": user.subscription,
            "words_learned": user.words_learned,
            "streak": user.streak,
            "progress": user.progress
        }
    }

@api_router.get("/me")
async def get_current_user_info(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    token = auth_header.split(" ")[1]
    user = await get_current_user_from_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    return {
        "user_id": user.user_id,
        "email": user.email,
        "name": user.name,
        "role": user.role,
        "subscription": user.subscription,
        "words_learned": user.words_learned,
        "streak": user.streak,
        "progress": user.progress
    }

@api_router.post("/auth/session")
async def create_auth_session(body: dict, response: Response):
    session_id = body.get("session_id")
    if not session_id:
        raise HTTPException(status_code=400, detail="session_id required")
    
    auth_data = await get_session_data(session_id)
    user = await create_or_update_user(auth_data)
    session_token = auth_data["session_token"]
    await create_session(user.user_id, session_token)
    
    response.set_cookie(
        key="session_token",
        value=session_token,
        max_age=7 * 24 * 60 * 60,
        httponly=True,
        secure=False,
        samesite="lax",
        path="/"
    )
    return user

@api_router.get("/auth/me")
async def get_me(request: Request):
    user = await get_current_user(request)
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user

@api_router.post("/auth/logout")
async def logout(request: Request, response: Response):
    session_token = request.cookies.get("session_token")
    if session_token:
        await db.user_sessions.delete_one({"session_token": session_token})
    response.delete_cookie("session_token", path="/")
    return {"message": "Logged out successfully"}

# ==================== SUPER ADMIN ENDPOINTS ====================

@api_router.get("/admin/users")
async def get_all_users(request: Request):
    await require_super_admin(request)
    users = await db.users.find({}, {"_id": 0}).to_list(1000)
    return users

@api_router.post("/admin/users/teacher")
async def create_teacher(request: Request, assignment: TeacherAssignment):
    await require_super_admin(request)
    existing_user = await db.users.find_one({"email": assignment.teacher_email}, {"_id": 0})
    
    if existing_user:
        await db.users.update_one(
            {"email": assignment.teacher_email},
            {"$set": {"role": "teacher", "subscription": assignment.subscription}}
        )
        user = await db.users.find_one({"email": assignment.teacher_email}, {"_id": 0})
        return User(**user)
    else:
        user_id = f"user_{uuid.uuid4().hex[:12]}"
        user_data = {
            "user_id": user_id,
            "email": assignment.teacher_email,
            "name": assignment.name,
            "picture": None,
            "role": "teacher",
            "subscription": assignment.subscription,
            "language_preference": "tr-ru",
            "created_at": datetime.now(timezone.utc),
            "words_learned": 0,
            "streak": 0,
            "progress": 0.0
        }
        await db.users.insert_one(user_data)
        return User(**user_data)

@api_router.put("/admin/users/{user_id}/role")
async def update_user_role(request: Request, user_id: str, body: dict):
    await require_super_admin(request)
    new_role = body.get("role")
    if new_role not in ["student", "teacher", "super_admin"]:
        raise HTTPException(status_code=400, detail="Invalid role")
    
    result = await db.users.update_one(
        {"user_id": user_id},
        {"$set": {"role": new_role}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "Role updated successfully"}

@api_router.put("/admin/users/{user_id}/subscription")
async def update_user_subscription(request: Request, user_id: str, body: dict):
    await require_super_admin(request)
    new_subscription = body.get("subscription")
    if new_subscription not in ["free", "basic", "standard", "premium"]:
        raise HTTPException(status_code=400, detail="Invalid subscription")
    
    result = await db.users.update_one(
        {"user_id": user_id},
        {"$set": {"subscription": new_subscription}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "Subscription updated successfully"}

# ==================== CATEGORY ENDPOINTS ====================

@api_router.get("/categories")
async def get_categories(request: Request):
    user = await require_auth(request)
    categories = await db.categories.find({}, {"_id": 0}).to_list(1000)
    return [Category(**cat) for cat in categories]

@api_router.post("/categories")
async def create_category(request: Request, category: CategoryCreate):
    user = await require_teacher(request)
    category_id = f"cat_{uuid.uuid4().hex[:12]}"
    category_data = {
        **category.model_dump(),
        "category_id": category_id,
        "created_at": datetime.now(timezone.utc)
    }
    await db.categories.insert_one(category_data)
    return Category(**category_data)

@api_router.put("/categories/{category_id}")
async def update_category(request: Request, category_id: str, category: CategoryCreate):
    user = await require_teacher(request)
    result = await db.categories.update_one(
        {"category_id": category_id},
        {"$set": category.model_dump()}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Category not found")
    updated = await db.categories.find_one({"category_id": category_id}, {"_id": 0})
    return Category(**updated)

@api_router.delete("/categories/{category_id}")
async def delete_category(request: Request, category_id: str):
    await require_super_admin(request)
    result = await db.categories.delete_one({"category_id": category_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Category not found")
    await db.words.delete_many({"category_id": category_id})
    return {"message": "Category deleted successfully"}

# ==================== WORD ENDPOINTS ====================

@api_router.get("/words")
async def get_words(request: Request, category_id: Optional[str] = None):
    user = await require_auth(request)
    query = {}
    if category_id:
        query["category_id"] = category_id
    words = await db.words.find(query, {"_id": 0}).to_list(10000)
    return [Word(**word) for word in words]

@api_router.post("/words")
async def create_word(request: Request, word: WordCreate):
    user = await require_teacher(request)
    word_id = f"word_{uuid.uuid4().hex[:12]}"
    word_data = {
        **word.model_dump(),
        "word_id": word_id,
        "created_at": datetime.now(timezone.utc),
        "ai_generated": False
    }
    await db.words.insert_one(word_data)
    await db.categories.update_one(
        {"category_id": word.category_id},
        {"$inc": {"word_count": 1}}
    )
    return Word(**word_data)

@api_router.post("/words/ai-example")
async def generate_ai_example(request: Request, ai_request: AIExampleRequest):
    user = await require_auth(request)
    if user.subscription not in ["standard", "premium"] and user.role != "super_admin":
        raise HTTPException(status_code=403, detail="Premium subscription required for AI features")
    
    api_key = os.environ.get("EMERGENT_LLM_KEY")
    chat = LlmChat(
        api_key=api_key,
        session_id=f"ai_{user.user_id}_{uuid.uuid4().hex[:8]}",
        system_message=f"You are a language learning assistant. Generate natural, {ai_request.level}-level example sentences for vocabulary words. Keep sentences simple and practical for language learners."
    ).with_model("gemini", "gemini-2.5-flash")
    
    tr_message = UserMessage(
        text=f"Create a simple {ai_request.level}-level Turkish sentence using the word '{ai_request.word_turkish}'. Only provide the sentence, nothing else."
    )
    example_tr = await chat.send_message(tr_message)
    
    ru_message = UserMessage(
        text=f"Create a simple {ai_request.level}-level Russian sentence using the word '{ai_request.word_russian}'. Only provide the sentence, nothing else."
    )
    example_ru = await chat.send_message(ru_message)
    
    return AIExampleResponse(
        example_tr=example_tr.strip(),
        example_ru=example_ru.strip()
    )

@api_router.put("/words/{word_id}")
async def update_word(request: Request, word_id: str, word: WordCreate):
    user = await require_teacher(request)
    result = await db.words.update_one(
        {"word_id": word_id},
        {"$set": word.model_dump()}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Word not found")
    updated = await db.words.find_one({"word_id": word_id}, {"_id": 0})
    return Word(**updated)

@api_router.delete("/words/{word_id}")
async def delete_word(request: Request, word_id: str):
    await require_super_admin(request)
    word = await db.words.find_one({"word_id": word_id}, {"_id": 0})
    if not word:
        raise HTTPException(status_code=404, detail="Word not found")
    result = await db.words.delete_one({"word_id": word_id})
    await db.categories.update_one(
        {"category_id": word["category_id"]},
        {"$inc": {"word_count": -1}}
    )
    return {"message": "Word deleted successfully"}

# ==================== PROGRESS ENDPOINTS ====================

@api_router.get("/progress")
async def get_progress(request: Request):
    user = await require_auth(request)
    progress = await db.user_progress.find(
        {"user_id": user.user_id},
        {"_id": 0}
    ).to_list(10000)
    return progress

@api_router.post("/progress/{word_id}/review")
async def review_word(request: Request, word_id: str, body: dict):
    user = await require_auth(request)
    correct = body.get("correct", False)
    
    progress = await db.user_progress.find_one(
        {"user_id": user.user_id, "word_id": word_id},
        {"_id": 0}
    )
    
    if not progress:
        progress = {
            "user_id": user.user_id,
            "word_id": word_id,
            "last_reviewed": datetime.now(timezone.utc),
            "next_review": datetime.now(timezone.utc) + timedelta(days=1),
            "correct_count": 1 if correct else 0,
            "incorrect_count": 0 if correct else 1,
            "mastery": 10 if correct else 0,
            "interval_days": 1
        }
        await db.user_progress.insert_one(progress)
    else:
        interval = progress.get("interval_days", 1)
        if correct:
            new_interval = min(interval * 2, 30)
            mastery_change = 10
        else:
            new_interval = 1
            mastery_change = -5
        
        new_mastery = max(0, min(100, progress.get("mastery", 0) + mastery_change))
        next_review = datetime.now(timezone.utc) + timedelta(days=new_interval)
        
        await db.user_progress.update_one(
            {"user_id": user.user_id, "word_id": word_id},
            {
                "$set": {
                    "last_reviewed": datetime.now(timezone.utc),
                    "next_review": next_review,
                    "interval_days": new_interval,
                    "mastery": new_mastery
                },
                "$inc": {
                    "correct_count": 1 if correct else 0,
                    "incorrect_count": 0 if correct else 1
                }
            }
        )
    
    words_learned = await db.user_progress.count_documents({
        "user_id": user.user_id,
        "mastery": {"$gte": 50}
    })
    await db.users.update_one(
        {"user_id": user.user_id},
        {"$set": {"words_learned": words_learned}}
    )
    return {"message": "Progress updated", "correct": correct}

@api_router.get("/progress/due")
async def get_due_words(request: Request):
    user = await require_auth(request)
    due_progress = await db.user_progress.find(
        {
            "user_id": user.user_id,
            "next_review": {"$lte": datetime.now(timezone.utc)}
        },
        {"_id": 0}
    ).to_list(1000)
    return due_progress

# Include routers
app.include_router(api_router)
app.include_router(progress_router, prefix="/api")
app.include_router(user_content_router, prefix="/api")
api_router.include_router(teacher_router)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()

logger.info("YLM Sözlük API started successfully")