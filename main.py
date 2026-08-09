import requests, os, re, time, html as htmllib
from datetime import datetime

BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHANNEL_ID = os.environ.get('CHANNEL_ID')
PEXELS_KEY = os.environ.get('PEXELS_KEY')
PROMO = '\n\n📢 @shegftanekhabar'
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

HOROSCOPES = {
    'فروردین': '🔮 امروز یه فرصت غیرمنتظره سر راهت قرار می‌گیره. با دل جلو برو ولی عجله نکن. عدد شانس: ۷',
    'اردیبهشت': '🔮 یه مکالمه مهم امروز می‌تونه مسیر هفته‌ت رو عوض کنه. صبور باش و گوش کن. عدد شانس: ۱۴',
    'خرداد': '🔮 خلاقیتت امروز تو اوجه! هر ایده‌ای داری یادداشت کن، بعداً ارزشمند میشه. عدد شانس: ۳',
    'تیر': '🔮 یه خبر مالی خوشحال‌کننده در راهه. مراقب خرج‌های اضافی باش. عدد شانس: ۲۲',
    'مرداد': '🔮 امروز روز خوبیه برای شروع یه کار جدید. اعتماد به نفس داشته باش. عدد شانس: ۸',
    'شهریور': '🔮 یه دوست قدیمی امروز بهت زنگ می‌زنه. خبر خوبی داره برات. عدد شانس: ۱۱',
    'مهر': '🔮 تمرکز کن روی کارای مهم. حواست رو پرت نکن، موفقیت نزدیکه. عدد شانس: ۵',
    'آبان': '🔮 احساساتت قویه امروز. ازشون استفاده کن برای تصمیم‌های مهم. عدد شانس: ۱۹',
    'آذر': '🔮 سفر کوتاه یا یه تغییر مکان امروز برات مفیده. انرژیت بالا میره. عدد شانس: ۲',
    'دی': '🔮 یه تصمیم مالی مهم امروز باید بگیری. با منطق جلو برو نه احساس. عدد شانس: ۱۶',
    'بهمن': '🔮 امروز روز خوبیه برای یادگیری چیز جدید. ذهنت بازه. عدد شانس: ۹',
    'اسفند': '🔮 یه ملاقات مهم امروز ممکنه اتفاق بیفته. آماده باش. عدد شانس: ۲۵',
}

LANDMARKS = [
    ('تخت جمشید', 'Persepolis', 'شکوه ایران باستان، پایتخت تشریفاتی هخامنشیان. ساخته شده توسط داریوش بزرگ در ۵۱۸ قبل از میلاد.'),
    ('میدان نقش جهان', 'Isfahan', 'قلب تپنده اصفهان، یکی از بزرگ‌ترین میدان‌های جهان. ساخته شده در دوره صفویه.'),
    ('برج آزادی', 'Tehran tower', 'نماد پایتخت ایران، ساخته شده در سال ۱۳۵۰. ترکیبی از معماری هخامنشی و اسلامی.'),
    ('باغ ارم شیراز', 'Shiraz garden', 'یکی از زیباترین باغ‌های ایرانی با درختان سرو کهنسال و عمارت قاجاری.'),
    ('پل خواجو', 'Isfahan bridge', 'شاهکار معماری صفوی در اصفهان، جایی برای قدم زدن و آواز خواندن.'),
    ('مسجد نصیرالملک', 'Pink Mosque', 'مسجد صورتی شیراز با شیشه‌های رنگی که رقص نور ایجاد می‌کنه.'),
    ('کاخ گلستان', 'Golestan Palace', 'میراث جهانی یونسکو در تهران، اقامتگاه شاهان قاجار.'),
    ('بازار تبریز', 'Tabriz bazaar', 'بزرگ‌ترین بازار سرپوشیده جهان و میراث جهانی یونسکو.'),
    ('دریاچه ارومیه', 'Urmia lake', 'بزرگ‌ترین دریاچه داخلی ایران و دومین دریاچه آب شور جهان.'),
    ('جنگل‌های هیرکانی', 'Hyrcanian forests', 'میراث جهانی یونسکو، جنگل‌های باستانی شمال ایران با قدمت ۵۰ میلیون سال.'),
    ('چغازنبیل', 'Chogha Zanbil', 'معبد باستانی ایلامی در خوزستان، قدیمی‌ترین بنای ایران ثبت شده در یونسکو.'),
    ('کویر لوت', 'Lut desert', 'گرم‌ترین نقطه زمین! ثبت شده به عنوان میراث جهانی یونسکو.'),
    ('جزیره کیش', 'Kish island', 'مروارید خلیج فارس با سواحل بکر و مراکز خرید مدرن.'),
    ('ماسوله', 'Masuleh', 'روستای پلکانی گیلان، معماری منحصر به فرد هزار ساله.'),
    ('بم و ارگ تاریخی', 'Bam citadel', 'بزرگ‌ترین سازه خشتی جهان قبل از زلزله، در حال بازسازی.'),
]

