from fake_useragent import UserAgent

# 创建一个 UserAgent 实例
ua = UserAgent()
ua.platforms.remove("mobile")
ua.platforms.remove("tablet")
# 获取随机的 User-Agent
random_user_agent = ua.chrome
print(random_user_agent)