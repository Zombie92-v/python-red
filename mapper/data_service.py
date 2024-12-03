from sqlalchemy import create_engine, Executable

from dto.req import RedImgIdReq
from mapper.dto import RedImg, RedLive

# 创建数据库连接
engine = create_engine('mysql+mysqlconnector://root:Root?159156@8.134.205.36:3306/red?charset=utf8mb4')

from sqlalchemy.orm import sessionmaker

# 创建声明性基类
from sqlalchemy.orm import declarative_base

Base = declarative_base()

import logging

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
# 创建会话
Session = sessionmaker(bind=engine)
"""
# 插入数据
"""


def add(record: Base):
    session = Session()
    try:
        session.add(record)
        session.commit()  # 提交事务
    except Exception as e:
        print("插入发生错误:", e)
    finally:
        session.close()


def update_by_condition(entity, where_condition, set):
    from sqlalchemy import update
    session = Session()
    # 假设 User 是定义的 ORM 模型
    # session.query(RedImg).filter(where_condition).update({"web": "new_value"})
    session.query(entity).filter(where_condition).update(set)
    # 执行更新并提交
    session.commit()


def selectList(statement: Executable):
    from sqlalchemy import select
    # stmt = select(RedImg).where(RedImg.web == 'red')
    # 执行查询
    session = Session()
    try:
        results = session.execute(statement).scalars().all()
        return results
    except Exception as e:
        print("查询发生错误:", e)
    finally:
        session.close()


def queryImgAll(prd,limit):
    print('获取图片中')
    from sqlalchemy import select
    stmt = select(RedImg).where(RedImg.prd == prd).limit(limit)
    res = selectList(stmt)
    print('获取图片', res)
    return selectList(stmt)


def changeImgs(req: RedImgIdReq):
    print('修改图片中')
    update_by_condition(RedImg, RedImg.img_id.in_(req.img_ids), {"prd": f"{req.prd}"})


from sqlalchemy import delete


# 假设你已经导入了 RedImg 模型
def delete_img(ids: list[int]):  # 指定 ids 为一个包含整数的列表
    print("删除图片", ids)

    try:
        # 构建删除语句
        stmt = delete(RedImg).where(RedImg.img_id.in_(ids))

        # 执行删除操作
        session = Session()
        result = session.execute(stmt)

        # 提交事务
        session.commit()
        print(f"成功删除 {result.rowcount} 条记录")

    except Exception as e:
        # 捕获并打印异常
        print("删除图片时发生错误:", str(e))
        session.rollback()  # 回滚事务以防止不完整的操作

    finally:
        session.close()  # 关闭会话


def selectImgById(imgId):
    imgId = str(imgId)
    from sqlalchemy import select
    stmt = select(RedImg).where(RedImg.img_id == imgId).limit(1)
    slist = selectList(stmt)
    if slist is not None and len(slist) > 0:
        return slist[0]
    return None


if __name__ == '__main__':
    print(selectImgById("a9b9d0c0b79d4a66"))
