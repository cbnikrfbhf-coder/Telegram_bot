import requests, os, re, time, html as htmllib

BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHANNEL_ID = os.environ.get('CHANNEL_ID')
PEXELS_KEY = os.environ.get('PEXELS_KEY')
PROMO = '\n\n📢 @shegftanekhabar'

NEWS_SOURCES = ['https://www.isna.ir/rss', 'https://www.mehrnews.com/rss']

FACTS = [
    '🐙 آیا می‌دانستی اختاپوس ۳ تا قلب داره و خونش آبیه؟',
    '🍯 عسل تنها ماده غذاییه که هرگز فاسد نمیشه',
    '🌍 یه روز در سیاره زهره از یه سالش طولانی‌تره',
    '🦈 کوسه‌ها قبل از دایناسورها روی زمین بودن',
    '🧠 مغز انسان موقع شب فعال‌تر از روزه',
    '🐘 فیل‌ها تنها حیوونایی هستن که نمی‌تونن بپرن',
    '💧 فقط ۳ درصد از آب‌های زمین شیرینه',
    '🌙 ماه هر سال ۳.۸ سانتی‌متر از زمین دورتر میشه',
]
HUMOR = [
    '😂 به دکتر گفتم همه منو نادیده می‌گیرن! دکتر رو کرد به منشیش گفت نفر بعدی لطفاً!',
    '😂 دوستم گفت پول خوشبختی نمی‌آره، گفتم باشه پولت رو بده من خودم تحملش می‌کنم!',
    '😂 تصمیم گرفتم هر روز صبح زود بیدار شم... از هفته دیگه شروع می‌کنم!',
    '😂 مامانم زنگ زد گفت چرا انقدر لاغر شدی؟ گفتم مامان قیمت مرغ رو دیدی؟!',
    '😂 تنها چیزی که تو این اوضاع ثابته، بی‌پولی منه!',
    '😂 وزنم رو پرسیدم، ترازو گفت لطفاً یکی یکی بیایید!',
]
SATIRE = [
    '🎭 قیمت‌ها انقدر سریع عوض میشن که فروشنده‌ها هم جا می‌مونن؛ دیروز گرون بود، امروز گرون‌تر!',
    '🎭 تورم انقدر تیزه که سرعت اینترنت پیشش لاک‌پشت به نظر میاد!',
    '🎭 برنامه پس‌انداز من و دلار: هر کی زودتر جا زد، اون یکی می‌بره!',
    '🎭 حقوق اول ماه میاد، وسط ماه نگاهش می‌کنیم، آخر ماه یادش می‌کنیم!',
    '🎭 سبد خریدمون انقدر کوچیک شده که حالا اسمش رو گذاشتیم سبد قلم!',
]
RELIGIOUS = [
    '🕌 «إِنَّ مَعَ الْعُسْرِ يُسْرًا»\nهمانا با هر سختی، آسانی است.',
    '🕌 «وَمَن يَتَوَكَّلْ عَلَى اللَّهِ فَهُوَ حَسْبُهُ»\nهر که بر خدا توکل کند، او کفایتش می‌کند.',
    '🕌 امام علی (ع): «ارزش هر کس به نیکوکاری اوست.»',
    '🕌 پیامبر اکرم (ص): «لبخند تو در چهره برادرت، صدقه است.»',
    '🕌 «الصَّبْرُ مِفتاحُ الفَرَجِ»\nصبر، کلید هر گشایشی است.',
]
ENERGY = [
    '🌸 بنی‌آدم اعضای یکدیگرند\nکه در آفرینش ز یک گوهرند\n— سعدی',
    '🌸 درخت دوستی بنشان که کام دل به بار آرد\nنهال دشمنی برکن که رنج بی‌شمار آرد\n— حافظ',
    '🌸 بشنو این نی چون شکایت می‌کند\nاز جدایی‌ها حکایت می‌کند\n— مولانا',
    '🌸 توانا بود هر که دانا بود\nز دانش دل پیر برنا بود\n— فردوسی',
    '🌸 زندگی آب‌تنی کردن در حوضچه اکنون است\n— سهراب سپهری',
]
WALL_TAGS = [('nature','طبیعت'),('mountain','کوه'),('ocean','دریا'),('forest','جنگل'),('flower','گل')]

