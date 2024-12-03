from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, LargeBinary, func

# 创建声明性基类
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# 定义模型
class RedImg(Base):
    __tablename__ = 'red_img'

    id = Column(Integer, primary_key=True, autoincrement=True)
    img_id = Column(String)
    url = Column(String)
    old_url = Column(String)
    source = Column(String)
    web = Column(String, default='red')
    label = Column(String)
    title = Column(String)
    create_time = Column(DateTime, default=datetime.utcnow)
    prd = Column(Integer, default=0)
    img_text = Column(String)
    img_type = Column(String)

    def __str__(self):
        return f"RedImg(id={self.id}, imd_id={self.img_id}, url={self.url}, name={self.old_url}, source={self.source}, web={self.web})"


class ArticleLog(Base):
    __tablename__ = 'article_log'

    id = Column(String(255), primary_key=True, comment='文章唯一id')
    context = Column(String, nullable=False, comment='内容')
    create_time = Column(DateTime, nullable=False, server_default=func.current_timestamp(), comment='创建时间')
    title = Column(String, nullable=True, comment='标题')
    banner = Column(String, nullable=True, comment='封面')

    def __repr__(self):
        return f"<ArticleLog(id='{self.id}', create_time='{self.create_time}')>"


class RedLive(Base):
    __tablename__ = 'red_live'
    auto_id = Column(Integer, primary_key=True, autoincrement=True)
    article_id = Column(String,comment='文章url')
    url = Column(String, nullable=False, comment='视频路径')
    create_time = Column(DateTime, nullable=False, server_default=func.current_timestamp(), comment='创建时间')

    def __repr__(self):
        return f"<RedLive(notes='{self.article_id}', url='{self.url}', create_time='{self.create_time}')>"