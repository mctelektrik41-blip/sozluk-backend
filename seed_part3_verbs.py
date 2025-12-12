"""Part 3: Verb Tenses and Daily Life Categories"""
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

# ==================== FİİL ZAMANLARI ====================

VERB_CATEGORIES = [
    {
        "category_id": "verb_past",
        "name_tr": "Geçmiş Zaman Fiiller",
        "name_ru": "Глаголы прошедшего времени",
        "icon": "⏮️",
        "level": "A2",
        "color": "#FF6B6B",
        "word_count": 40,
        "created_by": SUPER_ADMIN_USER_ID,
        "created_at": datetime.now(timezone.utc)
    },
    {
        "category_id": "verb_present",
        "name_tr": "Şimdiki Zaman Fiiller",
        "name_ru": "Глаголы настоящего времени",
        "icon": "▶️",
        "level": "A2",
        "color": "#4ECDC4",
        "word_count": 40,
        "created_by": SUPER_ADMIN_USER_ID,
        "created_at": datetime.now(timezone.utc)
    },
    {
        "category_id": "verb_future",
        "name_tr": "Gelecek Zaman Fiiller",
        "name_ru": "Глаголы будущего времени",
        "icon": "⏭️",
        "level": "A2",
        "color": "#95E1D3",
        "word_count": 40,
        "created_by": SUPER_ADMIN_USER_ID,
        "created_at": datetime.now(timezone.utc)
    }
]

