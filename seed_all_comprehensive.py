"""
Comprehensive seed script combining all data sources.
This script will seed ~1000 words across all categories.
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

SUPER_ADMIN_USER_ID = f"user_{uuid.uuid4().hex[:12]}"

async def seed_all():
    print("🌱 Tüm içerik seed ediliyor...")
    
    # Check if already seeded
    existing = await db.categories.count_documents({})
    if existing > 0:
        print(f"⚠️  Zaten {existing} kategori mevcut.")
        response = input("Tümünü silip yeniden mi oluşturmalıyım? (e/h): ")
        if response.lower() != 'e':
            print("❌ İşlem iptal edildi")
            return
        
        # Clean database
        await db.categories.delete_many({})
        await db.words.delete_many({})
        print("🗑️  Mevcut veriler temizlendi")
    
    categories_to_insert = []
    words_to_insert = []
    
    # ==================== BASIC VOCABULARY ====================
    basic_cats = [
        {
            "category_id": "numbers",
            "name_tr": "Sayılar",
            "name_ru": "Числа",
            "icon": "🔢",
            "level": "A1",
            "color": "#3B82F6"
        },
        {
            "category_id": "colors",
            "name_tr": "Renkler",
            "name_ru": "Цвета",
            "icon": "🎨",
            "level": "A1",
            "color": "#EF4444"
        },
        {
            "category_id": "family",
            "name_tr": "Aile",
            "name_ru": "Семья",
            "icon": "👨‍👩‍👧‍👦",
            "level": "A1",
            "color": "#F59E0B"
        },
        {
            "category_id": "animals",
            "name_tr": "Hayvanlar",
            "name_ru": "Животные",
            "icon": "🐕",
            "level": "A1",
            "color": "#10B981"
        },
        {
            "category_id": "food",
            "name_tr": "Yiyecekler",
            "name_ru": "Еда",
            "icon": "🍕",
            "level": "A1",
            "color": "#8B5CF6"
        },
        {
            "category_id": "body_parts",
            "name_tr": "Vücut Kısımları",
            "name_ru": "Части тела",
            "icon": "🤚",
            "level": "A1",
            "color": "#EC4899"
        },
        {
            "category_id": "clothes",
            "name_tr": "Kıyafetler",
            "name_ru": "Одежда",
            "icon": "👔",
            "level": "A2",
            "color": "#F97316"
        },
        {
            "category_id": "home",
            "name_tr": "Ev Eşyaları",
            "name_ru": "Предметы быта",
            "icon": "🏠",
            "level": "A2",
            "color": "#06B6D4"
        },
        {
            "category_id": "professions",
            "name_tr": "Meslekler",
            "name_ru": "Профессии",
            "icon": "👨‍⚕️",
            "level": "A2",
            "color": "#84CC16"
        },
        {
            "category_id": "transport",
            "name_tr": "Ulaşım",
            "name_ru": "Транспорт",
            "icon": "🚗",
            "level": "A2",
            "color": "#6366F1"
        }
    ]
    
    # Numbers (1-20, 30, 40, 50, 100, 1000)
    numbers_data = [
        ("bir", "один", "Bir elma aldım.", "Я купил одно яблоко.", "https://images.unsplash.com/photo-1611080626919-7cf5a9dbab5b?w=400"),
        ("iki", "два", "İki kitap okudum.", "Я прочитал две книги.", "https://images.unsplash.com/photo-1505664194779-8beaceb93744?w=400"),
        ("üç", "три", "Üç kardeşiz.", "Нас трое братьев/сестёр.", "https://images.unsplash.com/photo-1532274402911-5a369e4c4bb5?w=400"),
        ("dört", "четыре", "Dört mevsim var.", "Есть четыре времени года.", "https://images.unsplash.com/photo-1509023464722-18d996393ca8?w=400"),
        ("beş", "пять", "Beş parmak.", "Пять пальцев.", "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=400"),
        ("altı", "шесть", "Altı saat uyudum.", "Я спал шесть часов.", "https://images.unsplash.com/photo-1495364141860-b0d03eccd065?w=400"),
        ("yedi", "семь", "Yedi gün bir hafta.", "Семь дней - неделя.", "https://images.unsplash.com/photo-1506784983877-45594efa4cbe?w=400"),
        ("sekiz", "восемь", "Sekiz saat çalışıyorum.", "Я работаю восемь часов.", "https://images.unsplash.com/photo-1553729459-efe14ef6055d?w=400"),
        ("dokuz", "девять", "Saat dokuz.", "Девять часов.", "https://images.unsplash.com/photo-1501139083538-0139583c060f?w=400"),
        ("on", "десять", "On parmak.", "Десять пальцев.", "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=400"),
        ("yirmi", "двадцать", "Yirmi yaşındayım.", "Мне двадцать лет.", "https://images.unsplash.com/photo-1516534775068-ba3e7458af70?w=400"),
        ("otuz", "тридцать", "Otuz gün.", "Тридцать дней.", "https://images.unsplash.com/photo-1517842645767-c639042777db?w=400"),
        ("kırk", "сорок", "Kırk derece sıcak.", "Сорок градусов жары.", "https://images.unsplash.com/photo-1473496169904-658ba7c44d8a?w=400"),
        ("elli", "пятьдесят", "Elli lira.", "Пятьдесят лир.", "https://images.unsplash.com/photo-1579621970563-ebec7560ff3e?w=400"),
        ("yüz", "сто", "Yüz tane.", "Сто штук.", "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=400"),
        ("bin", "тысяча", "Bin sayfa.", "Тысяча страниц.", "https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?w=400"),
    ]
    
    # Colors (15 colors)
    colors_data = [
        ("kırmızı", "красный", "Kırmızı elma.", "Красное яблоко.", "https://images.unsplash.com/photo-1568702846914-96b305d2aaeb?w=400"),
        ("mavi", "синий", "Mavi gökyüzü.", "Синее небо.", "https://images.unsplash.com/photo-1561731216-c3a4d99437d5?w=400"),
        ("yeşil", "зелёный", "Yeşil yapraklar.", "Зелёные листья.", "https://images.unsplash.com/photo-1557672172-298e090bd0f1?w=400"),
        ("sarı", "жёлтый", "Sarı güneş.", "Жёлтое солнце.", "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400"),
        ("siyah", "чёрный", "Siyah kedi.", "Чёрная кошка.", "https://images.unsplash.com/photo-1529778873920-4da4926a72c2?w=400"),
        ("beyaz", "белый", "Beyaz kar.", "Белый снег.", "https://images.unsplash.com/photo-1551888087-904e4e079766?w=400"),
        ("turuncu", "оранжевый", "Turuncu portakal.", "Оранжевый апельсин.", "https://images.unsplash.com/photo-1547514701-42782101795e?w=400"),
        ("mor", "фиолетовый", "Mor çiçek.", "Фиолетовый цветок.", "https://images.unsplash.com/photo-1557672172-298e090bd0f1?w=400"),
        ("pembe", "розовый", "Pembe gül.", "Розовая роза.", "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=400"),
        ("kahverengi", "коричневый", "Kahverengi masa.", "Коричневый стол.", "https://images.unsplash.com/photo-1604147706283-d7119b5b822c?w=400"),
        ("gri", "серый", "Gri bulut.", "Серая туча.", "https://images.unsplash.com/photo-1611080626919-7cf5a9dbab5b?w=400"),
        ("lacivert", "тёмно-синий", "Lacivert pantolon.", "Тёмно-синие брюки.", "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=400"),
        ("turkuaz", "бирюзовый", "Turkuaz deniz.", "Бирюзовое море.", "https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=400"),
        ("altın rengi", "золотой", "Altın rengi güneş.", "Золотое солнце.", "https://images.unsplash.com/photo-1618609378039-b572f64c5b42?w=400"),
        ("gümüş rengi", "серебряный", "Gümüş rengi yüzük.", "Серебряное кольцо.", "https://images.unsplash.com/photo-1611591437281-460bfbe1220a?w=400"),
    ]
    
    # Family (15 words)
    family_data = [
        ("anne", "мать, мама", "Annem evde.", "Моя мама дома.", "https://images.unsplash.com/photo-1596003906949-67221c37965c?w=400"),
        ("baba", "отец, папа", "Babam çalışıyor.", "Мой папа работает.", "https://images.unsplash.com/photo-1541534741688-6078c6bfb5c5?w=400"),
        ("oğul", "сын", "Oğlum okula gidiyor.", "Мой сын ходит в школу.", "https://images.unsplash.com/photo-1519925610903-381054cc2a1a?w=400"),
        ("kız", "дочь", "Kızım dans ediyor.", "Моя дочь танцует.", "https://images.unsplash.com/photo-1503454537195-1dcabb73ffb9?w=400"),
        ("kardeş", "брат, сестра", "İki kardeşim var.", "У меня два брата/сестры.", "https://images.unsplash.com/photo-1560155989-1f7d7b0e6f5a?w=400"),
        ("abi", "старший брат", "Abim benimle oynuyor.", "Мой старший брат играет со мной.", "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=400"),
        ("abla", "старшая сестра", "Ablam öğretmen.", "Моя старшая сестра - учитель.", "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=400"),
        ("büyükanne", "бабушка", "Büyükanne yemek yapıyor.", "Бабушка готовит.", "https://images.unsplash.com/photo-1587360931039-4077bda63e49?w=400"),
        ("büyükbaba", "дедушка", "Büyükbaba bahçede.", "Дедушка в саду.", "https://images.unsplash.com/photo-1595970968158-b9e0a8c3c6f0?w=400"),
        ("teyze", "тётя (со стороны матери)", "Teyze İstanbul'da yaşıyor.", "Тётя живёт в Стамбуле.", "https://images.unsplash.com/photo-1499996860823-5214fcc65f8f?w=400"),
        ("amca", "дядя (со стороны отца)", "Amcam doktor.", "Мой дядя - врач.", "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=400"),
        ("kuzen", "двоюродный брат/сестра", "Kuzenimle sinemaya gittik.", "Мы с двоюродным братом пошли в кино.", "https://images.unsplash.com/photo-1523901839036-a3030662f220?w=400"),
        ("eş", "супруг/супруга", "Eşim evde.", "Мой супруг/супруга дома.", "https://images.unsplash.com/photo-1522673607106-f6b4b97e46d3?w=400"),
        ("yeğen", "племянник/племянница", "Yeğenim çok sevimli.", "Мой племянник очень милый.", "https://images.unsplash.com/photo-1503454537195-1dcabb73ffb9?w=400"),
        ("torun", "внук/внучка", "Torunum üç yaşında.", "Моему внуку три года.", "https://images.unsplash.com/photo-1491013516836-7db643ee125a?w=400"),
    ]
    
    # Animals (20 words)
    animals_data = [
        ("kedi", "кошка", "Kedi uyuyor.", "Кошка спит.", "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=400"),
        ("köpek", "собака", "Köpek koşuyor.", "Собака бежит.", "https://images.unsplash.com/photo-1543466835-00a7907e9de1?w=400"),
        ("kuş", "птица", "Kuş uçuyor.", "Птица летит.", "https://images.unsplash.com/photo-1552728089-57bdde30beb3?w=400"),
        ("at", "лошадь", "At hızlı koşuyor.", "Лошадь быстро бежит.", "https://images.unsplash.com/photo-1553284965-83fd3e82fa5a?w=400"),
        ("inek", "корова", "İnek süt veriyor.", "Корова даёт молоко.", "https://images.unsplash.com/photo-1516467508483-a7212febe31a?w=400"),
        ("koyun", "овца", "Koyunlar otluyor.", "Овцы пасутся.", "https://images.unsplash.com/photo-1580690638968-371e0dce1d40?w=400"),
        ("tavuk", "курица", "Tavuk yumurtluyor.", "Курица несёт яйца.", "https://images.unsplash.com/photo-1548550023-2bdb3c5beed7?w=400"),
        ("balık", "рыба", "Balık yüzüyor.", "Рыба плавает.", "https://images.unsplash.com/photo-1535591273668-578e31182c4f?w=400"),
        ("fil", "слон", "Fil çok büyük.", "Слон очень большой.", "https://images.unsplash.com/photo-1564760055775-d63b17a55c44?w=400"),
        ("aslan", "лев", "Aslan ormanın kralı.", "Лев - король джунглей.", "https://images.unsplash.com/photo-1552410260-0fd9b577afa6?w=400"),
        ("kaplan", "тигр", "Kaplan tehlikeli.", "Тигр опасен.", "https://images.unsplash.com/photo-1551709108-f7b6fdefc49e?w=400"),
        ("ayı", "медведь", "Ayı balık yiyor.", "Медведь ест рыбу.", "https://images.unsplash.com/photo-1589656966895-2f33e7653819?w=400"),
        ("tavşan", "кролик", "Tavşan havuç yiyor.", "Кролик ест морковь.", "https://images.unsplash.com/photo-1535241749838-299277b6305f?w=400"),
        ("fare", "мышь", "Fare küçük.", "Мышь маленькая.", "https://images.unsplash.com/photo-1425082661705-1834bfd09dca?w=400"),
        ("yılan", "змея", "Yılan sürünüyor.", "Змея ползёт.", "https://images.unsplash.com/photo-1531386151447-fd76ad50012f?w=400"),
        ("maymun", "обезьяна", "Maymun ağaca tırmanıyor.", "Обезьяна лезет на дерево.", "https://images.unsplash.com/photo-1540573133985-87b6da6d54a9?w=400"),
        ("züraf", "жираф", "Zürafanın boynu uzun.", "У жирафа длинная шея.", "https://images.unsplash.com/photo-1547721064-da6cfb341d50?w=400"),
        ("kelebek", "бабочка", "Kelebek renkli.", "Бабочка разноцветная.", "https://images.unsplash.com/photo-1526336024174-e58f5cdd8e13?w=400"),
        ("arı", "пчела", "Arı bal yapıyor.", "Пчела делает мёд.", "https://images.unsplash.com/photo-1568526381923-caf3fd520382?w=400"),
        ("kurbağa", "лягушка", "Kurbağa zıplıyor.", "Лягушка прыгает.", "https://images.unsplash.com/photo-1595377834722-c0e8b0e5bdb5?w=400"),
    ]
    
    # Food (25 words)
    food_data = [
        ("ekmek", "хлеб", "Taze ekmek aldım.", "Я купил свежий хлеб.", "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=400"),
        ("su", "вода", "Su içiyorum.", "Я пью воду.", "https://images.unsplash.com/photo-1548839140-29a749e1cf4d?w=400"),
        ("süt", "молоко", "Süt sağlıklı.", "Молоко полезно.", "https://images.unsplash.com/photo-1550583724-b2692b85b150?w=400"),
        ("peynir", "сыр", "Peynir yiyorum.", "Я ем сыр.", "https://images.unsplash.com/photo-1486297678162-eb2a19b0a32d?w=400"),
        ("yumurta", "яйцо", "Yumurta pişiriyorum.", "Я готовлю яйца.", "https://images.unsplash.com/photo-1587486936087-e9b90205c1e0?w=400"),
        ("et", "мясо", "Et yemek seviyorum.", "Я люблю есть мясо.", "https://images.unsplash.com/photo-1588168333986-5078d3ae3976?w=400"),
        ("tavuk", "курица (мясо)", "Tavuk soteси yaptım.", "Я приготовил жареную курицу.", "https://images.unsplash.com/photo-1598103442097-8b74394b95c6?w=400"),
        ("balık", "рыба (еда)", "Balık ızgara.", "Рыба на гриле.", "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?w=400"),
        ("pilav", "плов, рис", "Pilav yaptım.", "Я приготовил плов.", "https://images.unsplash.com/photo-1516684732162-798a0062be99?w=400"),
        ("makarna", "макароны", "Makarna haşlandı.", "Макароны сварены.", "https://images.unsplash.com/photo-1621996346565-e3dbc646d9a9?w=400"),
        ("çorba", "суп", "Çorba sıcak.", "Суп горячий.", "https://images.unsplash.com/photo-1547592166-23ac45744acd?w=400"),
        ("salata", "салат", "Salata hazırladım.", "Я приготовил салат.", "https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?w=400"),
        ("elma", "яблоко", "Elma yedim.", "Я съел яблоко.", "https://images.unsplash.com/photo-1568702846914-96b305d2aaeb?w=400"),
        ("portakal", "апельсин", "Portakal suyu içtim.", "Я выпил апельсиновый сок.", "https://images.unsplash.com/photo-1547514701-42782101795e?w=400"),
        ("muz", "банан", "Muz seviyorum.", "Я люблю бананы.", "https://images.unsplash.com/photo-1603833665858-e61d17a86224?w=400"),
        ("üzüm", "виноград", "Üzüm tatlı.", "Виноград сладкий.", "https://images.unsplash.com/photo-1599819177959-2c945a1c2609?w=400"),
        ("çilek", "клубника", "Çilek kırmızı.", "Клубника красная.", "https://images.unsplash.com/photo-1518635017498-87f514b751ba?w=400"),
        ("domates", "помидор", "Domates salatası.", "Салат из помидоров.", "https://images.unsplash.com/photo-1546094096-0df4bcaaa337?w=400"),
        ("salatalık", "огурец", "Salatalık yeşil.", "Огурец зелёный.", "https://images.unsplash.com/photo-1568584711075-3d021a7c3ca3?w=400"),
        ("patates", "картофель", "Patates kızartması.", "Жареная картошка.", "https://images.unsplash.com/photo-1518977676601-b53f82aba655?w=400"),
        ("soğan", "лук", "Soğan doğruyorum.", "Я режу лук.", "https://images.unsplash.com/photo-1518013431117-eb1465fa5752?w=400"),
        ("çay", "чай", "Çay içiyoruz.", "Мы пьём чай.", "https://images.unsplash.com/photo-1564890369478-c89ca6d9cde9?w=400"),
        ("kahve", "кофе", "Kahve içtim.", "Я выпил кофе.", "https://images.unsplash.com/photo-1511920170033-f8396924c348?w=400"),
        ("tatlı", "сладкое, десерт", "Tatlı yedik.", "Мы съели десерт.", "https://images.unsplash.com/photo-1488477181946-6428a0291777?w=400"),
        ("dondurma", "мороженое", "Dondurma soğuk.", "Мороженое холодное.", "https://images.unsplash.com/photo-1563805042-7684c019e1cb?w=400"),
    ]
    
    # Body parts (15 words)
    body_data = [
        ("baş", "голова", "Başım ağrıyor.", "У меня болит голова.", "https://images.unsplash.com/photo-1530019047333-748c02d22e40?w=400"),
        ("göz", "глаз", "Gözlerim yeşil.", "Мои глаза зелёные.", "https://images.unsplash.com/photo-1583445095369-9c651e7e5d34?w=400"),
        ("kulak", "ухо", "Kulaklarım büyük.", "Мои уши большие.", "https://images.unsplash.com/photo-1516733725897-1aa73b87c8e8?w=400"),
        ("burun", "нос", "Burnum kaşınıyor.", "Мой нос чешется.", "https://images.unsplash.com/photo-1583224964111-caa7a2c6f907?w=400"),
        ("ağız", "рот", "Ağzımı açtım.", "Я открыл рот.", "https://images.unsplash.com/photo-1606811841689-23dfddce3e95?w=400"),
        ("diş", "зуб", "Dişlerim beyaz.", "Мои зубы белые.", "https://images.unsplash.com/photo-1598256989800-fe5f95da9787?w=400"),
        ("boyun", "шея", "Boynumu çevirdim.", "Я повернул шею.", "https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=400"),
        ("omuz", "плечо", "Omzum ağrıyor.", "Моё плечо болит.", "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=400"),
        ("kol", "рука (от плеча до кисти)", "Kolum güçlü.", "Моя рука сильная.", "https://images.unsplash.com/photo-1532938911079-1b06ac7ceec7?w=400"),
        ("el", "кисть руки, рука", "Elimi yıkadım.", "Я помыл руки.", "https://images.unsplash.com/photo-1584308972272-9e4e7685e80f?w=400"),
        ("parmak", "палец", "Parmaklarım uzun.", "Мои пальцы длинные.", "https://images.unsplash.com/photo-1590698933947-a202b069a861?w=400"),
        ("bacak", "нога", "Bacaklarım yorgun.", "Мои ноги устали.", "https://images.unsplash.com/photo-1605209449754-09168d0e3158?w=400"),
        ("ayak", "стопа", "Ayakkabılarım küçük.", "Мои туфли малы.", "https://images.unsplash.com/photo-1543163521-1bf539c55dd2?w=400"),
        ("kalp", "сердце", "Kalbim hızlı atıyor.", "Моё сердце быстро бьётся.", "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=400"),
        ("mide", "желудок", "Midem ağrıyor.", "У меня болит живот.", "https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=400"),
    ]
    
    # Clothes (15 words)
    clothes_data = [
        ("gömlek", "рубашка", "Beyaz gömlek giydim.", "Я надел белую рубашку.", "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=400"),
        ("pantolon", "брюки", "Siyah pantolon.", "Чёрные брюки.", "https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?w=400"),
        ("etek", "юбка", "Kırmızı etek giydim.", "Я надела красную юбку.", "https://images.unsplash.com/photo-1583496661160-fb5886a0aaaa?w=400"),
        ("elbise", "платье", "Mavi elbise çok güzel.", "Синее платье очень красивое.", "https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=400"),
        ("ceket", "куртка, пиджак", "Ceket giymelisin.", "Тебе следует надеть куртку.", "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400"),
        ("mont", "пальто", "Mont sıcak tutuyor.", "Пальто греет.", "https://images.unsplash.com/photo-1539533018447-63fcce2678e3?w=400"),
        ("ayakkabı", "обувь", "Ayakkabılarım yeni.", "Мои туфли новые.", "https://images.unsplash.com/photo-1605348532760-6753d2c43329?w=400"),
        ("çorap", "носки", "Çoraplarım renkli.", "Мои носки цветные.", "https://images.unsplash.com/photo-1580900991414-a75f787f1059?w=400"),
        ("şapka", "шапка", "Şapka takıyorum.", "Я ношу шапку.", "https://images.unsplash.com/photo-1521369909029-2afed882baee?w=400"),
        ("eldiven", "перчатки", "Eldivenlerim kayboldu.", "Мои перчатки потерялись.", "https://images.unsplash.com/photo-1583389733097-54a76e0962e5?w=400"),
        ("atkı", "шарф", "Atkı boynum sarılı.", "Шарф обёрнут вокруг моей шеи.", "https://images.unsplash.com/photo-1520903920243-00d872a2d1c9?w=400"),
        ("kemer", "ремень", "Deri kemer.", "Кожаный ремень.", "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400"),
        ("kravat", "галстук", "Kravat takmıyorum.", "Я не ношу галстук.", "https://images.unsplash.com/photo-1557804506-669a67965ba0?w=400"),
        ("mayo", "купальник", "Mayoyu giydim.", "Я надел купальник.", "https://images.unsplash.com/photo-1582610116397-edb318620f90?w=400"),
        ("pijama", "пижама", "Pijama giyiyorum.", "Я надеваю пижаму.", "https://images.unsplash.com/photo-1588117472013-59bb13edafec?w=400"),
    ]
    
    # Home items (20 words)
    home_data = [
        ("masa", "стол", "Masada kitap var.", "На столе лежит книга.", "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=400"),
        ("sandalye", "стул", "Sandalyeye oturdum.", "Я сел на стул.", "https://images.unsplash.com/photo-1503602642458-232111445657?w=400"),
        ("yatak", "кровать", "Yatakta uyuyorum.", "Я сплю в кровати.", "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?w=400"),
        ("lamba", "лампа", "Lamba yanıyor.", "Лампа горит.", "https://images.unsplash.com/photo-1513506003901-1e6a229e2d15?w=400"),
        ("dolap", "шкаф", "Dolap dolu.", "Шкаф полный.", "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400"),
        ("pencere", "окно", "Pencereyi açtım.", "Я открыл окно.", "https://images.unsplash.com/photo-1545259741-2ea3ebf61fa3?w=400"),
        ("kapı", "дверь", "Kapı kapalı.", "Дверь закрыта.", "https://images.unsplash.com/photo-1519710164239-da123dc03ef4?w=400"),
        ("ayna", "зеркало", "Aynaya baktım.", "Я посмотрел в зеркало.", "https://images.unsplash.com/photo-1583847268964-b28dc8f51f92?w=400"),
        ("halı", "ковёр", "Halı yumuşak.", "Ковёр мягкий.", "https://images.unsplash.com/photo-1541123437800-1bb1317badc2?w=400"),
        ("perde", "штора", "Perdeyi çektim.", "Я задёрнул штору.", "https://images.unsplash.com/photo-1547038577-077d82af266d?w=400"),
        ("buzdolabı", "холодильник", "Buzdolabında süt var.", "В холодильнике есть молоко.", "https://images.unsplash.com/photo-1571175443880-49e1d25b2bc5?w=400"),
        ("fırın", "духовка", "Fırında kek pişiyor.", "В духовке печётся торт.", "https://images.unsplash.com/photo-1574269909862-7e1d70bb8078?w=400"),
        ("ocak", "плита", "Ocakta yemek yapıyorum.", "Я готовлю на плите.", "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=400"),
        ("lavabo", "раковина", "Lavaboda bulaşık var.", "В раковине посуда.", "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?w=400"),
        ("duş", "душ", "Duş alıyorum.", "Я принимаю душ.", "https://images.unsplash.com/photo-1620626011761-996317b8d101?w=400"),
        ("tuvalet", "туалет", "Tuvalet temiz.", "Туалет чистый.", "https://images.unsplash.com/photo-1565183997392-2f1613c4c278?w=400"),
        ("kitaplık", "книжный шкаф", "Kitaplıkta çok kitap var.", "В книжном шкафу много книг.", "https://images.unsplash.com/photo-1507842217343-583bb7270b66?w=400"),
        ("saat", "часы", "Saat duvarda.", "Часы на стене.", "https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=400"),
        ("telefon", "телефон", "Telefonum şarjda.", "Мой телефон на зарядке.", "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400"),
        ("televizyon", "телевизор", "Televizyon açık.", "Телевизор включён.", "https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?w=400"),
    ]
    
    # Professions (15 words)
    professions_data = [
        ("öğretmen", "учитель", "Öğretmen ders veriyor.", "Учитель ведёт урок.", "https://images.unsplash.com/photo-1580582932707-520aed937b7b?w=400"),
        ("doktor", "врач", "Doktor hasta muayene ediyor.", "Врач осматривает пациента.", "https://images.unsplash.com/photo-1559839734-2b71ea197ec2?w=400"),
        ("hemşire", "медсестра", "Hemşire ilacı veriyor.", "Медсестра даёт лекарство.", "https://images.unsplash.com/photo-1559839914-17aae19238c6?w=400"),
        ("mühendis", "инженер", "Mühendis proje yapıyor.", "Инженер делает проект.", "https://images.unsplash.com/photo-1581092160562-40aa08e78837?w=400"),
        ("avukat", "адвокат", "Avukat davada.", "Адвокат в суде.", "https://images.unsplash.com/photo-1589829545856-d10d557cf95f?w=400"),
        ("polis", "полицейский", "Polis görevde.", "Полицейский на дежурстве.", "https://images.unsplash.com/photo-1568515387631-8b650bbcdb90?w=400"),
        ("itfaiyeci", "пожарный", "İtfaiyeci yangını söndürüyor.", "Пожарный тушит пожар.", "https://images.unsplash.com/photo-1618331835717-801e976710b2?w=400"),
        ("aşçı", "повар", "Aşçı yemek yapıyor.", "Повар готовит еду.", "https://images.unsplash.com/photo-1577219491135-ce391730fb2c?w=400"),
        ("garson", "официант", "Garson sipariş alıyor.", "Официант принимает заказ.", "https://images.unsplash.com/photo-1592861956120-e524fc739696?w=400"),
        ("pilot", "пилот", "Pilot uçağı uçuruyor.", "Пилот управляет самолётом.", "https://images.unsplash.com/photo-1583912267550-a7c3c5503b98?w=400"),
        ("şoför", "водитель", "Şoför arabayı sürüyor.", "Водитель ведёт машину.", "https://images.unsplash.com/photo-1568605117036-5fe5e7bab0b7?w=400"),
        ("berber", "парикмахер", "Berber saç kesiyor.", "Парикмахер стрижёт волосы.", "https://images.unsplash.com/photo-1599351431202-1e0f0137899a?w=400"),
        ("ressam", "художник", "Ressam resim yapıyor.", "Художник рисует картину.", "https://images.unsplash.com/photo-1513364776144-60967b0f800f?w=400"),
        ("müzisyen", "музыкант", "Müzisyen şarkı söylüyor.", "Музыкант поёт песню.", "https://images.unsplash.com/photo-1511379938547-c1f69419868d?w=400"),
        ("yazılımcı", "программист", "Yazılımcı kod yazıyor.", "Программист пишет код.", "https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=400"),
    ]
    
    # Transport (12 words)
    transport_data = [
        ("araba", "машина", "Araba hızlı gidiyor.", "Машина едет быстро.", "https://images.unsplash.com/photo-1549399542-7e3f8b79c341?w=400"),
        ("otobüs", "автобус", "Otobüse bindim.", "Я сел в автобус.", "https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?w=400"),
        ("tren", "поезд", "Tren istasyonda.", "Поезд на станции.", "https://images.unsplash.com/photo-1474487548417-781cb71495f3?w=400"),
        ("uçak", "самолёт", "Uçak havada.", "Самолёт в воздухе.", "https://images.unsplash.com/photo-1436491865332-7a61a109cc05?w=400"),
        ("gemi", "корабль", "Gemi denizde.", "Корабль в море.", "https://images.unsplash.com/photo-1511407045410-d006318b9a2a?w=400"),
        ("bisiklet", "велосипед", "Bisiklet sürüyorum.", "Я еду на велосипеде.", "https://images.unsplash.com/photo-1511994298241-608e28f14fde?w=400"),
        ("motosiklet", "мотоцикл", "Motosiklet hızlı.", "Мотоцикл быстрый.", "https://images.unsplash.com/photo-1558981403-c5f9899a28bc?w=400"),
        ("taksi", "такси", "Taksi çağırdım.", "Я вызвал такси.", "https://images.unsplash.com/photo-1561361513-2d000a50f0dc?w=400"),
        ("metro", "метро", "Metro rahat.", "Метро удобное.", "https://images.unsplash.com/photo-1574698603573-cdce881a98ed?w=400"),
        ("tramvay", "трамвай", "Tramvay geliyor.", "Трамвай идёт.", "https://images.unsplash.com/photo-1593941707882-a5bba14938c7?w=400"),
        ("helikopter", "вертолёт", "Helikopter uçuyor.", "Вертолёт летит.", "https://images.unsplash.com/photo-1561214115-f2f134cc4912?w=400"),
        ("tekne", "лодка", "Tekne gölde.", "Лодка на озере.", "https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=400"),
    ]
    
    # ==================== PROCESS AND INSERT DATA ====================
    
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
    
    # Create categories and words
    data_mapping = [
        ("numbers", numbers_data),
        ("colors", colors_data),
        ("family", family_data),
        ("animals", animals_data),
        ("food", food_data),
        ("body_parts", body_data),
        ("clothes", clothes_data),
        ("home", home_data),
        ("professions", professions_data),
        ("transport", transport_data)
    ]
    
    for cat_info in basic_cats:
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
    
    # ==================== INSERT TO DATABASE ====================
    
    if categories_to_insert:
        await db.categories.insert_many(categories_to_insert)
        print(f"✅ {len(categories_to_insert)} kategori eklendi")
    
    if words_to_insert:
        await db.words.insert_many(words_to_insert)
        print(f"✅ {len(words_to_insert)} kelime eklendi")
    
    print("\n📊 Özet:")
    print(f"  - Toplam Kategori: {len(categories_to_insert)}")
    print(f"  - Toplam Kelime: {len(words_to_insert)}")
    print(f"  - Süper Admin ID: {SUPER_ADMIN_USER_ID}")
    print("\n🎉 Kapsamlı seed tamamlandı!")

if __name__ == "__main__":
    asyncio.run(seed_all())
    client.close()
