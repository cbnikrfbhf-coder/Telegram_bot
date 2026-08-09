import requests, os, re, time, html as htmllib, random, hashlib
from datetime import datetime

BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHANNEL_ID = os.environ.get('CHANNEL_ID')
PEXELS_KEY = os.environ.get('PEXELS_KEY')
PROMO = '\n\n📢 @shegftanekhabar'
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

# ===== فیلتر قوی =====
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
NAMES = {
    'bitcoin':'بیت‌کوین','ethereum':'اتریوم','tron':'ترون',
    'the-sandbox':'سندباکس 🎮','axie-infinity':'اکسی اینفینیتی 🎮',
    'gala':'گالا 🎮','decentraland':'دیسنترالند 🎮'
}

IRAN_CITIES = [
    ('تهران', 35.68, 51.38),('مشهد', 36.26, 59.61),('اصفهان', 32.65, 51.67),
    ('شیراز', 29.59, 52.58),('تبریز', 38.09, 46.29),
]

# ===== ۳۰ طنز اجتماعی (چون API نداره) =====
SATIRE = [
    '🎭 قیمت مرغ انقدر رفته بالا که حالا مرغ‌ها فکر می‌کنن برن بورس!',
    '🎭 تورم انقدر تیزه که حتی بادکنک‌ها هم از ما جلو می‌زنن!',
    '🎭 حقوقم انقدر کمه که حتی خودم هم نمی‌تونم استخدامش کنم!',
    '🎭 دلار انقدر رفته بالا که حالا داره به ما نگاه می‌کنه و می‌خنده!',
    '🎭 رفتم رستوران، منو رو دیدم، گفتم یه لیوان اشک بدید، خودم تولید می‌کنم!',
    '🎭 قیمت پراید از قیمت خونه‌مون توی شهرستان گرون‌تر شده!',
    '🎭 رفتم مغازه گفتم یه چیز ارزون بدید، گفت «هوای آزاد مجانی‌ست!»',
    '🎭 حقوقم رو که می‌گیرم، قبل از اینکه به دستم برسه از دستم میره!',
    '🎭 ماشینم انقدر قدیمیه که حالا موزه ازم درخواست اجاره کرده!',
    '🎭 یخچالم فقط یه لامپ داره که روشنه، بقیه‌ش تعطیلات تابستونیه!',
    '🎭 تصمیم گرفتم پس‌انداز کنم؛ الان فقط یه سکه ۵۰۰ تومنی دارم!',
    '🎭 قیمت گوشت انقدر رفته بالا که حالا گاو‌ها دارن بهمون فخر می‌فروشن!',
    '🎭 رفتم بانک وام بگیرم، گفتن ضامن می‌خوای؛ خودم ضامنم بودم، قبول نکردن!',
    '🎭 اجاره خونه ام رو حساب کردم، دیدم صاحبخونه داره به جای من کار می‌کنه!',
    '🎭 تصمیم گرفتم ماشینم رو بفروشم، خریدار گفت «اینو کی می‌خره؟!»',
    '🎭 رفتم سفر، فقط تا سر کوچه! بقیه‌ش رو از گوگل مپ دیدم!',
    '🎭 قیمت آجیل شب عید رو که دیدم، تصمیم گرفتم عید رو کنسل کنم!',
    '🎭 مامانم گفت چرا لاغر شدی؟ گفتم مامان قیمت مرغ رو دیدی؟!',
    '🎭 دوستم پرسید شغلت چیه؟ گفتم «مدیر بحران مالی شخصی!»',
    '🎭 عروسی دعوت شدم، کادو رو که فکر کردم، تصمیم گرفتم مجرد بمونم!',
    '🎭 رفتم بازار طلا، ویترین رو نگاه کردم، شیشه ترک خورد!',
    '🎭 به بابام گفتم ماشین می‌خوام، گفت «منم می‌خوام!»',
    '🎭 حقوق اول ماه میاد، وسط ماه نگاهش می‌کنیم، آخر ماه یادش می‌کنیم!',
    '🎭 سبد خریدمون انقدر کوچیکه که حالا اسمش رو گذاشتیم «سبد قلم»!',
    '🎭 قیمت بنزین ثابته، همه‌چیز دیگه گرون شده!',
    '🎭 رفتم داروخانه، گفتم یه چیز خوب برای سرماخوردگی بدید، گفت ۲۰۰ تومن! گفتم باشه، خودم خوب میشم!',
    '🎭 تنها ورزشی که استادم، ورزشِ از زیر کار در رفتنه!',
    '🎭 وزنم رو پرسیدم، ترازو گفت «لطفاً یکی یکی بیایید!»',
    '🎭 تنها چیزی که تو این مملکت ثابته، بی‌پولی منه!',
    '🎭 تصمیم گرفتم رژیم بگیرم؛ مامانم گفت «امروز قورمه‌سبزی داریم!»',
]

