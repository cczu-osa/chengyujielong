import pymysql
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('mysql+mysqlconnector://root:password@localhost/chengyu',
                       encoding='utf-8', echo=False, pool_size=100, pool_recycle=10)
Base = declarative_base()


# 定义User对象:
class Chengyu(Base):
    # 表的名字:
    __tablename__ = 'chengyu'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    py = Column(String(1024))   # 全拼音
    jumplink = Column(String(255))
    spy = Column(String(32))    # 首字拼音
    add_time = Column(DateTime, default=func.now())

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.name)


if __name__ == '__main__':
    # 创建DBSession类型:
    Base.metadata.create_all(engine)  # 创建表






# connection = pymysql.connect(host='localhost',
#                              port=3306,
#                              user='root',
#                              passwd='password',
#                              db='chengyu',
#                              charset='utf8mb4',
#                              cursorclass=pymysql.cursors.DictCursor)
#
# cursor = connection.cursor()
