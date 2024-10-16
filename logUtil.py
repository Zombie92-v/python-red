import logging

# 创建日志记录函数，打印当前时间精确到秒
def log(message):
    # 记录日志
    from datetime import datetime;
    formatted_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    logging.info(f"{formatted_time},{message}")