def clean(t):
    t = re.sub(r'<!\[CDATA\[(.*?)\]\]>', r'\1', t)
    t = re.sub(r'<[^>]+>', '', t)
    return htmllib.unescape(t).strip()

def get_rss(url):
    try:
        r = requests.get(url, timeout=15)
        items = re.findall(r'<item>(.*?)</item>', r.text, re.DOTALL)
        out = []
        for it in items[:15]:
            m = re.search(r'<title[^>]*>(.*?)</title>', it, re.DOTALL)
            if m:
                out.append(clean(m.group(1)))
        return out
    except: return []

def get_news(idx):
    for url in NEWS_SOURCES:
        items = get_rss(url)
        if items: return f'📰 {items[idx % len(items)]}' + PROMO
    return None

def get_gold():
    try:
        r = requests.get('https://www.tgju.org/', headers={'User-Agent':'Mozilla/5.0'}, timeout=20)
        def after(label):
            i = r.text.find(label)
            if i==-1: return None
            m = re.search(r'([\d][\d,]{4,})', r.text[i+len(label):i+len(label)+600])
            return m.group(1) if m else None
        coin = after('سکه امامی') or after('سکه')
        gold18 = after('طلا ۱۸') or after('طلا 18')
        dollar = after('دلار')
        if coin or dollar:
            lines = ['🪙 قیمت لحظه‌ای بازار:','']
            if coin: lines.append(f'💰 سکه امامی: {coin} تومان')
            if gold18: lines.append(f'✨ طلای ۱۸ عیار: {gold18} تومان')
            if dollar: lines.append(f'💵 دلار: {dollar} تومان')
            return '\n'.join(lines) + '\n\n#طلا #سکه #ارز' + PROMO
    except: pass
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
            return p['src']['large'], f'🖼 والپیپر {fa}\n\n📸 عکاس: {p.get("photographer","")}\n#والپیپر' + PROMO
    except: pass
    return None, None

def send(msg, photo=None):
    if photo:
        url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto'
        return requests.post(url, json={'chat_id':CHANNEL_ID,'photo':photo,'caption':msg}, timeout=15).json()
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    return requests.post(url, json={'chat_id':CHANNEL_ID,'text':msg}, timeout=15).json()

def main():
    if not (BOT_TOKEN and CHANNEL_ID and PEXELS_KEY): return
    slot = int(time.time() // 1800)
    types = ['news','gold','humor','wallpaper','religious','fact','satire','energy']
    ctype = types[slot % len(types)]
    idx = slot // len(types)
    print(f'Posting: {ctype}')
    if ctype == 'news':
        t = get_news(idx)
        if t: send(t)
    elif ctype == 'gold':
        t = get_gold()
        if t: send(t)
    elif ctype == 'humor': send(HUMOR[idx % len(HUMOR)] + '\n#طنز' + PROMO)
    elif ctype == 'satire': send(SATIRE[idx % len(SATIRE)] + '\n#طنز_اجتماعی' + PROMO)
    elif ctype == 'religious': send(RELIGIOUS[idx % len(RELIGIOUS)] + '\n#مذهبی' + PROMO)
    elif ctype == 'fact': send(FACTS[idx % len(FACTS)] + '\n#دانستنی' + PROMO)
    elif ctype == 'energy': send(ENERGY[idx % len(ENERGY)] + '\n#شعر' + PROMO)
    elif ctype == 'wallpaper':
        photo, cap = get_wallpaper(idx)
        if photo: send(cap, photo)
        else: send(FACTS[idx % len(FACTS)] + '\n#دانستنی' + PROMO)

if __name__ == '__main__':
    for i in range(3):
        main()
        if i < 2: time.sleep(600)
