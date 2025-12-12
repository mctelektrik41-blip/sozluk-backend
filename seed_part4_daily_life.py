"""Part 4: Daily Life Categories - Comprehensive vocabulary"""
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

# ==================== GÜNLÜK HAYAT KATEGORİLERİ ====================

DAILY_LIFE_CATEGORIES = [
    {
        "category_id": "home_items",
        "name_tr": "Ev Eşyaları",
        "name_ru": "Предметы быта",
        "icon": "🏠",
        "level": "A1",
        "color": "#FF6B6B",
        "word_count": 50,
        "created_by": SUPER_ADMIN_USER_ID,
        "created_at": datetime.now(timezone.utc)
    },
    {
        "category_id": "school",
        "name_tr": "Okul",
        "name_ru": "Школа",
        "icon": "📚",
        "level": "A1",
        "color": "#4ECDC4",
        "word_count": 40,
        "created_by": SUPER_ADMIN_USER_ID,
        "created_at": datetime.now(timezone.utc)
    },
    {
        "category_id": "work_office",
        "name_tr": "İş ve Ofis",
        "name_ru": "Работа и офис",
        "icon": "💼",
        "level": "B1",
        "color": "#95E1D3",
        "word_count": 40,
        "created_by": SUPER_ADMIN_USER_ID,
        "created_at": datetime.now(timezone.utc)
    },
    {
        "category_id": "transport",
        "name_tr": "Ulaşım",
        "name_ru": "Транспорт",
        "icon": "🚗",
        "level": "A2",
        "color": "#F38181",
        "word_count": 35,
        "created_by": SUPER_ADMIN_USER_ID,
        "created_at": datetime.now(timezone.utc)
    },
    {
        "category_id": "health",
        "name_tr": "Sağlık",
        "name_ru": "Здоровье",
        "icon": "🏥",
        "level": "A2",
        "color": "#AA96DA",
        "word_count": 40,
        "created_by": SUPER_ADMIN_USER_ID,
        "created_at": datetime.now(timezone.utc)
    },
    {
        "category_id": "shopping",
        "name_tr": "Alışveriş",
        "name_ru": "Покупки",
        "icon": "🛍️",
        "level": "A2",
        "color": "#FCBAD3",
        "word_count": 35,
        "created_by": SUPER_ADMIN_USER_ID,
        "created_at": datetime.now(timezone.utc)
    },
    {
        "category_id": "sports",
        "name_tr": "Spor",
        "name_ru": "Спорт",
        "icon": "⚽",
        "level": "A2",
        "color": "#A8D8EA",
        "word_count": 35,
        "created_by": SUPER_ADMIN_USER_ID,
        "created_at": datetime.now(timezone.utc)
    },
    {
        "category_id": "technology",
        "name_tr": "Teknoloji",
        "name_ru": "Технология",
        "icon": "💻",
        "level": "B1",
        "color": "#FFCCCC",
        "word_count": 35,
        "created_by": SUPER_ADMIN_USER_ID,
        "created_at": datetime.now(timezone.utc)
    },
    {
        "category_id": "nature",
        "name_tr": "Doğa",
        "name_ru": "Природа",
        "icon": "🌳",
        "level": "A2",
        "color": "#B4E7CE",
        "word_count": 40,
        "created_by": SUPER_ADMIN_USER_ID,
        "created_at": datetime.now(timezone.utc)
    },
    {
        "category_id": "body_parts",
        "name_tr": "Vücut Kısımları",
        "name_ru": "Части тела",
        "icon": "👤",
        "level": "A1",
        "color": "#FFD93D",
        "word_count": 30,
        "created_by": SUPER_ADMIN_USER_ID,
        "created_at": datetime.now(timezone.utc)
    },
    {
        "category_id": "emotions",
        "name_tr": "Duygular",
        "name_ru": "Эмоции",
        "icon": "😊",
        "level": "A2",
        "color": "#C490E4",
        "word_count": 30,
        "created_by": SUPER_ADMIN_USER_ID,
        "created_at": datetime.now(timezone.utc)
    },
    {
        "category_id": "animals",
        "name_tr": "Hayvanlar",
        "name_ru": "Животные",
        "icon": "🐕",
        "level": "A1",
        "color": "#A5DD9B",
        "word_count": 40,
        "created_by": SUPER_ADMIN_USER_ID,
        "created_at": datetime.now(timezone.utc)
    },
    {
        "category_id": "clothes",
        "name_tr": "Kıyafetler",
        "name_ru": "Одежда",
        "icon": "👔",
        "level": "A1",
        "color": "#FFB6C1",
        "word_count": 35,
        "created_by": SUPER_ADMIN_USER_ID,
        "created_at": datetime.now(timezone.utc)
    },
    {
        "category_id": "city",
        "name_tr": "Şehir",
        "name_ru": "Город",
        "icon": "🏙️",
        "level": "A2",
        "color": "#87CEEB",
        "word_count": 35,
        "created_by": SUPER_ADMIN_USER_ID,
        "created_at": datetime.now(timezone.utc)
    }
]

