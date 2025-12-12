"""Part 2: Russian Grammar Categories (Gender + Verb Tenses)"""
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

# ==================== RUSÇA CİNSİYET KATEGORİLERİ ====================

GENDER_CATEGORIES = [
    {
        "category_id": "gender_masculine",
        "name_tr": "Erkek Cinsiyetli İsimler (он)",
        "name_ru": "Существительные мужского рода",
        "icon": "👨",
        "level": "A2",
        "color": "#4A90E2",
        "word_count": 40,
        "created_by": SUPER_ADMIN_USER_ID,
        "created_at": datetime.now(timezone.utc)
    },
    {
        "category_id": "gender_feminine",
        "name_tr": "Dişi Cinsiyetli İsimler (она)",
        "name_ru": "Существительные женского рода",
        "icon": "👩",
        "level": "A2",
        "color": "#E91E63",
        "word_count": 40,
        "created_by": SUPER_ADMIN_USER_ID,
        "created_at": datetime.now(timezone.utc)
    },
    {
        "category_id": "gender_neuter",
        "name_tr": "Nötr Cinsiyetli İsimler (оно)",
        "name_ru": "Существительные среднего рода",
        "icon": "⚪",
        "level": "A2",
        "color": "#9C27B0",
        "word_count": 30,
        "created_by": SUPER_ADMIN_USER_ID,
        "created_at": datetime.now(timezone.utc)
    }
]

# Maskülen isimler (он)
MASCULINE_WORDS = [
    {
        "word_id": f"masc_{i}",
        "turkish": word_tr,
        "russian": word_ru,
        "pronunciation": word_tr.lower(),
        "example_tr": example_tr,
        "example_ru": example_ru,
        "image_url": img,
        "level": "A2",
        "category_id": "gender_masculine",
        "created_by": SUPER_ADMIN_USER_ID,
        "created_at": datetime.now(timezone.utc),
        "ai_generated": False
    }
    for i, (word_tr, word_ru, example_tr, example_ru, img) in enumerate([
        ("masa", "стол", "Bu büyük bir masa.", "Это большой стол.", "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=400"),
        ("sandalye", "стул", "Sandalye rahat.", "Стул удобный.", "https://images.unsplash.com/photo-1503602642458-232111445657?w=400"),
        ("ev", "дом", "Güzel bir ev.", "Красивый дом.", "https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=400"),
        ("araba", "автомобиль", "Yeni bir araba.", "Новый автомобиль.", "https://images.unsplash.com/photo-1494976388531-d1058494cdd8?w=400"),
        ("telefon", "телефон", "Telefonum yeni.", "Мой телефон новый.", "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400"),
        ("bilgisayar", "компьютер", "Hızlı bir bilgisayar.", "Быстрый компьютер.", "https://images.unsplash.com/photo-1547082299-de196ea013d6?w=400"),
        ("kitap", "учебник", "Rusça kitabı.", "Учебник русского языка.", "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=400"),
        ("defter", "тетрадь (он)", "Mavi defter.", "Синий блокнот.", "https://images.unsplash.com/photo-1517842645767-c639042777db?w=400"),
        ("kalem", "карандаш", "Siyah kalem.", "Чёрный карандаш.", "https://images.unsplash.com/photo-1586075010923-2dd4570fb338?w=400"),
        ("sözlük", "словарь", "Türkçe-Rusça sözlük.", "Турецко-русский словарь.", "https://images.unsplash.com/photo-1524578271613-d550eacf6090?w=400"),
        ("öğretmen (erkek)", "учитель", "İyi bir öğretmen.", "Хороший учитель.", "https://images.unsplash.com/photo-1580582932707-520aed937b7b?w=400"),
        ("doktor (erkek)", "врач", "Tecrübeli bir doktor.", "Опытный врач.", "https://images.unsplash.com/photo-1612349317150-e413f6a5b16d?w=400"),
        ("mühendis", "инженер", "Yazılım mühendisi.", "Инженер-программист.", "https://images.unsplash.com/photo-1573497019940-1c28c88b4f3e?w=400"),
        ("avukat", "адвокат", "İyi bir avukat.", "Хороший адвокат.", "https://images.unsplash.com/photo-1589829545856-d10d557cf95f?w=400"),
        ("şoför", "водитель", "Deneyimli şoför.", "Опытный водитель.", "https://images.unsplash.com/photo-1555406916-d153d6816fb3?w=400"),
        ("garson", "официант", "Kibar garson.", "Вежливый официант.", "https://images.unsplash.com/photo-1556740738-b6a63e27c4df?w=400"),
        ("aşçı", "повар", "Ünlü bir aşçı.", "Известный повар.", "https://images.unsplash.com/photo-1577219491135-ce391730fb2c?w=400"),
        ("müdür", "директор", "Okul müdürü.", "Директор школы.", "https://images.unsplash.com/photo-1560250097-0b93528c311a?w=400"),
        ("başkan", "президент", "Şirket başkanı.", "Президент компании.", "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400"),
        ("sporcu", "спортсмен", "Profesyonel sporcu.", "Профессиональный спортсмен.", "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=400"),
    ])
]

