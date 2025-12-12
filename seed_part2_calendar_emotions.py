"""
Part 2: Calendar (Days, Months, Seasons, Time), Emotions, Nature, City
Adds ~120 words
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

# Get existing super admin ID
async def get_super_admin_id():
    user = await db.users.find_one({"role": "super_admin"})
    if user:
        return user.get("user_id") or user.get("id")
    return f"user_{uuid.uuid4().hex[:12]}"

async def seed_calendar_emotions():
    print("🌱 Takvim, Duygular ve Doğa kategorileri ekleniyor...")
    
    SUPER_ADMIN_USER_ID = await get_super_admin_id()
    
    # Check if already exists
    existing = await db.categories.count_documents({"category_id": "days"})
    if existing > 0:
        print("⚠️  Bu kategoriler zaten mevcut.")
        return
    
    categories_to_insert = []
    words_to_insert = []
    
    # ==================== CALENDAR ====================
    calendar_cats = [
        {
            "category_id": "days",
            "name_tr": "Günler",
            "name_ru": "Дни недели",
            "icon": "📅",
            "level": "A1",
            "color": "#FF6B6B"
        },
        {
            "category_id": "months",
            "name_tr": "Aylar",
            "name_ru": "Месяцы",
            "icon": "🗓️",
            "level": "A1",
            "color": "#4ECDC4"
        },
        {
            "category_id": "seasons",
            "name_tr": "Mevsimler",
            "name_ru": "Времена года",
            "icon": "🌸",
            "level": "A1",
            "color": "#95E1D3"
        },
        {
            "category_id": "time_expressions",
            "name_tr": "Zaman İfadeleri",
            "name_ru": "Выражения времени",
            "icon": "⏰",
            "level": "A2",
            "color": "#F38181"
        },
        {
            "category_id": "emotions",
            "name_tr": "Duygular",
            "name_ru": "Эмоции",
            "icon": "😊",
            "level": "A1",
            "color": "#AA96DA"
        },
        {
            "category_id": "nature",
            "name_tr": "Doğa",
            "name_ru": "Природа",
            "icon": "🌳",
            "level": "A2",
            "color": "#FCBAD3"
        },
        {
            "category_id": "city",
            "name_tr": "Şehir",
            "name_ru": "Город",
            "icon": "🏙️",
            "level": "A2",
            "color": "#FFFFD2"
        }
    ]
    
    # Days of the week (14 words - 7 days + 7 related words)
    days_data = [
        ("Pazartesi", "понедельник", "Pazartesi işe gidiyorum.", "В понедельник я иду на работу.", "https://images.unsplash.com/photo-1506784983877-45594efa4cbe?w=400"),
        ("Salı", "вторник", "Salı günü toplantım var.", "Во вторник у меня встреча.", "https://images.unsplash.com/photo-1516534775068-ba3e7458af70?w=400"),
        ("Çarşamba", "среда", "Çarşamba ortası.", "Середина недели - среда.", "https://images.unsplash.com/photo-1533154683836-84ea7a0bc310?w=400"),
        ("Perşembe", "четверг", "Perşembe akşamı sinemaya gidiyoruz.", "В четверг вечером мы идём в кино.", "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=400"),
        ("Cuma", "пятница", "Cuma günü dinleniyorum.", "В пятницу я отдыхаю.", "https://images.unsplash.com/photo-1553444836-bc6c8d340ba7?w=400"),
        ("Cumartesi", "суббота", "Cumartesi alışverişe gidiyoruz.", "В субботу мы идём за покупками.", "https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=400"),
        ("Pazar", "воскресенье", "Pazar günü ailece yemek yiyoruz.", "В воскресенье мы обедаем всей семьёй.", "https://images.unsplash.com/photo-1517842645767-c639042777db?w=400"),
        ("hafta", "неделя", "Bir hafta yedi gün.", "В неделе семь дней.", "https://images.unsplash.com/photo-1611003228941-98852ba62227?w=400"),
        ("bugün", "сегодня", "Bugün güzel bir gün.", "Сегодня хороший день.", "https://images.unsplash.com/photo-1501139083538-0139583c060f?w=400"),
        ("dün", "вчера", "Dün sinemaya gittim.", "Вчера я ходил в кино.", "https://images.unsplash.com/photo-1478720568477-152d9b164e26?w=400"),
        ("yarın", "завтра", "Yarın sınav var.", "Завтра экзамен.", "https://images.unsplash.com/photo-1506784365847-bbad939e9335?w=400"),
        ("hafta sonu", "выходные", "Hafta sonu dinleniyorum.", "На выходных я отдыхаю.", "https://images.unsplash.com/photo-1506784926709-22f1ec395907?w=400"),
        ("hafta içi", "будни", "Hafta içi çalışıyorum.", "В будни я работаю.", "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=400"),
        ("gün", "день", "Güzel bir gün.", "Хороший день.", "https://images.unsplash.com/photo-1495364141860-b0d03eccd065?w=400"),
    ]
    
    # Months (12 words)
    months_data = [
        ("Ocak", "январь", "Ocak ayı soğuk.", "Январь холодный.", "https://images.unsplash.com/photo-1483664852095-d6cc6870702d?w=400"),
        ("Şubat", "февраль", "Şubat kısa bir ay.", "Февраль - короткий месяц.", "https://images.unsplash.com/photo-1486870591958-9b9d0d1dda99?w=400"),
        ("Mart", "март", "Mart'ta bahar başlıyor.", "В марте начинается весна.", "https://images.unsplash.com/photo-1490750967868-88aa4486c946?w=400"),
        ("Nisan", "апрель", "Nisan yağmurlu.", "Апрель дождливый.", "https://images.unsplash.com/photo-1491677533189-49af044391ed?w=400"),
        ("Mayıs", "май", "Mayıs çiçek açıyor.", "В мае цветут цветы.", "https://images.unsplash.com/photo-1462216589242-9e3e00a47a48?w=400"),
        ("Haziran", "июнь", "Haziran sıcak.", "Июнь жаркий.", "https://images.unsplash.com/photo-1499728603263-13726abce5fd?w=400"),
        ("Temmuz", "июль", "Temmuz en sıcak ay.", "Июль - самый жаркий месяц.", "https://images.unsplash.com/photo-1494783367193-149034c05e8f?w=400"),
        ("Ağustos", "август", "Ağustos'ta tatil yapıyoruz.", "В августе мы отдыхаем.", "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=400"),
        ("Eylül", "сентябрь", "Eylül'de okul başlıyor.", "В сентябре начинается школа.", "https://images.unsplash.com/photo-1502082553048-f009c37129b9?w=400"),
        ("Ekim", "октябрь", "Ekim'de yapraklar dökülüyor.", "В октябре опадают листья.", "https://images.unsplash.com/photo-1509579332522-892d62f9bbb8?w=400"),
        ("Kasım", "ноябрь", "Kasım soğuk.", "Ноябрь холодный.", "https://images.unsplash.com/photo-1447752875215-b2761acb3c5d?w=400"),
        ("Aralık", "декабрь", "Aralık'ta kar yağıyor.", "В декабре идёт снег.", "https://images.unsplash.com/photo-1482517967863-00e15c9b44be?w=400"),
    ]
    
    # Seasons (12 words - 4 seasons + 8 related)
    seasons_data = [
        ("ilkbahar", "весна", "İlkbaharda çiçekler açıyor.", "Весной цветут цветы.", "https://images.unsplash.com/photo-1490750967868-88aa4486c946?w=400"),
        ("yaz", "лето", "Yaz çok sıcak.", "Лето очень жаркое.", "https://images.unsplash.com/photo-1473496169904-658ba7c44d8a?w=400"),
        ("sonbahar", "осень", "Sonbaharda yapraklar sarı.", "Осенью листья жёлтые.", "https://images.unsplash.com/photo-1509579332522-892d62f9bbb8?w=400"),
        ("kış", "зима", "Kışın kar yağıyor.", "Зимой идёт снег.", "https://images.unsplash.com/photo-1482517967863-00e15c9b44be?w=400"),
        ("hava", "погода", "Hava güzel.", "Погода хорошая.", "https://images.unsplash.com/photo-1504608524841-42fe6f032b4b?w=400"),
        ("güneş", "солнце", "Güneş parlıyor.", "Солнце светит.", "https://images.unsplash.com/photo-1602496674108-a5aab96d51a7?w=400"),
        ("yağmur", "дождь", "Yağmur yağıyor.", "Идёт дождь.", "https://images.unsplash.com/photo-1519692933481-e162a57d6721?w=400"),
        ("kar", "снег", "Kar beyaz.", "Снег белый.", "https://images.unsplash.com/photo-1491002052546-bf38f186af56?w=400"),
        ("rüzgar", "ветер", "Rüzgar esiyor.", "Дует ветер.", "https://images.unsplash.com/photo-1534088568595-a066f410bcda?w=400"),
        ("bulut", "облако, туча", "Bulutlar gri.", "Облака серые.", "https://images.unsplash.com/photo-1534088568595-a066f410bcda?w=400"),
        ("sıcak", "жарко", "Çok sıcak.", "Очень жарко.", "https://images.unsplash.com/photo-1521651201144-634f700b36ef?w=400"),
        ("soğuk", "холодно", "Çok soğuk.", "Очень холодно.", "https://images.unsplash.com/photo-1477601263568-180e2c6d046e?w=400"),
    ]
    
    # Time expressions (20 words)
    time_data = [
        ("şimdi", "сейчас", "Şimdi ne yapıyorsun?", "Что ты делаешь сейчас?", "https://images.unsplash.com/photo-1501139083538-0139583c060f?w=400"),
        ("sonra", "потом, позже", "Sonra görüşürüz.", "Увидимся позже.", "https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=400"),
        ("önce", "раньше, сначала", "Önce yemek ye.", "Сначала поешь.", "https://images.unsplash.com/photo-1577219491135-ce391730fb2c?w=400"),
        ("her zaman", "всегда", "Her zaman mutluyum.", "Я всегда счастлив.", "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400"),
        ("hiçbir zaman", "никогда", "Hiçbir zaman yalan söylemem.", "Я никогда не лгу.", "https://images.unsplash.com/photo-1504593811423-6dd665756598?w=400"),
        ("bazen", "иногда", "Bazen sinemaya giderim.", "Иногда я хожу в кино.", "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=400"),
        ("genellikle", "обычно", "Genellikle erken kalkarım.", "Обычно я встаю рано.", "https://images.unsplash.com/photo-1483664852095-d6cc6870702d?w=400"),
        ("sık sık", "часто", "Sık sık spor yaparım.", "Я часто занимаюсь спортом.", "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=400"),
        ("nadiren", "редко", "Nadiren et yerim.", "Я редко ем мясо.", "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=400"),
        ("sabah", "утро", "Sabah kahvaltı yapıyorum.", "Утром я завтракаю.", "https://images.unsplash.com/photo-1495214783159-3503fd1b572d?w=400"),
        ("öğle", "полдень", "Öğle yemeği yedik.", "Мы пообедали.", "https://images.unsplash.com/photo-1547592166-23ac45744acd?w=400"),
        ("akşam", "вечер", "Akşam eve geliyorum.", "Вечером я прихожу домой.", "https://images.unsplash.com/photo-1470252649378-9c29740c9fa8?w=400"),
        ("gece", "ночь", "Gece uyuyorum.", "Ночью я сплю.", "https://images.unsplash.com/photo-1513002749550-c59d786b8e6c?w=400"),
        ("erken", "рано", "Erken kalkıyorum.", "Я встаю рано.", "https://images.unsplash.com/photo-1495364141860-b0d03eccd065?w=400"),
        ("geç", "поздно", "Geç yattım.", "Я лёг поздно.", "https://images.unsplash.com/photo-1513002749550-c59d786b8e6c?w=400"),
        ("saat", "час, время", "Saat kaç?", "Который час?", "https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=400"),
        ("dakika", "минута", "Beş dakika bekle.", "Подожди пять минут.", "https://images.unsplash.com/photo-1501139083538-0139583c060f?w=400"),
        ("saniye", "секунда", "Bir saniye!", "Секунду!", "https://images.unsplash.com/photo-1495364141860-b0d03eccd065?w=400"),
        ("yıl", "год", "Bu yıl çok çalıştım.", "В этом году я много работал.", "https://images.unsplash.com/photo-1506784365847-bbad939e9335?w=400"),
        ("ay", "месяц", "Geçen ay tatile gittim.", "В прошлом месяце я ездил в отпуск.", "https://images.unsplash.com/photo-1506784983877-45594efa4cbe?w=400"),
    ]
    
    # Emotions (20 words)
    emotions_data = [
        ("mutlu", "счастливый", "Çok mutluyum.", "Я очень счастлив.", "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400"),
        ("üzgün", "грустный", "Biraz üzgünüm.", "Я немного грущу.", "https://images.unsplash.com/photo-1467810563316-b5476525c0f9?w=400"),
        ("kızgın", "сердитый", "Ona kızgınım.", "Я сержусь на него.", "https://images.unsplash.com/photo-1485178575877-1a13bf489dfe?w=400"),
        ("yorgun", "уставший", "Çok yorgunum.", "Я очень устал.", "https://images.unsplash.com/photo-1541593095826-d8bb64b3a21e?w=400"),
        ("heyecanlı", "взволнованный", "Çok heyecanlıyım.", "Я очень взволнован.", "https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?w=400"),
        ("sakin", "спокойный", "Sakin ol.", "Будь спокоен.", "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400"),
        ("endişeli", "встревоженный", "Biraz endişeliyim.", "Я немного встревожен.", "https://images.unsplash.com/photo-1499209974431-9dddcece7f88?w=400"),
        ("şaşırmış", "удивлённый", "Çok şaşırdım.", "Я очень удивлён.", "https://images.unsplash.com/photo-1551069613-1904dbdcda11?w=400"),
        ("korkmuş", "испуганный", "Korktum.", "Я испугался.", "https://images.unsplash.com/photo-1609743522653-52354461eb27?w=400"),
        ("gülümseyen", "улыбающийся", "Gülümsüyorum.", "Я улыбаюсь.", "https://images.unsplash.com/photo-1542596768-5d1d21f1cf98?w=400"),
        ("üşümüş", "замёрзший", "Çok üşüdüm.", "Я очень замёрз.", "https://images.unsplash.com/photo-1477601263568-180e2c6d046e?w=400"),
        ("aç", "голодный", "Çok açım.", "Я очень голоден.", "https://images.unsplash.com/photo-1547592166-23ac45744acd?w=400"),
        ("tok", "сытый", "Tokum.", "Я сыт.", "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=400"),
        ("susuz", "жаждущий", "Susuzum.", "Я хочу пить.", "https://images.unsplash.com/photo-1548839140-29a749e1cf4d?w=400"),
        ("hasta", "больной", "Hastayım.", "Я болен.", "https://images.unsplash.com/photo-1584515933487-779824d29309?w=400"),
        ("sağlıklı", "здоровый", "Sağlıklıyım.", "Я здоров.", "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=400"),
        ("güçlü", "сильный", "Çok güçlüyüm.", "Я очень сильный.", "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=400"),
        ("zayıf", "слабый", "Biraz zayıfım.", "Я немного слаб.", "https://images.unsplash.com/photo-1541593095826-d8bb64b3a21e?w=400"),
        ("sıkılmış", "скучающий", "Çok sıkıldım.", "Мне очень скучно.", "https://images.unsplash.com/photo-1499209974431-9dddcece7f88?w=400"),
        ("eğlenen", "веселящийся", "Çok eğleniyorum.", "Я очень веселюсь.", "https://images.unsplash.com/photo-1511632765486-a01980e01a18?w=400"),
    ]
    
    # Nature (25 words)
    nature_data = [
        ("ağaç", "дерево", "Ağaç büyük.", "Дерево большое.", "https://images.unsplash.com/photo-1542273917363-3b1817f69a2d?w=400"),
        ("çiçek", "цветок", "Çiçek güzel.", "Цветок красивый.", "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=400"),
        ("yaprak", "лист", "Yapraklar yeşil.", "Листья зелёные.", "https://images.unsplash.com/photo-1557672172-298e090bd0f1?w=400"),
        ("ot", "трава", "Ot yeşil.", "Трава зелёная.", "https://images.unsplash.com/photo-1560750588-73207b1ef5b8?w=400"),
        ("toprak", "земля, почва", "Toprak kahverengi.", "Земля коричневая.", "https://images.unsplash.com/photo-1530836369250-ef72a3f5cda8?w=400"),
        ("taş", "камень", "Taş sert.", "Камень твёрдый.", "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=400"),
        ("dağ", "гора", "Dağlar yüksek.", "Горы высокие.", "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400"),
        ("deniz", "море", "Deniz mavi.", "Море синее.", "https://images.unsplash.com/photo-1505142468610-359e7d316be0?w=400"),
        ("göl", "озеро", "Göl sakin.", "Озеро спокойное.", "https://images.unsplash.com/photo-1439066615861-d1af74d74000?w=400"),
        ("nehir", "река", "Nehir akıyor.", "Река течёт.", "https://images.unsplash.com/photo-1501594907352-04cda38ebc29?w=400"),
        ("orman", "лес", "Ormanda yürüyoruz.", "Мы гуляем в лесу.", "https://images.unsplash.com/photo-1542273917363-3b1817f69a2d?w=400"),
        ("kum", "песок", "Kum sarı.", "Песок жёлтый.", "https://images.unsplash.com/photo-1519046904884-53103b34b206?w=400"),
        ("kumsal", "пляж", "Kumsalda oynuyoruz.", "Мы играем на пляже.", "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=400"),
        ("ada", "остров", "Adada tatil yapıyoruz.", "Мы отдыхаем на острове.", "https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=400"),
        ("gökyüzü", "небо", "Gökyüzü mavi.", "Небо синее.", "https://images.unsplash.com/photo-1419242902214-272b3f66ee7a?w=400"),
        ("yıldız", "звезда", "Yıldızlar parlıyor.", "Звёзды сияют.", "https://images.unsplash.com/photo-1502134249126-9f3755a50d78?w=400"),
        ("ay", "луна", "Ay parlak.", "Луна яркая.", "https://images.unsplash.com/photo-1509023464722-18d996393ca8?w=400"),
        ("dünya", "земля, мир", "Dünya güzel.", "Мир прекрасен.", "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=400"),
        ("yangın", "пожар", "Orman yangını tehlikeli.", "Лесной пожар опасен.", "https://images.unsplash.com/photo-1515162305285-0293e4767cc2?w=400"),
        ("sel", "наводнение", "Sel felaket.", "Наводнение - это бедствие.", "https://images.unsplash.com/photo-1527482797697-8795b05a13fe?w=400"),
        ("deprem", "землетрясение", "Deprem korkunç.", "Землетрясение страшное.", "https://images.unsplash.com/photo-1540574163026-643ea20ade25?w=400"),
        ("fırtına", "буря, шторм", "Fırtına geliyor.", "Приближается буря.", "https://images.unsplash.com/photo-1527482937786-6608b9740778?w=400"),
        ("gök gürültüsü", "гром", "Gök gürültüsü duydum.", "Я услышал гром.", "https://images.unsplash.com/photo-1525183077936-e5fca0f194df?w=400"),
        ("şimşek", "молния", "Şimşek çaktı.", "Сверкнула молния.", "https://images.unsplash.com/photo-1519693062680-1043a4d6a8b0?w=400"),
        ("gökkuşağı", "радуга", "Gökkuşağı renkli.", "Радуга разноцветная.", "https://images.unsplash.com/photo-1419833173245-f59e1b93f9ee?w=400"),
    ]
    
    # City (20 words)
    city_data = [
        ("bina", "здание", "Bina yüksek.", "Здание высокое.", "https://images.unsplash.com/photo-1480714378408-67cf0d13bc1b?w=400"),
        ("cadde", "улица, проспект", "Cadde kalabalık.", "Улица многолюдная.", "https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=400"),
        ("sokak", "улица (узкая)", "Sokak dar.", "Улица узкая.", "https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?w=400"),
        ("park", "парк", "Parkta oynuyoruz.", "Мы играем в парке.", "https://images.unsplash.com/photo-1564760055775-d63b17a55c44?w=400"),
        ("meydan", "площадь", "Meydanda insanlar var.", "На площади есть люди.", "https://images.unsplash.com/photo-1555109307-f7d9da25c244?w=400"),
        ("köprü", "мост", "Köprüden geçiyoruz.", "Мы проходим через мост.", "https://images.unsplash.com/photo-1518623001395-125242310d0c?w=400"),
        ("okul", "школа", "Okula gidiyorum.", "Я иду в школу.", "https://images.unsplash.com/photo-1580582932707-520aed937b7b?w=400"),
        ("hastane", "больница", "Hastane büyük.", "Больница большая.", "https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?w=400"),
        ("market", "магазин, супермаркет", "Marketten alışveriş yaptık.", "Мы купили в магазине.", "https://images.unsplash.com/photo-1578916171728-46686eac8d58?w=400"),
        ("restoran", "ресторан", "Restoranda yemek yiyoruz.", "Мы едим в ресторане.", "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=400"),
        ("kafe", "кафе", "Kafede oturuyoruz.", "Мы сидим в кафе.", "https://images.unsplash.com/photo-1445116572660-236099ec97a0?w=400"),
        ("sinema", "кинотеатр", "Sinemaya gidiyoruz.", "Мы идём в кино.", "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=400"),
        ("müze", "музей", "Müzede geziyoruz.", "Мы гуляем по музею.", "https://images.unsplash.com/photo-1555421689-43fe3e0c6b2b?w=400"),
        ("kütüphane", "библиотека", "Kütüphanede kitap okuyorum.", "Я читаю книги в библиотеке.", "https://images.unsplash.com/photo-1521587760476-6c12a4b040da?w=400"),
        ("postane", "почта", "Postaneye gidiyorum.", "Я иду на почту.", "https://images.unsplash.com/photo-1514849302-984523450cf4?w=400"),
        ("banka", "банк", "Bankada param var.", "У меня есть деньги в банке.", "https://images.unsplash.com/photo-1541354329998-f4d9a9f9297f?w=400"),
        ("otel", "отель", "Otelde kalıyoruz.", "Мы останавливаемся в отеле.", "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=400"),
        ("havaalanı", "аэропорт", "Havaalanında bekliyoruz.", "Мы ждём в аэропорту.", "https://images.unsplash.com/photo-1436491865332-7a61a109cc05?w=400"),
        ("istasyon", "станция, вокзал", "İstasyonda treni bekliyoruz.", "Мы ждём поезд на станции.", "https://images.unsplash.com/photo-1474487548417-781cb71495f3?w=400"),
        ("otopark", "парковка", "Otoparkta araba var.", "На парковке есть машины.", "https://images.unsplash.com/photo-1509824227185-9c5a01ceba0d?w=400"),
    ]
    
    # Create words
    def create_words_from_data(cat_id, data_list):
        words = []
        for turkish, russian, tr_sentence, ru_sentence, image in data_list:
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
        ("days", days_data),
        ("months", months_data),
        ("seasons", seasons_data),
        ("time_expressions", time_data),
        ("emotions", emotions_data),
        ("nature", nature_data),
        ("city", city_data)
    ]
    
    for cat_info in calendar_cats:
        cat_id = cat_info["category_id"]
        cat_words = []
        for mapping_id, data in data_mapping:
            if mapping_id == cat_id:
                cat_words = create_words_from_data(cat_id, data)
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
    
    print(f"\n📊 Part 2 Özet:")
    print(f"  - Yeni Kategori: {len(categories_to_insert)}")
    print(f"  - Yeni Kelime: {len(words_to_insert)}")
    print("🎉 Part 2 tamamlandı!")

if __name__ == "__main__":
    asyncio.run(seed_calendar_emotions())
    client.close()