# Geçmiş Zaman
PAST_VERBS = [
    {
        "word_id": f"past_{i}",
        "turkish": verb_tr,
        "russian": verb_ru,
        "pronunciation": verb_tr.lower(),
        "example_tr": example_tr,
        "example_ru": example_ru,
        "image_url": img,
        "level": "A2",
        "category_id": "verb_past",
        "created_by": SUPER_ADMIN_USER_ID,
        "created_at": datetime.now(timezone.utc),
        "ai_generated": False
    }
    for i, (verb_tr, verb_ru, example_tr, example_ru, img) in enumerate([
        ("gittim", "я ходил/ходила", "Dün markete gittim.", "Вчера я ходил в магазин.", "https://images.unsplash.com/photo-1534452203293-494d7ddbf7e0?w=400"),
        ("yedim", "я ел/ела", "Sabah kahvaltı yedim.", "Утром я позавтракал.", "https://images.unsplash.com/photo-1533777419517-3e4017e2e15a?w=400"),
        ("içtim", "я пил/пила", "Su içtim.", "Я выпил воды.", "https://images.unsplash.com/photo-1548839140-29a749e1cf4d?w=400"),
        ("uyudum", "я спал/спала", "İyi uyudum.", "Я хорошо спал.", "https://images.unsplash.com/photo-1541781774459-bb2af2f05b55?w=400"),
        ("uyandım", "я проснулся/проснулась", "Erken uyandım.", "Я рано проснулся.", "https://images.unsplash.com/photo-1495954222046-2c427ecb546d?w=400"),
        ("çalıştım", "я работал/работала", "Ofiste çalıştım.", "Я работал в офисе.", "https://images.unsplash.com/photo-1497032628192-86f99bcd76bc?w=400"),
        ("okudum", "я читал/читала", "Kitap okudum.", "Я читал книгу.", "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=400"),
        ("yazdım", "я писал/писала", "Mektup yazdım.", "Я писал письмо.", "https://images.unsplash.com/photo-1455390582262-044cdead277a?w=400"),
        ("izledim", "я смотрел/смотрела", "Film izledim.", "Я смотрел фильм.", "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=400"),
        ("dinledim", "я слушал/слушала", "Müzik dinledim.", "Я слушал музыку.", "https://images.unsplash.com/photo-1511379938547-c1f69419868d?w=400"),
        ("konuştum", "я говорил/говорила", "Arkadaşımla konuştum.", "Я говорил с другом.", "https://images.unsplash.com/photo-1543269865-cbf427effbad?w=400"),
        ("öğrendim", "я учил/учила", "Rusça öğrendim.", "Я учил русский язык.", "https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=400"),
        ("anladım", "я понял/поняла", "Dersi anladım.", "Я понял урок.", "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=400"),
        ("gördüm", "я видел/видела", "Filmi gördüm.", "Я видел фильм.", "https://images.unsplash.com/photo-1485095329183-d0797cdc5676?w=400"),
        ("aldım", "я взял/взяла", "Kitabı aldım.", "Я взял книгу.", "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=400"),
        ("verdim", "я дал/дала", "Para verdim.", "Я дал деньги.", "https://images.unsplash.com/photo-1580519542036-c47de6196ba5?w=400"),
        ("söyledim", "я сказал/сказала", "Doğruyu söyledim.", "Я сказал правду.", "https://images.unsplash.com/photo-1517842645767-c639042777db?w=400"),
        ("sordum", "я спросил/спросила", "Soru sordum.", "Я спросил.", "https://images.unsplash.com/photo-1516534775068-ba3e7458af70?w=400"),
        ("cevap verdim", "я ответил/ответила", "Soruya cevap verdim.", "Я ответил на вопрос.", "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=400"),
        ("yaptım", "я делал/делала", "Ev ödevi yaptım.", "Я делал домашнее задание.", "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=400"),
        ("geldim", "я пришёл/пришла", "Eve geldim.", "Я пришёл домой.", "https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=400"),
        ("çıktım", "я вышел/вышла", "Dışarı çıktım.", "Я вышел на улицу.", "https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?w=400"),
        ("oturdum", "я сидел/сидела", "Sandalyede oturdum.", "Я сидел на стуле.", "https://images.unsplash.com/photo-1503602642458-232111445657?w=400"),
        ("kalktım", "я встал/встала", "Erken kalktım.", "Я рано встал.", "https://images.unsplash.com/photo-1485290334039-a3c69043e517?w=400"),
        ("yürüdüm", "я ходил/ходила", "Parkta yürüdüm.", "Я гулял в парке.", "https://images.unsplash.com/photo-1488646953014-85cb44e25828?w=400"),
        ("koştum", "я бежал/бежала", "Hızlı koştum.", "Я быстро бежал.", "https://images.unsplash.com/photo-1476480862126-209bfaa8edc8?w=400"),
        ("düştüm", "я упал/упала", "Yere düştüm.", "Я упал на землю.", "https://images.unsplash.com/photo-1527525443983-6e60c75fff46?w=400"),
        ("buldum", "я нашёл/нашла", "Anahtarı buldum.", "Я нашёл ключ.", "https://images.unsplash.com/photo-1582139329536-e7284fece509?w=400"),
        ("kaybettim", "я потерял/потеряла", "Telefonumu kaybettim.", "Я потерял телефон.", "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400"),
        ("unuttum", "я забыл/забыла", "İsmini unuttum.", "Я забыл имя.", "https://images.unsplash.com/photo-1506452819137-0422416856b8?w=400"),
        ("hatırladım", "я вспомнил/вспомнила", "Seni hatırladım.", "Я вспомнил тебя.", "https://images.unsplash.com/photo-1484480974693-6ca0a78fb36b?w=400"),
        ("sevdim", "я любил/любила", "Filmi sevdim.", "Я любил фильм.", "https://images.unsplash.com/photo-1478720568477-152d9b164e26?w=400"),
        ("beğendim", "я понравился", "Yemeği beğendim.", "Мне понравилась еда.", "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=400"),
        ("istedim", "я хотел/хотела", "Su istedim.", "Я хотел воды.", "https://images.unsplash.com/photo-1548839140-29a749e1cf4d?w=400"),
        ("bekledi", "я ждал/ждала", "Otobüs bekledim.", "Я ждал автобус.", "https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?w=400"),
        ("başladım", "я начал/начала", "İşe başladım.", "Я начал работу.", "https://images.unsplash.com/photo-1507679799987-c73779587ccf?w=400"),
        ("bitirdim", "я закончил/закончила", "Ödevimi bitirdim.", "Я закончил задание.", "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=400"),
        ("açtım", "я открыл/открыла", "Kapıyı açtım.", "Я открыл дверь.", "https://images.unsplash.com/photo-1516455590571-18256e5bb9ff?w=400"),
        ("kapattım", "я закрыл/закрыла", "Pencereyi kapattım.", "Я закрыл окно.", "https://images.unsplash.com/photo-1513694203232-719a280e022f?w=400"),
        ("pişirdim", "я готовил/готовила", "Yemek pişirdim.", "Я готовил еду.", "https://images.unsplash.com/photo-1556910103-1c02745aae4d?w=400"),
    ])
]

