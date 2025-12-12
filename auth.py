from fastapi import HTTPException, Request
from typing import Optional
from datetime import datetime, timezone, timedelta
import os
import uuid
from motor.motor_asyncio import AsyncIOMotorClient
import aiohttp
from dotenv import load_dotenv
from pathlib import Path
from models import User, UserSession, SUPER_ADMIN_EMAILS, is_super_admin
from passlib.context import CryptContext
from jose import JWTError, jwt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.environ.get("SECRET_KEY", "ylm-sozluk-secret-key-2024")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 7

# Load environment variables
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

AUTH_API_URL = "https://demobackend.emergentagent.com/auth/v1/env/oauth/session-data"

async def get_session_data(session_id: str) -> dict:
    """Get user data from Emergent Auth API"""
    headers = {"X-Session-ID": session_id}
    async with aiohttp.ClientSession() as session:
        async with session.get(AUTH_API_URL, headers=headers) as response:
            if response.status != 200:
                raise HTTPException(status_code=401, detail="Invalid session ID")
            return await response.json()

async def create_or_update_user(auth_data: dict) -> User:
    """Create new user or update existing user"""
    email = auth_data["email"]
    
    # Check if user exists
    existing_user = await db.users.find_one({"email": email}, {"_id": 0})
    
    if existing_user:
        # Update existing user
        user = User(**existing_user)
        # Update name and picture if changed
        await db.users.update_one(
            {"email": email},
            {"$set": {
                "name": auth_data["name"],
                "picture": auth_data["picture"]
            }}
        )
    else:
        # Create new user
        user_id = f"user_{uuid.uuid4().hex[:12]}"
        
        # Determine role based on email
        role = "super_admin" if is_super_admin(email) else "student"
        subscription = "premium" if role == "super_admin" else "free"
        
        user_data = {
            "user_id": user_id,
            "email": email,
            "name": auth_data["name"],
            "picture": auth_data["picture"],
            "role": role,
            "subscription": subscription,
            "language_preference": "tr-ru",
            "created_at": datetime.now(timezone.utc),
            "words_learned": 0,
            "streak": 0,
            "progress": 0.0
        }
        
        await db.users.insert_one(user_data)
        user = User(**user_data)
    
    return user

async def create_session(user_id: str, session_token: str) -> UserSession:
    """Create new session in database"""
    # Check if session already exists
    existing_session = await db.user_sessions.find_one({"session_token": session_token}, {"_id": 0})
    if existing_session:
        return UserSession(**existing_session)
    
    # Create new session
    expires_at = datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(days=7)
    session_data = {
        "user_id": user_id,
        "session_token": session_token,
        "expires_at": expires_at,
        "created_at": datetime.now(timezone.utc)
    }
    
    await db.user_sessions.insert_one(session_data)
    return UserSession(**session_data)

async def get_current_user(request: Request) -> Optional[User]:
    """Get current user from session token or JWT"""
    # Try JWT token from Authorization header first
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        user = await get_current_user_from_token(token)
        if user:
            return user
    
    # Try cookie
    session_token = request.cookies.get("session_token")
    
    # Fallback to Authorization header
    if not session_token:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            session_token = auth_header.replace("Bearer ", "")
    
    if not session_token:
        return None
    
    # Find session in database
    session_doc = await db.user_sessions.find_one({"session_token": session_token}, {"_id": 0})
    if not session_doc:
        return None
    
    # Check expiration
    expires_at = session_doc["expires_at"]
    if isinstance(expires_at, str):
        expires_at = datetime.fromisoformat(expires_at)
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)
    
    if expires_at < datetime.now(timezone.utc):
        # Delete expired session
        await db.user_sessions.delete_one({"session_token": session_token})
        return None
    
    # Get user
    user_doc = await db.users.find_one({"user_id": session_doc["user_id"]}, {"_id": 0})
    if not user_doc:
        return None
    
    return User(**user_doc)

async def require_auth(request: Request) -> User:
    """Require authentication - raise exception if not authenticated"""
    user = await get_current_user(request)
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user

async def require_teacher(request: Request) -> User:
    """Require teacher or admin role"""
    user = await require_auth(request)
    if user.role not in ["teacher", "super_admin"]:
        raise HTTPException(status_code=403, detail="Teacher access required")
    return user

async def require_super_admin(request: Request) -> User:
    """Require super admin role"""
    user = await require_auth(request)
    if user.role != "super_admin":
        raise HTTPException(status_code=403, detail="Super admin access required")
    return user


# ==================== JWT TOKEN FUNCTIONS ====================

def verify_password(plain_password, hashed_password):
    """Verify a password against a hash"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """Hash a password"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def authenticate_user(email: str, password: str):
    """Authenticate user with email and password"""
    user_doc = await db.users.find_one({"email": email}, {"_id": 0})
    if not user_doc:
        return False
    if not verify_password(password, user_doc.get("hashed_password", "")):
        return False
    return User(**user_doc)

async def get_current_user_from_token(token: str) -> Optional[User]:
    """Get user from JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            return None
    except JWTError:
        return None
    
    user_doc = await db.users.find_one({"email": email}, {"_id": 0})
    if user_doc is None:
        return None
    return User(**user_doc)