# EV EŞYALARI - 50 kelime
HOME_ITEMS = [
    ("yatak", "кровать", "Rahat bir yatak.", "Удобная кровать.", "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?w=400"),
    ("yastık", "подушка", "Yumuşak yastık.", "Мягкая подушка.", "https://images.unsplash.com/photo-1584100936595-c0654b55a2e2?w=400"),
    ("battaniye", "одеяло", "Sıcak battaniye.", "Тёплое одеяло.", "https://images.unsplash.com/photo-1615800098779-1be32e60cca3?w=400"),
    ("dolap", "шкаф", "Büyük dolap.", "Большой шкаф.", "https://images.unsplash.com/photo-1595428774223-ef52624120d2?w=400"),
    ("ayna", "зеркало", "Duvarda ayna.", "Зеркало на стене.", "https://images.unsplash.com/photo-1621610015848-d53f1f7a2b5d?w=400"),
    ("lamba", "лампа", "Masa lambası.", "Настольная лампа.", "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=400"),
    ("saat", "часы", "Duvar saati.", "Настенные часы.", "https://images.unsplash.com/photo-1509048191080-d2984bad6ae5?w=400"),
    ("halı", "ковёр", "Renkli halı.", "Цветной ковёр.", "https://images.unsplash.com/photo-1600210491892-03d54c0aaf87?w=400"),
    ("perde", "штора", "Beyaz perde.", "Белая штора.", "https://images.unsplash.com/photo-1524498250077-390f9e378fc0?w=400"),
    ("sofra", "стол", "Yemek sofrası.", "Обеденный стол.", "https://images.unsplash.com/photo-1617098900591-3f90928e8c54?w=400"),
    ("tabak", "тарелка", "Beyaz tabak.", "Белая тарелка.", "https://images.unsplash.com/photo-1610563717043-1b1ab7d353cb?w=400"),
    ("bardak", "стакан", "Su bardağı.", "Стакан воды.", "https://images.unsplash.com/photo-1572635148818-ef6fd45eb394?w=400"),
    ("çatal", "вилка", "Metal çatal.", "Металлическая вилка.", "https://images.unsplash.com/photo-1595665593673-bf1ad72905c0?w=400"),
    ("bıçak", "нож", "Keskin bıçak.", "Острый нож.", "https://images.unsplash.com/photo-1591209356734-88616a9110f3?w=400"),
    ("kaşık", "ложка", "Çay kaşığı.", "Чайная ложка.", "https://images.unsplash.com/photo-1606858420509-b4e6c68f2091?w=400"),
    ("tencere", "кастрюля", "Büyük tencere.", "Большая кастрюля.", "https://images.unsplash.com/photo-1585515320310-259814833e62?w=400"),
    ("tava", "сковорода", "Teflon tava.", "Тефлоновая сковорода.", "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=400"),
    ("buzdolabı", "холодильник", "Büyük buzdolabı.", "Большой холодильник.", "https://images.unsplash.com/photo-1571175443880-49e1d25b2bc5?w=400"),
    ("fırın", "духовка", "Elektrikli fırın.", "Электрическая духовка.", "https://images.unsplash.com/photo-1574269909862-7e1d70bb8078?w=400"),
    ("mikrodalga", "микроволновка", "Hızlı mikrodalga.", "Быстрая микроволновка.", "https://images.unsplash.com/photo-1585659722983-3a675dabf23d?w=400"),
    ("çamaşır makinesi", "стиральная машина", "Yeni çamaşır makinesi.", "Новая стиральная машина.", "https://images.unsplash.com/photo-1626806787461-102c1bfaaea1?w=400"),
    ("süpürge", "пылесос", "Elektrikli süpürge.", "Электрический пылесос.", "https://images.unsplash.com/photo-1558317374-067fb5f30001?w=400"),
    ("deterjan", "моющее средство", "Çamaşır deterjanı.", "Стиральный порошок.", "https://images.unsplash.com/photo-1610557892470-55d9e80c0bce?w=400"),
    ("çöp kovası", "мусорное ведро", "Plastik çöp kovası.", "Пластиковое мусорное ведро.", "https://images.unsplash.com/photo-1610557892470-55d9e80c0bce?w=400"),
    ("lavabo", "раковина", "Banyo lavabоsu.", "Раковина в ванной.", "https://images.unsplash.com/photo-1552321270-db6e8e4b9dae?w=400"),
]

