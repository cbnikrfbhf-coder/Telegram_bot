import requests, os, re, time, html as htmllib, random
from datetime import datetime, timedelta, timezone

BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHANNEL_ID = os.environ.get('CHANNEL_ID')
PEXELS_KEY = os.environ.get('PEXELS_KEY')
CHANNEL_URL = 'https://t.me/shegftanekhabar'
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
TZ = timezone(timedelta(hours=3, minutes=30))
LINE = '━━━━━━━━━━━━━━━'

def fa_num(n):
    return str(n).translate(str.maketrans('0123456789', '۰۱۲۴۵۶۸۹'))

def tehran_now():
    return datetime.now(TZ)

def keyboard():
    return {'inline_keyboard': [[
        {'text': '📢 عضویت در کانال', 'url': CHANNEL_URL},
        {'text': '🔗 اشتراک‌گذاری', 'url': f'https://t.me/share/url?url={CHANNEL_URL}'}
    ]]}

BLACKLIST_FA = ['سکس','عریان','پورن','الکل','مواد مخدر','فحش','لعنتی','شهوت','جنسی','بمب','ترور','قتل','کشتار','حروم','کافر','مرتد']
BLACKLIST_EN = ['sex','porn','nude','fuck','shit','bitch','weed','drug','alcohol','kill','murder','terror','bomb','suicide','nazi','rape','war']

NEWS_SOURCES = [
    'https://www.isna.ir/rss','https://www.mehrnews.com/rss',
    'https://www.irna.ir/rss','https://www.tasnimnews.com/fa/rss',
    'https://www.farsnews.ir/rss','https://www.khabaronline.ir/rss',
]
SAFE_SUBS = {
    'facts': ['todayilearned','AskScience','space','science'],
    'jokes': ['Jokes','dadjokes','cleanjokes','funny'],
    'world': ['worldnews','technology','science'],
}
CRYPTO_IDS = 'bitcoin,ethereum,tron,the-sandbox,axie-infinity,gala,decentraland'
GAME_IDS = {'the-sandbox','axie-infinity','gala','decentraland'}
NAMES = {'bitcoin':'بیت‌کوین','ethereum':'اتریوم','tron':'ترون',
         'the-sandbox':'سندباکس 🎮','axie-infinity':'اکسی اینفینیتی 🎮',
         'gala':'گالا 🎮','decentraland':'دیسنترالند 🎮'}
IRAN_CITIES = [('تهران',35.68,51.38),('مشهد',36.26,59.61),('اصفهان',32.65,51.67),
               ('شیراز',29.59,52.58),('تبریز',38.09,46.29)]
PLACES = ['تخت_جمشید','میدان_نقش_جهان','برج_آزادی','باغ_ارم','پل_خواجو',
          'کاخ_گلستان','بازار_تبریز','کویر_لوت','ماسوله','جنگل‌های_هیرکانی']
WORDS = ['serendipity','ephemeral','resilient','eloquent','luminous','meticulous',
         'vibrant','profound','whimsical','tenacious','benevolent','gratitude',
         'courage','wisdom','harmony','adventure','curiosity','passion','creative','inspire']
WALL_TAGS = [('nature','طبیعت'),('mountain','کوه'),('ocean','دریا'),('forest','جنگل'),('flower','گل'),('sunset','غروب')]

def is_safe(text):
    if not text: return False
    tl = text.lower()
    for w in BLACKLIST_FA:
        if w in text: return False
    for w in BLACKLIST_EN:
        if w in tl: return False
    return True

def clean(t):
    t = re.sub(r'<!\[CDATA\[(.*?)\]\]>', r'\1', t)
    t = re.sub(r'<[^>]+>', '', t)
    return htmllib.unescape(t).strip()