# Şimdiki Zaman
PRESENT_VERBS = [
    {
        "word_id": f"pres_{i}",
        "turkish": verb_tr,
        "russian": verb_ru,
        "pronunciation": verb_tr.lower(),
        "example_tr": example_tr,
        "example_ru": example_ru,
        "image_url": img,
        "level": "A2",
        "category_id": "verb_present",
        "created_by": SUPER_ADMIN_USER_ID,
        "created_at": datetime.now(timezone.utc),
        "ai_generated": False
    }
    for i, (verb_tr, verb_ru, example_tr, example_ru, img) in enumerate([
        ("gidiyorum", "я хожу", "Her gün okula gidiyorum.", "Каждый день я хожу в школу.", "https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=400"),
        ("yiyorum", "я ем", "Elma yiyorum.", "Я ем яблоко.", "https://images.unsplash.com/photo-1619546813926-a78fa6372cd2?w=400"),
        ("içiyorum", "я пью", "Çay içiyorum.", "Я пью чай.", "https://images.unsplash.com/photo-1564890369478-c89ca6d9cde9?w=400"),
        ("uyuyorum", "я сплю", "Şimdi uyuyorum.", "Сейчас я сплю.", "https://images.unsplash.com/photo-1541781774459-bb2af2f05b55?w=400"),
        ("çalışıyorum", "я работаю", "Ofiste çalışıyorum.", "Я работаю в офисе.", "https://images.unsplash.com/photo-1497032628192-86f99bcd76bc?w=400"),
        ("okuyorum", "я читаю", "Kitap okuyorum.", "Я читаю книгу.", "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=400"),
        ("yazıyorum", "я пишу", "Mektup yazıyorum.", "Я пишу письмо.", "https://images.unsplash.com/photo-1455390582262-044cdead277a?w=400"),
        ("izliyorum", "я смотрю", "Televizyon izliyorum.", "Я смотрю телевизор.", "https://images.unsplash.com/photo-1522869635100-9f4c5e86aa37?w=400"),
        ("dinliyorum", "я слушаю", "Müzik dinliyorum.", "Я слушаю музыку.", "https://images.unsplash.com/photo-1511379938547-c1f69419868d?w=400"),
        ("konuşuyorum", "я говорю", "Telefonla konuşuyorum.", "Я говорю по телефону.", "https://images.unsplash.com/photo-1543269865-cbf427effbad?w=400"),
        ("öğreniyorum", "я учу", "Rusça öğreniyorum.", "Я учу русский язык.", "https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=400"),
        ("anlıyorum", "я понимаю", "Dersi anlıyorum.", "Я понимаю урок.", "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=400"),
        ("görüyorum", "я вижу", "Seni görüyorum.", "Я вижу тебя.", "https://images.unsplash.com/photo-1516199707916-5dc815e1cca2?w=400"),
        ("alıyorum", "я беру", "Kitap alıyorum.", "Я беру книгу.", "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=400"),
        ("veriyorum", "я даю", "Sana para veriyorum.", "Я даю тебе деньги.", "https://images.unsplash.com/photo-1580519542036-c47de6196ba5?w=400"),
        ("söylüyorum", "я говорю", "Doğruyu söylüyorum.", "Я говорю правду.", "https://images.unsplash.com/photo-1517842645767-c639042777db?w=400"),
        ("soruyorum", "я спрашиваю", "Soru soruyorum.", "Я спрашиваю.", "https://images.unsplash.com/photo-1516534775068-ba3e7458af70?w=400"),
        ("yapıyorum", "я делаю", "Ödev yapıyorum.", "Я делаю домашнее задание.", "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=400"),
        ("geliyorum", "я прихожу", "Eve geliyorum.", "Я прихожу домой.", "https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=400"),
        ("gülüyorum", "я смеюсь", "Şakaya gülüyorum.", "Я смеюсь над шуткой.", "https://images.unsplash.com/photo-1489424731084-a5d8b219a5bb?w=400"),
        ("ağlıyorum", "я плачу", "Film izlerken ağlıyorum.", "Я плачу, когда смотрю фильм.", "https://images.unsplash.com/photo-1509909756405-be0199881695?w=400"),
        ("oturuyorum", "я сижу", "Sandalyede oturuyorum.", "Я сижу на стуле.", "https://images.unsplash.com/photo-1503602642458-232111445657?w=400"),
        ("duruyorum", "я стою", "Ayakta duruyorum.", "Я стою.", "https://images.unsplash.com/photo-1531058020387-3be344556be6?w=400"),
        ("yatıyorum", "я лежу", "Yatakta yatıyorum.", "Я лежу в кровати.", "https://images.unsplash.com/photo-1540518614846-7eded433c457?w=400"),
        ("yürüyorum", "я иду", "Parkta yürüyorum.", "Я иду в парке.", "https://images.unsplash.com/photo-1488646953014-85cb44e25828?w=400"),
        ("koşuyorum", "я бегу", "Hızlı koşuyorum.", "Я быстро бегу.", "https://images.unsplash.com/photo-1476480862126-209bfaa8edc8?w=400"),
        ("düşünüyorum", "я думаю", "Seni düşünüyorum.", "Я думаю о тебе.", "https://images.unsplash.com/photo-1506452819137-0422416856b8?w=400"),
        ("hissediyorum", "я чувствую", "İyi hissediyorum.", "Я чувствую себя хорошо.", "https://images.unsplash.com/photo-1499209974431-9dddcece7f88?w=400"),
        ("seviyorum", "я люблю", "Seni seviyorum.", "Я люблю тебя.", "https://images.unsplash.com/photo-1518199266791-5375a83190b7?w=400"),
        ("istiyorum", "я хочу", "Su istiyorum.", "Я хочу воды.", "https://images.unsplash.com/photo-1548839140-29a749e1cf4d?w=400"),
        ("bekliyorum", "я жду", "Otobüs bekliyorum.", "Я жду автобус.", "https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?w=400"),
        ("başlıyorum", "я начинаю", "İşe başlıyorum.", "Я начинаю работу.", "https://images.unsplash.com/photo-1507679799987-c73779587ccf?w=400"),
        ("bitiriyorum", "я заканчиваю", "İşi bitiriyorum.", "Я заканчиваю работу.", "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=400"),
        ("açıyorum", "я открываю", "Kapıyı açıyorum.", "Я открываю дверь.", "https://images.unsplash.com/photo-1516455590571-18256e5bb9ff?w=400"),
        ("kapatıyorum", "я закрываю", "Pencereyi kapatıyorum.", "Я закрываю окно.", "https://images.unsplash.com/photo-1513694203232-719a280e022f?w=400"),
        ("temizliyorum", "я убираю", "Odayı temizliyorum.", "Я убираю комнату.", "https://images.unsplash.com/photo-1527515862127-a4fc05baf7a5?w=400"),
        ("yıkıyorum", "я мою", "Bulaşık yıkıyorum.", "Я мою посуду.", "https://images.unsplash.com/photo-1563453392212-326f5e854473?w=400"),
        ("pişiriyorum", "я готовлю", "Yemek pişiriyorum.", "Я готовлю еду.", "https://images.unsplash.com/photo-1556910103-1c02745aae4d?w=400"),
        ("yardım ediyorum", "я помогаю", "Anneme yardım ediyorum.", "Я помогаю маме.", "https://images.unsplash.com/photo-1488521787991-ed7bbaae773c?w=400"),
        ("oynuyorum", "я играю", "Futbol oynuyorum.", "Я играю в футбол.", "https://images.unsplash.com/photo-1431324155629-1a6deb1dec8d?w=400"),
    ])
]

