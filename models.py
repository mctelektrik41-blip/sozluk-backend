from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime
import uuid

# Super admin email addresses - hardcoded
SUPER_ADMIN_EMAILS = [
    "mctelektrik41@gmail.com",
    "e-turkrut@yandex.ru"
]

def is_super_admin(email: str) -> bool:
    """Check if email is a super admin"""
    return email.lower() in [e.lower() for e in SUPER_ADMIN_EMAILS]

# User Models
class UserBase(BaseModel):
    user_id: str
    email: EmailStr
    name: str
    picture: Optional[str] = None
    role: str = "student"  # student, teacher, super_admin
    subscription: str = "free"  # free, basic, standard, premium
    language_preference: str = "tr-ru"  # tr-ru or ru-tr
    created_at: datetime
    words_learned: int = 0
    streak: int = 0
    progress: float = 0.0
    hashed_password: Optional[str] = None
    assigned_students: Optional[list] = []

class User(UserBase):
    model_config = {"extra": "ignore"}

class UserSession(BaseModel):
    user_id: str
    session_token: str
    expires_at: datetime
    created_at: datetime

# Category Models
class CategoryBase(BaseModel):
    name_tr: str
    name_ru: str
    icon: str
    level: str  # A1, A2, B1, B2, C1, C2
    color: str
    word_count: int = 0
    created_by: str  # user_id of teacher/admin

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    category_id: str
    created_at: datetime

# Word Models
class WordBase(BaseModel):
    turkish: str
    russian: str
    pronunciation: str
    example_tr: str
    example_ru: str
    image_url: str
    level: str
    category_id: str
    created_by: str  # user_id of teacher/admin

class WordCreate(WordBase):
    pass

class Word(WordBase):
    word_id: str
    created_at: datetime
    ai_generated: bool = False

# Progress Models
class UserProgress(BaseModel):
    user_id: str
    word_id: str
    last_reviewed: datetime
    next_review: datetime
    correct_count: int = 0
    incorrect_count: int = 0
    mastery: float = 0.0  # 0-100
    interval_days: int = 1  # Spaced repetition interval

# AI Generation Models
class AIExampleRequest(BaseModel):
    word_turkish: str


# Progress Models
class UserProgress(BaseModel):
    progress_id: str = Field(default_factory=lambda: f"prog_{uuid.uuid4().hex[:12]}")
    user_id: str
    word_id: str
    category_id: str
    learned: bool = False
    correct_count: int = 0
    incorrect_count: int = 0
    level: int = 0  # 0-5, 5 means mastered
    last_reviewed: Optional[datetime] = None
    next_review: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

class ProgressUpdate(BaseModel):
    word_id: str
    correct: bool

class ProgressStats(BaseModel):
    total_words: int
    words_learned: int
    words_in_progress: int
    accuracy: float
    streak: int
    categories_progress: List[dict]
    recent_activity: List[dict]

    word_russian: str
    level: str

class AIExampleResponse(BaseModel):
    example_tr: str
    example_ru: str

# Admin Models
class UserManagementRequest(BaseModel):
    user_id: str
    action: str  # promote_teacher, demote_teacher, change_subscription
    new_value: Optional[str] = None

class TeacherAssignment(BaseModel):
    teacher_email: EmailStr
    name: str
    subscription: str = "premium"  # Teachers get premium by default
