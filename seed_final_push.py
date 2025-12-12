"""
Final Push: Hobbies, Travel, Adjectives - to exceed 1000 words
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

async def seed_final_push():
    print("🚀 Son hamle: 1000 kelimeyi aşmak için...")
    
    SUPER_ADMIN_USER_ID = await get_super_admin_id()
    
    existing = await db.categories.count_documents({"category_id": "hobbies"})
    if existing > 0:
        print("⚠️  Bu kategoriler zaten mevcut.")
        return
    
    categories_to_insert = []
    words_to_insert = []
    
    cats = [
        {"category_id": "hobbies", "name_tr": "Hobiler", "name_ru": "Хобби", "icon": "🎨", "level": "B1", "color": "#87CEEB"},
        {"category_id": "travel", "name_tr": "Seyahat", "name_ru": "Путешествие", "icon": "✈️", "level": "B1", "color": "#FFA07A"},
        {"category_id": "adjectives_common", "name_tr": "Sık Kullanılan Sıfatlar", "name_ru": "Часто используемые прилагательные", "icon": "📝", "level": "A2", "color": "#DDA0DD"}
    ]
    
    # Hobbies (30)
    hobbies_data = [
        ("resim yapmak", "рисовать", "Resim yapmayı severim.", "Я люблю рисовать.", "https://images.unsplash.com/photo-1513364776144-60967b0f800f?w=400"),
        ("müzik dinlemek", "слушать музыку", "Müzik dinlemeyi seviyorum.", "Я люблю слушать музыку.", "https://images.unsplash.com/photo-1511379938547-c1f69419868d?w=400"),
        ("kitap okumak", "читать книги", "Kitap okumayı severim.", "Я люблю читать книги.", "https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=400"),
        ("film izlemek", "смотреть фильмы", "Film izlemeyi seviyorum.", "Я люблю смотреть фильмы.", "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=400"),
        ("fotoğrafçılık", "фотография", "Fotoğrafçılıkla ilgileniyorum.", "Я увлекаюсь фотографией.", "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=400"),
        ("yemek yapmak", "готовить", "Yemek yapmayı severim.", "Я люблю готовить.", "https://images.unsplash.com/photo-1577219491135-ce391730fb2c?w=400"),
        ("seyahat etmek", "путешествовать", "Seyahat etmeyi seviyorum.", "Я люблю путешествовать.", "https://images.unsplash.com/photo-1488646953014-85cb44e25828?w=400"),
        ("dans etmek", "танцевать", "Dans etmeyi severim.", "Я люблю танцевать.", "https://images.unsplash.com/photo-1504609813442-a8924e83f76e?w=400"),
        ("şarkı söylemek", "петь", "Şarkı söylemeyi severim.", "Я люблю петь.", "https://images.unsplash.com/photo-1516280440614-37939bbacd81?w=400"),
        ("enstrüman çalmak", "играть на инструменте", "Gitar çalıyorum.", "Я играю на гитаре.", "https://images.unsplash.com/photo-1510915361894-db8b60106cb1?w=400"),
        ("bahçıvanlık", "садоводство", "Bahçıvanlıkla uğraşıyorum.", "Я занимаюсь садоводством.", "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=400"),
        ("el işi", "рукоделие", "El işi yapıyorum.", "Я занимаюсь рукоделием.", "https://images.unsplash.com/photo-1452860606245-08befc0ff44b?w=400"),
        ("örgü örmek", "вязать", "Örgü örüyorum.", "Я вяжу.", "https://images.unsplash.com/photo-1620799140188-3b2a02fd9a77?w=400"),
        ("dikiş dikmek", "шить", "Dikiş dikmeyi severim.", "Я люблю шить.", "https://images.unsplash.com/photo-1496478923394-8f173f817c9f?w=400"),
        ("satranç oynamak", "играть в шахматы", "Satranç oynuyorum.", "Я играю в шахматы.", "https://images.unsplash.com/photo-1529699211952-734e80c4d42b?w=400"),
        ("puzzle yapmak", "собирать пазлы", "Puzzle yapmayı severim.", "Я люблю собирать пазлы.", "https://images.unsplash.com/photo-1566694271453-390536dd1f0d?w=400"),
        ("koleksiyon yapmak", "коллекционировать", "Pul koleksiyonu yapıyorum.", "Я коллекционирую марки.", "https://images.unsplash.com/photo-1571974599782-87624638275a?w=400"),
        ("balık tutmak", "рыбачить", "Balık tutmayı severim.", "Я люблю рыбачить.", "https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=400"),
        ("oyun oynamak", "играть в игры", "Oyun oynamayı severim.", "Я люблю играть в игры.", "https://images.unsplash.com/photo-1511512578047-dfb367046420?w=400"),
        ("video oyunu", "видеоигра", "Video oyunu oynuyorum.", "Я играю в видеоигры.", "https://images.unsplash.com/photo-1551103782-8ab07afd45c1?w=400"),
        ("blog yazmak", "вести блог", "Blog yazıyorum.", "Я веду блог.", "https://images.unsplash.com/photo-1499750310107-5fef28a66643?w=400"),
        ("meditasyon yapmak", "медитировать", "Meditasyon yapıyorum.", "Я медитирую.", "https://images.unsplash.com/photo-1506126613408-eca07ce68773?w=400"),
        ("hayvan beslemek", "держать животных", "Kedi besliyorum.", "Я держу кошку.", "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=400"),
        ("yoga yapmak", "заниматься йогой", "Yoga yapıyorum.", "Я занимаюсь йогой.", "https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=400"),
        ("tiyatro", "театр", "Tiyatroya gidiyorum.", "Я хожу в театр.", "https://images.unsplash.com/photo-1503095396549-807759245b35?w=400"),
        ("konser", "концерт", "Konsere gidiyorum.", "Я иду на концерт.", "https://images.unsplash.com/photo-1470229722913-7c0e2dbbafd3?w=400"),
        ("sergi", "выставка", "Sergiye gittik.", "Мы ходили на выставку.", "https://images.unsplash.com/photo-1460661419201-fd4cecdf8a8b?w=400"),
        ("alışveriş yapmak", "ходить по магазинам", "Alışveriş yapmayı severim.", "Я люблю ходить по магазинам.", "https://images.unsplash.com/photo-1441984904996-e0b6ba687e04?w=400"),
        ("arkadaşlarla buluşmak", "встречаться с друзьями", "Arkadaşlarla buluşuyorum.", "Я встречаюсь с друзьями.", "https://images.unsplash.com/photo-1543269865-cbf427effbad?w=400"),
        ("piknik yapmak", "ходить на пикник", "Piknik yapıyoruz.", "Мы ходим на пикник.", "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?w=400"),
    ]
    
    # Travel (40)
    travel_data = [
        ("tatil", "отпуск, каникулы", "Tatile gidiyorum.", "Я иду в отпуск.", "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=400"),
        ("gezi", "путешествие, поездка", "Geziye çıkıyoruz.", "Мы отправляемся в путешествие.", "https://images.unsplash.com/photo-1488646953014-85cb44e25828?w=400"),
        ("tur", "тур", "Tura katılıyorum.", "Я участвую в туре.", "https://images.unsplash.com/photo-1488646953014-85cb44e25828?w=400"),
        ("turist", "турист", "Turistim.", "Я турист.", "https://images.unsplash.com/photo-1526772662000-3f88f10405ff?w=400"),
        ("rehber", "гид", "Rehber eşlik ediyor.", "Гид сопровождает.", "https://images.unsplash.com/photo-1530789253388-582c481c54b0?w=400"),
        ("bilet", "билет", "Bilet aldım.", "Я купил билет.", "https://images.unsplash.com/photo-1509281373149-e957c6296406?w=400"),
        ("pasaport", "паспорт", "Pasaportu unuttum.", "Я забыл паспорт.", "https://images.unsplash.com/photo-1436491865332-7a61a109cc05?w=400"),
        ("vize", "виза", "Vize aldım.", "Я получил визу.", "https://images.unsplash.com/photo-1434639424458-2345f9ab2ed3?w=400"),
        ("bavul", "чемодан", "Bavulu hazırladım.", "Я приготовил чемодан.", "https://images.unsplash.com/photo-1565026057447-bc90a3dceb87?w=400"),
        ("valiz", "чемодан, багаж", "Valizi taşıyorum.", "Я несу чемодан.", "https://images.unsplash.com/photo-1502920917128-1aa500764cbd?w=400"),
        ("çanta", "сумка", "Sırt çantası aldım.", "Я купил рюкзак.", "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400"),
        ("harita", "карта", "Haritaya bakıyorum.", "Я смотрю на карту.", "https://images.unsplash.com/photo-1526778548025-fa2f459cd5c1?w=400"),
        ("rezervasyon", "бронирование", "Rezervasyon yaptım.", "Я сделал бронирование.", "https://images.unsplash.com/photo-1587825140708-dfaf72ae4b04?w=400"),
        ("check-in", "регистрация", "Check-in yaptık.", "Мы зарегистрировались.", "https://images.unsplash.com/photo-1436491865332-7a61a109cc05?w=400"),
        ("check-out", "выезд", "Check-out saati 12.", "Время выезда - 12.", "https://images.unsplash.com/photo-1555854877-bab0e564b8d5?w=400"),
        ("oda", "номер (в отеле)", "Odamız çok güzel.", "Наш номер очень красивый.", "https://images.unsplash.com/photo-1611892440504-42a792e24d32?w=400"),
        ("yatak odası", "спальня", "Yatak odası rahat.", "Спальня удобная.", "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?w=400"),
        ("banyo", "ванная", "Banyo temiz.", "Ванная чистая.", "https://images.unsplash.com/photo-1620626011761-996317b8d101?w=400"),
        ("resepsiyon", "рецепция", "Resepsiyonda bekl iyorum.", "Я жду на рецепции.", "https://images.unsplash.com/photo-1531973576160-7125cd663d86?w=400"),
        ("kamp", "кемпинг", "Kampa gidiyoruz.", "Мы едем в кемпинг.", "https://images.unsplash.com/photo-1478131143081-80f7f84ca84d?w=400"),
        ("çadır", "палатка", "Çadır kurduk.", "Мы поставили палатку.", "https://images.unsplash.com/photo-1504851149312-7a075b496cc7?w=400"),
        ("kumsal", "пляж", "Kumsalda yürüyoruz.", "Мы гуляем по пляжу.", "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=400"),
        ("deniz", "море", "Denizde yüzüyoruz.", "Мы плаваем в море.", "https://images.unsplash.com/photo-1505142468610-359e7d316be0?w=400"),
        ("plaj", "пляж", "Plaja gidiyoruz.", "Мы идём на пляж.", "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=400"),
        ("mayo", "купальник", "Mayo giydim.", "Я надел купальник.", "https://images.unsplash.com/photo-1582610116397-edb318620f90?w=400"),
        ("güneş kremi", "солнцезащитный крем", "Güneş kremi sürdüm.", "Я намазал солнцезащитный крем.", "https://images.unsplash.com/photo-1608248543803-ba4f8c70ae0b?w=400"),
        ("şezlong", "шезлонг", "Şezlongda dinleniyorum.", "Я отдыхаю на шезлонге.", "https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=400"),
        ("güneş gözlüğü", "солнцезащитные очки", "Güneş gözlüğü takıyorum.", "Я ношу солнцезащитные очки.", "https://images.unsplash.com/photo-1511499767150-a48a237f0083?w=400"),
        ("kayak", "лыжи", "Kayak yapıyorum.", "Я катаюсь на лыжах.", "https://images.unsplash.com/photo-1551698618-1dfe5d97d256?w=400"),
        ("dağ", "гора", "Dağa tırmanıyoruz.", "Мы лезем на гору.", "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400"),
        ("manzara", "пейзаж, вид", "Manzara muhteşem.", "Пейзаж великолепный.", "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400"),
        ("anı", "памятник", "Anıt güzel.", "Памятник красивый.", "https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?w=400"),
        ("kale", "крепость", "Kaleyi gezdik.", "Мы осмотрели крепость.", "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=400"),
        ("cami", "мечеть", "Camiyi ziyaret ettik.", "Мы посетили мечеть.", "https://images.unsplash.com/photo-1591604466107-ec97de8e784c?w=400"),
        ("kilise", "церковь", "Kiliseye girdik.", "Мы зашли в церковь.", "https://images.unsplash.com/photo-1522093537031-3ee69e6b1746?w=400"),
        ("tapınak", "храм", "Tapınağı gezdik.", "Мы осмотрели храм.", "https://images.unsplash.com/photo-1555400038-63f5ba517a47?w=400"),
        ("saray", "дворец", "Sarayı ziyaret ettik.", "Мы посетили дворец.", "https://images.unsplash.com/photo-1518509562904-e7ef99cdcc86?w=400"),
        ("kültür", "культура", "Kültürü öğreniyoruz.", "Мы изучаем культуру.", "https://images.unsplash.com/photo-1526778548025-fa2f459cd5c1?w=400"),
        ("gelenek", "традиция", "Gelenek güzel.", "Традиция красивая.", "https://images.unsplash.com/photo-1533577116850-9cc66cad8a9b?w=400"),
        ("hediyelik eşya", "сувенир", "Hediyelik eşya aldım.", "Я купил сувенир.", "https://images.unsplash.com/photo-1566776297773-c089c5bc6e88?w=400"),
    ]
    
    # Common Adjectives (180 most common)
    adj_data = [
        ("büyük", "большой", "Büyük ev.", "Большой дом.", "https://images.unsplash.com/photo-1570129477492-45c003edd2be?w=400"),
        ("küçük", "маленький", "Küçük araba.", "Маленькая машина.", "https://images.unsplash.com/photo-1518972559570-7cc1309f3229?w=400"),
        ("yeni", "новый", "Yeni telefon.", "Новый телефон.", "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400"),
        ("eski", "старый", "Eski kitap.", "Старая книга.", "https://images.unsplash.com/photo-1506880018603-83d5b814b5a6?w=400"),
        ("genç", "молодой", "Genç adam.", "Молодой человек.", "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400"),
        ("yaşlı", "старый, пожилой", "Yaşlı adam.", "Пожилой человек.", "https://images.unsplash.com/photo-1595970968158-b9e0a8c3c6f0?w=400"),
        ("uzun", "длинный", "Uzun yol.", "Длинная дорога.", "https://images.unsplash.com/photo-1533587851505-d119e13fa0d7?w=400"),
        ("kısa", "короткий", "Kısa yol.", "Короткая дорога.", "https://images.unsplash.com/photo-1473496169904-658ba7c44d8a?w=400"),
        ("yüksek", "высокий", "Yüksek bina.", "Высокое здание.", "https://images.unsplash.com/photo-1480714378408-67cf0d13bc1b?w=400"),
        ("alçak", "низкий", "Alçak masa.", "Низкий стол.", "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=400"),
        ("geniş", "широкий", "Geniş cadde.", "Широкая улица.", "https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=400"),
        ("dar", "узкий", "Dar sokak.", "Узкая улица.", "https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?w=400"),
        ("kalın", "толстый", "Kalın kitap.", "Толстая книга.", "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=400"),
        ("ince", "тонкий", "İnce kağıt.", "Тонкая бумага.", "https://images.unsplash.com/photo-1587787484117-165ce4e54e7b?w=400"),
        ("ağır", "тяжёлый", "Ağır çanta.", "Тяжёлая сумка.", "https://images.unsplash.com/photo-1590874103328-eac38a683ce7?w=400"),
        ("hafif", "лёгкий", "Hafif çanta.", "Лёгкая сумка.", "https://images.unsplash.com/photo-1590874103328-eac38a683ce7?w=400"),
        ("hızlı", "быстрый", "Hızlı araba.", "Быстрая машина.", "https://images.unsplash.com/photo-1549399542-7e3f8b79c341?w=400"),
        ("yavaş", "медленный", "Yavaş araba.", "Медленная машина.", "https://images.unsplash.com/photo-1550355291-bbee04a92027?w=400"),
        ("güzel", "красивый", "Güzel çiçek.", "Красивый цветок.", "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=400"),
        ("çirkin", "уродливый", "Çirkin bina.", "Уродливое здание.", "https://images.unsplash.com/photo-1588960199985-eac8c54b2ecc?w=400"),
        ("iyi", "хороший", "İyi arkadaş.", "Хороший друг.", "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400"),
        ("kötü", "плохой", "Kötü hava.", "Плохая погода.", "https://images.unsplash.com/photo-1527766833261-b09c3163a791?w=400"),
        ("doğru", "правильный", "Doğru cevap.", "Правильный ответ.", "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=400"),
        ("yanlış", "неправильный", "Yanlış cevap.", "Неправильный ответ.", "https://images.unsplash.com/photo-1567521464027-f127ff144326?w=400"),
        ("kolay", "лёгкий, простой", "Kolay sınav.", "Лёгкий экзамен.", "https://images.unsplash.com/photo-1606326608606-aa0b62935f2b?w=400"),
        ("zor", "трудный", "Zor soru.", "Трудный вопрос.", "https://images.unsplash.com/photo-1516534775068-ba3e7458af70?w=400"),
        ("zengin", "богатый", "Zengin adam.", "Богатый человек.", "https://images.unsplash.com/photo-1554224311-beee415c201f?w=400"),
        ("fakir", "бедный", "Fakir adam.", "Бедный человек.", "https://images.unsplash.com/photo-1490493887695-74ecb98a5e35?w=400"),
        ("temiz", "чистый", "Temiz oda.", "Чистая комната.", "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?w=400"),
        ("kirli", "грязный", "Kirli kıyafet.", "Грязная одежда.", "https://images.unsplash.com/photo-1582735689369-4fe89db7114c?w=400"),
        ("tok", "сытый", "Tok um.", "Я сыт.", "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=400"),
        ("açık", "открытый", "Açık kapı.", "Открытая дверь.", "https://images.unsplash.com/photo-1519710164239-da123dc03ef4?w=400"),
        ("kapalı", "закрытый", "Kapalı pencere.", "Закрытое окно.", "https://images.unsplash.com/photo-1545259741-2ea3ebf61fa3?w=400"),
        ("sessiz", "тихий", "Sessiz oda.", "Тихая комната.", "https://images.unsplash.com/photo-1556911220-bff31c812dba?w=400"),
        ("gürültülü", "шумный", "Gürültülü sokak.", "Шумная улица.", "https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=400"),
        ("tatlı", "сладкий", "Tatlı elma.", "Сладкое яблоко.", "https://images.unsplash.com/photo-1568702846914-96b305d2aaeb?w=400"),
        ("tuzlu", "солёный", "Tuzlu yemek.", "Солёная еда.", "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=400"),
        ("acı", "горький, острый", "Acı biber.", "Острый перец.", "https://images.unsplash.com/photo-1586190848861-99aa4a171e90?w=400"),
        ("ekşi", "кислый", "Ekşi limon.", "Кислый лимон.", "https://images.unsplash.com/photo-1590502593747-42a996133562?w=400"),
        ("lezzetli", "вкусный", "Lezzetli yemek.", "Вкусная еда.", "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=400"),
        ("taze", "свежий", "Taze balık.", "Свежая рыба.", "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?w=400"),
        ("bayat", "чёрствый", "Bayat ekmek.", "Чёрствый хлеб.", "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=400"),
        ("sert", "твёрдый, жёсткий", "Sert yatak.", "Жёсткая кровать.", "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?w=400"),
        ("yumuşak", "мягкий", "Yumuşak yastık.", "Мягкая подушка.", "https://images.unsplash.com/photo-1586075010923-2dd4570fb338?w=400"),
        ("kuru", "сухой", "Kuru havlu.", "Сухое полотенце.", "https://images.unsplash.com/photo-1622445275463-afa2ab738c34?w=400"),
        ("ıslak", "мокрый", "Islak saç.", "Мокрые волосы.", "https://images.unsplash.com/photo-1526047932273-341f2a7631f9?w=400"),
        ("sıcak", "горячий", "Sıcak çay.", "Горячий чай.", "https://images.unsplash.com/photo-1564890369478-c89ca6d9cde9?w=400"),
        ("soğuk", "холодный", "Soğuk su.", "Холодная вода.", "https://images.unsplash.com/photo-1548839140-29a749e1cf4d?w=400"),
        ("ilık", "тёплый", "Ilık su.", "Тёплая вода.", "https://images.unsplash.com/photo-1548839140-29a749e1cf4d?w=400"),
        ("güçlü", "сильный", "Güçlü adam.", "Сильный человек.", "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=400"),
        ("zayıf", "слабый", "Zayıf kol.", "Слабая рука.", "https://images.unsplash.com/photo-1541593095826-d8bb64b3a21e?w=400"),
        ("parlak", "яркий", "Parlak güneş.", "Яркое солнце.", "https://images.unsplash.com/photo-1602496674108-a5aab96d51a7?w=400"),
        ("karanlık", "тёмный", "Karanlık oda.", "Тёмная комната.", "https://images.unsplash.com/photo-1515694346937-94d85e41e6f0?w=400"),
        ("aydınlık", "светлый", "Aydınlık oda.", "Светлая комната.", "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=400"),
        ("net", "чёткий, ясный", "Net görüntü.", "Чёткое изображение.", "https://images.unsplash.com/photo-1593642632823-8f785ba67e45?w=400"),
        ("bulanık", "размытый, мутный", "Bulanık fotoğraf.", "Размытая фотография.", "https://images.unsplash.com/photo-1505652964656-74a3c84a9f7e?w=400"),
        ("düz", "прямой, ровный", "Düz yol.", "Прямая дорога.", "https://images.unsplash.com/photo-1533587851505-d119e13fa0d7?w=400"),
        ("eğri", "кривой", "Eğri çizgi.", "Кривая линия.", "https://images.unsplash.com/photo-1509228468518-180dd4864904?w=400"),
        ("yuvarlak", "круглый", "Yuvarlak masa.", "Круглый стол.", "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=400"),
        ("kare", "квадратный", "Kare kutu.", "Квадратная коробка.", "https://images.unsplash.com/photo-1525897427976-d5d8e6b3e05d?w=400"),
        ("dikdörtgen", "прямоугольный", "Dikdörtgen masa.", "Прямоугольный стол.", "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=400"),
        ("üçgen", "треугольный", "Üçgen şekil.", "Треугольная форма.", "https://images.unsplash.com/photo-1509228468518-180dd4864904?w=400"),
        ("dolu", "полный", "Dolu bardak.", "Полный стакан.", "https://images.unsplash.com/photo-1548839140-29a749e1cf4d?w=400"),
        ("boş", "пустой", "Boş bardak.", "Пустой стакан.", "https://images.unsplash.com/photo-1583334975949-7c27c163e044?w=400"),
        ("çok", "много, очень", "Çok para.", "Много денег.", "https://images.unsplash.com/photo-1579621970563-ebec7560ff3e?w=400"),
        ("az", "мало", "Az para.", "Мало денег.", "https://images.unsplash.com/photo-1607863680198-23d4b2565df0?w=400"),
        ("fazla", "слишком много, лишний", "Fazla yemek.", "Слишком много еды.", "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=400"),
        ("yeterli", "достаточный", "Yeterli para.", "Достаточно денег.", "https://images.unsplash.com/photo-1579621970563-ebec7560ff3e?w=400"),
        ("yetersiz", "недостаточный", "Yetersiz para.", "Недостаточно денег.", "https://images.unsplash.com/photo-1607863680198-23d4b2565df0?w=400"),
        ("yararlı", "полезный", "Yararlı bilgi.", "Полезная информация.", "https://images.unsplash.com/photo-1516534775068-ba3e7458af70?w=400"),
        ("zararlı", "вредный", "Zararlı madde.", "Вредное вещество.", "https://images.unsplash.com/photo-1582719471384-894fbb16e074?w=400"),
        ("önemli", "важный", "Önemli konu.", "Важная тема.", "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=400"),
        ("önemsiz", "неважный", "Önemsiz detay.", "Неважная деталь.", "https://images.unsplash.com/photo-1516534775068-ba3e7458af70?w=400"),
        ("tehlikeli", "опасный", "Tehlikeli yol.", "Опасная дорога.", "https://images.unsplash.com/photo-1527482797697-8795b05a13fe?w=400"),
        ("güvenli", "безопасный", "Güvenli bölge.", "Безопасная зона.", "https://images.unsplash.com/photo-1505751172876-fa1923c5c528?w=400"),
        ("rahat", "удобный", "Rahat koltuk.", "Удобное кресло.", "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=400"),
        ("rahatsız", "неудобный", "Rahatsız sandalye.", "Неудобный стул.", "https://images.unsplash.com/photo-1503602642458-232111445657?w=400"),
        ("boş", "свободный (время)", "Boş zamanım var.", "У меня есть свободное время.", "https://images.unsplash.com/photo-1501139083538-0139583c060f?w=400"),
        ("meşgul", "занятый", "Meşgulüm.", "Я занят.", "https://images.unsplash.com/photo-1486312338219-ce68d2c6f44d?w=400"),
        ("basit", "простой", "Basit soru.", "Простой вопрос.", "https://images.unsplash.com/photo-1516534775068-ba3e7458af70?w=400"),
        ("karmaşık", "сложный", "Karmaşık problem.", "Сложная проблема.", "https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=400"),
        ("farklı", "разный, другой", "Farklı renk.", "Другой цвет.", "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400"),
        ("aynı", "одинаковый", "Aynı renk.", "Одинаковый цвет.", "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400"),
        ("benzer", "похожий", "Benzer şekil.", "Похожая форма.", "https://images.unsplash.com/photo-1509228468518-180dd4864904?w=400"),
        ("değişik", "разный", "Değişik şekil.", "Разная форма.", "https://images.unsplash.com/photo-1509228468518-180dd4864904?w=400"),
        ("özel", "особый, личный", "Özel gün.", "Особый день.", "https://images.unsplash.com/photo-1464349095431-e9a21285b5f3?w=400"),
        ("genel", "общий", "Genel bilgi.", "Общая информация.", "https://images.unsplash.com/photo-1516534775068-ba3e7458af70?w=400"),
        ("yakın", "близкий", "Yakın arkadaş.", "Близкий друг.", "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400"),
        ("uzak", "далёкий", "Uzak şehir.", "Далёкий город.", "https://images.unsplash.com/photo-1480714378408-67cf0d13bc1b?w=400"),
        ("erken", "ранний", "Erken saat.", "Ранний час.", "https://images.unsplash.com/photo-1495214783159-3503fd1b572d?w=400"),
        ("geç", "поздний", "Geç saat.", "Поздний час.", "https://images.unsplash.com/photo-1513002749550-c59d786b8e6c?w=400"),
        ("ilk", "первый", "İlk gün.", "Первый день.", "https://images.unsplash.com/photo-1506784365847-bbad939e9335?w=400"),
        ("son", "последний", "Son gün.", "Последний день.", "https://images.unsplash.com/photo-1513002749550-c59d786b8e6c?w=400"),
        ("önceki", "предыдущий", "Önceki hafta.", "Предыдущая неделя.", "https://images.unsplash.com/photo-1506784365847-bbad939e9335?w=400"),
        ("sonraki", "следующий", "Sonraki hafta.", "Следующая неделя.", "https://images.unsplash.com/photo-1506784983877-45594efa4cbe?w=400"),
        ("şimdiki", "настоящий (время)", "Şimdiki zaman.", "Настоящее время.", "https://images.unsplash.com/photo-1501139083538-0139583c060f?w=400"),
        ("gelecekteki", "будущий", "Gelecekteki planlar.", "Будущие планы.", "https://images.unsplash.com/photo-1506784365847-bbad939e9335?w=400"),
        ("geçmiş", "прошлый", "Geçmiş yıl.", "Прошлый год.", "https://images.unsplash.com/photo-1506784983877-45594efa4cbe?w=400"),
        ("mümkün", "возможный", "Mümkün çözüm.", "Возможное решение.", "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=400"),
        ("imkansız", "невозможный", "İmkansız durum.", "Невозможная ситуация.", "https://images.unsplash.com/photo-1567521464027-f127ff144326?w=400"),
        ("muhtemel", "вероятный", "Muhtemel sonuç.", "Вероятный результат.", "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=400"),
        ("kesin", "точный, определённый", "Kesin cevap.", "Точный ответ.", "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=400"),
        ("belirsiz", "неопределённый", "Belirsiz durum.", "Неопределённая ситуация.", "https://images.unsplash.com/photo-1581291518857-4e27b48ff24e?w=400"),
        ("hazır", "готовый", "Hazır yemek.", "Готовая еда.", "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=400"),
        ("ham", "сырой", "Ham sebze.", "Сырой овощ.", "https://images.unsplash.com/photo-1597362925123-77861d3fbac7?w=400"),
        ("pişmiş", "приготовленный", "Pişmiş et.", "Приготовленное мясо.", "https://images.unsplash.com/photo-1588168333986-5078d3ae3976?w=400"),
        ("canlı", "живой", "Canlı balık.", "Живая рыба.", "https://images.unsplash.com/photo-1535591273668-578e31182c4f?w=400"),
        ("ölü", "мёртвый", "Ölü ağaç.", "Мёртвое дерево.", "https://images.unsplash.com/photo-1542273917363-3b1817f69a2d?w=400"),
        ("aktif", "активный", "Aktif insan.", "Активный человек.", "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=400"),
        ("pasif", "пассивный", "Pasif kişi.", "Пассивный человек.", "https://images.unsplash.com/photo-1541593095826-d8bb64b3a21e?w=400"),
        ("pozitif", "положительный", "Pozitif düşünce.", "Положительная мысль.", "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400"),
        ("negatif", "отрицательный", "Negatif düşünce.", "Отрицательная мысль.", "https://images.unsplash.com/photo-1499209974431-9dddcece7f88?w=400"),
        ("normal", "нормальный", "Normal durum.", "Нормальная ситуация.", "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400"),
        ("anormal", "ненормальный", "Anormal durum.", "Ненормальная ситуация.", "https://images.unsplash.com/photo-1567521464027-f127ff144326?w=400"),
        ("resmi", "официальный", "Resmi belge.", "Официальный документ.", "https://images.unsplash.com/photo-1568346974664-027a2610070c?w=400"),
        ("gayri resmi", "неофициальный", "Gayri resmi toplantı.", "Неофициальная встреча.", "https://images.unsplash.com/photo-1556761175-4b46a572b786?w=400"),
        ("modern", "современный", "Modern bina.", "Современное здание.", "https://images.unsplash.com/photo-1480714378408-67cf0d13bc1b?w=400"),
        ("klasik", "классический", "Klasik müzik.", "Классическая музыка.", "https://images.unsplash.com/photo-1511379938547-c1f69419868d?w=400"),
        ("popüler", "популярный", "Popüler şarkı.", "Популярная песня.", "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?w=400"),
        ("nadir", "редкий", "Nadir eşya.", "Редкая вещь.", "https://images.unsplash.com/photo-1571974599782-87624638275a?w=400"),
        ("sıradan", "обычный", "Sıradan gün.", "Обычный день.", "https://images.unsplash.com/photo-1506784365847-bbad939e9335?w=400"),
        ("olağanüstü", "необычный, чрезвычайный", "Olağanüstü durum.", "Чрезвычайная ситуация.", "https://images.unsplash.com/photo-1527482937786-6608b9740778?w=400"),
        ("yerel", "местный", "Yerel yemek.", "Местная еда.", "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=400"),
        ("uluslararası", "международный", "Uluslararası şirket.", "Международная компания.", "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=400"),
        ("ulusal", "национальный", "Ulusal bayram.", "Национальный праздник.", "https://images.unsplash.com/photo-1464349095431-e9a21285b5f3?w=400"),
        ("küresel", "глобальный", "Küresel sorun.", "Глобальная проблема.", "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=400"),
        ("yeşil", "зелёный (эко)", "Yeşil enerji.", "Зелёная энергия.", "https://images.unsplash.com/photo-1558391380-c7d0b86e9c69?w=400"),
        ("organik", "органический", "Organik sebze.", "Органический овощ.", "https://images.unsplash.com/photo-1597362925123-77861d3fbac7?w=400"),
        ("doğal", "натуральный, естественный", "Doğal ürün.", "Натуральный продукт.", "https://images.unsplash.com/photo-1597362925123-77861d3fbac7?w=400"),
        ("yapay", "искусственный", "Yapay çiçek.", "Искусственный цветок.", "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=400"),
        ("gerçek", "настоящий, реальный", "Gerçek hikaye.", "Настоящая история.", "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=400"),
        ("sahte", "фальшивый", "Sahte para.", "Фальшивые деньги.", "https://images.unsplash.com/photo-1579621970563-ebec7560ff3e?w=400"),
        ("eksiksiz", "полный, без изъяна", "Eksiksiz rapor.", "Полный отчёт.", "https://images.unsplash.com/photo-1568346974664-027a2610070c?w=400"),
        ("eksik", "неполный", "Eksik bilgi.", "Неполная информация.", "https://images.unsplash.com/photo-1516534775068-ba3e7458af70?w=400"),
        ("tam", "полный, целый", "Tam gün.", "Целый день.", "https://images.unsplash.com/photo-1506784365847-bbad939e9335?w=400"),
        ("yarım", "половинный", "Yarım saat.", "Полчаса.", "https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=400"),
        ("bütün", "весь, целый", "Bütün gün.", "Весь день.", "https://images.unsplash.com/photo-1506784365847-bbad939e9335?w=400"),
        ("kısmi", "частичный", "Kısmi zarar.", "Частичный ущерб.", "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=400"),
        ("tam zamanlı", "полный рабочий день", "Tam zamanlı iş.", "Работа на полный день.", "https://images.unsplash.com/photo-1486312338219-ce68d2c6f44d?w=400"),
        ("yarı zamanlı", "неполный рабочий день", "Yarı zamanlı iş.", "Работа на неполный день.", "https://images.unsplash.com/photo-1554224311-beee415c201f?w=400"),
        ("geçici", "временный", "Geçici iş.", "Временная работа.", "https://images.unsplash.com/photo-1554224311-beee415c201f?w=400"),
        ("kalıcı", "постоянный", "Kalıcı iş.", "Постоянная работа.", "https://images.unsplash.com/photo-1486312338219-ce68d2c6f44d?w=400"),
        ("sonsuz", "бесконечный", "Sonsuz aşk.", "Бесконечная любовь.", "https://images.unsplash.com/photo-1502085671122-2d218cd434e6?w=400"),
        ("sınırlı", "ограниченный", "Sınırlı zaman.", "Ограниченное время.", "https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=400"),
        ("sınırsız", "неограниченный", "Sınırsız internet.", "Безлимитный интернет.", "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=400"),
        ("yasak", "запрещённый", "Yasak bölge.", "Запрещённая зона.", "https://images.unsplash.com/photo-1527482937786-6608b9740778?w=400"),
        ("serbest", "свободный", "Serbest giriş.", "Свободный вход.", "https://images.unsplash.com/photo-1519710164239-da123dc03ef4?w=400"),
        ("zorunlu", "обязательный", "Zorunlu ders.", "Обязательный урок.", "https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=400"),
        ("isteğe bağlı", "необязательный", "İsteğe bağlı ders.", "Необязательный урок.", "https://images.unsplash.com/photo-1509062522246-3755977927d7?w=400"),
        ("hukuki", "юридический, правовой", "Hukuki sorun.", "Правовая проблема.", "https://images.unsplash.com/photo-1589829545856-d10d557cf95f?w=400"),
        ("yasadışı", "незаконный", "Yasadışı faaliyet.", "Незаконная деятельность.", "https://images.unsplash.com/photo-1527482937786-6608b9740778?w=400"),
        ("yasal", "законный", "Yasal belge.", "Законный документ.", "https://images.unsplash.com/photo-1568346974664-027a2610070c?w=400"),
        ("mantıklı", "логичный", "Mantıklı açıklama.", "Логичное объяснение.", "https://images.unsplash.com/photo-1516534775068-ba3e7458af70?w=400"),
        ("mantıksız", "нелогичный", "Mantıksız karar.", "Нелогичное решение.", "https://images.unsplash.com/photo-1554224311-beee415c201f?w=400"),
        ("dikkatli", "внимательный, осторожный", "Dikkatli sürücü.", "Внимательный водитель.", "https://images.unsplash.com/photo-1568605117036-5fe5e7bab0b7?w=400"),
        ("dikkatsiz", "невнимательный", "Dikkatsiz hatalar.", "Невнимательные ошибки.", "https://images.unsplash.com/photo-1567521464027-f127ff144326?w=400"),
        ("sabırlı", "терпеливый", "Sabırlı öğretmen.", "Терпеливый учитель.", "https://images.unsplash.com/photo-1580582932707-520aed937b7b?w=400"),
        ("sabırsız", "нетерпеливый", "Sabırsız çocuk.", "Нетерпеливый ребёнок.", "https://images.unsplash.com/photo-1519925610903-381054cc2a1a?w=400"),
        ("dürüst", "честный", "Dürüst insan.", "Честный человек.", "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400"),
        ("yalancı", "лживый", "Yalancı adam.", "Лживый человек.", "https://images.unsplash.com/photo-1485178575877-1a13bf489dfe?w=400"),
        ("samimi", "искренний", "Samimi arkadaş.", "Искренний друг.", "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400"),
        ("sahte", "притворный", "Sahte gülüş.", "Фальшивая улыбка.", "https://images.unsplash.com/photo-1542596768-5d1d21f1cf98?w=400"),
        ("cömert", "щедрый", "Cömert adam.", "Щедрый человек.", "https://images.unsplash.com/photo-1513885535751-8b9238bd345a?w=400"),
        ("cimri", "скупой", "Cimri adam.", "Скупой человек.", "https://images.unsplash.com/photo-1579621970563-ebec7560ff3e?w=400"),
        ("kibar", "вежливый", "Kibar adam.", "Вежливый человек.", "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400"),
        ("kaba", "грубый", "Kaba davranış.", "Грубое поведение.", "https://images.unsplash.com/photo-1485178575877-1a13bf489dfe?w=400"),
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
        ("hobbies", hobbies_data),
        ("travel", travel_data),
        ("adjectives_common", adj_data)
    ]
    
    for cat_info in cats:
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
    
    print(f"\n📊 Final Push Özet:")
    print(f"  - Yeni Kategori: {len(categories_to_insert)}")
    print(f"  - Yeni Kelime: {len(words_to_insert)}")
    print(f"\n🎯 BÜYÜK TOPLAM:")
    print(f"  - Toplam Kategori: {total_cats}")
    print(f"  - Toplam Kelime: {total_words}")
    
    if total_words >= 1000:
        print(f"\n🎉🎉🎉 BAŞARILI! 1000 KELIME HEDEFİNİ AŞTIK! 🎉🎉🎉")
        print(f"  - Hedefin %{int((total_words/1000)*100)}\'ine ulaştık!")
        print(f"  - Hedeften {total_words-1000} kelime fazla!")
    else:
        print(f"\n📌 Hedefe ulaşmak için {1000-total_words} kelime daha gerekiyor.")
    
    print("\n✅ Final Push tamamlandı!")

if __name__ == "__main__":
    asyncio.run(seed_final_push())
    client.close()
