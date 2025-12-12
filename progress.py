"""Progress tracking endpoints for YLM Sözlük"""
from fastapi import APIRouter, HTTPException, Request
from typing import List
from datetime import datetime, timezone, timedelta
from motor.motor_asyncio import AsyncIOMotorClient
from models import UserProgress, ProgressUpdate, ProgressStats
from auth import require_auth
import os

router = APIRouter(prefix="/progress", tags=["progress"])

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]


def calculate_next_review(level: int) -> datetime:
    """Calculate next review date based on spaced repetition"""
    intervals = {
        0: 0,      # Immediate review
        1: 1,      # 1 day
        2: 3,      # 3 days
        3: 7,      # 7 days
        4: 15,     # 15 days
        5: 30      # 30 days (mastered)
    }
    days = intervals.get(level, 0)
    return datetime.now(timezone.utc) + timedelta(days=days)


@router.post("/update")
async def update_progress(request: Request, progress_data: ProgressUpdate):
    """Update user progress after quiz/flashcard"""
    user = await require_auth(request)
    
    # Get the word to find category_id
    word = await db.words.find_one({"word_id": progress_data.word_id}, {"_id": 0})
    if not word:
        raise HTTPException(status_code=404, detail="Word not found")
    
    # Find existing progress
    existing = await db.user_progress.find_one({
        "user_id": user.user_id,
        "word_id": progress_data.word_id
    }, {"_id": 0})
    
    now = datetime.now(timezone.utc)
    
    if existing:
        # Update existing progress
        new_level = existing.get("level", 0)
        correct_count = existing.get("correct_count", 0)
        incorrect_count = existing.get("incorrect_count", 0)
        
        if progress_data.correct:
            correct_count += 1
            new_level = min(new_level + 1, 5)  # Max level 5
        else:
            incorrect_count += 1
            new_level = max(new_level - 1, 0)  # Min level 0
        
        learned = new_level >= 5
        next_review = calculate_next_review(new_level)
        
        await db.user_progress.update_one(
            {"user_id": user.user_id, "word_id": progress_data.word_id},
            {"$set": {
                "correct_count": correct_count,
                "incorrect_count": incorrect_count,
                "level": new_level,
                "learned": learned,
                "last_reviewed": now,
                "next_review": next_review,
                "updated_at": now
            }}
        )
    else:
        # Create new progress entry
        new_level = 1 if progress_data.correct else 0
        progress_entry = {
            "progress_id": f"prog_{user.user_id[:8]}_{progress_data.word_id[:8]}",
            "user_id": user.user_id,
            "word_id": progress_data.word_id,
            "category_id": word.get("category_id", ""),
            "learned": False,
            "correct_count": 1 if progress_data.correct else 0,
            "incorrect_count": 0 if progress_data.correct else 1,
            "level": new_level,
            "last_reviewed": now,
            "next_review": calculate_next_review(new_level),
            "created_at": now,
            "updated_at": now
        }
        await db.user_progress.insert_one(progress_entry)
    
    # Update user's overall stats
    total_learned = await db.user_progress.count_documents({
        "user_id": user.user_id,
        "learned": True
    })
    
    await db.users.update_one(
        {"user_id": user.user_id},
        {"$set": {"words_learned": total_learned}}
    )
    
    return {
        "success": True,
        "words_learned": total_learned,
        "message": "İlerleme kaydedildi" if progress_data.correct else "Tekrar dene!"
    }


