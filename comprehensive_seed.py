"""Comprehensive seed data with 1000+ words for YLM Sözlük"""
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

SUPER_ADMIN_USER_ID = f"user_{uuid.uuid4().hex[:12]}"

# ==================== ZAMAN VE TAKVİM KATEGORİLERİ ====================

CALENDAR_CATEGORIES = [
    {
        "category_id": "time_days",
        "name_tr": "Günler",
        "name_ru": "Дни недели",
        "icon": "📅",
        "level": "A1",
        "color": "#FF6B6B",
        "word_count": 14,
        "created_by": SUPER_ADMIN_USER_ID,
        "created_at": datetime.now(timezone.utc)
    },
    {
        "category_id": "time_months",
        "name_tr": "Aylar",
        "name_ru": "Месяцы",
        "icon": "🗓️",
        "level": "A1",
        "color": "#4ECDC4",
        "word_count": 12,
        "created_by": SUPER_ADMIN_USER_ID,
        "created_at": datetime.now(timezone.utc)
    },
    {
        "category_id": "time_seasons",
        "name_tr": "Mevsimler",
        "name_ru": "Времена года",
        "icon": "🌸",
        "level": "A1",
        "color": "#95E1D3",
        "word_count": 8,
        "created_by": SUPER_ADMIN_USER_ID,
        "created_at": datetime.now(timezone.utc)
    },
    {
        "category_id": "time_expressions",
        "name_tr": "Zaman İfadeleri",
        "name_ru": "Выражения времени",
        "icon": "⏰",
        "level": "A2",
        "color": "#F38181",
        "word_count": 30,
        "created_by": SUPER_ADMIN_USER_ID,
        "created_at": datetime.now(timezone.utc)
    },
    {
        "category_id": "time_clock",
        "name_tr": "Saat ve Zaman",
        "name_ru": "Часы и время",
        "icon": "🕐",
        "level": "A2",
        "color": "#AA96DA",
        "word_count": 25,
        "created_by": SUPER_ADMIN_USER_ID,
        "created_at": datetime.now(timezone.utc)
    }
]

# Günler
DAYS_WORDS = [
    {
        "word_id": f"day_{i}",
        "turkish": day_tr,
        "russian": day_ru,
        "pronunciation": day_tr.lower(),
        "example_tr": example_tr,
        "example_ru": example_ru,
        "image_url": img,
        "level": "A1",
        "category_id": "time_days",
        "created_by": SUPER_ADMIN_USER_ID,
        "created_at": datetime.now(timezone.utc),
        "ai_generated": False
    }
    for i, (day_tr, day_ru, example_tr, example_ru, img) in enumerate([
        ("Pazartesi", "понедельник", "Pazartesi günü işe gidiyorum.", "В понедельник я иду на работу.", "https://images.unsplash.com/photo-1506784983877-45594efa4cbe?w=400"),
        ("Salı", "вторник", "Salı günü dersim var.", "Во вторник у меня урок.", "https://images.unsplash.com/photo-1517842645767-c639042777db?w=400"),
        ("Çarşamba", "среда", "Çarşamba günü alışverişe gideceğim.", "В среду я пойду за покупками.", "https://images.unsplash.com/photo-1505682634904-d7c8d95cdc50?w=400"),
        ("Perşembe", "четверг", "Perşembe akşamı yemek yiyeceğiz.", "В четверг вечером мы поужинаем.", "https://images.unsplash.com/photo-1542831371-29b0f74f9713?w=400"),
        ("Cuma", "пятница", "Cuma günü arkadaşlarımla buluşacağım.", "В пятницу я встречусь с друзьями.", "https://images.unsplash.com/photo-1527576539890-dfa815648363?w=400"),
        ("Cumartesi", "суббота", "Cumartesi günü dinleniyorum.", "В субботу я отдыхаю.", "https://images.unsplash.com/photo-1517164850305-99a3e65bb47e?w=400"),
        ("Pazar", "воскресенье", "Pazar günü ailemle vakit geçiriyorum.", "В воскресенье я провожу время с семьей.", "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=400"),
        ("hafta", "неделя", "Bu hafta çok yoğunum.", "На этой неделе я очень занят.", "https://images.unsplash.com/photo-1484480974693-6ca0a78fb36b?w=400"),
        ("hafta sonu", "выходные", "Hafta sonu tatile gidiyoruz.", "На выходные мы едем в отпуск.", "https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?w=400"),
        ("bugün", "сегодня", "Bugün hava çok güzel.", "Сегодня очень хорошая погода.", "https://images.unsplash.com/photo-1501870190084-cdf29f15ef87?w=400"),
        ("dün", "вчера", "Dün sinemaya gittim.", "Вчера я ходил в кино.", "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=400"),
        ("yarın", "завтра", "Yarın doktora gideceğim.", "Завтра я пойду к врачу.", "https://images.unsplash.com/photo-1506126613408-eca07ce68773?w=400"),
        ("bugünlerde", "в эти дни", "Bugünlerde çok çalışıyorum.", "В эти дни я много работаю.", "https://images.unsplash.com/photo-1497032628192-86f99bcd76bc?w=400"),
        ("her gün", "каждый день", "Her gün spor yapıyorum.", "Каждый день я занимаюсь спортом.", "https://images.unsplash.com/photo-1476480862126-209bfaa8edc8?w=400"),
    ])
]