# Feminen isimler (она)
FEMININE_WORDS = [
    {
        "word_id": f"fem_{i}",
        "turkish": word_tr,
        "russian": word_ru,
        "pronunciation": word_tr.lower(),
        "example_tr": example_tr,
        "example_ru": example_ru,
        "image_url": img,
        "level": "A2",
        "category_id": "gender_feminine",
        "created_by": SUPER_ADMIN_USER_ID,
        "created_at": datetime.now(timezone.utc),
        "ai_generated": False
    }
    for i, (word_tr, word_ru, example_tr, example_ru, img) in enumerate([
        ("kapı", "дверь", "Kapı açık.", "Дверь открыта.", "https://images.unsplash.com/photo-1516455590571-18256e5bb9ff?w=400"),
        ("pencere", "окно", "Büyük pencere.", "Большое окно.", "https://images.unsplash.com/photo-1513694203232-719a280e022f?w=400"),
        ("duvar", "стена", "Beyaz duvar.", "Белая стена.", "https://images.unsplash.com/photo-1513506003901-1e6a229e2d15?w=400"),
        ("sokak", "улица", "Geniş sokak.", "Широкая улица.", "https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?w=400"),
        ("şehir", "город", "Güzel şehir.", "Красивый город.", "https://images.unsplash.com/photo-1480714378408-67cf0d13bc1b?w=400"),
        ("ülke", "страна", "Büyük ülke.", "Большая страна.", "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=400"),
        ("kitap", "книга", "İlginç bir kitap.", "Интересная книга.", "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=400"),
        ("gazete", "газета", "Günlük gazete.", "Ежедневная газета.", "https://images.unsplash.com/photo-1504711434969-e33886168f5c?w=400"),
        ("dergi", "журнал", "Moda dergisi.", "Журнал мод.", "https://images.unsplash.com/photo-1533628635777-112b2239b1c7?w=400"),
        ("çanta", "сумка", "Kırmızı çanta.", "Красная сумка.", "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=400"),
        ("masa (yemek)", "еда", "Lezzetli yemek.", "Вкусная еда.", "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=400"),
        ("okul", "школа", "Büyük okul.", "Большая школа.", "https://images.unsplash.com/photo-1562774053-701939374585?w=400"),
        ("üniversite", "университет", "İyi üniversite.", "Хороший университет.", "https://images.unsplash.com/photo-1562774053-701939374585?w=400"),
        ("hastane", "больница", "Modern hastane.", "Современная больница.", "https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?w=400"),
        ("kütüphane", "библиотека", "Sessiz kütüphane.", "Тихая библиотека.", "https://images.unsplash.com/photo-1521587760476-6c12a4b040da?w=400"),
        ("müze", "музей", "Eski müze.", "Старый музей.", "https://images.unsplash.com/photo-1565630916779-e303be97b6f5?w=400"),
        ("tiyatro", "театр", "Ünlü tiyatro.", "Известный театр.", "https://images.unsplash.com/photo-1503095396549-807759245b35?w=400"),
        ("sinema", "кино", "Yeni sinema.", "Новое кино.", "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=400"),
        ("öğretmen (kadın)", "учительница", "İyi öğretmen.", "Хорошая учительница.", "https://images.unsplash.com/photo-1524638431109-93d95c968f03?w=400"),
        ("hemşire", "медсестра", "Tecrübeli hemşire.", "Опытная медсестра.", "https://images.unsplash.com/photo-1559839734-2b71ea197ec2?w=400"),
    ])
]