# ===== ۱۲۰ فال حافظ =====
HAFEZ_FAL = [
    'یوسف گمگشته بازآید به کنعان غم مخور\nکلبه احزان شود روزی گلستان غم مخور',
    'الا یا ایها الساقی ادر کاسا و ناولها\nکه عشق آسان نمود اول ولی افتاد مشکل‌ها',
    'رسید مژده که ایام غم نخواهد ماند\nچنان نماند چنین نیز هم نخواهد ماند',
    'دوش وقت سحر از غصه نجاتم دادند\nواندر آن ظلمت شب آب حیاتم دادند',
    'منم که شهره شهرم به عشق ورزیدن\nمنم که دیده به دیدار دوست دوختم',
    'به می سجاده رنگین کن گرت پیر مغان گوید\nکه سالک بی خبر نبود ز راه و رسم منزل‌ها',
    'خلوت گزیده را به تماشا چه حاجت است\nچون کوی دوست هست چه حاجت برون رفتن',
    'ساقی به نور باده برافروز جام ما\nمطرب بگو که کار جهان شد به کام ما',
    'هر آن که جانب اهل وفا نگه دارد\nخداش در همه حال از بلا نگه دارد',
    'بیا که قصر امل سخت سست بنیاد است\nبیار باده که بنیاد عمر بر باد است',
    'دوش دیدم که ملایم در میخانه زدند\nبابا گشودند و به رویم در میخانه زدند',
    'ما بر سر این ایم که گر زنده بمانیم\nدوستداران خویش را غمگین نکنیم',
    'ای پادشه خوبان داد از غم تنهایی\nدل بی تو به جان آمد وقت است که بازآیی',
    'در بیابان گر به شوق کعبه خواهی زد قدم\nسرزنش‌ها گر کند خار مغیلان غم مخور',
    'صبا به لطف بگو آن غزال رعنا را\nکه سر به کوه و بیابان تو داده‌ای ما را',
    'ز چشمت جان نشاید برد کاین سودای پنهانی\nبه دل هر دم فکند از غمزه‌ات تیری، کمان ابرو',
    'محتسب شیخ و زاهد و صوفی از من رنجیده‌اند\nمن همانم که همه شهر به من گواهی دهند',
    'عاقبت منزل ما ویرانه سرا خواهد بود\nچرخ بازیگر از این خانه به خانه خواهد بود',
    'ما بدین در نه پی حشمت و جاه آمده‌ایم\nاز بد حادثه اینجا به پناه آمده‌ایم',
    'به ملازمان سلطان که رساند این دعا را\nکه به شکر پادشاهی ز نظر مران گدا را',
    'عاشق شو ار نه روزی کار جهان سرآید\nناگفته هزار نقش در خاطر تو ماند',
    'عاشقان را گر در آتش می‌زنی پنداری نیست\nچون تو آتش پاره‌ای هر جا روی می‌سوزی',
    'هر که را جامه ز پشم است ز شمشیر برهن\nبه که جامه ز اطلس که ز دیبا باشد',
    'از صدای سخن عشق ندیدم خوش‌تر\nیادگاری که در این گنبد دوار بماند',
    'محتسب در خرابات مبین ما را مست\nکه ز خیر تو گذشتیم و به بد مست هستیم',
    'عشق‌هایی کز پی رنگی بود\nعشق نبود عاقبت ننگی بود',
    'ای ساربان آهسته رو آرام جانم می‌رود\nوان دل که با خود می‌برم چون دلستانم می‌رود',
    'ای گل باده ده و شادی کن این کاخ گل را\nپیش از آن که شود خاک در این خاکدان ما',
    'صبا به لطف بگو آن غزال رعنا را\nکه سر به کوه و بیابان داده‌ای ما را',
    'بیا تا گل برافشانیم و می در ساغر اندازیم\nفلک را سقف بشکافیم و طرحی نو دراندازیم',
    'دل می‌رود ز دستم صاحب‌دلان خدا را\nدردا که راز پنهان خواهد شد آشکارا',
    'زلف آشفته و خوی کرده و خندان لب و مست\nپیرهن چاک و غزل خوان و صراحی در دست',
    'الا یا ایها الساقی ادر کاسا و ناولها\nکه عشق آسان نمود اول ولی افتاد مشکل‌ها',
    'ای هدهد صبا به سبا می‌فرستمت\nبنگر که از کجا به کجا می‌فرستمت',
    'مژده‌ای دل که دگر بار صبا بازآمد\nهدهد خوش‌قدم از طَرف سبا بازآمد',
    'مرا عهدی است با جانان که تا جان در بدن دارم\nهوای‌دار آن سرو گل‌اندام گلستان باشم',
    'زاهد ظاهرپرست از حال ما آگاه نیست\nدر حق ما هر چه گوید جای هیچ اکراه نیست',
    'بیدلی از همه اقوام عذر می‌خواهد\nکه ز ما جز غم و اندوه نیاموخت کسی',
    'من از آن حسن روزافزون که یوسف داشت دانستم\nکه عشق از پرده برون آرد زلیخا را',
    'دلا دلالت خیرت کنم به راه نجات\nبه آب رنگ و ریا و ریا ریای ریای',
    'اگر آن ترک شیرازی به دست آرد دل ما را\nبه خال هندویش بخشم سمرقند و بخارا را',
    'گفتم غم تو دارم گفتا غمت سر آید\nگفتم که ماه مایی گفتا اگر برآید',
    'چو پیراهن به بالا می‌کشید آن سرو رعنا را\nدلم را برد و می‌گفت ای پسر مردانه باش و مرد',
    'ای صبا نکهت کوی آن نگار یار من بر\nکه غبار رهش را توتیای دیدار من بر',
    'ساقی بیار باده که رمزی ز خواجه گویم\nاز آن عجب که چون تو چرا بی‌نظیر ماند',
    'عقل گوید که ز می پرهیز و مستی مکن\nدل گوید که می خور و شادی کن و شادی',
    'عاقبت گوهر مقصود به چنگ آوردم\nزین پس از دست غم و رنج به در خواهم شد',
    'گر طبیبانه بیایی به بالین من\nبه دو عالم ندهم لذت بیماری را',
    'به می سجاده رنگین کن گرت پیر مغان گوید\nکه سالک بی‌خبر نبود ز راه و رسم منزل‌ها',
    'مرا در منزل جانان چه امن عیش چون هر دم\nجرس فریاد می‌دارد که بربندید محمل‌ها',
    'ای که در کاخ گنبد مینا\nخسروی می‌کنی و جام می‌نوش',
    'به خالق بودن خویش عارفم و بس\nوگرنه خاکم و دانای بی‌نشان همه‌اند',
    'به کوی عشق منه بی‌دلیل و راه مرو\nکه در ره او همه گمراه و بی‌نشان همه‌اند',
    'عشقست بر آسمان پریدن\nبه یک جهان دل به یک دلبر بستن',
    'چو بوی گل ز بن جانم برآمد\nدلم ز شوق به پرواز آمد',
    'در کوی ما شکسته‌دلی می‌خرند و بس\nبازار خودفروشی از آن‌سوی دیگرست',
    'ای گل تازه رسیده به چمن\nآشنایی نه غریبی چون من',
    'عشق و مستی و رندی و داد و دهش\nاین همه را به ما آموخت پیر مغان',
    'دریغ و درد که تا این دَم از سر غفلت\nز فیض بادهٔ گلرنگ لعل‌فام بماند',
    'به شیر و پلنگ و گرگ و گوسفند\nبه گور و به آهو و به مرغ و پلنگ',
    'عشق را خواهی که تا پایان بری\nهمچنان در آتش خود سوخته می‌باید زیست',
    'خدا چنان کند که بر سر بدخواهان ما\nچنان غمی بزند کز غم تو رها گردند',
    'دریغ از این همه رنج و تعب که از هجران\nنوشتم از سر انگشت خون به جای قلم',
    'خسروا شیرین‌دل و شکربار و شهدآگین‌لب\nچو عسل در شکربار و چو شکر در شهد',
    'ای که از نرگس مستت همه بیمارند\nهمه را پرده‌دری بر سر بازارند',
    'من از آن حسن روزافزون که یوسف داشت دانستم\nکه عشق از پرده برون آرد زلیخا را',
    'مرا عهدی است با جانان که تا جان در بدن دارم\nهوای‌دار آن سرو گل‌اندام گلستان باشم',
    'ساقی به نور باده برافروز جام ما\nمطرب بگو که کار جهان شد به کام ما',
    'چو پیراهن به بالا می‌کشید آن سرو رعنا را\nدلم را برد و می‌گفت ای پسر مردانه باش',
    'دلا دلالت خیرت کنم به راه نجات\nبه آب رنگ و ریا و ریا ریای ریای',
    'بیا که قصر امل سخت سست بنیاد است\nبیار باده که بنیاد عمر بر باد است',
    'خلوت گزیده را به تماشا چه حاجت است\nچون کوی دوست هست چه حاجت برون رفتن',
    'محتسب شیخ و زاهد و صوفی از من رنجیده‌اند\nمن همانم که همه شهر به من گواهی دهند',
    'عاقبت منزل ما ویرانه سرا خواهد بود\nچرخ بازیگر از این خانه به خانه خواهد بود',
    'ما بدین در نه پی حشمت و جاه آمده‌ایم\nاز بد حادثه اینجا به پناه آمده‌ایم',
    'به ملازمان سلطان که رساند این دعا را\nکه به شکر پادشاهی ز نظر مران گدا را',
    'عاشق شو ار نه روزی کار جهان سرآید\nناگفته هزار نقش در خاطر تو ماند',
    'عاشقان را گر در آتش می‌زنی پنداری نیست\nچون تو آتش پاره‌ای هر جا روی می‌سوزی',
    'هر که را جامه ز پشم است ز شمشیر برهن\nبه که جامه ز اطلس که ز دیبا باشد',
    'از صدای سخن عشق ندیدم خوش‌تر\nیادگاری که در این گنبد دوار بماند',
    'محتسب در خرابات مبین ما را مست\nکه ز خیر تو گذشتیم و به بد مست هستیم',
    'عشق‌هایی کز پی رنگی بود\nعشق نبود عاقبت ننگی بود',
    'ای ساربان آهسته رو آرام جانم می‌رود\nوان دل که با خود می‌برم چون دلستانم می‌رود',
    'ز چشمت جان نشاید برد کاین سودای پنهانی\nبه دل هر دم فکند از غمزه‌ات تیری کمان ابرو',
    'بیا تا گل برافشانیم و می در ساغر اندازیم\nفلک را سقف بشکافیم و طرحی نو دراندازیم',
    'دل می‌رود ز دستم صاحب‌دلان خدا را\nدردا که راز پنهان خواهد شد آشکارا',
    'زلف آشفته و خوی کرده و خندان لب و مست\nپیرهن چاک و غزل خوان و صراحی در دست',
    'ای هدهد صبا به سبا می‌فرستمت\nبنگر که از کجا به کجا می‌فرستمت',
    'مژده‌ای دل که دگر بار صبا بازآمد\nهدهد خوش‌قدم از طَرف سبا بازآمد',
    'دوش وقت سحر از غصه نجاتم دادند\nواندر آن ظلمت شب آب حیاتم دادند',
    'منم که شهره شهرم به عشق ورزیدن\nمنم که دیده به دیدار دوست دوختم',
    'به می سجاده رنگین کن گرت پیر مغان گوید\nکه سالک بی خبر نبود ز راه و رسم منزل‌ها',
    'خلوت گزیده را به تماشا چه حاجت است\nچون کوی دوست هست چه حاجت برون رفتن',
    'ساقی به نور باده برافروز جام ما\nمطرب بگو که کار جهان شد به کام ما',
    'هر آن که جانب اهل وفا نگه دارد\nخداش در همه حال از بلا نگه دارد',
    'بیا که قصر امل سخت سست بنیاد است\nبیار باده که بنیاد عمر بر باد است',
    'دوش دیدم که ملایم در میخانه زدند\nبابا گشودند و به رویم در میخانه زدند',
    'ما بر سر این ایم که گر زنده بمانیم\nدوستداران خویش را غمگین نکنیم',
    'ای پادشه خوبان داد از غم تنهایی\nدل بی تو به جان آمد وقت است که بازآیی',
    'در بیابان گر به شوق کعبه خواهی زد قدم\nسرزنش‌ها گر کند خار مغیلان غم مخور',
    'صبا به لطف بگو آن غزال رعنا را\nکه سر به کوه و بیابان تو داده‌ای ما را',
    'ز چشمت جان نشاید برد کاین سودای پنهانی\nبه دل هر دم فکند از غمزه‌ات تیری، کمان ابرو',
    'محتسب شیخ و زاهد و صوفی از من رنجیده‌اند\nمن همانم که همه شهر به من گواهی دهند',
    'عاقبت منزل ما ویرانه سرا خواهد بود\nچرخ بازیگر از این خانه به خانه خواهد بود',
    'ما بدین در نه پی حشمت و جاه آمده‌ایم\nاز بد حادثه اینجا به پناه آمده‌ایم',
    'به ملازمان سلطان که رساند این دعا را\nکه به شکر پادشاهی ز نظر مران گدا را',
]

