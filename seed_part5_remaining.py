"""
Part 5: Remaining categories to reach 1000+ words
Technology, Work, Daily Conversation, Hobbies, Travel, Adjectives
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

async def seed_remaining():
    print("🌱 Kalan kategoriler ekleniyor (1000 kelimeye ulaşmak için)...")
    
    SUPER_ADMIN_USER_ID = await get_super_admin_id()
    
    existing = await db.categories.count_documents({"category_id": "technology"})
    if existing > 0:
        print("⚠️  Bu kategoriler zaten mevcut.")
        return
    
    categories_to_insert = []
    words_to_insert = []
    
    # Categories
    remaining_cats = [
        {"category_id": "technology", "name_tr": "Teknoloji", "name_ru": "Технология", "icon": "💻", "level": "B1", "color": "#FF99FF"},
        {"category_id": "work_office", "name_tr": "İş ve Ofis", "name_ru": "Работа и офис", "icon": "💼", "level": "B1", "color": "#99FFFF"},
        {"category_id": "daily_conversation", "name_tr": "Günlük Konuşma", "name_ru": "Повседневный разговор", "icon": "💬", "level": "A1", "color": "#FFD700"},
        {"category_id": "hobbies", "name_tr": "Hobiler", "name_ru": "Хобби", "icon": "🎨", "level": "B1", "color": "#87CEEB"},
        {"category_id": "travel", "name_tr": "Seyahat", "name_ru": "Путешествие", "icon": "✈️", "level": "B1", "color": "#FFA07A"},
        {"category_id": "adjectives", "name_tr": "Sıfatlar", "name_ru": "Прилагательные", "icon": "📝", "level": "A2", "color": "#DDA0DD"}
    ]
    
    # Technology (40)
    tech_data = [
        ("bilgisayar", "компьютер", "Bilgisayarda çalışıyorum.", "Я работаю на компьютере.", "https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=400"),
        ("telefon", "телефон", "Telefonla konuşuyorum.", "Я разговариваю по телефону.", "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400"),
        ("tablet", "планшет", "Tabletle okuyorum.", "Я читаю на планшете.", "https://images.unsplash.com/photo-1561154464-82e9adf32764?w=400"),
        ("internet", "интернет", "İnternete bağlanıyorum.", "Я подключаюсь к интернету.", "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=400"),
        ("site", "сайт", "Siteye giriyorum.", "Я захожу на сайт.", "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=400"),
        ("uygulama", "приложение", "Uygulama indiriyorum.", "Я скачиваю приложение.", "https://images.unsplash.com/photo-1512941937669-90a1b58e7e9c?w=400"),
        ("şifre", "пароль", "Şifremi unuttum.", "Я забыл свой пароль.", "https://images.unsplash.com/photo-1633265486064-086b219458ec?w=400"),
        ("e-posta", "электронная почта", "E-posta gönderiyorum.", "Я отправляю письмо.", "https://images.unsplash.com/photo-1557200134-90327ee9fafa?w=400"),
        ("mesaj", "сообщение", "Mesaj yazdım.", "Я написал сообщение.", "https://images.unsplash.com/photo-1562155618-e1a8bc2eb04f?w=400"),
        ("video", "видео", "Video izliyorum.", "Я смотрю видео.", "https://images.unsplash.com/photo-1574717024653-61fd2cf4d44d?w=400"),
        ("fotoğraf", "фотография", "Fotoğraf çektim.", "Я сделал фотографию.", "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=400"),
        ("kamera", "камера", "Kamera açık.", "Камера включена.", "https://images.unsplash.com/photo-1502920917128-1aa500764cbd?w=400"),
        ("ekran", "экран", "Ekran büyük.", "Экран большой.", "https://images.unsplash.com/photo-1593642632823-8f785ba67e45?w=400"),
        ("klavye", "клавиатура", "Klavye rahat.", "Клавиатура удобная.", "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=400"),
        ("fare", "мышь (компьютерная)", "Fare küçük.", "Мышь маленькая.", "https://images.unsplash.com/photo-1563297007-0686b7003af7?w=400"),
        ("yazıcı", "принтер", "Yazıcı bozuk.", "Принтер сломан.", "https://images.unsplash.com/photo-1612815154858-60aa4c59eaa6?w=400"),
        ("tarayıcı", "сканер", "Tarayıcı çalışıyor.", "Сканер работает.", "https://images.unsplash.com/photo-1585771198544-a8dfdb3e4c92?w=400"),
        ("program", "программа", "Program yüklendi.", "Программа загружена.", "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=400"),
        ("dosya", "файл", "Dosyayı açtım.", "Я открыл файл.", "https://images.unsplash.com/photo-1618477388954-7852f32655ec?w=400"),
        ("klasör", "папка", "Klasör oluşturdum.", "Я создал папку.", "https://images.unsplash.com/photo-1544396821-4dd40b938ad3?w=400"),
        ("indirmek", "скачивать", "Dosyayı indiriyorum.", "Я скачиваю файл.", "https://images.unsplash.com/photo-1592659762303-90081d34b277?w=400"),
        ("yüklemek", "загружать", "Fotoğraf yüklüyorum.", "Я загружаю фотографию.", "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=400"),
        ("silmek", "удалять", "Dosyayı sildim.", "Я удалил файл.", "https://images.unsplash.com/photo-1594312915251-48db9280c8f1?w=400"),
        ("kaydetmek", "сохранять", "Dosyayı kaydettim.", "Я сохранил файл.", "https://images.unsplash.com/photo-1563986768609-322da13575f3?w=400"),
        ("kopyalamak", "копировать", "Metni kopyalıyorum.", "Я копирую текст.", "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=400"),
        ("yapıştırmak", "вставлять", "Metni yapıştırıyorum.", "Я вставляю текст.", "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=400"),
        ("aramak", "искать", "Google'da arıyorum.", "Я ищу в Google.", "https://images.unsplash.com/photo-1573804633927-bfcbcd909acd?w=400"),
        ("bağlantı", "ссылка", "Bağlantıya tıkladım.", "Я нажал на ссылку.", "https://images.unsplash.com/photo-1593720213428-28a5b9e94613?w=400"),
        ("tıklamak", "нажимать, кликать", "Butona tıklıyorum.", "Я нажимаю на кнопку.", "https://images.unsplash.com/photo-1563986768609-322da13575f3?w=400"),
        ("açmak", "открывать", "Programı açıyorum.", "Я открываю программу.", "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=400"),
        ("kapatmak", "закрывать", "Programı kapatıyorum.", "Я закрываю программу.", "https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=400"),
        ("şarj", "зарядка", "Telefon şarjda.", "Телефон на зарядке.", "https://images.unsplash.com/photo-1609693411508-f1c886e69821?w=400"),
        ("pil", "батарея, аккумулятор", "Pil bitti.", "Батарея села.", "https://images.unsplash.com/photo-1626495764640-d0e2c81cc1e9?w=400"),
        ("kulaklık", "наушники", "Kulaklıkla müzik dinliyorum.", "Я слушаю музыку в наушниках.", "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400"),
        ("hoparlör", "динамик, колонка", "Hoparlör açık.", "Динамик включён.", "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=400"),
        ("wifi", "вай-фай", "Wifi şifresi nedir?", "Какой пароль от вай-фая?", "https://images.unsplash.com/photo-1606904825846-647eb07f5be2?w=400"),
        ("bluetooth", "блютуз", "Bluetooth'u açtım.", "Я включил блютуз.", "https://images.unsplash.com/photo-1608889476518-738c9b1dcb10?w=400"),
        ("kablo", "кабель", "Kablo uzun.", "Кабель длинный.", "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400"),
        ("çekmek", "снимать (фото)", "Fotoğraf çekiyorum.", "Я фотографирую.", "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=400"),
        ("paylaşmak", "делиться", "Fotoğrafı paylaştım.", "Я поделился фотографией.", "https://images.unsplash.com/photo-1611162617213-7d7a39e9b1d7?w=400"),
    ]
    
    # Work & Office (40)
    work_data = [
        ("iş", "работа", "İşe gidiyorum.", "Я иду на работу.", "https://images.unsplash.com/photo-1486312338219-ce68d2c6f44d?w=400"),
        ("ofis", "офис", "Ofiste çalışıyorum.", "Я работаю в офисе.", "https://images.unsplash.com/photo-1497366216548-37526070297c?w=400"),
        ("şirket", "компания", "Şirkette çalışıyorum.", "Я работаю в компании.", "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=400"),
        ("patron", "начальник, босс", "Patronla konuştum.", "Я поговорил с начальником.", "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400"),
        ("müdür", "директор, менеджер", "Müdür toplantıda.", "Директор на совещании.", "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=400"),
        ("çalışan", "сотрудник, работник", "Çalışanlar toplantıda.", "Сотрудники на совещании.", "https://images.unsplash.com/photo-1521737711867-e3b97375f902?w=400"),
        ("maaş", "зарплата", "Maaşımı aldım.", "Я получил зарплату.", "https://images.unsplash.com/photo-1579621970563-ebec7560ff3e?w=400"),
        ("mola", "перерыв", "Mola veriyoruz.", "Мы делаем перерыв.", "https://images.unsplash.com/photo-1556761175-4b46a572b786?w=400"),
        ("toplantı", "собрание, совещание", "Toplantı başladı.", "Собрание началось.", "https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?w=400"),
        ("proje", "проект", "Projede çalışıyorum.", "Я работаю над проектом.", "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=400"),
        ("görev", "задание, задача", "Görevimi tamamladım.", "Я выполнил задание.", "https://images.unsplash.com/photo-1484480974693-6ca0a78fb36b?w=400"),
        ("rapor", "отчёт", "Rapor hazırladım.", "Я подготовил отчёт.", "https://images.unsplash.com/photo-1568346974664-027a2610070c?w=400"),
        ("belge", "документ", "Belgeyi imzaladım.", "Я подписал документ.", "https://images.unsplash.com/photo-1568346974664-027a2610070c?w=400"),
        ("imza", "подпись", "İmzamı attım.", "Я поставил подпись.", "https://images.unsplash.com/photo-1450101499163-c8848c66ca85?w=400"),
        ("sözleşme", "контракт, договор", "Sözleşmeyi imzaladım.", "Я подписал контракт.", "https://images.unsplash.com/photo-1450101499163-c8848c66ca85?w=400"),
        ("müşteri", "клиент", "Müşteriyle görüştüm.", "Я встретился с клиентом.", "https://images.unsplash.com/photo-1556745753-b2904692b3cd?w=400"),
        ("satış", "продажа", "Satış yaptım.", "Я совершил продажу.", "https://images.unsplash.com/photo-1556742111-a301076d9d18?w=400"),
        ("pazarlama", "маркетинг", "Pazarlama ekibindeyim.", "Я в отделе маркетинга.", "https://images.unsplash.com/photo-1557804506-669a67965ba0?w=400"),
        ("reklam", "реклама", "Reklam hazırladık.", "Мы подготовили рекламу.", "https://images.unsplash.com/photo-1542744095-291d1f67b221?w=400"),
        ("sunum", "презентация", "Sunum yapıyorum.", "Я делаю презентацию.", "https://images.unsplash.com/photo-1557804506-669a67965ba0?w=400"),
        ("ekip", "команда", "Ekiple çalışıyorum.", "Я работаю в команде.", "https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=400"),
        ("terfi", "повышение", "Terfi ettim.", "Я получил повышение.", "https://images.unsplash.com/photo-1507679799987-c73779587ccf?w=400"),
        ("işten çıkarma", "увольнение", "İşten çıkarıldım.", "Меня уволили.", "https://images.unsplash.com/photo-1554224311-bfd8029a318f?w=400"),
        ("işe almak", "нанимать", "Yeni çalışan işe aldık.", "Мы наняли нового сотрудника.", "https://images.unsplash.com/photo-1573496799652-408c2ac9fe98?w=400"),
        ("mülakat", "собеседование", "Mülakattayım.", "Я на собеседовании.", "https://images.unsplash.com/photo-1573497161161-c3e73707e25c?w=400"),
        ("özgeçmiş", "резюме", "Özgeçmişimi gönderdim.", "Я отправил своё резюме.", "https://images.unsplash.com/photo-1586281380349-632531db7ed4?w=400"),
        ("referans", "рекомендация", "Referans istedim.", "Я попросил рекомендацию.", "https://images.unsplash.com/photo-1450101499163-c8848c66ca85?w=400"),
        ("deneyim", "опыт", "Deneyimim var.", "У меня есть опыт.", "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=400"),
        ("yetenek", "навык, способность", "Yeteneklerim var.", "У меня есть навыки.", "https://images.unsplash.com/photo-1516534775068-ba3e7458af70?w=400"),
        ("kariyer", "карьера", "Kariyerim önemli.", "Моя карьера важна.", "https://images.unsplash.com/photo-1487528278747-ba99ed528ebc?w=400"),
        ("mesai", "рабочее время", "Mesai bitti.", "Рабочее время закончилось.", "https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=400"),
        ("fazla mesai", "сверхурочная работа", "Fazla mesai yapıyorum.", "Я работаю сверхурочно.", "https://images.unsplash.com/photo-1486312338219-ce68d2c6f44d?w=400"),
        ("izin", "отпуск", "İzne çıkıyorum.", "Я иду в отпуск.", "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400"),
        ("hastalık izni", "больничный", "Hastalık izni aldım.", "Я взял больничный.", "https://images.unsplash.com/photo-1584515933487-779824d29309?w=400"),
        ("dosya dolabı", "картотека", "Dosya dolabına baktım.", "Я посмотрел в картотеку.", "https://images.unsplash.com/photo-1554224311-beee415c201f?w=400"),
        ("zımba", "степлер", "Zımba ile tutturdum.", "Я скрепил степлером.", "https://images.unsplash.com/photo-1611378437190-f88c29e8e4c4?w=400"),
        ("ataş", "скрепка", "Ataşla birleştirdim.", "Я соединил скрепкой.", "https://images.unsplash.com/photo-1598971639160-e60dbfe5f7ad?w=400"),
        ("evrak", "документы, бумаги", "Evrakları düzenledim.", "Я систематизировал документы.", "https://images.unsplash.com/photo-1568346974664-027a2610070c?w=400"),
        ("arşiv", "архив", "Arşive kaldırdım.", "Я убрал в архив.", "https://images.unsplash.com/photo-1544717305-2782549b5136?w=400"),
        ("departman", "отдел", "Hangi departmantasın?", "В каком отделе ты работаешь?", "https://images.unsplash.com/photo-1497366216548-37526070297c?w=400"),
    ]
    
    # Daily Conversation (60) - Most common phrases
    conversation_data = [
        ("merhaba", "привет, здравствуй", "Merhaba, nasılsın?", "Привет, как дела?", "https://images.unsplash.com/photo-1542273917363-3b1817f69a2d?w=400"),
        ("selam", "привет (неформально)", "Selam!", "Привет!", "https://images.unsplash.com/photo-1491438590914-bc09fcaaf77a?w=400"),
        ("günaydın", "доброе утро", "Günaydın!", "Доброе утро!", "https://images.unsplash.com/photo-1495214783159-3503fd1b572d?w=400"),
        ("iyi akşamlar", "добрый вечер", "İyi akşamlar!", "Добрый вечер!", "https://images.unsplash.com/photo-1470252649378-9c29740c9fa8?w=400"),
        ("iyi geceler", "спокойной ночи", "İyi geceler!", "Спокойной ночи!", "https://images.unsplash.com/photo-1513002749550-c59d786b8e6c?w=400"),
        ("hoşçakal", "до свидания", "Hoşçakal!", "До свидания!", "https://images.unsplash.com/photo-1491438590914-bc09fcaaf77a?w=400"),
        ("görüşürüz", "увидимся", "Görüşürüz!", "Увидимся!", "https://images.unsplash.com/photo-1491438590914-bc09fcaaf77a?w=400"),
        ("nasılsın", "как дела", "Nasılsın?", "Как дела?", "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400"),
        ("iyiyim", "я в порядке", "İyiyim, teşekkürler.", "Я в порядке, спасибо.", "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400"),
        ("teşekkür ederim", "спасибо", "Teşekkür ederim!", "Спасибо!", "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400"),
        ("teşekkürler", "спасибо (короткое)", "Teşekkürler!", "Спасибо!", "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400"),
        ("rica ederim", "пожалуйста (ответ на спасибо)", "Rica ederim.", "Пожалуйста.", "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400"),
        ("lütfen", "пожалуйста (просьба)", "Lütfen yardım et.", "Пожалуйста, помоги.", "https://images.unsplash.com/photo-1559027615-cd4628902d4a?w=400"),
        ("özür dilerim", "извините", "Özür dilerim.", "Извините.", "https://images.unsplash.com/photo-1582581088994-27fcff98e044?w=400"),
        ("pardon", "простите, извините", "Pardon!", "Простите!", "https://images.unsplash.com/photo-1485178575877-1a13bf489dfe?w=400"),
        ("evet", "да", "Evet, doğru.", "Да, правильно.", "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=400"),
        ("hayır", "нет", "Hayır, yanlış.", "Нет, неправильно.", "https://images.unsplash.com/photo-1567168544813-cc03465b4fa8?w=400"),
        ("tamam", "хорошо, ладно", "Tamam, anladım.", "Хорошо, я понял.", "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=400"),
        ("peki", "ладно, хорошо", "Peki, olur.", "Ладно, ладно.", "https://images.unsplash.com/photo-1516534775068-ba3e7458af70?w=400"),
        ("maalesef", "к сожалению", "Maalesef gelemem.", "К сожалению, я не смогу прийти.", "https://images.unsplash.com/photo-1499209974431-9dddcece7f88?w=400"),
        ("ne yazık ki", "к сожалению", "Ne yazık ki zamanım yok.", "К сожалению, у меня нет времени.", "https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=400"),
        ("tabi", "конечно", "Tabi ki!", "Конечно!", "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=400"),
        ("elbette", "конечно, разумеется", "Elbette yardım ederim.", "Конечно, я помогу.", "https://images.unsplash.com/photo-1559027615-cd4628902d4a?w=400"),
        ("belki", "может быть", "Belki gelirim.", "Может быть, я приду.", "https://images.unsplash.com/photo-1516534775068-ba3e7458af70?w=400"),
        ("neden", "почему", "Neden gelmedin?", "Почему ты не пришёл?", "https://images.unsplash.com/photo-1516534775068-ba3e7458af70?w=400"),
        ("çünkü", "потому что", "Çünkü zamanım yoktu.", "Потому что у меня не было времени.", "https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=400"),
        ("ne", "что", "Ne yapıyorsun?", "Что ты делаешь?", "https://images.unsplash.com/photo-1516534775068-ba3e7458af70?w=400"),
        ("kim", "кто", "Bu kim?", "Кто это?", "https://images.unsplash.com/photo-1500917293891-ef795e70e1f6?w=400"),
        ("nerede", "где", "Neredesin?", "Где ты?", "https://images.unsplash.com/photo-1524661135-423995f22d0b?w=400"),
        ("ne zaman", "когда", "Ne zaman geliyorsun?", "Когда ты приезжаешь?", "https://images.unsplash.com/photo-1506784365847-bbad939e9335?w=400"),
        ("nasıl", "как", "Nasıl gidiyorsun?", "Как ты едешь?", "https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?w=400"),
        ("kaç", "сколько (счёт)", "Saat kaç?", "Сколько времени?", "https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=400"),
        ("ne kadar", "сколько (цена)", "Ne kadar?", "Сколько (стоит)?", "https://images.unsplash.com/photo-1579621970563-ebec7560ff3e?w=400"),
        ("hangi", "какой, который", "Hangi renk?", "Какой цвет?", "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400"),
        ("anlamıyorum", "я не понимаю", "Anlamıyorum.", "Я не понимаю.", "https://images.unsplash.com/photo-1516534775068-ba3e7458af70?w=400"),
        ("anlıyor musun", "ты понимаешь", "Anlıyor musun?", "Ты понимаешь?", "https://images.unsplash.com/photo-1516534775068-ba3e7458af70?w=400"),
        ("bilmiyorum", "я не знаю", "Bilmiyorum.", "Я не знаю.", "https://images.unsplash.com/photo-1581291518857-4e27b48ff24e?w=400"),
        ("biliyor musun", "ты знаешь", "Biliyor musun?", "Ты знаешь?", "https://images.unsplash.com/photo-1516534775068-ba3e7458af70?w=400"),
        ("yardım", "помощь", "Yardıma ihtiyacım var.", "Мне нужна помощь.", "https://images.unsplash.com/photo-1559027615-cd4628902d4a?w=400"),
        ("yardım eder misin", "поможешь ли ты", "Yardım eder misin?", "Ты поможешь?", "https://images.unsplash.com/photo-1559027615-cd4628902d4a?w=400"),
        ("afiyet olsun", "приятного аппетита", "Afiyet olsun!", "Приятного аппетита!", "https://images.unsplash.com/photo-1533089860892-a7c6f0a88666?w=400"),
        ("geçmiş olsun", "выздоравливай", "Geçmiş olsun!", "Выздоравливай!", "https://images.unsplash.com/photo-1584515933487-779824d29309?w=400"),
        ("kolay gelsin", "лёгкой работы", "Kolay gelsin!", "Лёгкой работы!", "https://images.unsplash.com/photo-1486312338219-ce68d2c6f44d?w=400"),
        ("hayırlı olsun", "поздравляю (с покупкой)", "Hayırlı olsun!", "Поздравляю!", "https://images.unsplash.com/photo-1513885535751-8b9238bd345a?w=400"),
        ("tebrikler", "поздравления", "Tebrikler!", "Поздравляю!", "https://images.unsplash.com/photo-1464349095431-e9a21285b5f3?w=400"),
        ("kutlu olsun", "поздравляю", "Doğum günün kutlu olsun!", "С днём рождения!", "https://images.unsplash.com/photo-1464349095431-e9a21285b5f3?w=400"),
        ("iyi şanslar", "удачи", "İyi şanslar!", "Удачи!", "https://images.unsplash.com/photo-1527689368864-3a821dbccc34?w=400"),
        ("başarılar", "успехов", "Başarılar dilerim!", "Желаю успехов!", "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=400"),
        ("hoş geldiniz", "добро пожаловать", "Hoş geldiniz!", "Добро пожаловать!", "https://images.unsplash.com/photo-1570129477492-45c003edd2be?w=400"),
        ("hoş bulduk", "спасибо (ответ)", "Hoş bulduk!", "Спасибо! (ответ на хош гельдиниз)", "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400"),
        ("aynı şekilde", "взаимно", "Aynı şekilde.", "Взаимно.", "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400"),
        ("sağ ol", "спасибо (неформально)", "Sağ ol!", "Спасибо!", "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400"),
        ("iyi günler", "хорошего дня", "İyi günler!", "Хорошего дня!", "https://images.unsplash.com/photo-1506784983877-45594efa4cbe?w=400"),
        ("iyi akşamlar", "хорошего вечера", "İyi akşamlar!", "Хорошего вечера!", "https://images.unsplash.com/photo-1470252649378-9c29740c9fa8?w=400"),
        ("iyi yolculuklar", "счастливого пути", "İyi yolculuklar!", "Счастливого пути!", "https://images.unsplash.com/photo-1436491865332-7a61a109cc05?w=400"),
        ("iyi tatiller", "хорошего отдыха", "İyi tatiller!", "Хорошего отдыха!", "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=400"),
        ("güle güle", "до свидания (говорит уходящий)", "Güle güle!", "До свидания!", "https://images.unsplash.com/photo-1491438590914-bc09fcaaf77a?w=400"),
        ("işte", "вот, вон", "İşte burada!", "Вот здесь!", "https://images.unsplash.com/photo-1516534775068-ba3e7458af70?w=400"),
        ("şey", "вещь, штука", "Bu ne şey?", "Что это за штука?", "https://images.unsplash.com/photo-1516534775068-ba3e7458af70?w=400"),
        ("yani", "то есть", "Yani, öyle mi?", "То есть, так?", "https://images.unsplash.com/photo-1516534775068-ba3e7458af70?w=400"),
    ]
    
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
        ("technology", tech_data),
        ("work_office", work_data),
        ("daily_conversation", conversation_data)
    ]
    
    for cat_info in remaining_cats[:3]:  # First 3 categories
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
    
    total_cats = await db.categories.count_documents({})
    total_words = await db.words.count_documents({})
    
    print(f"\n📊 Part 5 Özet:")
    print(f"  - Yeni Kategori: {len(categories_to_insert)}")
    print(f"  - Yeni Kelime: {len(words_to_insert)}")
    print(f"\n🎯 GENEL TOPLAM:")
    print(f"  - Toplam Kategori: {total_cats}")
    print(f"  - Toplam Kelime: {total_words}")
    print(f"  - Hedefin %{int((total_words/1000)*100)}\'ine ulaşıldı!")
    
    if total_words >= 1000:
        print("\n🎉🎉🎉 1000 KELIME HEDEFİNE ULAŞILDI! 🎉🎉🎉")
    else:
        print(f"\n📌 Hedefe ulaşmak için {1000-total_words} kelime daha gerekiyor.")
    
    print("\n✅ Part 5 tamamlandı!")

if __name__ == "__main__":
    asyncio.run(seed_remaining())
    client.close()
