import requests, os, re, time, html as htmllib
from datetime import datetime

BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHANNEL_ID = os.environ.get('CHANNEL_ID')
PEXELS_KEY = os.environ.get('PEXELS_KEY')
PROMO = '\n\n📢 @shegftanekhabar'
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

# لیست سیاه - کلمات نامناسب فارسی و انگلیسی
BLACKLIST_FA = [
    'سکس', 'سکسی', 'عریان', 'برهنه', 'پورن', 'مست', 'الکل', 'مواد مخدر',
    'تریاک', 'هروئین', 'شیشه', 'گل', 'عربده', 'فحش', 'لعنتی', 'گوه', 'کیری',
    'کون', 'ممه', 'سینه', 'باسن', 'شهوت', 'ارگاسم', 'جنسی', 'همجنس', 'لزبین',
    'کس', 'کیر', 'تخمی', 'حروم', 'حرامزاده', 'پدرسگ', 'مادرسگ', 'جنده',
    'فاحشه', 'خفه', 'بکیر', 'تخم', 'خارشهری', 'عوضی', 'آشغال', 'پتیاره',
    'مردار', 'لاشی', 'کثافت', 'کث', 'حرومزاده', 'بی‌شرف', 'بی‌پدر',
    'کافر', 'مرتد', 'اسرائیل', 'صهیونیست', 'یهودی', 'بمب', 'ترور',
    'انفجار', 'خون', 'قتل', 'کشتار', 'جنگ', 'شهید', 'شهادت',
]
BLACKLIST_EN = [
    'sex', 'sexy', 'porn', 'nude', 'naked', 'xxx', 'fuck', 'shit', 'ass',
    'bitch', 'dick', 'cock', 'pussy', 'boob', 'tits', 'weed', 'drug',
    'alcohol', 'beer', 'wine', 'vodka', 'kill', 'murder', 'terror',
    'bomb', 'gun', 'weapon', 'blood', 'death', 'dead', 'suicide',
    'nazi', 'hitler', 'rape', 'violent', 'violence', 'war', 'israel',
    'jewish', 'zionist', 'arab', 'muslim', 'islam', 'christian',
]

# ساب‌ردیت‌های امن (فقط محتوای تمیز)
SAFE_SUBS = {
    'facts': ['todayilearned', 'AskScience', 'space', 'science'],
    'jokes': ['Jokes', 'dadjokes', 'cleanjokes'],
    'world': ['worldnews', 'technology'],
}

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
    ('تخت جمشید', 'Persepolis', 'شکوه ایران باستان، پایتخت تشریفاتی هخامنشیان.'),
    ('میدان نقش جهان', 'Isfahan', 'قلب تپنده اصفهان، یکی از بزرگ‌ترین میدان‌های جهان.'),
    ('برج آزادی', 'Tehran tower', 'نماد پایتخت ایران.'),
    ('باغ ارم شیراز', 'Shiraz garden', 'یکی از زیباترین باغ‌های ایرانی.'),
    ('پل خواجو', 'Isfahan bridge', 'شاهکار معماری صفوی در اصفهان.'),
    ('مسجد نصیرالملک', 'Pink Mosque', 'مسجد صورتی شیراز.'),
    ('کاخ گلستان', 'Golestan Palace', 'میراث جهانی یونسکو در تهران.'),
    ('بازار تبریز', 'Tabriz bazaar', 'بزرگ‌ترین بازار سرپوشیده جهان.'),
    ('کویر لوت', 'Lut desert', 'گرم‌ترین نقطه زمین!'),
    ('جنگل‌های هیرکانی', 'Hyrcanian forests', 'جنگل‌های باستانی شمال ایران.'),
    ('ماسوله', 'Masuleh', 'روستای پلکانی گیلان.'),
]

