import requests
import os
import re
import time
import html as htmllib

BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHANNEL_ID = os.environ.get('CHANNEL_ID')
PEXELS_KEY = os.environ.get('PEXELS_KEY')
PROMO = '\n\n📢 @shegftanekhabar'

FACTS = [
    '🐙 آیا می‌دانستی اختاپوس ۳ تا قلب داره و خونش آبی رنگه؟',
    '🍯 آیا می‌دانستی عسل تنها ماده غذاییه که هرگز فاسد نمیشه؟',
    '🌍 آیا می‌دانستی یه روز در سیاره زهره از یه سالش طولانی‌تره؟',
    '🦈 آیا می‌دانستی کوسه‌ها قبل از دایناسورها روی زمین بودن؟',
    '🧠 آیا می‌دانستی مغز انسان موقع شب فعال‌تر از روزه؟',
    '🐘 آیا می‌دانستی فیل‌ها تنها حیوونایی هستن که نمی‌تونن بپرن؟',
    '💧 آیا می‌دانستی فقط ۳ درصد از آب‌های زمین شیرینه؟',
    '🌙 آیا می‌دانستی ماه هر سال ۳.۸ سانتی‌متر از زمین دورتر میشه؟',
]

HUMOR = [
    '😂 به دکتر گفتم: «دکتر، همه منو نادیده می‌گیرن!» دکتر رو کرد به منشیش گفت: «نفر بعدی لطفاً!»',
    '😂 دوستم گفت: «پول خوشبختی نمی‌آره.» گفتم: «باشه، پولت رو بده من، خودم تحملش می‌کنم!»',
    '😂 تصمیم گرفتم هر روز صبح زود بیدار شم... از هفته دیگه شروع می‌کنم!',
    '😂 مامانم زنگ زد گفت: «چرا انقدر لاغر شدی؟» گفتم: «مامان، قیمت مرغ رو دیدی؟!»',
    '😂 تنها چیزی که تو این اوضاع ثابته، بی‌پولی منه!',
    '😂 وزنم رو پرسیدم، ترازو گفت: «لطفاً یکی یکی بیایید!»',
    '😂 گوشیم انقدر حافظه‌ش پره که حتی فکر کردن رو هم باید اول حذف کنم!',
    '😂 رفتم مصاحبه کار، گفتن سابقه ۱۰ ساله می‌خوایم، با حقوق ۳ میلیون! گفتم: «باشه، از دوران باستان براتون کار کردم!»',
]

SATIRE = [
    '🎭 قیمت‌ها انقدر سریع عوض میشن که فروشنده‌ها هم جا می‌مونن؛ دیروز گرون بود، امروز گرون‌تر!',
    '🎭 تورم انقدر تیزه که سرعت اینترنت پیشش لاک‌پشت به نظر میاد!',
    '🎭 برنامه پس‌انداز من و دلار: هر کی زودتر جا زد، اون یکی می‌بره!',
    '🎭 حقوق اول ماه میاد، وسط ماه نگاهش می‌کنیم، آخر ماه یادش می‌کنیم!',
    '🎭 سبد خریدمون انقدر کوچیک شده که حالا اسمش رو گذاشتیم «سبد قلم»!',
    '🎭 ترافیک و قیمت‌ها، دو چیزیه که هیچ‌وقت کم نمی‌شن؛ فقط زیاد می‌شن!',
]

RELIGIOUS = [
    '🕌 «بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ»\nبه نام خدای بخشندهٔ مهربان',
    '🕌 «إِنَّ مَعَ الْعُسْرِ يُسْرًا»\nهمانا با هر سختی، آسانی است.',
    '🕌 «وَمَن يَتَوَكَّلْ عَلَى اللَّهِ فَهُوَ حَسْبُهُ»\nهر که بر خدا توکل کند، او کفایتش می‌کند.',
    '🕌 امام علی (ع): «ارزش هر کس به نیکوکاری اوست.»',
    '🕌 پیامبر اکرم (ص): «لبخند تو در چهره برادرت، صدقه است.»',
    '🕌 «الصَّبْرُ مِفتاحُ الفَرَجِ»\nصبر، کلید هر گشایشی است.',
]

ENERGY = [
    '🌸 بنی‌آدم اعضای یکدیگرند\nکه در آفرینش ز یک گوهرند\n\n— سعدی',
    '🌸 درخت دوستی بنشان که کام دل به بار آرد\nنهال دشمنی برکن که رنج بی‌شمار آرد\n\n— حافظ',
    '🌸 بشنو این نی چون شکایت می‌کند\nاز جدایی‌ها حکایت می‌کند\n\n— مولانا',
    '🌸 توانا بود هر که دانا بود\nز دانش دل پیر برنا بود\n\n— فردوسی',
    '🌸 زندگی آب‌تنی کردن در حوضچه «اکنون» است\n\n— سهراب سپهری',
    '🌸 میازار موری که دانه‌کش است\nکه جان دارد و جان شیرین خوش است\n\n— سعدی',
]