WALL_TAGS = [('nature','طبیعت'),('mountain','کوه'),('ocean','دریا'),('forest','جنگل'),('flower','گل'),('sunset','غروب')]

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
    all_titles = []
    for sub in SAFE_SUBS.get(category, ['todayilearned']):
        try:
            r = requests.get(f'https://www.reddit.com/r/{sub}/hot.json?limit={n}',
                           headers=UA, timeout=15)
            for c in r.json()['data']['children']:
                title = c['data']['title']
                if not c['data'].get('over_18', False) and is_safe(title):
                    all_titles.append(title)
        except:
            pass
    return all_titles

# ===== شعر از گنجور (کاملاً آنلاین) =====
def get_poem_online():
    try:
        # گنجور: ۳۲ = حافظ، ۱۱ = سعدی، ۲۰ = مولانا، ۲۴ = خیام، ۱۴۲ = شاملو
        poets = [('حافظ',32),('سعدی',11),('مولانا',20),('خیام',24),('شاملو',142)]
        name, pid = random.choice(poets)
        r = requests.get(f'https://api.ganjoor.net/api/ganjoor/poet/{pid}/randompoem', timeout=15)
        if r.status_code == 200:
            data = r.json()
            # شعر کامل
            poem_id = data.get('id')
            if poem_id:
                r2 = requests.get(f'https://api.ganjoor.net/api/ganjoor/poem/{poem_id}', timeout=15)
                poem = r2.json()
                text = poem.get('plainText', '').strip()
                if text and is_safe(text):
                    # فقط ۲ بیت اول
                    lines = [l for l in text.split('\n') if l.strip()][:4]
                    poem_text = '\n'.join(lines)
                    return f'🌙 {poem_text}\n\n— {name}\n\n#شعر #{name}' + PROMO
    except:
        pass
    return None

