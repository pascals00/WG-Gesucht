from time import sleep
import random
from .url import *
from .user_agents import USER_AGENTS

class RequestHeaders:
    def __init__(self):
        self.headers = {
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

    @staticmethod
    def change_user_agent():
        return random.choice(USER_AGENTS)

    @staticmethod
    def random_delay():
        delay = random.uniform(0.5, 3)  # Delay between 0.5 and 3 seconds
        sleep(delay)

    @staticmethod
    def change_platform():
        platform = ['macOS', 'Windows']
        return random.choice(platform)

    def init_headers(self):
        self.headers['Referer'] = 'www.wg-gesucht.de'
        self.headers['User-Agent'] = self.change_user_agent()
        self.headers['sec-ch-ua-platform'] = self.change_platform()
        return self.headers