def translate(text, sl='en', tl='fa'):
    try:
        r = requests.get('https://translate.googleapis.com/translate_a/single',
            params={'client':'gtx','sl':sl,'tl':tl,'dt':'t','q':text}, timeout=10)
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
    out = []
    for sub in SAFE_SUBS.get(category, ['todayilearned']):
        try:
            r = requests.get(f'https://www.reddit.com/r/{sub}/hot.json?limit={n}', headers=UA, timeout=15)
            for c in r.json()['data']['children']:
                t = c['data']['title']
                if not c['data'].get('over_18') and is_safe(t): out.append(t)
        except:
            pass
    return out

def send(msg, photo=None):
    try:
        if photo:
            url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto'
            r = requests.post(url, json={'chat_id':CHANNEL_ID,'photo':photo,'caption':msg,'parse_mode':'Markdown','reply_markup':keyboard()}, timeout=20)
        else:
            url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
            r = requests.post(url, json={'chat_id':CHANNEL_ID,'text':msg,'parse_mode':'Markdown','reply_markup':keyboard()}, timeout=20)
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
        r = requests.post(url, json={'chat_id':CHANNEL_ID,'question':q,'options':opts,'is_anonymous':False}, timeout=20)
        print('Poll:', r.status_code)
    except:
        pass

# ===== خبر (سبک خبری مدرن) =====
def get_news(idx):
    for url in NEWS_SOURCES:
        items = rss_titles(url)
        if items:
            now = tehran_now()
            return (f'⚡ **فوری** | ساعت {fa_num(now.strftime("%H:%M"))}\n\n'
                    f'📰 {items[idx % len(items)]}\n\n{LINE}\n'
                    f'🕐 به‌روزرسانی لحظه‌ای')
    return None

# ===== طلا (سبک مجله‌ای) =====
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
            now = tehran_now()
            lines = ['┏━━━━━━━━━━━━━━┓', '   💰 **گزارش بازار**', '┗━━━━━━━━━━━━━━┛', '']
            if coin: lines.append(f'💰 سکه امامی\n   {fa_num(coin)} تومان')
            if gold18: lines.append(f'✨ طلای ۱۸ عیار\n   {fa_num(gold18)} تومان')
            if dollar: lines.append(f'💵 دلار\n   {fa_num(dollar)} تومان')
            lines.append(f'\n{LINE}\n🕐 ساعت {fa_num(now.strftime("%H:%M"))} | 📊 بازار تهران')
            return '\n'.join(lines)
    except:
        pass
    return None

# ===== کریپتو (سبک مجله‌ای) =====
def get_crypto():
    try:
        r = requests.get('https://api.coingecko.com/api/v3/simple/price',
            params={'ids':CRYPTO_IDS,'vs_currencies':'usd','include_24hr_change':'true'},
            headers=UA, timeout=15)
        data = r.json()
        lines = ['┏━━━━━━━━━━━━━━┓', '   💹 **بازار کریپتو**', '┗━━━━━━━━━━━━━━┛', '']
        games = False
        for k, v in data.items():
            price = v.get('usd', 0)
            change = v.get('usd_24h_change', 0)
            emoji = '🟢' if change >= 0 else '🔴'
            if k in GAME_IDS and not games:
                lines.append('')
                lines.append('🎮 **توکن بازی‌های آنلاین:**')
                games = True
            fmt = '{:,.4f}' if price < 1 else '{:,.0f}'
            lines.append(f'{emoji} {NAMES.get(k,k)}: ${fmt.format(price)} ({change:+.1f}%)')
        return '\n'.join(lines) + '\n\n#کریپتو #بازی'
    except:
        return None

