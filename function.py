from utils import GetChengYu
from models import Chengyu
from pypinyin import pinyin, lazy_pinyin

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

engine = create_engine('mysql+mysqlconnector://root:password@localhost/chengyu',
                       encoding='utf-8', echo=False, pool_size=100, pool_recycle=10)

import time

'''因为报错导致缺少150个成语'''


def db_init():
    data = []
    CY = GetChengYu()
    for i in range(1445, 1447):
        print(i)
        res = CY.get_data(cur_page_num=i)
        # print(data)
        if not res:
            print('---------跳过----------', i)
        try:
            res = res['data'][0]['result']
            for cy in res:
                # print(cy)
                cy = Chengyu(
                    name=cy['ename'],
                    py=''.join(lazy_pinyin(cy['ename'])),
                    spy=lazy_pinyin(cy['ename'])[0],
                    jumplink=cy['jumplink']
                )
                data.append(cy)
                # print(len(data), end=' ')
            if len(data) > 100:
                DBSession = sessionmaker(bind=engine)
                session = DBSession()
                session.add_all(data)
                session.commit()
                print(data)
                data.clear()
                print('clear')
                print(data)
                time.sleep(1)
        except Exception as e:
            print(str(e))
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    session.add_all(data)
    session.commit()
    session.close()

if __name__ == '__main__':
    db_init()
