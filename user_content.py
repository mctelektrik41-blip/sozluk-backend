"""User-generated content endpoints for YLM Sözlük"""
from fastapi import APIRouter, HTTPException, Request
from typing import Optional
from datetime import datetime, timezone
from motor.motor_asyncio import AsyncIOMotorClient
from models import Word, WordCreate, Category, CategoryCreate
from auth import require_auth
import os
import uuid

router = APIRouter(prefix="/user-content", tags=["user-content"])

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]


def check_premium_access(user):
    """Check if user has premium/pro subscription"""
    subscription = user.subscription if hasattr(user, 'subscription') else 'free'
    if subscription not in ['premium', 'pro']:
        raise HTTPException(
            status_code=403,
            detail="Bu özellik sadece premium/pro kullanıcılar için geçerlidir. Lütfen aboneliğinizi yükseltin."
        )


@router.post("/words/create")
async def create_user_word(request: Request, word_data: dict):
    """Create a new word (premium users only)"""
    user = await require_auth(request)
    
    # Check premium access
    check_premium_access(user)
    
    # Validate required fields
    required_fields = ['turkish', 'russian', 'category_id']
    for field in required_fields:
        if field not in word_data or not word_data[field]:
            raise HTTPException(status_code=400, detail=f"{field} alanı zorunludur")
    
    # Check if category exists
    category = await db.categories.find_one({"category_id": word_data['category_id']}, {"_id": 0})
    if not category:
        raise HTTPException(status_code=404, detail="Kategori bulunamadı")
    
    # Create word
    word_id = f"word_{uuid.uuid4().hex[:12]}"
    new_word = {
        "word_id": word_id,
        "category_id": word_data['category_id'],
        "turkish": word_data['turkish'],
        "russian": word_data['russian'],
        "turkish_sentence": word_data.get('turkish_sentence', ''),
        "russian_sentence": word_data.get('russian_sentence', ''),
        "image_url": word_data.get('image_url', 'https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=400'),
        "audio_url_turkish": f"https://texttospeech.googleapis.com/v1/text:synthesize?text={word_data['turkish']}",
        "audio_url_russian": f"https://texttospeech.googleapis.com/v1/text:synthesize?text={word_data['russian']}",
        "created_by": user.user_id,
        "created_at": datetime.now(timezone.utc),
        "user_generated": True
    }
    
    await db.words.insert_one(new_word)
    
    # Update category word count
    await db.categories.update_one(
        {"category_id": word_data['category_id']},
        {"$inc": {"word_count": 1}}
    )
    
    return {
        "success": True,
        "word_id": word_id,
        "message": "Kelime başarıyla eklendi!"
    }


@router.get("/words/my-words")
async def get_my_words(request: Request):
    """Get user's own words"""
    user = await require_auth(request)
    
    # Get all words created by user
    my_words = await db.words.find({
        "created_by": user.user_id,
        "user_generated": True
    }, {"_id": 0}).to_list(10000)
    
    return {
        "count": len(my_words),
        "words": my_words
    }


@router.put("/words/{word_id}")
async def update_user_word(request: Request, word_id: str, word_data: dict):
    """Update user's own word"""
    user = await require_auth(request)
    
    # Check if word exists and belongs to user
    word = await db.words.find_one({"word_id": word_id}, {"_id": 0})
    if not word:
        raise HTTPException(status_code=404, detail="Kelime bulunamadı")
    
    # Check ownership (or super admin)
    if word.get("created_by") != user.user_id and user.role != "super_admin":
        raise HTTPException(status_code=403, detail="Bu kelimeyi düzenleme yetkiniz yok")
    
    # Update fields
    update_data = {}
    updatable_fields = ['turkish', 'russian', 'turkish_sentence', 'russian_sentence', 'image_url']
    for field in updatable_fields:
        if field in word_data:
            update_data[field] = word_data[field]
    
    if update_data:
        update_data['updated_at'] = datetime.now(timezone.utc)
        await db.words.update_one(
            {"word_id": word_id},
            {"$set": update_data}
        )
    
    return {
        "success": True,
        "message": "Kelime güncellendi!"
    }


@router.delete("/words/{word_id}")
async def delete_user_word(request: Request, word_id: str):
    """Delete user's own word"""
    user = await require_auth(request)
    
    # Check if word exists and belongs to user
    word = await db.words.find_one({"word_id": word_id}, {"_id": 0})
    if not word:
        raise HTTPException(status_code=404, detail="Kelime bulunamadı")
    
    # Check ownership (or super admin)
    if word.get("created_by") != user.user_id and user.role != "super_admin":
        raise HTTPException(status_code=403, detail="Bu kelimeyi silme yetkiniz yok")
    
    # Delete word
    await db.words.delete_one({"word_id": word_id})
    
    # Update category word count
    await db.categories.update_one(
        {"category_id": word.get("category_id")},
        {"$inc": {"word_count": -1}}
    )
    
    return {
        "success": True,
        "message": "Kelime silindi!"
    }


@router.post("/categories/create")
async def create_user_category(request: Request, category_data: dict):
    """Create a new category (premium users only)"""
    user = await require_auth(request)
    
    # Check premium access
    check_premium_access(user)
    
    # Validate required fields
    required_fields = ['name_tr', 'name_ru']
    for field in required_fields:
        if field not in category_data or not category_data[field]:
            raise HTTPException(status_code=400, detail=f"{field} alanı zorunludur")
    
    # Create category ID from name
    category_id = f"user_{user.user_id[:8]}_{category_data['name_tr'].lower().replace(' ', '_')}"
    
    # Check if category already exists
    existing = await db.categories.find_one({"category_id": category_id})
    if existing:
        raise HTTPException(status_code=400, detail="Bu isimde bir kategori zaten mevcut")
    
    # Create category
    new_category = {
        "category_id": category_id,
        "name_tr": category_data['name_tr'],
        "name_ru": category_data['name_ru'],
        "icon": category_data.get('icon', '📚'),
        "color": category_data.get('color', '#3B82F6'),
        "level": category_data.get('level', 'A1'),
        "word_count": 0,
        "created_by": user.user_id,
        "created_at": datetime.now(timezone.utc),
        "user_generated": True
    }
    
    await db.categories.insert_one(new_category)
    
    return {
        "success": True,
        "category_id": category_id,
        "message": "Kategori başarıyla oluşturuldu!"
    }


@router.get("/categories/my-categories")
async def get_my_categories(request: Request):
    """Get user's own categories"""
    user = await require_auth(request)
    
    # Get all categories created by user
    my_categories = await db.categories.find({
        "created_by": user.user_id,
        "user_generated": True
    }, {"_id": 0}).to_list(1000)
    
    return {
        "count": len(my_categories),
        "categories": my_categories
    }


@router.delete("/categories/{category_id}")
async def delete_user_category(request: Request, category_id: str):
    """Delete user's own category (and all its words)"""
    user = await require_auth(request)
    
    # Check if category exists and belongs to user
    category = await db.categories.find_one({"category_id": category_id}, {"_id": 0})
    if not category:
        raise HTTPException(status_code=404, detail="Kategori bulunamadı")
    
    # Check ownership (or super admin)
    if category.get("created_by") != user.user_id and user.role != "super_admin":
        raise HTTPException(status_code=403, detail="Bu kategoriyi silme yetkiniz yok")
    
    # Delete all words in category created by user
    await db.words.delete_many({
        "category_id": category_id,
        "created_by": user.user_id
    })
    
    # Delete category
    await db.categories.delete_one({"category_id": category_id})
    
    return {
        "success": True,
        "message": "Kategori ve kelimeleri silindi!"
    }