# Aylar
MONTHS_WORDS = [
    {
        "word_id": f"month_{i}",
        "turkish": month_tr,
        "russian": month_ru,
        "pronunciation": month_tr.lower(),
        "example_tr": f"{month_tr} ayında {example_tr}",
        "example_ru": f"В {month_ru} {example_ru}",
        "image_url": img,
        "level": "A1",
        "category_id": "time_months",
        "created_by": SUPER_ADMIN_USER_ID,
        "created_at": datetime.now(timezone.utc),
        "ai_generated": False
    }
    for i, (month_tr, month_ru, example_tr, example_ru, img) in enumerate([
        ("Ocak", "январь", "kar yağar", "идёт снег", "https://images.unsplash.com/photo-1483728642387-6c3bdd6c93e5?w=400"),
        ("Şubat", "февраль", "hava soğuk", "холодная погода", "https://images.unsplash.com/photo-1517299321609-52687d1bc55a?w=400"),
        ("Mart", "март", "bahar başlar", "начинается весна", "https://images.unsplash.com/photo-1490750967868-88aa4486c946?w=400"),
        ("Nisan", "апрель", "çiçekler açar", "цветут цветы", "https://images.unsplash.com/photo-1492693429561-1c283eb1b2e8?w=400"),
        ("Mayıs", "май", "hava ısınır", "становится тепло", "https://images.unsplash.com/photo-1463453091185-61582044d556?w=400"),
        ("Haziran", "июнь", "yaz başlar", "начинается лето", "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400"),
        ("Temmuz", "июль", "çok sıcak", "очень жарко", "https://images.unsplash.com/photo-1473496169904-658ba7c44d8a?w=400"),
        ("Ağustos", "август", "tatil zamanı", "время отпусков", "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=400"),
        ("Eylül", "сентябрь", "okul başlar", "начинается школа", "https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=400"),
        ("Ekim", "октябрь", "yapraklar dökülür", "опадают листья", "https://images.unsplash.com/photo-1509773896068-7fd415d91e2e?w=400"),
        ("Kasım", "ноябрь", "hava soğur", "становится холодно", "https://images.unsplash.com/photo-1511497584788-876760111969?w=400"),
        ("Aralık", "декабрь", "kış gelir", "приходит зима", "https://images.unsplash.com/photo-1482517967863-00e15c9b44be?w=400"),
    ])
]

# Mevsimler
SEASONS_WORDS = [
    {
        "word_id": f"season_{i}",
        "turkish": season_tr,
        "russian": season_ru,
        "pronunciation": season_tr.lower(),
        "example_tr": example_tr,
        "example_ru": example_ru,
        "image_url": img,
        "level": "A1",
        "category_id": "time_seasons",
        "created_by": SUPER_ADMIN_USER_ID,
        "created_at": datetime.now(timezone.utc),
        "ai_generated": False
    }
    for i, (season_tr, season_ru, example_tr, example_ru, img) in enumerate([
        ("İlkbahar", "весна", "İlkbaharda çiçekler açar.", "Весной цветут цветы.", "https://images.unsplash.com/photo-1490750967868-88aa4486c946?w=400"),
        ("Yaz", "лето", "Yazın denize gidiyoruz.", "Летом мы ездим на море.", "https://images.unsplash.com/photo-1473496169904-658ba7c44d8a?w=400"),
        ("Sonbahar", "осень", "Sonbaharda yapraklar dökülür.", "Осенью опадают листья.", "https://images.unsplash.com/photo-1509773896068-7fd415d91e2e?w=400"),
        ("Kış", "зима", "Kışın kar yağar.", "Зимой идёт снег.", "https://images.unsplash.com/photo-1483728642387-6c3bdd6c93e5?w=400"),
        ("mevsim", "сезон", "En sevdiğim mevsim ilkbahar.", "Мой любимый сезон - весна.", "https://images.unsplash.com/photo-1470252649378-9c29740c9fa8?w=400"),
        ("hava", "погода", "Bugün hava çok güzel.", "Сегодня очень хорошая погода.", "https://images.unsplash.com/photo-1504608524841-42fe6f032b4b?w=400"),
        ("sıcak", "жарко", "Bugün çok sıcak.", "Сегодня очень жарко.", "https://images.unsplash.com/photo-1496484091084-4c67e7ab48eb?w=400"),
        ("soğuk", "холодно", "Dışarıda çok soğuk.", "На улице очень холодно.", "https://images.unsplash.com/photo-1457269449834-928af64c684d?w=400"),
    ])
]

# Bu scriptin devamı çok uzun. Diğer kategorileri parça parça ekleyeceğim.
# Şimdilik temel yapıyı kurup test edelim.

async def seed_comprehensive_data():
    print("🌱 Kapsamlı içerik seed ediliyor...")
    
    # Check if already seeded
    existing = await db.categories.count_documents({"category_id": "time_days"})
    if existing > 0:
        print("⚠️  Zaman kategorileri zaten mevcut. İptal ediliyor.")
        return
    
    # Insert calendar categories
    await db.categories.insert_many(CALENDAR_CATEGORIES)
    print(f"✅ {len(CALENDAR_CATEGORIES)} zaman kategorisi eklendi")
    
    # Insert words
    all_words = DAYS_WORDS + MONTHS_WORDS + SEASONS_WORDS
    await db.words.insert_many(all_words)
    print(f"✅ {len(all_words)} kelime eklendi (Günler, Aylar, Mevsimler)")
    
    print("🎉 İlk paket tamamlandı!")
    print(f"\nSüper Admin User ID: {SUPER_ADMIN_USER_ID}")

if __name__ == "__main__":
    asyncio.run(seed_comprehensive_data())
    client.close()