# Nötr isimler (оно)
NEUTER_WORDS = [
    {
        "word_id": f"neut_{i}",
        "turkish": word_tr,
        "russian": word_ru,
        "pronunciation": word_tr.lower(),
        "example_tr": example_tr,
        "example_ru": example_ru,
        "image_url": img,
        "level": "A2",
        "category_id": "gender_neuter",
        "created_by": SUPER_ADMIN_USER_ID,
        "created_at": datetime.now(timezone.utc),
        "ai_generated": False
    }
    for i, (word_tr, word_ru, example_tr, example_ru, img) in enumerate([
        ("deniz", "море", "Mavi deniz.", "Синее море.", "https://images.unsplash.com/photo-1505142468610-359e7d316be0?w=400"),
        ("göl", "озеро", "Büyük göl.", "Большое озеро.", "https://images.unsplash.com/photo-1439066615861-d1af74d74000?w=400"),
        ("gökyüzü", "небо", "Açık gökyüzü.", "Ясное небо.", "https://images.unsplash.com/photo-1534088568595-a066f410bcda?w=400"),
        ("güneş", "солнце", "Parlak güneş.", "Яркое солнце.", "https://images.unsplash.com/photo-1495567720989-cebdbdd97913?w=400"),
        ("kalp", "сердце", "Sağlıklı kalp.", "Здоровое сердце.", "https://images.unsplash.com/photo-1516281439317-68e0b7e07d3d?w=400"),
        ("yüz", "лицо", "Gülen yüz.", "Улыбающееся лицо.", "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400"),
        ("isim", "имя", "Güzel isim.", "Красивое имя.", "https://images.unsplash.com/photo-1484480974693-6ca0a78fb36b?w=400"),
        ("kelime", "слово", "Yeni kelime.", "Новое слово.", "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=400"),
        ("mektup", "письмо", "Uzun mektup.", "Длинное письмо.", "https://images.unsplash.com/photo-1516319100-c8af0b380f3e?w=400"),
        ("ağaç", "дерево", "Yeşil ağaç.", "Зелёное дерево.", "https://images.unsplash.com/photo-1513836279014-a89f7a76ae86?w=400"),
        ("çiçek", "растение", "Güzel çiçek.", "Красивое растение.", "https://images.unsplash.com/photo-1490750967868-88aa4486c946?w=400"),
        ("gözlük", "очки", "Yeni gözlük.", "Новые очки.", "https://images.unsplash.com/photo-1574258495973-f010dfbb5371?w=400"),
        ("ayna", "зеркало", "Büyük ayna.", "Большое зеркало.", "https://images.unsplash.com/photo-1621610015848-d53f1f7a2b5d?w=400"),
        ("sabun", "мыло", "Kokulu sabun.", "Ароматное мыло.", "https://images.unsplash.com/photo-1585838447120-5a9bc2045908?w=400"),
        ("havlu", "полотенце", "Temiz havlu.", "Чистое полотенце.", "https://images.unsplash.com/photo-1622279457486-62dcc4a431d6?w=400"),
    ])
]

async def seed_grammar_data():
    print("🌱 Rusça cinsiyet kategorileri seed ediliyor...")
    
    existing = await db.categories.count_documents({"category_id": "gender_masculine"})
    if existing > 0:
        print("⚠️  Cinsiyet kategorileri zaten mevcut.")
        return
    
    await db.categories.insert_many(GENDER_CATEGORIES)
    print(f"✅ {len(GENDER_CATEGORIES)} cinsiyet kategorisi eklendi")
    
    all_words = MASCULINE_WORDS + FEMININE_WORDS + NEUTER_WORDS
    await db.words.insert_many(all_words)
    print(f"✅ {len(all_words)} kelime eklendi (Maskülen, Feminen, Nötr)")
    
    print("🎉 Cinsiyet kategorileri tamamlandı!")

if __name__ == "__main__":
    asyncio.run(seed_grammar_data())
    client.close()
