"""
Part 3: Russian Grammar (Gender categories) + Verb Tenses
Adds ~180 words
"""
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

async def get_super_admin_id():
    user = await db.users.find_one({"role": "super_admin"})
    if user:
        return user.get("user_id") or user.get("id")
    return f"user_{uuid.uuid4().hex[:12]}"

async def seed_grammar_verbs():
    print("🌱 Rusça dilbilgisi ve fiil çekimleri ekleniyor...")
    
    SUPER_ADMIN_USER_ID = await get_super_admin_id()
    
    # Check if already exists
    existing = await db.categories.count_documents({"category_id": "gender_masculine"})
    if existing > 0:
        print("⚠️  Bu kategoriler zaten mevcut.")
        return
    
    categories_to_insert = []
    words_to_insert = []
    
    # ==================== RUSSIAN GENDER CATEGORIES ====================
    grammar_cats = [
        {
            "category_id": "gender_masculine",
            "name_tr": "Erkek Cinsiyetli İsimler (он)",
            "name_ru": "Существительные мужского рода (он)",
            "icon": "♂️",
            "level": "A2",
            "color": "#4A90E2"
        },
        {
            "category_id": "gender_feminine",
            "name_tr": "Dişi Cinsiyetli İsimler (она)",
            "name_ru": "Существительные женского рода (она)",
            "icon": "♀️",
            "level": "A2",
            "color": "#E24A90"
        },
        {
            "category_id": "gender_neuter",
            "name_tr": "Nötr Cinsiyetli İsimler (оно)",
            "name_ru": "Существительные среднего рода (оно)",
            "icon": "⚥",
            "level": "A2",
            "color": "#90E24A"
        },
        {
            "category_id": "verbs_present",
            "name_tr": "Şimdiki Zaman Fiiller",
            "name_ru": "Глаголы настоящего времени",
            "icon": "⏰",
            "level": "A2",
            "color": "#E2904A"
        },
        {
            "category_id": "verbs_past",
            "name_tr": "Geçmiş Zaman Fiiller",
            "name_ru": "Глаголы прошедшего времени",
            "icon": "⏮️",
            "level": "A2",
            "color": "#904AE2"
        },
        {
            "category_id": "verbs_future",
            "name_tr": "Gelecek Zaman Fiiller",
            "name_ru": "Глаголы будущего времени",
            "icon": "⏭️",
            "level": "A2",
            "color": "#4AE290"
        }
    ]
    
    # Masculine nouns (30 words)
    masculine_data = [
        ("стол", "masa", "Стол большой.", "Masa büyük.", "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=400"),
        ("стул", "sandalye", "Стул удобный.", "Sandalye rahat.", "https://images.unsplash.com/photo-1503602642458-232111445657?w=400"),
        ("дом", "ev", "Дом красивый.", "Ev güzel.", "https://images.unsplash.com/photo-1570129477492-45c003edd2be?w=400"),
        ("город", "şehir", "Город большой.", "Şehir büyük.", "https://images.unsplash.com/photo-1480714378408-67cf0d13bc1b?w=400"),
        ("магазин", "mağaza", "Магазин открыт.", "Mağaza açık.", "https://images.unsplash.com/photo-1441984904996-e0b6ba687e04?w=400"),
        ("врач", "doktor", "Врач лечит.", "Doktor tedavi ediyor.", "https://images.unsplash.com/photo-1559839734-2b71ea197ec2?w=400"),
        ("учитель", "öğretmen", "Учитель учит.", "Öğretmen öğretiyor.", "https://images.unsplash.com/photo-1580582932707-520aed937b7b?w=400"),
        ("студент", "öğrenci (erkek)", "Студент учится.", "Öğrenci okuyor.", "https://images.unsplash.com/photo-1523240795612-9a054b0db644?w=400"),
        ("друг", "arkadaş (erkek)", "Друг помогает.", "Arkadaş yardım ediyor.", "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=400"),
        ("брат", "erkek kardeş", "Брат работает.", "Erkek kardeş çalışıyor.", "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400"),
        ("отец", "baba", "Отец дома.", "Baba evde.", "https://images.unsplash.com/photo-1541534741688-6078c6bfb5c5?w=400"),
        ("сын", "oğul", "Сын играет.", "Oğul oynuyor.", "https://images.unsplash.com/photo-1519925610903-381054cc2a1a?w=400"),
        ("муж", "koca, eş", "Муж готовит.", "Eş yemek yapıyor.", "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=400"),
        ("дедушка", "dede", "Дедушка читает.", "Dede okuyor.", "https://images.unsplash.com/photo-1595970968158-b9e0a8c3c6f0?w=400"),
        ("дядя", "amca", "Дядя приехал.", "Amca geldi.", "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=400"),
        ("мальчик", "erkek çocuk", "Мальчик бежит.", "Erkek çocuk koşuyor.", "https://images.unsplash.com/photo-1519925610903-381054cc2a1a?w=400"),
        ("человек", "insan", "Человек живёт.", "İnsan yaşıyor.", "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400"),
        ("язык", "dil", "Язык трудный.", "Dil zor.", "https://images.unsplash.com/photo-1546410531-bb4caa6b424d?w=400"),
        ("хлеб", "ekmek", "Хлеб свежий.", "Ekmek taze.", "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=400"),
        ("сок", "meyve suyu", "Сок вкусный.", "Meyve suyu lezzetli.", "https://images.unsplash.com/photo-1600271886742-f049cd451bba?w=400"),
        ("чай", "çay", "Чай горячий.", "Çay sıcak.", "https://images.unsplash.com/photo-1564890369478-c89ca6d9cde9?w=400"),
        ("суп", "çorba", "Суп готов.", "Çorba hazır.", "https://images.unsplash.com/photo-1547592166-23ac45744acd?w=400"),
        ("карандаш", "kalem (kurşun)", "Карандаш острый.", "Kalem keskin.", "https://images.unsplash.com/photo-1587467512693-254fe1a4e2e6?w=400"),
        ("компьютер", "bilgisayar", "Компьютер работает.", "Bilgisayar çalışıyor.", "https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=400"),
        ("телефон", "telefon", "Телефон звонит.", "Telefon çalıyor.", "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400"),
        ("журнал", "dergi", "Журнал интересный.", "Dergi ilginç.", "https://images.unsplash.com/photo-1457369804613-52c61a468e7d?w=400"),
        ("словарь", "sözlük", "Словарь полезный.", "Sözlük faydalı.", "https://images.unsplash.com/photo-1591124943053-97319b16e28d?w=400"),
        ("вопрос", "soru", "Вопрос трудный.", "Soru zor.", "https://images.unsplash.com/photo-1516534775068-ba3e7458af70?w=400"),
        ("ответ", "cevap", "Ответ правильный.", "Cevap doğru.", "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=400"),
        ("автобус", "otobüs", "Автобус идёт.", "Otobüs gidiyor.", "https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?w=400"),
    ]
    
    # Feminine nouns (30 words)
    feminine_data = [
        ("книга", "kitap", "Книга интересная.", "Kitap ilginç.", "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=400"),
        ("школа", "okul", "Школа большая.", "Okul büyük.", "https://images.unsplash.com/photo-1580582932707-520aed937b7b?w=400"),
        ("комната", "oda", "Комната чистая.", "Oda temiz.", "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?w=400"),
        ("мама", "anne", "Мама готовит.", "Anne yemek yapıyor.", "https://images.unsplash.com/photo-1596003906949-67221c37965c?w=400"),
        ("сестра", "kız kardeş", "Сестра читает.", "Kız kardeş okuyor.", "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=400"),
        ("дочь", "kız evlat", "Дочь поёт.", "Kızı şarkı söylüyor.", "https://images.unsplash.com/photo-1503454537195-1dcabb73ffb9?w=400"),
        ("жена", "karı, eş", "Жена работает.", "Eş çalışıyor.", "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=400"),
        ("бабушка", "nine, babaanne", "Бабушка готовит.", "Nine yemek yapıyor.", "https://images.unsplash.com/photo-1587360931039-4077bda63e49?w=400"),
        ("тётя", "teyze, hala", "Тётя приехала.", "Teyze geldi.", "https://images.unsplash.com/photo-1499996860823-5214fcc65f8f?w=400"),
        ("девочка", "kız çocuk", "Девочка играет.", "Kız çocuk oynuyor.", "https://images.unsplash.com/photo-1503454537195-1dcabb73ffb9?w=400"),
        ("студентка", "öğrenci (kız)", "Студентка пишет.", "Öğrenci yazıyor.", "https://images.unsplash.com/photo-1524638431109-93d95c968f03?w=400"),
        ("учительница", "öğretmen (kadın)", "Учительница объясняет.", "Öğretmen açıklıyor.", "https://images.unsplash.com/photo-1505501981847-1b8a58f7e055?w=400"),
        ("вода", "su", "Вода холодная.", "Su soğuk.", "https://images.unsplash.com/photo-1548839140-29a749e1cf4d?w=400"),
        ("рука", "el, kol", "Рука сильная.", "El güçlü.", "https://images.unsplash.com/photo-1584308972272-9e4e7685e80f?w=400"),
        ("нога", "bacak, ayak", "Нога болит.", "Bacak ağrıyor.", "https://images.unsplash.com/photo-1605209449754-09168d0e3158?w=400"),
        ("голова", "baş, kafa", "Голова болит.", "Baş ağrıyor.", "https://images.unsplash.com/photo-1530019047333-748c02d22e40?w=400"),
        ("дверь", "kapı", "Дверь открыта.", "Kapı açık.", "https://images.unsplash.com/photo-1519710164239-da123dc03ef4?w=400"),
        ("улица", "sokak", "Улица шумная.", "Sokak gürültülü.", "https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?w=400"),
        ("страна", "ülke", "Страна большая.", "Ülke büyük.", "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=400"),
        ("работа", "iş", "Работа трудная.", "İş zor.", "https://images.unsplash.com/photo-1486312338219-ce68d2c6f44d?w=400"),
        ("жизнь", "hayat", "Жизнь прекрасна.", "Hayat güzel.", "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400"),
        ("музыка", "müzik", "Музыка красивая.", "Müzik güzel.", "https://images.unsplash.com/photo-1511379938547-c1f69419868d?w=400"),
        ("песня", "şarkı", "Песня весёлая.", "Şarkı neşeli.", "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?w=400"),
        ("машина", "araba", "Машина быстрая.", "Araba hızlı.", "https://images.unsplash.com/photo-1549399542-7e3f8b79c341?w=400"),
        ("газета", "gazete", "Газета свежая.", "Gazete taze.", "https://images.unsplash.com/photo-1504711434969-e33886168f5c?w=400"),
        ("ручка", "kalem (tükenmez)", "Ручка пишет.", "Kalem yazıyor.", "https://images.unsplash.com/photo-1586281380349-632531db7ed4?w=400"),
        ("тетрадь", "defter", "Тетрадь новая.", "Defter yeni.", "https://images.unsplash.com/photo-1531346878377-a5be20888e57?w=400"),
        ("сумка", "çanta", "Сумка тяжёлая.", "Çanta ağır.", "https://images.unsplash.com/photo-1590874103328-eac38a683ce7?w=400"),
        ("кухня", "mutfak", "Кухня чистая.", "Mutfak temiz.", "https://images.unsplash.com/photo-1556911220-bff31c812dba?w=400"),
        ("кровать", "yatak", "Кровать мягкая.", "Yatak yumuşak.", "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?w=400"),
    ]
    
    # Neuter nouns (30 words)
    neuter_data = [
        ("окно", "pencere", "Окно открыто.", "Pencere açık.", "https://images.unsplash.com/photo-1545259741-2ea3ebf61fa3?w=400"),
        ("место", "yer", "Место свободно.", "Yer boş.", "https://images.unsplash.com/photo-1556911220-bff31c812dba?w=400"),
        ("море", "deniz", "Море синее.", "Deniz mavi.", "https://images.unsplash.com/photo-1505142468610-359e7d316be0?w=400"),
        ("солнце", "güneş", "Солнце светит.", "Güneş parlıyor.", "https://images.unsplash.com/photo-1602496674108-a5aab96d51a7?w=400"),
        ("небо", "gök, gökyüzü", "Небо голубое.", "Gökyüzü mavi.", "https://images.unsplash.com/photo-1419242902214-272b3f66ee7a?w=400"),
        ("дерево", "ağaç", "Дерево высокое.", "Ağaç yüksek.", "https://images.unsplash.com/photo-1542273917363-3b1817f69a2d?w=400"),
        ("лицо", "yüz", "Лицо красивое.", "Yüz güzel.", "https://images.unsplash.com/photo-1531746020798-e6953c6e8e04?w=400"),
        ("сердце", "kalp", "Сердце бьётся.", "Kalp atıyor.", "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=400"),
        ("здание", "bina", "Здание новое.", "Bina yeni.", "https://images.unsplash.com/photo-1480714378408-67cf0d13bc1b?w=400"),
        ("яблоко", "elma", "Яблоко вкусное.", "Elma lezzetli.", "https://images.unsplash.com/photo-1568702846914-96b305d2aaeb?w=400"),
        ("молоко", "süt", "Молоко свежее.", "Süt taze.", "https://images.unsplash.com/photo-1550583724-b2692b85b150?w=400"),
        ("мясо", "et", "Мясо вкусное.", "Et lezzetli.", "https://images.unsplash.com/photo-1588168333986-5078d3ae3976?w=400"),
        ("письмо", "mektup", "Письмо длинное.", "Mektup uzun.", "https://images.unsplash.com/photo-1579275542618-a1dfed5f54ba?w=400"),
        ("слово", "kelime", "Слово трудное.", "Kelime zor.", "https://images.unsplash.com/photo-1518622358385-8ea7d0794bf6?w=400"),
        ("дело", "iş, mesele", "Дело важное.", "İş önemli.", "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=400"),
        ("время", "zaman, vakit", "Время идёт.", "Zaman geçiyor.", "https://images.unsplash.com/photo-1501139083538-0139583c060f?w=400"),
        ("утро", "sabah", "Утро прекрасное.", "Sabah harika.", "https://images.unsplash.com/photo-1495214783159-3503fd1b572d?w=400"),
        ("лето", "yaz", "Лето жаркое.", "Yaz sıcak.", "https://images.unsplash.com/photo-1473496169904-658ba7c44d8a?w=400"),
        ("озеро", "göl", "Озеро глубокое.", "Göl derin.", "https://images.unsplash.com/photo-1439066615861-d1af74d74000?w=400"),
        ("здоровье", "sağlık", "Здоровье важное.", "Sağlık önemli.", "https://images.unsplash.com/photo-1505751172876-fa1923c5c528?w=400"),
        ("счастье", "mutluluk", "Счастье большое.", "Mutluluk büyük.", "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400"),
        ("имя", "isim", "Имя красивое.", "İsim güzel.", "https://images.unsplash.com/photo-1516534775068-ba3e7458af70?w=400"),
        ("животное", "hayvan", "Животное большое.", "Hayvan büyük.", "https://images.unsplash.com/photo-1564760055775-d63b17a55c44?w=400"),
        ("растение", "bitki", "Растение зелёное.", "Bitki yeşil.", "https://images.unsplash.com/photo-1466781783364-36c955e42a7f?w=400"),
        ("поле", "tarla, alan", "Поле большое.", "Tarla büyük.", "https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=400"),
        ("село", "köy", "Село тихое.", "Köy sessiz.", "https://images.unsplash.com/photo-1560493676-04071c5f467b?w=400"),
        ("кино", "sinema", "Кино интересное.", "Sinema ilginç.", "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=400"),
        ("метро", "metro", "Метро быстрое.", "Metro hızlı.", "https://images.unsplash.com/photo-1574698603573-cdce881a98ed?w=400"),
        ("кафе", "kafe", "Кафе уютное.", "Kafe rahat.", "https://images.unsplash.com/photo-1445116572660-236099ec97a0?w=400"),
        ("пальто", "palto", "Пальто тёплое.", "Palto sıcak tutuyor.", "https://images.unsplash.com/photo-1539533018447-63fcce2678e3?w=400"),
    ]
    
    # Present tense verbs (30 words)
    present_verbs_data = [
        ("говорить", "konuşmak", "Я говорю по-русски.", "Rusça konuşuyorum.", "https://images.unsplash.com/photo-1543269664-76bc3997d9ea?w=400"),
        ("читать", "okumak", "Я читаю книгу.", "Kitap okuyorum.", "https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=400"),
        ("писать", "yazmak", "Я пишу письмо.", "Mektup yazıyorum.", "https://images.unsplash.com/photo-1455390582262-044cdead277a?w=400"),
        ("слушать", "dinlemek", "Я слушаю музыку.", "Müzik dinliyorum.", "https://images.unsplash.com/photo-1511379938547-c1f69419868d?w=400"),
        ("смотреть", "bakmak, seyretmek", "Я смотрю фильм.", "Film seyrediyorum.", "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=400"),
        ("работать", "çalışmak", "Я работаю дома.", "Evde çalışıyorum.", "https://images.unsplash.com/photo-1486312338219-ce68d2c6f44d?w=400"),
        ("учиться", "öğrenmek, okumak", "Я учусь в школе.", "Okulda okuyorum.", "https://images.unsplash.com/photo-1523240795612-9a054b0db644?w=400"),
        ("думать", "düşünmek", "Я думаю о тебе.", "Seni düşünüyorum.", "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400"),
        ("знать", "bilmek", "Я знаю ответ.", "Cevabı biliyorum.", "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=400"),
        ("понимать", "anlamak", "Я понимаю по-турецки.", "Türkçe anlıyorum.", "https://images.unsplash.com/photo-1516534775068-ba3e7458af70?w=400"),
        ("любить", "sevmek", "Я люблю тебя.", "Seni seviyorum.", "https://images.unsplash.com/photo-1522673607106-f6b4b97e46d3?w=400"),
        ("жить", "yaşamak", "Я живу в Стамбуле.", "İstanbul'da yaşıyorum.", "https://images.unsplash.com/photo-1527838832700-5059252407fa?w=400"),
        ("есть", "yemek", "Я ем завтрак.", "Kahvaltı ediyorum.", "https://images.unsplash.com/photo-1533089860892-a7c6f0a88666?w=400"),
        ("пить", "içmek", "Я пью воду.", "Su içiyorum.", "https://images.unsplash.com/photo-1548839140-29a749e1cf4d?w=400"),
        ("спать", "uyumak", "Я сплю ночью.", "Geceleri uyuyorum.", "https://images.unsplash.com/photo-1513002749550-c59d786b8e6c?w=400"),
        ("идти", "gitmek, yürümek", "Я иду в школу.", "Okula gidiyorum.", "https://images.unsplash.com/photo-1483664852095-d6cc6870702d?w=400"),
        ("бежать", "koşmak", "Я бегу быстро.", "Hızlı koşuyorum.", "https://images.unsplash.com/photo-1476480862126-209bfaa8edc8?w=400"),
        ("сидеть", "oturmak", "Я сижу на стуле.", "Sandalyede oturuyorum.", "https://images.unsplash.com/photo-1503602642458-232111445657?w=400"),
        ("стоять", "durmak, ayakta durmak", "Я стою здесь.", "Burada duruyorum.", "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=400"),
        ("играть", "oynamak", "Я играю в футбол.", "Futbol oynuyorum.", "https://images.unsplash.com/photo-1574629810360-7efbbe195018?w=400"),
        ("петь", "şarkı söylemek", "Я пою песню.", "Şarkı söylüyorum.", "https://images.unsplash.com/photo-1516280440614-37939bbacd81?w=400"),
        ("танцевать", "dans etmek", "Я танцую.", "Dans ediyorum.", "https://images.unsplash.com/photo-1504609813442-a8924e83f76e?w=400"),
        ("готовить", "yemek yapmak", "Я готовлю обед.", "Öğle yemeği yapıyorum.", "https://images.unsplash.com/photo-1577219491135-ce391730fb2c?w=400"),
        ("покупать", "satın almak", "Я покупаю еду.", "Yiyecek satın alıyorum.", "https://images.unsplash.com/photo-1534452203293-494d7ddbf7e0?w=400"),
        ("продавать", "satmak", "Я продаю машину.", "Araba satıyorum.", "https://images.unsplash.com/photo-1549399542-7e3f8b79c341?w=400"),
        ("открывать", "açmak", "Я открываю дверь.", "Kapıyı açıyorum.", "https://images.unsplash.com/photo-1519710164239-da123dc03ef4?w=400"),
        ("закрывать", "kapatmak", "Я закрываю окно.", "Pencereyi kapatıyorum.", "https://images.unsplash.com/photo-1545259741-2ea3ebf61fa3?w=400"),
        ("брать", "almak", "Я беру книгу.", "Kitabı alıyorum.", "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=400"),
        ("давать", "vermek", "Я даю совет.", "Tavsiye veriyorum.", "https://images.unsplash.com/photo-1516534775068-ba3e7458af70?w=400"),
        ("помогать", "yardım etmek", "Я помогаю другу.", "Arkadaşa yardım ediyorum.", "https://images.unsplash.com/photo-1559027615-cd4628902d4a?w=400"),
    ]
    
    # Past tense verbs (30 words)
    past_verbs_data = [
        ("сказал", "söyledi (он)", "Он сказал правду.", "Doğruyu söyledi.", "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400"),
        ("прочитал", "okudu (он)", "Он прочитал книгу.", "Kitap okudu.", "https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=400"),
        ("написал", "yazdı (он)", "Он написал письмо.", "Mektup yazdı.", "https://images.unsplash.com/photo-1455390582262-044cdead277a?w=400"),
        ("послушал", "dinledi (он)", "Он послушал музыку.", "Müzik dinledi.", "https://images.unsplash.com/photo-1511379938547-c1f69419868d?w=400"),
        ("посмотрел", "baktı, seyretti (он)", "Он посмотрел фильм.", "Film seyretti.", "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=400"),
        ("работал", "çalıştı (он)", "Он работал вчера.", "Dün çalıştı.", "https://images.unsplash.com/photo-1486312338219-ce68d2c6f44d?w=400"),
        ("учился", "öğrendi (он)", "Он учился в школе.", "Okulda okudu.", "https://images.unsplash.com/photo-1523240795612-9a054b0db644?w=400"),
        ("думал", "düşündü (он)", "Он думал о работе.", "İş hakkında düşündü.", "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=400"),
        ("знал", "bildi (он)", "Он знал ответ.", "Cevabı bildi.", "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=400"),
        ("понял", "anladı (он)", "Он понял задачу.", "Görevi anladı.", "https://images.unsplash.com/photo-1516534775068-ba3e7458af70?w=400"),
        ("любил", "sevdi (он)", "Он любил музыку.", "Müziği sevdi.", "https://images.unsplash.com/photo-1511379938547-c1f69419868d?w=400"),
        ("жил", "yaşadı (он)", "Он жил в Москве.", "Moskova'da yaşadı.", "https://images.unsplash.com/photo-1520106212299-d99c443e4568?w=400"),
        ("ел", "yedi (он)", "Он ел суп.", "Çorba yedi.", "https://images.unsplash.com/photo-1547592166-23ac45744acd?w=400"),
        ("пил", "içti (он)", "Он пил чай.", "Çay içti.", "https://images.unsplash.com/photo-1564890369478-c89ca6d9cde9?w=400"),
        ("спал", "uyudu (он)", "Он спал весь день.", "Bütün gün uyudu.", "https://images.unsplash.com/photo-1513002749550-c59d786b8e6c?w=400"),
        ("пошёл", "gitti (он)", "Он пошёл домой.", "Eve gitti.", "https://images.unsplash.com/photo-1570129477492-45c003edd2be?w=400"),
        ("бежал", "koştu (он)", "Он бежал быстро.", "Hızlı koştu.", "https://images.unsplash.com/photo-1476480862126-209bfaa8edc8?w=400"),
        ("сидел", "oturdu (он)", "Он сидел на диване.", "Kanepede oturdu.", "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=400"),
        ("стоял", "durdu (он)", "Он стоял у окна.", "Pencerenin yanında durdu.", "https://images.unsplash.com/photo-1545259741-2ea3ebf61fa3?w=400"),
        ("играл", "oynadı (он)", "Он играл в футбол.", "Futbol oynadı.", "https://images.unsplash.com/photo-1574629810360-7efbbe195018?w=400"),
        ("пел", "şarkı söyledi (он)", "Он пел песню.", "Şarkı söyledi.", "https://images.unsplash.com/photo-1516280440614-37939bbacd81?w=400"),
        ("танцевал", "dans etti (он)", "Он танцевал на вечеринке.", "Partide dans etti.", "https://images.unsplash.com/photo-1504609813442-a8924e83f76e?w=400"),
        ("приготовил", "hazırladı (он)", "Он приготовил ужин.", "Akşam yemeğini hazırladı.", "https://images.unsplash.com/photo-1577219491135-ce391730fb2c?w=400"),
        ("купил", "satın aldı (он)", "Он купил машину.", "Araba satın aldı.", "https://images.unsplash.com/photo-1549399542-7e3f8b79c341?w=400"),
        ("продал", "sattı (он)", "Он продал дом.", "Evi sattı.", "https://images.unsplash.com/photo-1570129477492-45c003edd2be?w=400"),
        ("открыл", "açtı (он)", "Он открыл дверь.", "Kapıyı açtı.", "https://images.unsplash.com/photo-1519710164239-da123dc03ef4?w=400"),
        ("закрыл", "kapattı (он)", "Он закрыл окно.", "Pencereyi kapattı.", "https://images.unsplash.com/photo-1545259741-2ea3ebf61fa3?w=400"),
        ("взял", "aldı (он)", "Он взял книгу.", "Kitabı aldı.", "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=400"),
        ("дал", "verdi (он)", "Он дал совет.", "Tavsiye verdi.", "https://images.unsplash.com/photo-1516534775068-ba3e7458af70?w=400"),
        ("помог", "yardım etti (он)", "Он помог другу.", "Arkadaşa yardım etti.", "https://images.unsplash.com/photo-1559027615-cd4628902d4a?w=400"),
    ]
    
    # Future tense verbs (30 words)
    future_verbs_data = [
        ("скажу", "söyleyeceğim", "Я скажу правду.", "Doğruyu söyleyeceğim.", "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400"),
        ("прочитаю", "okuyacağım", "Я прочитаю книгу.", "Kitap okuyacağım.", "https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=400"),
        ("напишу", "yazacağım", "Я напишу письмо.", "Mektup yazacağım.", "https://images.unsplash.com/photo-1455390582262-044cdead277a?w=400"),
        ("послушаю", "dinleyeceğim", "Я послушаю музыку.", "Müzik dinleyeceğim.", "https://images.unsplash.com/photo-1511379938547-c1f69419868d?w=400"),
        ("посмотрю", "bakacağım, seyredeceğim", "Я посмотрю фильм.", "Film seyredeceğim.", "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=400"),
        ("буду работать", "çalışacağım", "Я буду работать завтра.", "Yarın çalışacağım.", "https://images.unsplash.com/photo-1486312338219-ce68d2c6f44d?w=400"),
        ("буду учиться", "öğreneceğim", "Я буду учиться в университете.", "Üniversitede okuyacağım.", "https://images.unsplash.com/photo-1523240795612-9a054b0db644?w=400"),
        ("буду думать", "düşüneceğim", "Я буду думать о будущем.", "Gelecek hakkında düşüneceğim.", "https://images.unsplash.com/photo-1506784983877-45594efa4cbe?w=400"),
        ("узнаю", "öğreneceğim", "Я узнаю ответ.", "Cevabı öğreneceğim.", "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=400"),
        ("пойму", "anlayacağım", "Я пойму урок.", "Dersi anlayacağım.", "https://images.unsplash.com/photo-1516534775068-ba3e7458af70?w=400"),
        ("полюблю", "seveceğim", "Я полюблю этот город.", "Bu şehri seveceğim.", "https://images.unsplash.com/photo-1480714378408-67cf0d13bc1b?w=400"),
        ("буду жить", "yaşayacağım", "Я буду жить в Турции.", "Türkiye'de yaşayacağım.", "https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?w=400"),
        ("съем", "yiyeceğim", "Я съем завтрак.", "Kahvaltı edeceğim.", "https://images.unsplash.com/photo-1533089860892-a7c6f0a88666?w=400"),
        ("выпью", "içeceğim", "Я выпью кофе.", "Kahve içeceğim.", "https://images.unsplash.com/photo-1511920170033-f8396924c348?w=400"),
        ("буду спать", "uyuyacağım", "Я буду спать рано.", "Erken uyuyacağım.", "https://images.unsplash.com/photo-1513002749550-c59d786b8e6c?w=400"),
        ("пойду", "gideceğim", "Я пойду в парк.", "Parka gideceğim.", "https://images.unsplash.com/photo-1564760055775-d63b17a55c44?w=400"),
        ("побегу", "koşacağım", "Я побегу утром.", "Sabah koşacağım.", "https://images.unsplash.com/photo-1476480862126-209bfaa8edc8?w=400"),
        ("буду сидеть", "oturacağım", "Я буду сидеть здесь.", "Burada oturacağım.", "https://images.unsplash.com/photo-1503602642458-232111445657?w=400"),
        ("буду стоять", "duracağım", "Я буду стоять в очереди.", "Kuyrukta duracağım.", "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=400"),
        ("буду играть", "oynayacağım", "Я буду играть в игру.", "Oyun oynayacağım.", "https://images.unsplash.com/photo-1511512578047-dfb367046420?w=400"),
        ("спою", "şarkı söyleyeceğim", "Я спою песню.", "Şarkı söyleyeceğim.", "https://images.unsplash.com/photo-1516280440614-37939bbacd81?w=400"),
        ("буду танцевать", "dans edeceğim", "Я буду танцевать.", "Dans edeceğim.", "https://images.unsplash.com/photo-1504609813442-a8924e83f76e?w=400"),
        ("приготовлю", "hazırlayacağım", "Я приготовлю ужин.", "Akşam yemeğini hazırlayacağım.", "https://images.unsplash.com/photo-1577219491135-ce391730fb2c?w=400"),
        ("куплю", "satın alacağım", "Я куплю билет.", "Bilet satın alacağım.", "https://images.unsplash.com/photo-1509281373149-e957c6296406?w=400"),
        ("продам", "satacağım", "Я продам машину.", "Araba satacağım.", "https://images.unsplash.com/photo-1549399542-7e3f8b79c341?w=400"),
        ("открою", "açacağım", "Я открою магазин.", "Mağaza açacağım.", "https://images.unsplash.com/photo-1441984904996-e0b6ba687e04?w=400"),
        ("закрою", "kapatacağım", "Я закрою дверь.", "Kapıyı kapatacağım.", "https://images.unsplash.com/photo-1519710164239-da123dc03ef4?w=400"),
        ("возьму", "alacağım", "Я возьму сумку.", "Çantayı alacağım.", "https://images.unsplash.com/photo-1590874103328-eac38a683ce7?w=400"),
        ("дам", "vereceğim", "Я дам совет.", "Tavsiye vereceğim.", "https://images.unsplash.com/photo-1516534775068-ba3e7458af70?w=400"),
        ("помогу", "yardım edeceğim", "Я помогу тебе.", "Sana yardım edeceğim.", "https://images.unsplash.com/photo-1559027615-cd4628902d4a?w=400"),
    ]
    
    # Create words
    def create_words_from_data(cat_id, data_list, is_russian_first=False):
        words = []
        for item in data_list:
            if is_russian_first:
                russian, turkish, ru_sentence, tr_sentence, image = item
            else:
                turkish, russian, tr_sentence, ru_sentence, image = item
            
            words.append({
                "word_id": f"word_{uuid.uuid4().hex[:12]}",
                "category_id": cat_id,
                "turkish": turkish,
                "russian": russian,
                "turkish_sentence": tr_sentence,
                "russian_sentence": ru_sentence,
                "image_url": image,
                "audio_url_turkish": f"https://texttospeech.googleapis.com/v1/text:synthesize?text={turkish}",
                "audio_url_russian": f"https://texttospeech.googleapis.com/v1/text:synthesize?text={russian}",
                "created_by": SUPER_ADMIN_USER_ID,
                "created_at": datetime.now(timezone.utc)
            })
        return words
    
    data_mapping = [
        ("gender_masculine", masculine_data, True),
        ("gender_feminine", feminine_data, True),
        ("gender_neuter", neuter_data, True),
        ("verbs_present", present_verbs_data, True),
        ("verbs_past", past_verbs_data, True),
        ("verbs_future", future_verbs_data, True)
    ]
    
    for cat_info in grammar_cats:
        cat_id = cat_info["category_id"]
        cat_words = []
        for mapping_id, data, is_russian_first in data_mapping:
            if mapping_id == cat_id:
                cat_words = create_words_from_data(cat_id, data, is_russian_first)
                break
        
        cat_info["word_count"] = len(cat_words)
        cat_info["created_by"] = SUPER_ADMIN_USER_ID
        cat_info["created_at"] = datetime.now(timezone.utc)
        
        categories_to_insert.append(cat_info)
        words_to_insert.extend(cat_words)
    
    # Insert to database
    if categories_to_insert:
        await db.categories.insert_many(categories_to_insert)
        print(f"✅ {len(categories_to_insert)} kategori eklendi")
    
    if words_to_insert:
        await db.words.insert_many(words_to_insert)
        print(f"✅ {len(words_to_insert)} kelime eklendi")
    
    print(f"\n📊 Part 3 Özet:")
    print(f"  - Yeni Kategori: {len(categories_to_insert)}")
    print(f"  - Yeni Kelime: {len(words_to_insert)}")
    print("🎉 Part 3 tamamlandı!")

if __name__ == "__main__":
    asyncio.run(seed_grammar_verbs())
    client.close()
