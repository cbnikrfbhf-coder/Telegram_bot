import requests, os, re, time, html as htmllib
from datetime import datetime

BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHANNEL_ID = os.environ.get('CHANNEL_ID')
PEXELS_KEY = os.environ.get('PEXELS_KEY')
PROMO = '\n\n📢 @shegftanekhabar'
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

POETRY = [
    '🌙 من از نهایت شب حرف می‌زنم\nمن از نهایت تاریکی\nو از نهایت شب حرف می‌زنم\n— فروغ فرخزاد',
    '🌙 بوی باران، بوی سبزه، بوی خاک\nشاخه‌های شسته، باران‌خورده، پاک\n— سهراب سپهری',
    '🌙 زندگی خالی نیست\nمهربانی هست، سیب هست، ایمان هست\n— سهراب سپهری',
    '🌙 من و انکار تو و این صدای باران\nکه می‌شنودش کسی که نیست\n— احمد شاملو',
    '🌙 از صدای سخن عشق ندیدم خوش‌تر\nیادگاری که در این گنبد دوار بماند\n— حافظ',
    '🌙 چه خوش گفت آن شبی کز عشق می‌گفت\nکه عشق آسان نمود اول، ولی افتاد مشکل‌ها\n— حافظ',
    '🌙 درخت دوستی بنشان که کام دل به بار آرد\nنهال دشمنی برکن که رنج بی‌شمار آرد\n— حافظ',
    '🌸 بنی‌آدم اعضای یکدیگرند\nکه در آفرینش ز یک گوهرند\n— سعدی',
    '🌸 توانا بود هر که دانا بود\nز دانش دل پیر برنا بود\n— فردوسی',
    '🌸 میازار موری که دانه‌کش است\nکه جان دارد و جان شیرین خوش است\n— سعدی',
]
RELIGIOUS = [
    '🕌 «إِنَّ مَعَ الْعُسْرِ يُسْرًا»\nهمانا با هر سختی، آسانی است.',
    '🕌 «وَمَن يَتَوَكَّلْ عَلَى اللَّهِ فَهُوَ حَسْبُهُ»\nهر که بر خدا توکل کند، او کفایتش می‌کند.',
    '🕌 امام علی (ع): «ارزش هر کس به نیکوکاری اوست.»',
    '🕌 پیامبر اکرم (ص): «لبخند تو در چهره برادرت، صدقه است.»',
    '🕌 «الصَّبْرُ مِفتاحُ الفَرَجِ»\nصبر، کلید هر گشایشی است.',
]
SATIRE = [
    '🎭 قیمت مرغ انقدر رفته بالا که حالا مرغ‌ها فکر می‌کنن برن بورس!',
    '🎭 تورم انقدر تیزه که حتی بادکنک‌ها هم از ما جلو می‌زنن!',
    '🎭 حقوقم انقدر کمه که حتی خودم هم نمی‌تونم استخدامش کنم!',
    '🎭 دلار انقدر رفته بالا که حالا داره به ما نگاه می‌کنه و می‌خنده!',
    '🎭 رفتم رستوران، منو رو دیدم، گفتم یه لیوان اشک بدید، خودم تولید می‌کنم!',
]
ENERGY = [
    '💪 زندگی مثل دوچرخه‌سواریه؛ برای حفظ تعادل باید حرکت کنی!',
    '🌟 هر طلوع خورشید یه فرصت جدیده؛ ازش استفاده کن!',
    '⭐ رویاهات تاریخ انقضا ندارن؛ یه نفس عمیق بکش و دوباره شروع کن!',
    '🌈 بعد از هر طوفانی، رنگین‌کمان میاد؛ صبور باش!',
]
COOKING = [
    '🍳 نیمرو: روغن، تخم‌مرغ، نمک و فلفل. ساده‌ترین صبحانه دنیا!',
    '🍲 قورمه‌سبزی: سبزی، گوشت، لیموعمانی و یه ذره زعفران. غذای ملی ما!',
    '🥘 زرشک‌پلو با مرغ: برنج، زرشک، مرغ، زعفران. ساده و خوشمزه!',
]
MOVIES = [
    '🎬 از «پایتخت» تا «زخم کاری»؛ سریال‌های ایرانی پر از شاهکارن!',
    '🎬 سینمای ایران با اصغر فرهادی همیشه در سطح جهان درخشیده!',
    '🍿 دنیای مارول و DC؛ ابرقهرمان‌هایی که باکس‌آفیس رو می‌ترکونن!',
]
BOOKS = [
    '📚 «صد سال تنهایی» مارکز؛ شاهکار ادبیات جهان!',
    '📚 «کلیدر» دولت‌آبادی؛ بلندترین رمان فارسی!',
    '📚 «بوف کور» صادق هدایت؛ رمانی که هنوز مرموزه!',
    '📚 «سمفونی مردگان» عباس معروفی؛ روایتی تکان‌دهنده!',
]
FACTS = [
    '🐙 اختاپوس ۳ تا قلب داره و خونش آبیه!',
    '🍯 عسل هرگز فاسد نمیشه؛ عسل ۳۰۰۰ ساله هنوز قابل خوردنه!',
    '🌍 یه روز در سیاره زهره از یه سالش طولانی‌تره!',
    '🦈 کوسه‌ها ۴۰۰ میلیون ساله، قبل از دایناسورها وجود داشتن!',
    '🧠 مغز موقع خواب فعال‌تر از روزه؛ داره اطلاعات رو مرتب می‌کنه!',
]
HUMOR = [
    '😂 رفتم داروخانه گفتم یه چیز خوب برای سرماخوردگی بدید، گفت ۲۰۰ تومن! گفتم باشه، خودم خوب میشم!',
    '😂 دوستم گفت پول خوشبختی نمی‌آره، گفتم باشه پولت رو بده من تحمل می‌کنم!',
    '😂 مامانم گفت چرا لاغر شدی؟ گفتم مامان قیمت مرغ رو دیدی؟!',
    '😂 تنها ورزشی که استادم، ورزشِ از زیر کار در رفتنه!',
]
TECH = [
    '🤖 هوش مصنوعی داره همه‌چیز رو عوض می‌کنه؛ آینده همین الان اینجاست!',
    '📱 گوشی‌های تاشو؛ سامسونگ و هواوی در رقابت نفس‌گیر!',
    '🚗 خودروهای برقی تسلا و BYD دارن بازار رو قبضه می‌کنن!',
]
SPORTS = [
    '⚽ دربی پرسپولیس و استقلال؛ جنگ تمام‌عیار دو غول فوتبال ایران!',
    '🏐 والیبال ایران؛ افتخارآفرین آسیا و جهان!',
    '🥋 کشتی؛ ورزش ملی و مدال‌آور ایران!',
]
WALL_TAGS = [('nature','طبیعت'),('mountain','کوه'),('ocean','دریا'),('forest','جنگل'),('flower','گل'),('sunset','غروب')]