# ===== آیه قرآن آنلاین =====
def get_quran_verse():
    try:
        # آیه رندوم از قرآن با ترجمه فارسی
        r = requests.get('https://api.alquran.cloud/v1/ayah/random/fa.ghomshei', timeout=15)
        if r.status_code == 200:
            data = r.json().get('data', {})
            text = data.get('text', '')
            number = data.get('numberInSurah', '')
            surah = data.get('surah', {}).get('name', '')
            if text and is_safe(text):
                return f'📖 **{surah}، آیه {number}**\n\n{text}\n\n#قرآن #آیه_روز' + PROMO
    except:
        pass
    return None

# ===== انرژی مثبت از ZenQuotes (آنلاین، ترجمه) =====
def get_inspiration():
    try:
        r = requests.get('https://zenquotes.io/api/random', timeout=10)
        if r.status_code == 200:
            data = r.json()[0]
            quote = data.get('q', '')
            author = data.get('a', '')
            if quote and is_safe(quote):
                quote_fa = translate(quote)
                author_fa = translate(author)
                return f'💪 **{quote_fa}**\n\n— {author_fa}\n\n#انرژی_مثبت #نقل_قول' + PROMO
    except:
        pass
    return None

# ===== فال حافظ واقعی =====
def get_hafez_fal():
    now = datetime.now()
    # بر اساس روز + ساعت، یه فال انتخاب میشه (هر روز عوض میشه)
    seed = int(time.time() // 3600)  # هر ساعت عوض میشه
    random.seed(seed)
    fal = random.choice(HAFEZ_FAL)
    random.seed()  # ریست
    # تفسیر کوتاه
    interpretations = [
        '✨ به زودی خبر خوشی به گوشت می‌رسد.',
        '✨ صبر کن، اوضاع رو به بهبودی است.',
        '✨ یه دوست قدیمی در راهه.',
        '✨ به زودی سفر کوتاهی در پیش داری.',
        '✨ یه فرصت مالی جدید سر راهت قرار می‌گیره.',
        '✨ مراقب اطرافیانت باش، همه صادق نیستن.',
        '✨ به زودی به خواسته‌ت می‌رسی، ناامید نشو.',
        '✨ یه تصمیم مهم پیش روت قرار می‌گیره.',
        '✨ از سختی‌ها درس بگیر، روزهای خوب در راهه.',
        '✨ رویاهات به زودی تعبیر می‌شن.',
    ]
    interp = interpretations[seed % len(interpretations)]
    return f'🔮 **فال حافظ امروز:**\n\n{fal}\n\n💫 **تفسیر:** {interp}\n\n#فال_حافظ #طالع_بینی' + PROMO

def get_news(idx):
    for url in NEWS_SOURCES:
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
            params={'ids':CRYPTO_IDS,'vs_currencies':'usd','include_24hr_change':'true'},
            headers=UA, timeout=15)
        data = r.json()
        lines = ['💹 قیمت لحظه‌ای ارز دیجیتال:', '']
        games_added = False
        for k, v in data.items():
            price = v.get('usd', 0)
            change = v.get('usd_24h_change', 0)
            emoji = '🟢' if change >= 0 else '🔴'
            if k in GAME_IDS and not games_added:
                lines.append('')
                lines.append('🎮 توکن بازی‌های آنلاین:')
                games_added = True
            fmt = '{:,.4f}' if price < 1 else '{:,.0f}'
            lines.append(f'{emoji} {NAMES.get(k,k)}: ${fmt.format(price)} ({change:+.1f}%)')
        return '\n'.join(lines) + '\n\n#کریپتو #بازی' + PROMO
    except:
        return None