# ===== آب و هوا (سبک مجله‌ای) =====
def get_weather():
    try:
        codes = {0:'☀️',1:'🌤️',2:'⛅',3:'☁️',45:'🌫️',48:'🌫️',51:'🌦️',53:'🌧️',55:'🌧️',
                 61:'🌧️',63:'🌧️',65:'🌧️',71:'🌨️',73:'🌨️',75:'❄️',80:'🌦️',95:'⛈️',96:'⛈️'}
        lines = ['┏━━━━━━━━━━━━━━┓', '   🌤️ **هوای ایران**', '┗━━━━━━━━━━━━━━┛', '']
        for city, lat, lon in IRAN_CITIES:
            r = requests.get(f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true', timeout=10)
            w = r.json().get('current_weather', {})
            temp = w.get('temperature', '?')
            lines.append(f'📍 {city}: {fa_num(temp)}°C {codes.get(w.get("weathercode",0),"🌡️")}')
        return '\n'.join(lines) + f'\n\n{LINE}\n🕐 لحظه‌ای'
    except:
        return None

# ===== شعر از گنجور (سبک داستان‌گویی) =====
def get_poem_online(poet_only=None):
    try:
        poets = [('حافظ',32),('سعدی',11),('مولانا',20),('خیام',24)]
        if poet_only:
            name, pid = poet_only, 32
        else:
            name, pid = random.choice(poets)
        r = requests.get(f'https://api.ganjoor.net/api/ganjoor/poet/{pid}/randompoem', timeout=15)
        if r.status_code == 200:
            poem_id = r.json().get('id')
            if poem_id:
                r2 = requests.get(f'https://api.ganjoor.net/api/ganjoor/poem/{poem_id}', timeout=15)
                poem = r2.json()
                text = poem.get('plainText', '').strip()
                if text and is_safe(text):
                    lines = [l for l in text.split('\n') if l.strip()][:4]
                    return name, '\n'.join(lines)
    except:
        pass
    return None, None

def get_poetry():
    name, text = get_poem_online()
    if text:
        return (f'🌙 **از دیوان {name}**\n\n  {text}\n\n'
                f'✨ {name}، ستاره آسمان ادب فارسی\n\n{LINE}')
    return None

# ===== فال حافظ (گنجور + تفسیر ZenQuotes) =====
def get_hafez_fal():
    name, text = get_poem_online('حافظ')
    if text:
        interp = get_inspiration_text()
        msg = f'🔮 **فال حافظ شما**\n\n  {text}\n\n'
        if interp:
            msg += f'💫 **تفسیر:** {interp}\n\n'
        msg += f'{LINE}\n#فال_حافظ'
        return msg
    return None

# ===== آیه قرآن (آنلاین) =====
def get_quran_verse():
    try:
        r = requests.get('https://api.alquran.cloud/v1/ayah/random/fa.ghomshei', timeout=15)
        if r.status_code == 200:
            data = r.json().get('data', {})
            text = data.get('text', '')
            number = data.get('numberInSurah', '')
            surah = data.get('surah', {}).get('name', '')
            if text and is_safe(text):
                return f'📖 **{surah}، آیه {fa_num(number)}**\n\n{text}\n\n{LINE}\n#قرآن'
    except:
        pass
    return None

# ===== انرژی مثبت (ZenQuotes ترجمه) =====
def get_inspiration_text():
    try:
        r = requests.get('https://zenquotes.io/api/random', timeout=10)
        if r.status_code == 200:
            data = r.json()[0]
            quote = data.get('q', '')
            author = data.get('a', '')
            if quote and is_safe(quote):
                return f'{translate(quote)} — {translate(author)}'
    except:
        pass
    return None

def get_inspiration():
    t = get_inspiration_text()
    if t:
        return f'💪 **سخن امروز**\n\n{t}\n\n{LINE}\n#انرژی_مثبت'
    return None

# ===== مکان دیدنی (Wikipedia فارسی + Pexels) =====
def get_landmark(idx):
    try:
        place = PLACES[idx % len(PLACES)]
        r = requests.get(f'https://fa.wikipedia.org/api/rest_v1/page/summary/{place}', timeout=10)
        data = r.json()
        desc = data.get('extract', '')
        title = data.get('title', place.replace('_',' '))
        if desc and is_safe(desc):
            # عکس از pexels
            en = place.replace('_',' ')
            r2 = requests.get('https://api.pexels.com/v1/search',
                headers={'Authorization': PEXELS_KEY},
                params={'query': en, 'per_page': 3}, timeout=15)
            photos = r2.json().get('photos', [])
            caption = f'🌍 **{title}**\n\n{desc[:400]}\n\n{LINE}\n#گردشگری #ایرانگردی'
            if photos:
                return photos[0]['src']['large'], caption
            return None, caption
    except:
        pass
    return None, None

# ===== این روز در تاریخ =====
def get_this_day_in_history():
    try:
        now = tehran_now()
        r = requests.get(f'https://byabbe.se/on-this-day/{now.month}/{now.day}/events.json', timeout=15)
        events = r.json()
        if events:
            e = random.choice(events[:30])
            year = e.get('year', '')
            desc = e.get('content', '')
            if not is_safe(desc): return None
            return (f'📅 **در چنین روزی...**\n\nسال {fa_num(year)}:\n{translate(desc)}\n\n'
                    f'✨ تاریخ همیشه یه درس برای امروز داره!\n\n{LINE}\n#تاریخ')
    except:
        pass
    return None

# ===== معما =====
def get_riddle():
    try:
        r = requests.get('https://riddles-api.vercel.app/random', timeout=10)
        data = r.json()
        q = data.get('riddle', '')
        a = data.get('answer', '')
        if not q or not is_safe(q): return None
        return (f'🧩 **چالش مغزی امروز**\n\n{translate(q)}\n\n'
                f'⬇️ اول فکر کن، بعد جواب رو ببین!\n\n'
                f'💡 **جواب:** {translate(a)}\n\n{LINE}\n#معما')
    except:
        return None

# ===== trivia =====
def get_trivia():
    try:
        r = requests.get('https://opentdb.com/api.php?amount=1&type=multiple', timeout=10)
        data = r.json().get('results', [{}])[0]
        q = htmllib.unescape(data.get('question', ''))
        correct = htmllib.unescape(data.get('correct_answer', ''))
        if not is_safe(q): return None
        diff_fa = {'easy':'آسان','medium':'متوسط','hard':'سخت'}.get(data.get('difficulty',''), '')
        return (f'🎯 **سوال اطلاعات عمومی ({diff_fa})**\n\n❓ {translate(q)}\n\n'
                f'⬇️ جواب پایینه...\n\n✅ **جواب:** {translate(correct)}\n\n{LINE}\n#دانستنی')
    except:
        return None

# ===== کلمه روز =====
def get_word_of_day():
    try:
        slot = int(time.time() // 86400)
        word = WORDS[slot % len(WORDS)]
        r = requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}', timeout=10)
        data = r.json()[0]
        phonetic = data.get('phonetic', '')
        meanings = data.get('meanings', [{}])
        definition = meanings[0].get('definitions', [{}])[0].get('definition', '')
        example = meanings[0].get('definitions', [{}])[0].get('example', '')
        if not is_safe(definition): return None
        msg = (f'🇬🇧 **واژه‌آموزی | Word of the Day**\n\n'
               f'📖 {word}\n🔊 {phonetic}\n📖 معنی: {translate(word)}\n\n'
               f'📝 {translate(definition)}\n')
        if example:
            msg += f'\n💬 {example}\n   {translate(example)}\n'
        return msg + f'\n{LINE}\n#زبان_انگلیسی'
    except:
        return None

# ===== طنز (Reddit ترجمه) =====
def get_joke():
    items = reddit_titles('jokes')
    if items:
        return f'😂 **بخند تا دنیا به کامِت بشه!**\n\n{translate(random.choice(items))}\n\n{LINE}\n#طنز'
    return None

# ===== دانستنی =====
def get_fact():
    items = [t.replace('TIL ','') for t in reddit_titles('facts')]
    if items:
        return f'🤔 **آیا می‌دونستی؟**\n\n{translate(random.choice(items))}\n\n💡 دنیای عجیب و جذاب!\n\n{LINE}\n#دانستنی'
    return None

# ===== خبر جهان =====
def get_world():
    items = reddit_titles('world')
    if items:
        t = translate(random.choice(items))
        if is_safe(t):
            now = tehran_now()
            return f'🌍 **خبر جهانی** | ساعت {fa_num(now.strftime("%H:%M"))}\n\n{t}\n\n{LINE}\n#جهان'
    return None

def get_tech(idx):
    for url in ['https://www.zoomit.ir/feed','https://digiato.com/feed']:
        items = rss_titles(url)
        if items: return f'💻 **تکنولوژی**\n\n{items[idx % len(items)]}\n\n{LINE}\n#تکنولوژی'
    return None

def get_sports(idx):
    items = rss_titles('https://www.varzesh3.com/rss')
    if items: return f'⚽ **ورزشی**\n\n{items[idx % len(items)]}\n\n{LINE}\n#ورزشی'
    return None

def get_health(idx):
    for url in ['https://salamatnews.com/rss']:
        items = rss_titles(url)
        if items: return f'💊 **سلامتی**\n\n{items[idx % len(items)]}\n\n{LINE}\n#سلامتی'
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
            return p['src']['large'], f'🖼 **والپیپر {fa}**\n\n📸 عکاس: {p.get("photographer","")}\n\n{LINE}\n#والپیپر'
    except:
        pass
    return None, None

def post(ctype, idx):
    print('Posting:', ctype)
    try:
        if ctype == 'news':
            t = get_news(idx); (t and send(t))
        elif ctype == 'gold':
            t = get_gold(); (t and send(t))
        elif ctype == 'crypto':
            t = get_crypto(); (t and send(t))
        elif ctype == 'weather':
            t = get_weather(); (t and send(t))
        elif ctype == 'poetry':
            t = get_poetry(); (t and send(t))
        elif ctype == 'quran':
            t = get_quran_verse(); (t and send(t))
        elif ctype == 'horoscope':
            t = get_hafez_fal(); (t and send(t))
        elif ctype == 'inspiration':
            t = get_inspiration(); (t and send(t))
        elif ctype == 'landmark':
            photo, cap = get_landmark(idx)
            if cap: send(cap, photo)
        elif ctype == 'history':
            t = get_this_day_in_history(); (t and send(t))
        elif ctype == 'riddle':
            t = get_riddle(); (t and send(t))
        elif ctype == 'trivia':
            t = get_trivia(); (t and send(t))
        elif ctype == 'word':
            t = get_word_of_day(); (t and send(t))
        elif ctype == 'humor':
            t = get_joke(); (t and send(t))
        elif ctype == 'fact':
            t = get_fact(); (t and send(t))
        elif ctype == 'world':
            t = get_world(idx); (t and send(t))
        elif ctype == 'tech':
            t = get_tech(idx); (t and send(t))
        elif ctype == 'sports':
            t = get_sports(idx); (t and send(t))
        elif ctype == 'health':
            t = get_health(idx); (t and send(t))
        elif ctype == 'wallpaper':
            photo, cap = get_wallpaper(idx)
            if photo: send(cap, photo)
        elif ctype == 'poll': send_poll()
    except Exception as e:
        print(f'Post error for {ctype}:', e)

def main():
    if not (BOT_TOKEN and CHANNEL_ID and PEXELS_KEY):
        print('Missing credentials')
        return
    slot = int(time.time() // 1800)
    hour = tehran_now().hour
    if 6 <= hour < 12:
        base = ['weather','news','gold','crypto','word','inspiration','tech','sports','world','fact','history','riddle','trivia','quran','poll']
    elif 12 <= hour < 18:
        base = ['gold','crypto','news','horoscope','humor','world','health','word','trivia','tech','sports','fact','riddle','quran','poll']
    else:
        base = ['poetry','quran','horoscope','landmark','history','world','word','inspiration','humor','riddle','fact','crypto','trivia','poll']
    off = slot % len(base)
    for i in range(6):
        ctype = base[(off + i) % len(base)]
        idx = int(time.time() // 300)
        post(ctype, idx)
        if i < 5:
            time.sleep(300)

if __name__ == '__main__':
    main()