def clean(t):
    t = re.sub(r'<!\[CDATA\[(.*?)\]\]>', r'\1', t)
    t = re.sub(r'<[^>]+>', '', t)
    return htmllib.unescape(t).strip()

def translate(text):
    try:
        r = requests.get('https://translate.googleapis.com/translate_a/single',
            params={'client':'gtx','sl':'en','tl':'fa','dt':'t','q':text}, timeout=10)
        out = ''.join([p[0] for p in r.json()[0] if p and p[0]])
        return out.strip() or text
    except:
        return text

def rss_titles(url, n=15):
    try:
        r = requests.get(url, headers=UA, timeout=15)
        items = re.findall(r'<item>(.*?)</item>', r.text, re.DOTALL)
        out = []
        for it in items[:n]:
            m = re.search(r'<title[^>]*>(.*?)</title>', it, re.DOTALL)
            if m:
                t = clean(m.group(1))
                if t: out.append(t)
        return out
    except:
        return []

def reddit_titles(sub, n=15):
    try:
        r = requests.get(f'https://www.reddit.com/r/{sub}/hot.json?limit={n}', headers=UA, timeout=15)
        return [c['data']['title'] for c in r.json()['data']['children']]
    except:
        return []

def pick(items, idx, fallback):
    if items: return items[idx % len(items)]
    return fallback[idx % len(fallback)]

def get_news(idx):
    for url in ['https://www.isna.ir/rss','https://www.mehrnews.com/rss']:
        items = rss_titles(url)
        if items: return f'📰 {items[idx % len(items)]}' + PROMO
    return None

def get_tech(idx):
    for url in ['https://www.zoomit.ir/feed','https://digiato.com/feed']:
        items = rss_titles(url)
        if items: return f'💻 {items[idx % len(items)]}\n\n#تکنولوژی' + PROMO
    return f'💻 {pick([], idx, TECH)}\n\n#تکنولوژی' + PROMO

def get_sports(idx):
    items = rss_titles('https://www.varzesh3.com/rss')
    return f'⚽ {pick(items, idx, SPORTS)}\n\n#ورزشی' + PROMO

def get_world(idx):
    items = rss_titles('https://www.theverge.com/rss/index.xml')
    if not items:
        items = [translate(t) for t in reddit_titles('worldnews')]
    if items:
        t = items[idx % len(items)]
        if not any('\u0600' <= ch <= '\u06FF' for ch in t):
            t = translate(t)
        return f'🌍 {t}\n\n#جهان' + PROMO
    return None

def get_fact(idx):
    items = [t.replace('TIL ','') for t in reddit_titles('todayilearned')]
    if items:
        return f'🤔 آیا می‌دانستی؟ {translate(items[idx % len(items)])}\n\n#دانستنی' + PROMO
    return f'🤔 {pick([], idx, FACTS)}\n\n#دانستنی' + PROMO