def get_weather():
    try:
        lines = ['🌤️ **آب و هوای لحظه‌ای ایران:**', '']
        codes = {0:'☀️ صاف',1:'🌤️ عمدتاً صاف',2:'⛅ نیمه‌ابری',3:'☁️ ابری',
                 45:'🌫️ مه',48:'🌫️ مه',51:'🌦️ نم‌نم',53:'🌧️ بارون کم',55:'🌧️ بارون',
                 61:'🌧️ بارون',63:'🌧️ متوسط',65:'🌧️ شدید',
                 71:'🌨️ برف کم',73:'🌨️ برف',75:'❄️ برف شدید',80:'🌦️ رگبار',
                 95:'⛈️ رعدوبرق',96:'⛈️ رعدوبرق'}
        for city, lat, lon in IRAN_CITIES:
            url = f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true'
            r = requests.get(url, timeout=10)
            w = r.json().get('current_weather', {})
            temp = w.get('temperature', '?')
            code = w.get('weathercode', 0)
            lines.append(f'📍 {city}: {temp}°C {codes.get(code,"🌡️")}')
        return '\n'.join(lines) + '\n\n#آب_و_هوا' + PROMO
    except:
        return None

def get_this_day_in_history():
    try:
        now = datetime.now()
        url = f'https://byabbe.se/on-this-day/{now.month}/{now.day}/events.json'
        r = requests.get(url, timeout=15)
        events = r.json()
        if events:
            e = random.choice(events[:30])
            year = e.get('year', '')
            desc = e.get('content', '')
            if not is_safe(desc): return None
            translated = translate(desc)
            return f'📅 **در این روز از سال {year}:**\n\n{translated}\n\n#تاریخ #در_این_روز' + PROMO
    except:
        pass
    return None

