from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import INTEGER,CHAR
from sqlalchemy import create_engine,Column

import json
import datetime


def insert(data):
    engine = create_engine('postgresql+psycopg2://postgres:password@localhost/pair',
                           encoding='utf-8', echo=False, pool_size=100, pool_recycle=10)
    Base = declarative_base()
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    if type(data) == type([]):
        session.add_all(data)
    else:
        session.add(data)

    session.commit()
    session.close()


from sqlalchemy.ext.declarative import DeclarativeMeta


class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data)  # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:  # 添加了对datetime的处理
                    if isinstance(data, datetime.datetime):
                        fields[field] = data.strftime(u"%Y/%m/%d %H:%M:%S")
                    elif isinstance(data, datetime.date):
                        fields[field] = data.strftime(u"%Y/%m/%d %H:%M:%S")
                    elif isinstance(data, datetime.timedelta):
                        fields[field] = (datetime.datetime.min + data).time().strftime(u"%Y/%m/%d %H:%M:%S")
                    else:
                        fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)