@router.get("/stats")
async def get_progress_stats(request: Request):
    """Get user's progress statistics"""
    user = await require_auth(request)
    
    # Get all progress entries
    all_progress = await db.user_progress.find(
        {"user_id": user.user_id},
        {"_id": 0}
    ).to_list(10000)
    
    # Calculate stats
    total_words = len(all_progress)
    words_learned = len([p for p in all_progress if p.get("learned", False)])
    words_in_progress = total_words - words_learned
    
    # Calculate accuracy
    total_correct = sum(p.get("correct_count", 0) for p in all_progress)
    total_incorrect = sum(p.get("incorrect_count", 0) for p in all_progress)
    total_attempts = total_correct + total_incorrect
    accuracy = (total_correct / total_attempts * 100) if total_attempts > 0 else 0
    
    # Get category progress
    categories_dict = {}
    for p in all_progress:
        cat_id = p.get("category_id", "unknown")
        if cat_id not in categories_dict:
            categories_dict[cat_id] = {
                "total": 0,
                "learned": 0
            }
        categories_dict[cat_id]["total"] += 1
        if p.get("learned", False):
            categories_dict[cat_id]["learned"] += 1
    
    # Fetch category names
    categories_progress = []
    for cat_id, stats in categories_dict.items():
        cat = await db.categories.find_one({"category_id": cat_id}, {"_id": 0, "name_tr": 1, "name_ru": 1})
        if cat:
            categories_progress.append({
                "category_id": cat_id,
                "name_tr": cat.get("name_tr", ""),
                "name_ru": cat.get("name_ru", ""),
                "total": stats["total"],
                "learned": stats["learned"],
                "progress": (stats["learned"] / stats["total"] * 100) if stats["total"] > 0 else 0
            })
    
    # Get recent activity (last 10 reviews)
    recent = sorted(all_progress, key=lambda x: x.get("last_reviewed", datetime.min), reverse=True)[:10]
    recent_activity = []
    for r in recent:
        if r.get("last_reviewed"):
            word = await db.words.find_one({"word_id": r["word_id"]}, {"_id": 0, "turkish": 1, "russian": 1})
            if word:
                recent_activity.append({
                    "word_id": r["word_id"],
                    "turkish": word.get("turkish", ""),
                    "russian": word.get("russian", ""),
                    "level": r.get("level", 0),
                    "last_reviewed": r["last_reviewed"].isoformat()
                })
    
    # Calculate streak (simplified - days with any activity)
    user_data = await db.users.find_one({"user_id": user.user_id}, {"_id": 0})
    streak = user_data.get("streak", 0) if user_data else 0
    
    return {
        "total_words": total_words,
        "words_learned": words_learned,
        "words_in_progress": words_in_progress,
        "accuracy": round(accuracy, 1),
        "streak": streak,
        "categories_progress": categories_progress,
        "recent_activity": recent_activity
    }


@router.get("/words-to-review")
async def get_words_to_review(request: Request):
    """Get words that need to be reviewed (spaced repetition)"""
    user = await require_auth(request)
    
    now = datetime.now(timezone.utc)
    
    # Find words due for review
    progress_entries = await db.user_progress.find({
        "user_id": user.user_id,
        "learned": False,
        "next_review": {"$lte": now}
    }, {"_id": 0}).to_list(1000)
    
    # Get word details
    words_to_review = []
    for progress in progress_entries:
        word = await db.words.find_one({"word_id": progress["word_id"]}, {"_id": 0})
        if word:
            words_to_review.append({
                **word,
                "progress_level": progress.get("level", 0),
                "last_reviewed": progress.get("last_reviewed").isoformat() if progress.get("last_reviewed") else None
            })
    
    return {
        "count": len(words_to_review),
        "words": words_to_review
    }


@router.get("/learned-words")
async def get_learned_words(request: Request):
    """Get all learned words"""
    user = await require_auth(request)
    
    # Find learned words
    progress_entries = await db.user_progress.find({
        "user_id": user.user_id,
        "learned": True
    }, {"_id": 0}).to_list(10000)
    
    # Get word details
    learned_words = []
    for progress in progress_entries:
        word = await db.words.find_one({"word_id": progress["word_id"]}, {"_id": 0})
        if word:
            learned_words.append({
                **word,
                "mastered_at": progress.get("updated_at").isoformat() if progress.get("updated_at") else None
            })
    
    return {
        "count": len(learned_words),
        "words": learned_words
    }