def get_riddle():
    try:
        r = requests.get('https://riddles-api.vercel.app/random', timeout=10)
        data = r.json()
        q = data.get('riddle', '')
        a = data.get('answer', '')
        if not q or not is_safe(q): return None
        q_fa = translate(q)
        a_fa = translate(a)
        return (f'🧩 **معما:**\n{q_fa}\n\n'
                f'... فکر کن، بعد پایین رو ببین ...\n\n'
                f'💡 **جواب:** {a_fa}\n\n'
                f'#معما #چیستان' + PROMO)
    except:
        return None

def get_trivia():
    try:
        r = requests.get('https://opentdb.com/api.php?amount=1&type=multiple', timeout=10)
        data = r.json().get('results', [{}])[0]
        q = htmllib.unescape(data.get('question', ''))
        correct = htmllib.unescape(data.get('correct_answer', ''))
        category = htmllib.unescape(data.get('category', 'General'))
        difficulty = data.get('difficulty', 'easy')
        if not is_safe(q): return None
        q_fa = translate(q)
        correct_fa = translate(correct)
        category_fa = translate(category)
        diff_fa = {'easy':'آسان','medium':'متوسط','hard':'سخت'}.get(difficulty, '')
        return (f'🎯 **سوال اطلاعات عمومی ({diff_fa}):**\n'
                f'📚 {category_fa}\n\n'
                f'❓ {q_fa}\n\n'
                f'... فکر کن، بعد پایین رو ببین ...\n\n'
                f'✅ **جواب:** {correct_fa}\n\n'
                f'#اطلاعات_عمومی #دانستنی' + PROMO)
    except:
        return None