def get_joke(idx):
    items = reddit_titles('oneliners')
    if items:
        return f'😂 {translate(items[idx % len(items)])}\n\n#طنز' + PROMO
    return f'😂 {pick([], idx, HUMOR)}\n\n#طنز' + PROMO

def get_gold():
    try:
        r = requests.get('https://www.tgju.org/', headers=UA, timeout=20)
        def after(label):
            i = r.text.find(label)
            if i == -1: return None
            m = re.search(r'([\d][\d,]{4,})', r.text[i+len(label):i+len(label)+600])
            return m.group(1) if m else None
        coin = after('سکه امامی') or after('سکه')
        gold18 = after('طلا ۱۸') or after('طلا 18')
        dollar = after('دلار')
        if coin or dollar:
            lines = ['🪙 قیمت لحظه‌ای بازار:', '']
            if coin: lines.append(f'💰 سکه امامی: {coin} تومان')
            if gold18: lines.append(f'✨ طلای ۱۸ عیار: {gold18} تومان')
            if dollar: lines.append(f'💵 دلار: {dollar} تومان')
            return '\n'.join(lines) + '\n\n#طلا #سکه #ارز' + PROMO
    except:
        pass
    return None

def get_wallpaper(idx):
    try:
        en, fa = WALL_TAGS[idx % len(WALL_TAGS)]
        r = requests.get('https://api.pexels.com/v1/search',
            headers={'Authorization': PEXELS_KEY},
            params={'query': en, 'per_page': 15, 'orientation': 'portrait'}, timeout=15)
        photos = r.json().get('photos', [])
        if photos:
            p = photos[idx % len(photos)]
            return p['src']['large'], f'🖼 والپیپر {fa}\n\n📸 عکاس: {p.get("photographer","")}\n\n#والپیپر' + PROMO
    except:
        pass
    return None, None

def send(msg, photo=None):
    try:
        if photo:
            url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto'
            r = requests.post(url, json={'chat_id': CHANNEL_ID, 'photo': photo, 'caption': msg}, timeout=20)
        else:
            url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
            r = requests.post(url, json={'chat_id': CHANNEL_ID, 'text': msg}, timeout=20)
        print('Send:', r.status_code, r.json().get('ok'))
    except Exception as e:
        print('Send error:', e)

def post(ctype, idx):
    print('Posting:', ctype)
    if ctype == 'news':
        t = get_news(idx)
        if t: send(t)
    elif ctype == 'gold':
        t = get_gold()
        if t: send(t)
    elif ctype == 'tech': send(get_tech(idx))
    elif ctype == 'sports': send(get_sports(idx))
    elif ctype == 'world':
        t = get_world(idx)
        if t: send(t)
    elif ctype == 'fact': send(get_fact(idx))
    elif ctype == 'humor': send(get_joke(idx))
    elif ctype == 'poetry': send(POETRY[idx % len(POETRY)] + '\n\n#شعر' + PROMO)
    elif ctype == 'religious': send(RELIGIOUS[idx % len(RELIGIOUS)] + '\n\n#مذهبی' + PROMO)
    elif ctype == 'satire': send(SATIRE[idx % len(SATIRE)] + '\n\n#طنز_اجتماعی' + PROMO)
    elif ctype == 'energy': send(ENERGY[idx % len(ENERGY)] + '\n\n#انرژی_مثبت' + PROMO)
    elif ctype == 'cooking': send(COOKING[idx % len(COOKING)] + '\n\n#آشپزی' + PROMO)
    elif ctype == 'movies': send(MOVIES[idx % len(MOVIES)] + '\n\n#سینما' + PROMO)
    elif ctype == 'books': send(BOOKS[idx % len(BOOKS)] + '\n\n#کتاب' + PROMO)
    elif ctype == 'wallpaper':
        photo, cap = get_wallpaper(idx)
        if photo: send(cap, photo)
        else: send(FACTS[idx % len(FACTS)] + '\n\n#دانستنی' + PROMO)

def main():
    if not (BOT_TOKEN and CHANNEL_ID and PEXELS_KEY):
        print('Missing credentials')
        return
    slot = int(time.time() // 1800)
    hour = datetime.now().hour
    if 6 <= hour < 12:
        base = ['energy','news','gold','tech','sports','world','fact','wallpaper']
    elif 12 <= hour < 18:
        base = ['gold','news','humor','world','cooking','tech','sports','fact','movies','books']
    else:
        base = ['poetry','religious','satire','wallpaper','world','energy','humor','fact']
    off = slot % len(base)
    for i in range(6):
        ctype = base[(off + i) % len(base)]
        idx = int(time.time() // 300)
        post(ctype, idx)
        if i < 5:
            time.sleep(300)

if __name__ == '__main__':
    main()