HEALTH_SOURCES = ['https://salamatnews.com/rss']

FACTS = [
    '🐙 اختاپوس ۳ تا قلب داره و خونش آبیه!',
    '🍯 عسل هرگز فاسد نمیشه؛ عسل ۳۰۰۰ ساله هنوز قابل خوردنه!',
    '🌍 یه روز در سیاره زهره از یه سالش طولانی‌تره!',
    '🦈 کوسه‌ها ۴۰۰ میلیون ساله، قبل از دایناسورها وجود داشتن!',
    '🧠 مغز موقع خواب فعال‌تر از روزه؛ داره اطلاعات رو مرتب می‌کنه!',
    '🐘 فیل‌ها تنها حیوونایی هستن که نمی‌تونن بپرن!',
    '💧 فقط ۳ درصد از آب‌های زمین شیرینه!',
    '🌙 ماه هر سال ۳.۸ سانتی‌متر از زمین دورتر میشه!',
]
POETRY = [
    '🌙 من از نهایت شب حرف می‌زنم\nمن از نهایت تاریکی\nو از نهایت شب حرف می‌زنم\n— فروغ فرخزاد',
    '🌙 بوی باران، بوی سبزه، بوی خاک\nشاخه‌های شسته، باران‌خورده، پاک\n— سهراب سپهری',
    '🌙 زندگی خالی نیست\nمهربانی هست، سیب هست، ایمان هست\n— سهراب سپهری',
    '🌙 من و انکار تو و این صدای باران\nکه می‌شنودش کسی که نیست\n— احمد شاملو',
    '🌙 از صدای سخن عشق ندیدم خوش‌تر\nیادگاری که در این گنبد دوار بماند\n— حافظ',
    '🌸 بنی‌آدم اعضای یکدیگرند\nکه در آفرینش ز یک گوهرند\n— سعدی',
    '🌸 توانا بود هر که دانا بود\nز دانش دل پیر برنا بود\n— فردوسی',
]
RELIGIOUS = [
    '🕌 «إِنَّ مَعَ الْعُسْرِ يُسْرًا»\nهمانا با هر سختی، آسانی است.',
    '🕌 «وَمَن يَتَوَكَّلْ عَلَى اللَّهِ فَهُوَ حَسْبُهُ»\nهر که بر خدا توکل کند، او کفایتش می‌کند.',
    '🕌 امام علی (ع): «ارزش هر کس به نیکوکاری اوست.»',
    '🕌 پیامبر اکرم (ص): «لبخند تو در چهره برادرت، صدقه است.»',
]
SATIRE = [
    '🎭 قیمت مرغ انقدر رفته بالا که حالا مرغ‌ها فکر می‌کنن برن بورس!',
    '🎭 تورم انقدر تیزه که حتی بادکنک‌ها هم از ما جلو می‌زنن!',
    '🎭 حقوقم انقدر کمه که حتی خودم هم نمی‌تونم استخدامش کنم!',
    '🎭 دلار انقدر رفته بالا که حالا داره به ما نگاه می‌کنه و می‌خنده!',
]
ENERGY = [
    '💪 زندگی مثل دوچرخه‌سواریه؛ برای حفظ تعادل باید حرکت کنی!',
    '🌟 هر طلوع خورشید یه فرصت جدیده؛ ازش استفاده کن!',
    '⭐ رویاهات تاریخ انقضا ندارن؛ یه نفس عمیق بکش و دوباره شروع کن!',
    '🌈 بعد از هر طوفانی، رنگین‌کمان میاد؛ صبور باش!',
]
HUMOR = [
    '😂 رفتم داروخانه گفتم یه چیز خوب برای سرماخوردگی بدید، گفت ۲۰۰ تومن! گفتم باشه، خودم خوب میشم!',
    '😂 دوستم گفت پول خوشبختی نمی‌آره، گفتم باشه پولت رو بده من تحمل می‌کنم!',
    '😂 مامانم گفت چرا لاغر شدی؟ گفتم مامان قیمت مرغ رو دیدی؟!',
    '😂 تنها ورزشی که استادم، ورزشِ از زیر کار در رفتنه!',
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
    return None

def get_sports(idx):
    items = rss_titles('https://www.varzesh3.com/rss')
    if items: return f'⚽ {items[idx % len(items)]}\n\n#ورزشی' + PROMO
    return None

def get_health(idx):
    for url in ['https://salamatnews.com/rss', 'https://www.salamat.ir/rss']:
        items = rss_titles(url)
        if items: return f'💊 {items[idx % len(items)]}\n\n#سلامتی' + PROMO
    return None

def get_mobile_trick(idx):
    items = rss_titles('https://www.zoomit.ir/feed')
    items = [t for t in items if any(k in t for k in ['ترفند','آموزش','چگونه','نکته','بررسی'])]
    if items: return f'📱 {items[idx % len(items)]}\n\n#ترفند_موبایل' + PROMO
    return None

def get_crypto():
    try:
        r = requests.get('https://api.coingecko.com/api/v3/simple/price',
            params={'ids':'bitcoin,ethereum,tron','vs_currencies':'usd','include_24hr_change':'true'},
            headers=UA, timeout=15)
        data = r.json()
        lines = ['💹 قیمت لحظه‌ای ارز دیجیتال:', '']
        names = {'bitcoin':'بیت‌کوین (BTC)','ethereum':'اتریوم (ETH)','tron':'ترون (TRX)'}
        for k, v in data.items():
            price = v.get('usd', 0)
            change = v.get('usd_24h_change', 0)
            emoji = '🟢' if change >= 0 else '🔴'
            lines.append(f'{emoji} {names.get(k,k)}: ${price:,.0f} ({change:+.1f}%)')
        return '\n'.join(lines) + '\n\n#کریپتو #ارزدیجیتال' + PROMO
    except:
        return None

def get_horoscope():
    from datetime import datetime
    slot = int(time.time() // 86400)
    signs = list(HOROSCOPES.keys())
    sign = signs[slot % len(signs)]
    return f'**فال امروز - {sign}**\n\n{HOROSCOPES[sign]}\n\n#فال #طالع_بینی' + PROMO

def get_landmark(idx):
    try:
        fa_name, en_query, fa_desc = LANDMARKS[idx % len(LANDMARKS)]
        r = requests.get('https://api.pexels.com/v1/search',
            headers={'Authorization': PEXELS_KEY},
            params={'query': en_query, 'per_page': 5, 'orientation': 'landscape'}, timeout=15)
        photos = r.json().get('photos', [])
        if photos:
            p = photos[0]
            caption = f'🌍 **{fa_name}**\n\n{fa_desc}\n\n📸 عکاس: {p.get("photographer","")}\n\n#گردشگری #ایرانگردی' + PROMO
            return p['src']['large'], caption
    except:
        pass
    return None, None

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

def send(msg, photo=None, parse_mode='Markdown'):
    try:
        if photo:
            url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto'
            r = requests.post(url, json={'chat_id': CHANNEL_ID, 'photo': photo, 'caption': msg, 'parse_mode': parse_mode}, timeout=20)
        else:
            url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
            r = requests.post(url, json={'chat_id': CHANNEL_ID, 'text': msg, 'parse_mode': parse_mode}, timeout=20)
        print('Send:', r.status_code, r.json().get('ok'))
    except Exception as e:
        print('Send error:', e)

def send_poll():
    try:
        polls = [
            ('امروز حالت چطوره؟', ['عالی 😄','خوب 🙂','معمولی 😐','ناراحتم 😔']),
            ('کدوم محتوا رو بیشتر دوست داری؟', ['اخبار','طنز','قیمت طلا','شعر','فال']),
            ('برنامه تعطیلات بعدیت چیه؟', ['سفر','خونه استراحت','کار','مهمونی']),
            ('صبحانه مورد علاقه‌ت؟', ['نیمرو','نون و پنیر','صبحانه انگلیسی','هیچی']),
            ('بهترین اختراع بشر؟', ['اینترنت','گوشی','برق','چرخ']),
            ('اگه یه ابرقدرت داشتی؟', ['پرواز','تله‌پورت','نامرئی شدن','خواندن ذهن']),
            ('فصل مورد علاقه‌ت؟', ['بهار','تابستون','پاییز','زمستون']),
            ('کتاب یا فیلم؟', ['کتاب','فیلم','هر دو','هیچکدوم']),
        ]
        slot = int(time.time() // 3600)
        q, opts = polls[slot % len(polls)]
        url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendPoll'
        r = requests.post(url, json={
            'chat_id': CHANNEL_ID,
            'question': q + '\n\n📢 @shegftanekhabar',
            'options': opts,
            'is_anonymous': False,
        }, timeout=20)
        print('Poll:', r.status_code)
    except Exception as e:
        print('Poll error:', e)

def post(ctype, idx):
    print('Posting:', ctype)
    try:
        if ctype == 'news':
            t = get_news(idx)
            if t: send(t)
        elif ctype == 'gold':
            t = get_gold()
            if t: send(t)
        elif ctype == 'crypto':
            t = get_crypto()
            if t: send(t)
        elif ctype == 'tech':
            t = get_tech(idx)
            if t: send(t)
        elif ctype == 'sports':
            t = get_sports(idx)
            if t: send(t)
        elif ctype == 'health':
            t = get_health(idx)
            if t: send(t)
        elif ctype == 'mobile_trick':
            t = get_mobile_trick(idx)
            if t: send(t)
        elif ctype == 'world':
            t = get_world(idx)
            if t: send(t)
        elif ctype == 'fact': send(get_fact(idx))
        elif ctype == 'humor': send(get_joke(idx))
        elif ctype == 'poetry': send(POETRY[idx % len(POETRY)] + '\n\n#شعر' + PROMO)
        elif ctype == 'religious': send(RELIGIOUS[idx % len(RELIGIOUS)] + '\n\n#مذهبی' + PROMO)
        elif ctype == 'satire': send(SATIRE[idx % len(SATIRE)] + '\n\n#طنز_اجتماعی' + PROMO)
        elif ctype == 'energy': send(ENERGY[idx % len(ENERGY)] + '\n\n#انرژی_مثبت' + PROMO)
        elif ctype == 'horoscope': send(get_horoscope())
        elif ctype == 'landmark':
            photo, cap = get_landmark(idx)
            if photo: send(cap, photo)
            else: send(ENERGY[idx % len(ENERGY)] + '\n\n#انرژی_مثبت' + PROMO)
        elif ctype == 'wallpaper':
            photo, cap = get_wallpaper(idx)
            if photo: send(cap, photo)
            else: send(FACTS[idx % len(FACTS)] + '\n\n#دانستنی' + PROMO)
        elif ctype == 'poll':
            send_poll()
    except Exception as e:
        print(f'Post error for {ctype}:', e)

def main():
    if not (BOT_TOKEN and CHANNEL_ID and PEXELS_KEY):
        print('Missing credentials')
        return
    slot = int(time.time() // 1800)
    hour = datetime.now().hour
    if 6 <= hour < 12:
        base = ['energy','news','gold','crypto','tech','sports','world','fact','landmark','poll']
    elif 12 <= hour < 18:
        base = ['gold','crypto','news','horoscope','humor','world','health','mobile_trick','tech','sports','fact','poll']
    else:
        base = ['poetry','religious','satire','landmark','world','energy','humor','fact','crypto','poll']
    off = slot % len(base)
    for i in range(6):
        ctype = base[(off + i) % len(base)]
        idx = int(time.time() // 300)
        post(ctype, idx)
        if i < 5:
            time.sleep(300)

if __name__ == '__main__':
    main()
