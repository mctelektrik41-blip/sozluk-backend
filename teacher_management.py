"""Teacher management endpoints for student tracking and subscription management"""
from fastapi import APIRouter, Request, HTTPException
from typing import List
from datetime import datetime, timezone
from models import User
from auth import require_teacher, require_super_admin
import os
from motor.motor_asyncio import AsyncIOMotorClient

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

teacher_router = APIRouter(prefix="/teacher")

# ==================== STUDENT MANAGEMENT ====================

@teacher_router.get("/my-students")
async def get_my_students(request: Request):
    """Get all students assigned to this teacher"""
    teacher = await require_teacher(request)
    
    # Get students assigned to this teacher
    students = await db.users.find(
        {"assigned_teacher": teacher.user_id, "role": "student"},
        {"_id": 0}
    ).to_list(1000)
    
    # Get progress for each student
    student_data = []
    for student in students:
        # Get student's progress
        progress_count = await db.user_progress.count_documents({"user_id": student["user_id"]})
        mastered_count = await db.user_progress.count_documents({
            "user_id": student["user_id"],
            "mastery": {"$gte": 80}
        })
        
        student_data.append({
            **student,
            "total_words_studied": progress_count,
            "mastered_words": mastered_count,
            "last_activity": student.get("last_activity", None)
        })
    
    return student_data

@teacher_router.post("/assign-student")
async def assign_student_to_teacher(request: Request, body: dict):
    """Assign a student to teacher by email"""
    teacher = await require_teacher(request)
    student_email = body.get("student_email")
    
    if not student_email:
        raise HTTPException(status_code=400, detail="student_email required")
    
    # Find student
    student = await db.users.find_one({"email": student_email}, {"_id": 0})
    
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    if student.get("role") != "student":
        raise HTTPException(status_code=400, detail="User is not a student")
    
    # Assign teacher
    await db.users.update_one(
        {"email": student_email},
        {"$set": {"assigned_teacher": teacher.user_id}}
    )
    
    return {"message": "Student assigned successfully", "student": student}

@teacher_router.post("/grant-premium/{student_id}")
async def grant_premium_to_student(request: Request, student_id: str, body: dict):
    """Grant premium subscription to a student (Teacher/Admin only)"""
    teacher = await require_teacher(request)
    
    subscription_type = body.get("subscription", "premium")
    duration_days = body.get("duration_days", 365)  # Default 1 year
    
    # Check if student exists
    student = await db.users.find_one({"user_id": student_id}, {"_id": 0})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # For regular teachers, only allow students assigned to them
    if teacher.role == "teacher":
        if student.get("assigned_teacher") != teacher.user_id:
            raise HTTPException(status_code=403, detail="Student not assigned to you")
    
    # Update subscription
    expires_at = datetime.now(timezone.utc).replace(hour=23, minute=59, second=59)
    from datetime import timedelta
    expires_at = expires_at + timedelta(days=duration_days)
    
    await db.users.update_one(
        {"user_id": student_id},
        {
            "$set": {
                "subscription": subscription_type,
                "subscription_granted_by": teacher.user_id,
                "subscription_expires_at": expires_at,
                "subscription_granted_at": datetime.now(timezone.utc)
            }
        }
    )
    
    return {
        "message": f"{subscription_type.upper()} granted successfully",
        "expires_at": expires_at.isoformat(),
        "duration_days": duration_days
    }

@teacher_router.get("/student-progress/{student_id}")
async def get_student_detailed_progress(request: Request, student_id: str):
    """Get detailed progress for a specific student"""
    teacher = await require_teacher(request)
    
    # Check student
    student = await db.users.find_one({"user_id": student_id}, {"_id": 0})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # For regular teachers, only allow students assigned to them
    if teacher.role == "teacher":
        if student.get("assigned_teacher") != teacher.user_id:
            raise HTTPException(status_code=403, detail="Student not assigned to you")
    
    # Get all progress
    all_progress = await db.user_progress.find(
        {"user_id": student_id},
        {"_id": 0}
    ).to_list(10000)
    
    # Get words for each progress
    progress_with_words = []
    for prog in all_progress:
        word = await db.words.find_one({"word_id": prog["word_id"]}, {"_id": 0})
        if word:
            category = await db.categories.find_one({"category_id": word["category_id"]}, {"_id": 0})
            progress_with_words.append({
                **prog,
                "word": word,
                "category": category
            })
    
    # Calculate stats by category
    category_stats = {}
    for item in progress_with_words:
        cat_id = item["category"]["category_id"]
        if cat_id not in category_stats:
            category_stats[cat_id] = {
                "category": item["category"],
                "total_words": 0,
                "mastered": 0,
                "in_progress": 0,
                "average_mastery": 0
            }
        
        category_stats[cat_id]["total_words"] += 1
        if item["mastery"] >= 80:
            category_stats[cat_id]["mastered"] += 1
        elif item["mastery"] >= 40:
            category_stats[cat_id]["in_progress"] += 1
    
    return {
        "student": student,
        "total_words": len(all_progress),
        "progress_details": progress_with_words,
        "category_stats": list(category_stats.values())
    }

@teacher_router.get("/dashboard-stats")
async def get_teacher_dashboard_stats(request: Request):
    """Get teacher dashboard statistics"""
    teacher = await require_teacher(request)
    
    # Get students count
    students_count = await db.users.count_documents({
        "assigned_teacher": teacher.user_id,
        "role": "student"
    })
    
    # Get active students (activity in last 7 days)
    from datetime import timedelta
    week_ago = datetime.now(timezone.utc) - timedelta(days=7)
    active_students = await db.users.count_documents({
        "assigned_teacher": teacher.user_id,
        "role": "student",
        "last_activity": {"$gte": week_ago}
    })
    
    # Get total words created by teacher
    words_created = await db.words.count_documents({"created_by": teacher.user_id})
    
    # Get categories created by teacher
    categories_created = await db.categories.count_documents({"created_by": teacher.user_id})
    
    return {
        "total_students": students_count,
        "active_students": active_students,
        "words_created": words_created,
        "categories_created": categories_created
    }

# ==================== ADMIN ENDPOINTS ====================

@teacher_router.get("/all-teachers")
async def get_all_teachers(request: Request):
    """Get all teachers (Admin only)"""
    await require_super_admin(request)
    
    teachers = await db.users.find(
        {"role": {"$in": ["teacher", "super_admin"]}},
        {"_id": 0}
    ).to_list(1000)
    
    return teachers

@teacher_router.get("/all-students")
async def get_all_students_admin(request: Request):
    """Get all students (Admin only)"""
    await require_super_admin(request)
    
    students = await db.users.find(
        {"role": "student"},
        {"_id": 0}
    ).to_list(10000)
    
    return students
