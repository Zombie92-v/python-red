from fake_useragent import UserAgent
class SingletonUserAgent:
    ua = None
    def __init__(self):
        self.ua = UserAgent()
        self.ua.platforms.remove("mobile")
        self.ua.platforms.remove("tablet")
ua = SingletonUserAgent().ua