POETRY = [
    '🌙 من از نهایت شب حرف می‌زنم\n— فروغ فرخزاد',
    '🌙 بوی باران، بوی سبزه، بوی خاک\n— سهراب سپهری',
    '🌙 زندگی خالی نیست\nمهربانی هست، سیب هست، ایمان هست\n— سهراب سپهری',
    '🌸 بنی‌آدم اعضای یکدیگرند\n— سعدی',
    '🌸 توانا بود هر که دانا بود\n— فردوسی',
]
RELIGIOUS = [
    '🕌 «إِنَّ مَعَ الْعُسْرِ يُسْرًا»\nهمانا با هر سختی، آسانی است.',
    '🕌 امام علی (ع): «ارزش هر کس به نیکوکاری اوست.»',
    '🕌 پیامبر اکرم (ص): «لبخند تو در چهره برادرت، صدقه است.»',
]
SATIRE = [
    '🎭 قیمت مرغ انقدر رفته بالا که حالا مرغ‌ها فکر می‌کنن برن بورس!',
    '🎭 تورم انقدر تیزه که حتی بادکنک‌ها هم از ما جلو می‌زنن!',
]
ENERGY = [
    '💪 زندگی مثل دوچرخه‌سواریه؛ برای حفظ تعادل باید حرکت کنی!',
    '🌟 هر طلوع خورشید یه فرصت جدیده!',
    '🌈 بعد از هر طوفانی، رنگین‌کمان میاد!',
]
HUMOR_SAFE = [
    '😂 رفتم داروخانه گفتم یه چیز خوب برای سرماخوردگی بدید، گفت ۲۰۰ تومن! گفتم باشه، خودم خوب میشم!',
    '😂 دوستم گفت پول خوشبختی نمی‌آره، گفتم باشه پولت رو بده من تحمل می‌کنم!',
    '😂 مامانم گفت چرا لاغر شدی؟ گفتم مامان قیمت مرغ رو دیدی؟!',
]
FACTS_SAFE = [
    '🐙 اختاپوس ۳ تا قلب داره و خونش آبیه!',
    '🍯 عسل هرگز فاسد نمیشه!',
    '🌍 یه روز در سیاره زهره از یه سالش طولانی‌تره!',
]
WALL_TAGS = [('nature','طبیعت'),('mountain','کوه'),('ocean','دریا'),('forest','جنگل'),('flower','گل')]

def is_safe(text):
    if not text: return False
    text_lower = text.lower()
    for word in BLACKLIST_FA:
        if word in text: return False
    for word in BLACKLIST_EN:
        if word in text_lower: return False
    return True

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
                if t and is_safe(t): out.append(t)
        return out
    except:
        return []

def reddit_titles(category, n=10):
    all_titles = []
    for sub in SAFE_SUBS.get(category, ['todayilearned']):
        try:
            r = requests.get(f'https://www.reddit.com/r/{sub}/hot.json?limit={n}',
                           headers=UA, timeout=15)
            for c in r.json()['data']['children']:
                title = c['data']['title']
                # بررسی امنیت و اینکه NSFW نباشه
                if not c['data'].get('over_18', False) and is_safe(title):
                    all_titles.append(title)
        except:
            pass
    return all_titles

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
    for url in ['https://salamatnews.com/rss']:
        items = rss_titles(url)
        if items: return f'💊 {items[idx % len(items)]}\n\n#سلامتی' + PROMO
    return None

def get_crypto():
    try:
        r = requests.get('https://api.coingecko.com/api/v3/simple/price',
            params={'ids':'bitcoin,ethereum,tron','vs_currencies':'usd','include_24hr_change':'true'},
            headers=UA, timeout=15)
        data = r.json()
        lines = ['💹 قیمت لحظه‌ای ارز دیجیتال:', '']
        names = {'bitcoin':'بیت‌کوین','ethereum':'اتریوم','tron':'ترون'}
        for k, v in data.items():
            price = v.get('usd', 0)
            change = v.get('usd_24h_change', 0)
            emoji = '🟢' if change >= 0 else '🔴'
            lines.append(f'{emoji} {names.get(k,k)}: ${price:,.0f} ({change:+.1f}%)')
        return '\n'.join(lines) + '\n\n#کریپتو' + PROMO
    except:
        return None