WALL_TAGS = [
    ('nature', 'طبیعت'),
    ('mountain', 'کوه'),
    ('ocean', 'دریا'),
    ('forest', 'جنگل'),
    ('flower', 'گل'),
]


def clean_text(t):
    t = re.sub(r'<!\[CDATA\[(.*?)\]\]>', r'\1', t)
    t = re.sub(r'<[^>]+>', '', t)
    t = htmllib.unescape(t)
    return t.strip()


def get_rss_items(url, max_items=10):
    try:
        r = requests.get(url, timeout=15)
        text = r.text
        items = re.findall(r'<item>(.*?)</item>', text, re.DOTALL)
        result = []
        for it in items[:max_items]:
            title = re.search(r'<title[^>]*>(.*?)</title>', it, re.DOTALL)
            if title:
                t = clean_text(title.group(1))
                if t:
                    result.append(t)
        return result
    except Exception as e:
        print('RSS error:', e)
        return []


def get_news(idx):
    sources = [
        'https://www.isna.ir/rss',
        'https://www.mehrnews.com/rss',
    ]
    for url in sources:
        items = get_rss_items(url)
        if items:
            t = items[idx % len(items)]
            return f'📰 {t}' + PROMO
    return None


def get_gold():
    try:
        r = requests.get('https://www.tgju.org/',
                         headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'},
                         timeout=20)
        t = r.text

        def after(label):
            i = t.find(label)
            if i == -1:
                return None
            m = re.search(r'([\d][\d,]{4,})', t[i + len(label):i + len(label) + 600])
            return m.group(1) if m else None

        coin = after('سکه امامی') or after('سکه')
        gold18 = after('طلا ۱۸') or after('طلا 18')
        dollar = after('دلار')

        if coin or dollar:
            lines = ['🪙 قیمت لحظه‌ای بازار:', '']
            if coin:
                lines.append(f'💰 سکه امامی: {coin} تومان')
            if gold18:
                lines.append(f'✨ طلای ۱۸ عیار: {gold18} تومان')
            if dollar:
                lines.append(f'💵 دلار: {dollar} تومان')
            return '\n'.join(lines) + '\n\n#طلا #سکه #ارز' + PROMO
    except Exception as e:
        print('Gold error:', e)
    return None


def get_wallpaper(idx):
    try:
        en, fa = WALL_TAGS[idx % len(WALL_TAGS)]
        r = requests.get(
            'https://api.pexels.com/v1/search',
            headers={'Authorization': PEXELS_KEY},
            params={'query': en, 'per_page': 15, 'orientation': 'portrait'},
            timeout=15
        )
        photos = r.json().get('photos', [])
        if photos:
            p = photos[idx % len(photos)]
            caption = f'🖼 والپیپر {fa}\n\n📸 عکاس: {p.get("photographer", "")}' + '\n\n#والپیپر' + PROMO
            return p['src']['large'], caption
    except Exception as e:
        print('Pexels error:', e)
    return None, None


def send_text(text):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    r = requests.post(url, json={'chat_id': CHANNEL_ID, 'text': text}, timeout=15)
    print('Send:', r.status_code, r.json().get('ok'))


def send_photo(photo_url, caption):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto'
    r = requests.post(url, json={'chat_id': CHANNEL_ID, 'photo': photo_url, 'caption': caption}, timeout=15)
    print('Send:', r.status_code, r.json().get('ok'))


def main():
    if not (BOT_TOKEN and CHANNEL_ID and PEXELS_KEY):
        print('Missing credentials')
        return

    slot = int(time.time() // 600)
    types = ['news', 'gold', 'humor', 'wallpaper', 'religious', 'fact', 'satire', 'energy']
    ctype = types[slot % len(types)]
    idx = slot // len(types)

    print('Posting:', ctype)

    if ctype == 'news':
        text = get_news(idx)
        if text:
            send_text(text)
    elif ctype == 'gold':
        text = get_gold()
        if text:
            send_text(text)
    elif ctype == 'humor':
        send_text('😂 ' + HUMOR[idx % len(HUMOR)].replace('😂 ', '') + '\n\n#طنز' + PROMO)
    elif ctype == 'satire':
        send_text(SATIRE[idx % len(SATIRE)] + '\n\n#طنز_اجتماعی' + PROMO)
    elif ctype == 'religious':
        send_text(RELIGIOUS[idx % len(RELIGIOUS)] + '\n\n#مذهبی' + PROMO)
    elif ctype == 'fact':
        send_text(FACTS[idx % len(FACTS)] + '\n\n#دانستنی' + PROMO)
    elif ctype == 'energy':
        send_text(ENERGY[idx % len(ENERGY)] + '\n\n#شعر' + PROMO)
    elif ctype == 'wallpaper':
        photo, caption = get_wallpaper(idx)
        if photo:
            send_photo(photo, caption)
        else:
            send_text(FACTS[idx % len(FACTS)] + '\n\n#دانستنی' + PROMO)


if __name__ == '__main__':
    for _ in range(3):
        main()
        if _ < 2:
            time.sleep(600)