def get_word_of_day():
    try:
        words = ['serendipity','ephemeral','resilient','eloquent','luminous',
                 'meticulous','vibrant','profound','whimsical','tenacious',
                 'benevolent','gratitude','courage','wisdom','harmony',
                 'adventure','curiosity','passion','creative','inspire',
                 'nostalgia','melancholy','ethereal','solitude','wanderlust']
        slot = int(time.time() // 86400)
        word = words[slot % len(words)]
        r = requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}', timeout=10)
        data = r.json()[0]
        phonetic = data.get('phonetic', '')
        meanings = data.get('meanings', [{}])
        definition = meanings[0].get('definitions', [{}])[0].get('definition', '')
        example = meanings[0].get('definitions', [{}])[0].get('example', '')
        if not is_safe(definition): return None
        def_fa = translate(definition)
        example_fa = translate(example) if example else ''
        word_fa = translate(word)
        msg = (f'🇬🇧 **کلمه روز:** {word}\n'
               f'🔊 تلفظ: {phonetic}\n'
               f'📖 معنی: {word_fa}\n\n'
               f'📝 {def_fa}\n')
        if example_fa:
            msg += f'\n💬 مثال: {example}\n🔸 فارسی: {example_fa}\n'
        return msg + f'\n#زبان_انگلیسی #آموزش' + PROMO
    except:
        return None

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
    return None