def get_horoscope():
    slot = int(time.time() // 86400)
    signs = list(HOROSCOPES.keys())
    sign = signs[slot % len(signs)]
    return f'**فال امروز - {sign}**\n\n{HOROSCOPES[sign]}\n\n#فال' + PROMO

def get_landmark(idx):
    try:
        fa_name, en_query, fa_desc = LANDMARKS[idx % len(LANDMARKS)]
        r = requests.get('https://api.pexels.com/v1/search',
            headers={'Authorization': PEXELS_KEY},
            params={'query': en_query, 'per_page': 5}, timeout=15)
        photos = r.json().get('photos', [])
        if photos:
            p = photos[0]
            caption = f'🌍 **{fa_name}**\n\n{fa_desc}\n\n#گردشگری' + PROMO
            return p['src']['large'], caption
    except:
        pass
    return None, None

def get_world(idx):
    items = [translate(t) for t in reddit_titles('world')]
    items = [t for t in items if is_safe(t)]
    if items:
        return f'🌍 {items[idx % len(items)]}\n\n#جهان' + PROMO
    return None

def get_fact(idx):
    items = [translate(t.replace('TIL ','')) for t in reddit_titles('facts')]
    items = [t for t in items if is_safe(t)]
    if items:
        return f'🤔 آیا می‌دانستی؟ {items[idx % len(items)]}\n\n#دانستنی' + PROMO
    return f'🤔 {FACTS_SAFE[idx % len(FACTS_SAFE)]}\n\n#دانستنی' + PROMO

def get_joke(idx):
    items = [translate(t) for t in reddit_titles('jokes')]
    items = [t for t in items if is_safe(t)]
    if items:
        return f'😂 {items[idx % len(items)]}\n\n#طنز' + PROMO
    return f'😂 {HUMOR_SAFE[idx % len(HUMOR_SAFE)]}\n\n#طنز' + PROMO

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
            return '\n'.join(lines) + '\n\n#طلا #سکه' + PROMO
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
            return p['src']['large'], f'🖼 والپیپر {fa}\n\n#والپیپر' + PROMO
    except:
        pass
    return None, None

def send(msg, photo=None):
    try:
        if photo:
            url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto'
            r = requests.post(url, json={'chat_id': CHANNEL_ID, 'photo': photo, 'caption': msg, 'parse_mode': 'Markdown'}, timeout=20)
        else:
            url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
            r = requests.post(url, json={'chat_id': CHANNEL_ID, 'text': msg, 'parse_mode': 'Markdown'}, timeout=20)
        print('Send:', r.status_code, r.json().get('ok'))
    except Exception as e:
        print('Send error:', e)

def send_poll():
    try:
        polls = [
            ('امروز حالت چطوره؟', ['عالی 😄','خوب 🙂','معمولی 😐','ناراحتم 😔']),
            ('کدوم محتوا رو بیشتر دوست داری؟', ['اخبار','طنز','قیمت طلا','شعر','فال']),
            ('برنامه تعطیلات بعدیت چیه؟', ['سفر','خونه','کار','مهمونی']),
            ('فصل مورد علاقه‌ت؟', ['بهار','تابستون','پاییز','زمستون']),
        ]
        slot = int(time.time() // 3600)
        q, opts = polls[slot % len(polls)]
        url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendPoll'
        r = requests.post(url, json={
            'chat_id': CHANNEL_ID,
            'question': q,
            'options': opts,
            'is_anonymous': False,
        }, timeout=20)
        print('Poll:', r.status_code)
    except:
        pass

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
            else: send(FACTS_SAFE[idx % len(FACTS_SAFE)] + '\n\n#دانستنی' + PROMO)
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
        base = ['gold','crypto','news','horoscope','humor','world','health','tech','sports','fact','poll']
    else:
        base = ['poetry','religious','satire','landmark','world','energy','humor','fact','crypto','poll']
    off = slot % len(base)
    for i in range(4):
        ctype = base[(off + i) % len(base)]
        idx = int(time.time() // 420)
        post(ctype, idx)
        if i < 3:
            time.sleep(420)

if __name__ == '__main__':
    main()