# OKUL - 40 kelime
SCHOOL_ITEMS = [
    ("öğrenci", "ученик/ученица", "Çalışkan öğrenci.", "Прилежный ученик.", "https://images.unsplash.com/photo-1523580494863-6f3031224c94?w=400"),
    ("sınıf", "класс", "Geniş sınıf.", "Просторный класс.", "https://images.unsplash.com/photo-1580582932707-520aed937b7b?w=400"),
    ("ders", "урок", "Rusça dersi.", "Урок русского языка.", "https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=400"),
    ("ödev", "домашнее задание", "Zor ödev.", "Трудное домашнее задание.", "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=400"),
    ("sınav", "экзамен", "Zor sınav.", "Трудный экзамен.", "https://images.unsplash.com/photo-1606326608606-aa0b62935f2b?w=400"),
    ("soru", "вопрос", "Kolay soru.", "Лёгкий вопрос.", "https://images.unsplash.com/photo-1516534775068-ba3e7458af70?w=400"),
    ("cevap", "ответ", "Doğru cevap.", "Правильный ответ.", "https://images.unsplash.com/photo-1484480974693-6ca0a78fb36b?w=400"),
    ("not", "оценка", "İyi not.", "Хорошая оценка.", "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=400"),
    ("karne", "табель", "Dönem karnesi.", "Табель за семестр.", "https://images.unsplash.com/photo-1516534775068-ba3e7458af70?w=400"),
    ("tatil", "каникулы", "Yaz tatili.", "Летние каникулы.", "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400"),
    ("teneffüs", "перемена", "Kısa teneffüs.", "Короткая перемена.", "https://images.unsplash.com/photo-1427504494785-3a9ca7044f45?w=400"),
    ("kantin", "столовая", "Okul kantini.", "Школьная столовая.", "https://images.unsplash.com/photo-1567521464027-f127ff144326?w=400"),
    ("okul çantası", "школьный рюкзак", "Ağır okul çantası.", "Тяжёлый школьный рюкзак.", "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400"),
    ("silgi", "ластик", "Beyaz silgi.", "Белый ластик.", "https://images.unsplash.com/photo-1611223235982-59876d5481ed?w=400"),
    ("cetvel", "линейка", "Plastik cetvel.", "Пластиковая линейка.", "https://images.unsplash.com/photo-1613056690214-da1b27e8bfa2?w=400"),
    ("kalemtıraş", "точилка", "Metal kalemtıraş.", "Металлическая точилка.", "https://images.unsplash.com/photo-1595246140625-573b715d11dc?w=400"),
    ("harita", "карта", "Dünya haritası.", "Карта мира.", "https://images.unsplash.com/photo-1524661135-423995f22d0b?w=400"),
    ("küre", "глобус", "Büyük küre.", "Большой глобус.", "https://images.unsplash.com/photo-1526778548025-fa2f459cd5c1?w=400"),
    ("tahta", "доска", "Beyaz tahta.", "Белая доска.", "https://images.unsplash.com/photo-1581452888884-0a3948158463?w=400"),
    ("tebeşir", "мел", "Renkli tebeşir.", "Цветной мел.", "https://images.unsplash.com/photo-1598197748967-b4fc7f830f15?w=400"),
]