def get_joke(idx):
    items = [translate(t) for t in reddit_titles('jokes')]
    items = [t for t in items if is_safe(t)]
    if items:
        return f'😂 {items[idx % len(items)]}\n\n#طنز' + PROMO
    return None

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
            return p['src']['large'], f'🖼 والپیپر {fa}\n\n📸 عکاس: {p.get("photographer","")}\n\n#والپیپر' + PROMO
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
            ('بهترین اختراع بشر؟', ['اینترنت','گوشی','برق','چرخ']),
            ('اگه یه ابرقدرت داشتی؟', ['پرواز','تله‌پورت','نامرئی شدن','خواندن ذهن']),
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
            t = get_news(idx); (t and send(t))
        elif ctype == 'gold':
            t = get_gold(); (t and send(t))
        elif ctype == 'crypto':
            t = get_crypto(); (t and send(t))
        elif ctype == 'tech':
            t = get_tech(idx); (t and send(t))
        elif ctype == 'sports':
            t = get_sports(idx); (t and send(t))
        elif ctype == 'health':
            t = get_health(idx); (t and send(t))
        elif ctype == 'world':
            t = get_world(idx); (t and send(t))
        elif ctype == 'fact':
            t = get_fact(idx); (t and send(t))
        elif ctype == 'humor':
            t = get_joke(idx); (t and send(t))
        elif ctype == 'poetry':
            t = get_poem_online(); (t and send(t))
        elif ctype == 'quran':
            t = get_quran_verse(); (t and send(t))
        elif ctype == 'inspiration':
            t = get_inspiration(); (t and send(t))
        elif ctype == 'satire':
            send(SATIRE[idx % len(SATIRE)] + '\n\n#طنز_اجتماعی' + PROMO)
        elif ctype == 'horoscope':
            send(get_hafez_fal())
        elif ctype == 'weather':
            t = get_weather(); (t and send(t))
        elif ctype == 'history':
            t = get_this_day_in_history(); (t and send(t))
        elif ctype == 'riddle':
            t = get_riddle(); (t and send(t))
        elif ctype == 'trivia':
            t = get_trivia(); (t and send(t))
        elif ctype == 'word':
            t = get_word_of_day(); (t and send(t))
        elif ctype == 'wallpaper':
            photo, cap = get_wallpaper(idx)
            if photo: send(cap, photo)
            else: send(SATIRE[idx % len(SATIRE)] + '\n\n#طنز_اجتماعی' + PROMO)
        elif ctype == 'poll': send_poll()
    except Exception as e:
        print(f'Post error for {ctype}:', e)

def main():
    if not (BOT_TOKEN and CHANNEL_ID and PEXELS_KEY):
        print('Missing credentials')
        return
    slot = int(time.time() // 1800)
    hour = datetime.now().hour
    if 6 <= hour < 12:
        base = ['weather','news','gold','crypto','word','inspiration','tech','sports','world','fact','history','riddle','trivia','quran','poll']
    elif 12 <= hour < 18:
        base = ['gold','crypto','news','horoscope','humor','world','health','word','trivia','tech','sports','fact','riddle','quran','poll']
    else:
        base = ['poetry','quran','horoscope','satire','history','world','word','inspiration','humor','riddle','fact','crypto','trivia','poll']
    off = slot % len(base)
    for i in range(6):
        ctype = base[(off + i) % len(base)]
        idx = int(time.time() // 300)
        post(ctype, idx)
        if i < 5:
            time.sleep(300)

if __name__ == '__main__':
    main()