# Gelecek Zaman (sadece ilk 20 - uzun oluyor)
FUTURE_VERBS = [
    {
        "word_id": f"fut_{i}",
        "turkish": verb_tr,
        "russian": verb_ru,
        "pronunciation": verb_tr.lower(),
        "example_tr": example_tr,
        "example_ru": example_ru,
        "image_url": img,
        "level": "A2",
        "category_id": "verb_future",
        "created_by": SUPER_ADMIN_USER_ID,
        "created_at": datetime.now(timezone.utc),
        "ai_generated": False
    }
    for i, (verb_tr, verb_ru, example_tr, example_ru, img) in enumerate([
        ("gideceğim", "я пойду", "Yarın okula gideceğim.", "Завтра я пойду в школу.", "https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=400"),
        ("yiyeceğim", "я буду есть", "Akşam yemek yiyeceğim.", "Вечером я буду есть.", "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=400"),
        ("içeceğim", "я буду пить", "Su içeceğim.", "Я выпью воды.", "https://images.unsplash.com/photo-1548839140-29a749e1cf4d?w=400"),
        ("uyuyacağım", "я буду спать", "Erken uyuyacağım.", "Я буду спать рано.", "https://images.unsplash.com/photo-1541781774459-bb2af2f05b55?w=400"),
        ("çalışacağım", "я буду работать", "Yarın çalışacağım.", "Завтра я буду работать.", "https://images.unsplash.com/photo-1497032628192-86f99bcd76bc?w=400"),
        ("okuyacağım", "я буду читать", "Bu kitabı okuyacağım.", "Я буду читать эту книгу.", "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=400"),
        ("yazacağım", "я буду писать", "Mektup yazacağım.", "Я буду писать письмо.", "https://images.unsplash.com/photo-1455390582262-044cdead277a?w=400"),
        ("izleyeceğim", "я буду смотреть", "Film izleyeceğim.", "Я буду смотреть фильм.", "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=400"),
        ("dinleyeceğim", "я буду слушать", "Müzik dinleyeceğim.", "Я буду слушать музыку.", "https://images.unsplash.com/photo-1511379938547-c1f69419868d?w=400"),
        ("konuşacağım", "я буду говорить", "Seninle konuşacağım.", "Я буду говорить с тобой.", "https://images.unsplash.com/photo-1543269865-cbf427effbad?w=400"),
        ("öğreneceğim", "я буду учить", "Rusça öğreneceğim.", "Я буду учить русский язык.", "https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=400"),
        ("anlayacağım", "я пойму", "Dersi anlayacağım.", "Я пойму урок.", "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=400"),
        ("göreceğim", "я увижу", "Seni göreceğim.", "Я увижу тебя.", "https://images.unsplash.com/photo-1516199707916-5dc815e1cca2?w=400"),
        ("alacağım", "я возьму", "Kitap alacağım.", "Я возьму книгу.", "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=400"),
        ("vereceğim", "я дам", "Sana vereceğim.", "Я дам тебе.", "https://images.unsplash.com/photo-1580519542036-c47de6196ba5?w=400"),
        ("söyleyeceğim", "я скажу", "Doğruyu söyleyeceğim.", "Я скажу правду.", "https://images.unsplash.com/photo-1517842645767-c639042777db?w=400"),
        ("soracağım", "я спрошу", "Soru soracağım.", "Я спрошу.", "https://images.unsplash.com/photo-1516534775068-ba3e7458af70?w=400"),
        ("yapacağım", "я сделаю", "Ödev yapacağım.", "Я сделаю домашнее задание.", "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=400"),
        ("geleceğim", "я приду", "Yarın geleceğim.", "Завтра я приду.", "https://images.unsplash.com/photo-1506126613408-eca07ce68773?w=400"),
        ("başlayacağım", "я начну", "İşe başlayacağım.", "Я начну работу.", "https://images.unsplash.com/photo-1507679799987-c73779587ccf?w=400"),
    ])
]

async def seed_verbs_data():
    print("🌱 Fiil zamanları seed ediliyor...")
    
    existing = await db.categories.count_documents({"category_id": "verb_past"})
    if existing > 0:
        print("⚠️  Fiil kategorileri zaten mevcut.")
        return
    
    await db.categories.insert_many(VERB_CATEGORIES)
    print(f"✅ {len(VERB_CATEGORIES)} fiil kategorisi eklendi")
    
    all_words = PAST_VERBS + PRESENT_VERBS + FUTURE_VERBS
    await db.words.insert_many(all_words)
    print(f"✅ {len(all_words)} fiil eklendi")
    
    print("🎉 Fiil zamanları tamamlandı!")

if __name__ == "__main__":
    asyncio.run(seed_verbs_data())
    client.close()