# ULAŞIM - 35 kelime
TRANSPORT_ITEMS = [
    ("otobüs", "автобус", "Kalabalık otobüs.", "Переполненный автобус.", "https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?w=400"),
    ("metro", "метро", "Hızlı metro.", "Быстрое метро.", "https://images.unsplash.com/photo-1581950743684-0c74e09b6ea2?w=400"),
    ("tramvay", "трамвай", "Eski tramvay.", "Старый трамвай.", "https://images.unsplash.com/photo-1502920514313-52581002a659?w=400"),
    ("tren", "поезд", "Hızlı tren.", "Скоростной поезд.", "https://images.unsplash.com/photo-1474487548417-781cb71495f3?w=400"),
    ("uçak", "самолёт", "Büyük uçak.", "Большой самолёт.", "https://images.unsplash.com/photo-1436491865332-7a61a109cc05?w=400"),
    ("taksi", "такси", "Sarı taksi.", "Жёлтое такси.", "https://images.unsplash.com/photo-1449965408869-eaa3f722e40d?w=400"),
    ("bisiklet", "велосипед", "Yeni bisiklet.", "Новый велосипед.", "https://images.unsplash.com/photo-1485965120184-e220f721d03e?w=400"),
    ("motorsiklet", "мотоцикл", "Hızlı motorsiklet.", "Быстрый мотоцикл.", "https://images.unsplash.com/photo-1558981806-ec527fa84c39?w=400"),
    ("gemi", "корабль", "Büyük gemi.", "Большой корабль.", "https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=400"),
    ("vapur", "паром", "Yolcu vapuru.", "Пассажирский паром.", "https://images.unsplash.com/photo-1520483691742-bada60a1edd6?w=400"),
    ("durak", "остановка", "Otobüs durağı.", "Автобусная остановка.", "https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?w=400"),
    ("istasyon", "станция", "Tren istasyonu.", "Железнодорожная станция.", "https://images.unsplash.com/photo-1474487548417-781cb71495f3?w=400"),
    ("havalimanı", "аэропорт", "Uluslararası havalimanı.", "Международный аэропорт.", "https://images.unsplash.com/photo-1436491865332-7a61a109cc05?w=400"),
    ("bilet", "билет", "Tek yön bilet.", "Билет в один конец.", "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400"),
    ("yol", "дорога", "Geniş yol.", "Широкая дорога.", "https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?w=400"),
]

# Tüm kelimeleri birleştirip insert edeceğiz
async def seed_daily_life_data():
    print("🌱 Günlük hayat kategorileri seed ediliyor...")
    
    existing = await db.categories.count_documents({"category_id": "home_items"})
    if existing > 0:
        print("⚠️  Günlük hayat kategorileri zaten mevcut.")
        return
    
    # Insert categories
    await db.categories.insert_many(DAILY_LIFE_CATEGORIES)
    print(f"✅ {len(DAILY_LIFE_CATEGORIES)} günlük hayat kategorisi eklendi")
    
    # Prepare words
    all_words = []
    
    # Home items
    for i, (tr, ru, ex_tr, ex_ru, img) in enumerate(HOME_ITEMS):
        all_words.append({
            "word_id": f"home_{i}",
            "turkish": tr,
            "russian": ru,
            "pronunciation": tr.lower(),
            "example_tr": ex_tr,
            "example_ru": ex_ru,
            "image_url": img,
            "level": "A1",
            "category_id": "home_items",
            "created_by": SUPER_ADMIN_USER_ID,
            "created_at": datetime.now(timezone.utc),
            "ai_generated": False
        })
    
    # School items
    for i, (tr, ru, ex_tr, ex_ru, img) in enumerate(SCHOOL_ITEMS):
        all_words.append({
            "word_id": f"school_{i}",
            "turkish": tr,
            "russian": ru,
            "pronunciation": tr.lower(),
            "example_tr": ex_tr,
            "example_ru": ex_ru,
            "image_url": img,
            "level": "A1",
            "category_id": "school",
            "created_by": SUPER_ADMIN_USER_ID,
            "created_at": datetime.now(timezone.utc),
            "ai_generated": False
        })
    
    # Transport items
    for i, (tr, ru, ex_tr, ex_ru, img) in enumerate(TRANSPORT_ITEMS):
        all_words.append({
            "word_id": f"transport_{i}",
            "turkish": tr,
            "russian": ru,
            "pronunciation": tr.lower(),
            "example_tr": ex_tr,
            "example_ru": ex_ru,
            "image_url": img,
            "level": "A2",
            "category_id": "transport",
            "created_by": SUPER_ADMIN_USER_ID,
            "created_at": datetime.now(timezone.utc),
            "ai_generated": False
        })
    
    await db.words.insert_many(all_words)
    print(f"✅ {len(all_words)} kelime eklendi (Ev, Okul, Ulaşım)")
    
    print("🎉 Günlük hayat kategorileri tamamlandı!")
    print(f"\n📊 Toplam kategori: {len(DAILY_LIFE_CATEGORIES)} yeni")
    print(f"🔤 Toplam kelime: {len(all_words)} yeni")

if __name__ == "__main__":
    asyncio.run(seed_daily_life_data())
    client.close()
