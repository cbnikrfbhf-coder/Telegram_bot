import requests
import random
import os
import re
from datetime import datetime

BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHANNEL_ID = os.environ.get('CHANNEL_ID')
PEXELS_KEY = os.environ.get('PEXELS_KEY')

def get_wallpaper():
    try:
        url = 'https://api.pexels.com/v1/search'
        headers = {'Authorization': PEXELS_KEY}
        keywords = ['nature', 'landscape', 'mountain', 'ocean', 'forest']
        keyword = random.choice(keywords)
        params = {'query': keyword, 'per_page': 15, 'orientation': 'portrait'}
        
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        
        if 'photos' in data and len(data['photos']) > 0:
            photo = random.choice(data['photos'])
            return {
                'type': 'photo',
                'url': photo['src']['large'],
                'caption': f'🖼 والپیپر زیبای روز\n\n📸 عکاس: {photo["photographer"]}\n\n#والپیپر #طبیعت #{keyword}'
            }
    except Exception as e:
        print(f'Wallpaper error: {e}')
    return None

def get_news():
    try:
        url = 'https://feeds.bbci.co.uk/news/world/middle_east/rss.xml'
        response = requests.get(url)
        text = response.text
        items = re.findall(r'<item>(.*?)</item>', text, re.DOTALL)
        
        if items:
            item = random.choice(items[:5])
            title_match = re.search(r'<title><!\[CDATA\[(.*?)\]\]></title>', item)
            if not title_match:
                title_match = re.search(r'<title>(.*?)</title>', item)
            title = title_match.group(1) if title_match else 'خبر جدید'
            
            desc_match = re.search(r'<description><!\[CDATA\[(.*?)\]\]></description>', item)
            if not desc_match:
                desc_match = re.search(r'<description>(.*?)</description>', item)
            desc = desc_match.group(1) if desc_match else ''
            
            link_match = re.search(r'<link>(.*?)</link>', item)
            link = link_match.group(1) if link_match else ''
            
            return {
                'type': 'text',
                'text': f'📰 {title}\n\n{desc}\n\n🔗 {link}\n\n#خبر #اخبار'
            }
    except Exception as e:
        print(f'News error: {e}')
    return None

def get_tech_news():
    try:
        url = 'https://www.theverge.com/rss/index.xml'
        response = requests.get(url)
        text = response.text
        items = re.findall(r'<entry>(.*?)</entry>', text, re.DOTALL)
        
        if not items:
            items = re.findall(r'<item>(.*?)</item>', text, re.DOTALL)
        
        if items:
            item = random.choice(items[:5])
            title_match = re.search(r'<title[^>]*>(.*?)</title>', item)
            title = title_match.group(1) if title_match else 'Tech News'
            title = re.sub(r'<!\[CDATA\[(.*?)\]\]>', r'\1', title)
            
            return {
                'type': 'text',
                'text': f'💻 {title}\n\n#تکنولوژی #فناوری'
            }
    except Exception as e:
        print(f'Tech news error: {e}')
    return None

def get_lifehack():
    try:
        url = 'https://www.wikihow.com/Special:Randomizer'
        response = requests.get(url, allow_redirects=True)
        title_match = re.search(r'<title>(.*?)</title>', response.text)
        if title_match:
            title = title_match.group(1).replace(' - wikiHow', '')
            return {
                'type': 'text',
                'text': f'💡 {title}\n\n{response.url}\n\n#ترفند #آموزش'
            }
    except Exception as e:
        print(f'Lifehack error: {e}')
    return None

def send_to_telegram(message):
    try:
        if message['type'] == 'photo':
            url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto'
            data = {
                'chat_id': CHANNEL_ID,
                'photo': message['url'],
                'caption': message['caption']
            }
        else:
            url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
            data = {
                'chat_id': CHANNEL_ID,
                'text': message['text'],
                'disable_web_page_preview': False
            }
        
        response = requests.post(url, json=data)
        result = response.json()
        print(f'Posted: {response.status_code} - {result.get("ok")}')
        return result
    except Exception as e:
        print(f'Telegram error: {e}')
        return None

def main():
    if not BOT_TOKEN or not CHANNEL_ID or not PEXELS_KEY:
        print('Missing credentials')
        return
    
    hour = datetime.now().hour
    content_types = ['wallpaper', 'news', 'tech', 'lifehack']
    content_type = content_types[hour % len(content_types)]
    
    print(f'Posting {content_type}...')
    
    message = None
    if content_type == 'wallpaper':
        message = get_wallpaper()
    elif content_type == 'news':
        message = get_news()
    elif content_type == 'tech':
        message = get_tech_news()
    elif content_type == 'lifehack':
        message = get_lifehack()
    
    if message:
        send_to_telegram(message)
        print(f'✅ Posted {content_type}!')
    else:
        print('❌ Failed to get content')

if __name__ == '__main__':
    main()
