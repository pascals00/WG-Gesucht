from time import sleep
import random
from .url import *
from .user_agents import USER_AGENTS

payload = {}

headers = {
    'Accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7,no;q=0.6',
    'Connection': 'keep-alive',
    'Host': 'www.wg-gesucht.de',
    'Referer': 'www.wg-gesucht.de',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': '',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '',
}

# 2. Randomly change the user-agent
def change_user_agent():
    return random.choice(USER_AGENTS)

# 3. Add random delay
def random_delay():
    delay = random.uniform(0.5, 3)  # Delay between 0.5 and 3 seconds
    sleep(delay)

# 4. Clear cookies
def clear_cookies():
    return {}

def change_plattform():
    plattform = ['macOS', 'Windows']
    return random.choice(plattform)

def init_headers():
    headers['Referer'] = 'www.wg-gesucht.de'
    headers['User-Agent'] = change_user_agent()
    headers['sec-ch-ua-platform'] = change_plattform()
    headers.update(clear_cookies())
    return headers

def nextpage_headers(headers, url, currentpage_number):
    headers['Referer'] = switch_page(url, pagenumber=currentpage_number)
    return headers
