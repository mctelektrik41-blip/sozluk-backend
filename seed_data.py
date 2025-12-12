"""Seed mock data to MongoDB"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from pathlib import Path
import os
from datetime import datetime, timezone
import uuid

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Super admin user
SUPER_ADMIN_USER_ID = f"user_{uuid.uuid4().hex[:12]}"

CATEGORIES = [
    {
        "category_id": "cat1",
        "name_tr": "Sayılar",
        "name_ru": "Числа",
        "icon": "🔢",
        "level": "A1",
        "color": "#3B82F6",
        "word_count": 2,
        "created_by": SUPER_ADMIN_USER_ID,
        "created_at": datetime.now(timezone.utc)
    },
    {
        "category_id": "cat2",
        "name_tr": "Renkler",
        "name_ru": "Цвета",
        "icon": "🎨",
        "level": "A1",
        "color": "#EF4444",
        "word_count": 2,
        "created_by": SUPER_ADMIN_USER_ID,
        "created_at": datetime.now(timezone.utc)
    },
    {
        "category_id": "cat3",
        "name_tr": "Yiyecekler",
        "name_ru": "Еда",
        "icon": "🍕",
        "level": "A1",
        "color": "#10B981",
        "word_count": 2,
        "created_by": SUPER_ADMIN_USER_ID,
        "created_at": datetime.now(timezone.utc)
    },
    {
        "category_id": "cat4",
        "name_tr": "Aile",
        "name_ru": "Семья",
        "icon": "👨‍👩‍👧",
        "level": "A1",
        "color": "#F59E0B",
        "word_count": 2,
        "created_by": SUPER_ADMIN_USER_ID,
        "created_at": datetime.now(timezone.utc)
    },
    {
        "category_id": "cat5",
        "name_tr": "Günlük Konuşma",
        "name_ru": "Повседневный разговор",
        "icon": "💬",
        "level": "A2",
        "color": "#8B5CF6",
        "word_count": 0,
        "created_by": SUPER_ADMIN_USER_ID,
        "created_at": datetime.now(timezone.utc)
    },
    {
        "category_id": "cat6",
        "name_tr": "Meslekler",
        "name_ru": "Профессии",
        "icon": "💼",
        "level": "A2",
        "color": "#EC4899",
        "word_count": 0,
        "created_by": SUPER_ADMIN_USER_ID,
        "created_at": datetime.now(timezone.utc)
    }
]

WORDS = [
    {
        "word_id": "w1",
        "turkish": "bir",
        "russian": "один",
        "pronunciation": "bir",
        "example_tr": "Bir elma istiyorum.",
        "example_ru": "Я хочу одно яблоко.",
        "image_url": "https://images.unsplash.com/photo-1611735341450-74d61e660ad2?w=400",
        "level": "A1",
        "category_id": "cat1",
        "created_by": SUPER_ADMIN_USER_ID,
        "created_at": datetime.now(timezone.utc),
        "ai_generated": False
    },
    {
        "word_id": "w2",
        "turkish": "iki",
        "russian": "два",
        "pronunciation": "iki",
        "example_tr": "İki arkadaşım var.",
        "example_ru": "У меня два друга.",
        "image_url": "https://images.unsplash.com/photo-1581579438747-1dc8d17bbce4?w=400",
        "level": "A1",
        "category_id": "cat1",
        "created_by": SUPER_ADMIN_USER_ID,
        "created_at": datetime.now(timezone.utc),
        "ai_generated": False
    },
    {
        "word_id": "w3",
        "turkish": "kırmızı",
        "russian": "красный",
        "pronunciation": "kırmızı",
        "example_tr": "Kırmızı bir araba.",
        "example_ru": "Красная машина.",
        "image_url": "https://images.unsplash.com/photo-1511367461989-f85a21fda167?w=400",
        "level": "A1",
        "category_id": "cat2",
        "created_by": SUPER_ADMIN_USER_ID,
        "created_at": datetime.now(timezone.utc),
        "ai_generated": False
    },
    {
        "word_id": "w4",
        "turkish": "mavi",
        "russian": "синий",
        "pronunciation": "mavi",
        "example_tr": "Gökyüzü mavi.",
        "example_ru": "Небо синее.",
        "image_url": "https://images.unsplash.com/photo-1535320903710-d993d3d77d29?w=400",
        "level": "A1",
        "category_id": "cat2",
        "created_by": SUPER_ADMIN_USER_ID,
        "created_at": datetime.now(timezone.utc),
        "ai_generated": False
    },
    {
        "word_id": "w5",
        "turkish": "ekmek",
        "russian": "хлеб",
        "pronunciation": "ekmek",
        "example_tr": "Taze ekmek alıyorum.",
        "example_ru": "Я покупаю свежий хлеб.",
        "image_url": "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=400",
        "level": "A1",
        "category_id": "cat3",
        "created_by": SUPER_ADMIN_USER_ID,
        "created_at": datetime.now(timezone.utc),
        "ai_generated": False
    },
    {
        "word_id": "w6",
        "turkish": "su",
        "russian": "вода",
        "pronunciation": "su",
        "example_tr": "Su içiyorum.",
        "example_ru": "Я пью воду.",
        "image_url": "https://images.unsplash.com/photo-1548839140-29a749e1cf4d?w=400",
        "level": "A1",
        "category_id": "cat3",
        "created_by": SUPER_ADMIN_USER_ID,
        "created_at": datetime.now(timezone.utc),
        "ai_generated": False
    },
    {
        "word_id": "w7",
        "turkish": "anne",
        "russian": "мама",
        "pronunciation": "anne",
        "example_tr": "Annem evde.",
        "example_ru": "Моя мама дома.",
        "image_url": "https://images.unsplash.com/photo-1555252333-9f8e92e65df9?w=400",
        "level": "A1",
        "category_id": "cat4",
        "created_by": SUPER_ADMIN_USER_ID,
        "created_at": datetime.now(timezone.utc),
        "ai_generated": False
    },
    {
        "word_id": "w8",
        "turkish": "baba",
        "russian": "папа",
        "pronunciation": "baba",
        "example_tr": "Babam işte.",
        "example_ru": "Мой папа на работе.",
        "image_url": "https://images.unsplash.com/photo-1500917293891-ef795e70e1f6?w=400",
        "level": "A1",
        "category_id": "cat4",
        "created_by": SUPER_ADMIN_USER_ID,
        "created_at": datetime.now(timezone.utc),
        "ai_generated": False
    }
]

async def seed_data():
    print("🌱 Seeding data to MongoDB...")
    
    # Check if data already exists
    existing_categories = await db.categories.count_documents({})
    if existing_categories > 0:
        print(f"⚠️  Found {existing_categories} existing categories. Skipping seed.")
        return
    
    # Insert categories
    await db.categories.insert_many(CATEGORIES)
    print(f"✅ Inserted {len(CATEGORIES)} categories")
    
    # Insert words
    await db.words.insert_many(WORDS)
    print(f"✅ Inserted {len(WORDS)} words")
    
    print("🎉 Data seeding complete!")
    print(f"\nSuper Admin User ID: {SUPER_ADMIN_USER_ID}")
    print("This ID is used as created_by for all seeded content.")

if __name__ == "__main__":
    asyncio.run(seed_data())
    client.close()
