'''
2020/1/25
donke
'''

from flask import session, jsonify, request, url_for, redirect
from flask import Flask, make_response, render_template

from models import Chengyu
from sqlalchemy import func
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import os
import json
from pypinyin import lazy_pinyin
from handler import AlchemyEncoder

from datetime import timedelta

app = Flask(__name__)
# app.config['SECRET_KEY'] = os.urandom(24)  # 设置为24位的字符,每次运行服务器都是不同的，所以服务器启动一次上次的session就清除。
app.config['SECRET_KEY'] = 'hsifhs@o3id.h**o&vxd.-cv*pp#sdl'    # session key
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)  # 设置session的保存时间。

engine = create_engine('mysql+mysqlconnector://root:password@localhost/chengyu',
                       encoding='utf-8', echo=False, pool_size=100, pool_recycle=10)
Base = declarative_base()
DBSession = sessionmaker(bind=engine)


@app.route('/')
def hello_world():
    ip = request.remote_addr
    session.permanent = True  # 默认session的时间持续31天
    session['ip'] = ip
    session['is_login'] = True
    print(ip)
    return render_template('index.html')


@app.route('/search')
def test():
    if not session.get('is_login'):
        return redirect(url_for('hello_world'))
    key = request.args.get('key')
    key = lazy_pinyin(key)[0]
    print(key)
    db_session = DBSession()
    page_index = 1
    data = db_session.query(Chengyu).filter(Chengyu.spy == key).limit(50).offset((page_index-1)*50).all()
    print(data)
    res = {"data": []}
    for i in data:
        temp = json.dumps(i, cls=AlchemyEncoder)
        temp = json.loads(temp)
        res["data"].append(temp)
    res["status"] = 0
    res["count"] = db_session.query(Chengyu).filter(Chengyu.spy == key).count()
    res["respNum"] = len(data)
    print(res)
    return render_template('index.html', chengyu=res)
    # return make_response(jsonify(res))


@app.route('/json/test/<int:pn>/', methods=['GET'])
def json_test(pn=1):
    db_session = DBSession()
    page_index = pn
    data = db_session.query(Chengyu).filter(Chengyu.spy == 'ce').limit(50).offset((page_index - 1) * 50).all()
    res = {"data": []}
    for i in data:
        temp = json.dumps(i, cls=AlchemyEncoder)
        temp = json.loads(temp)
        res["data"].append(temp)
    return make_response(jsonify(res))


if __name__ == '__main__':
    app.run(port=8000)
    # test()
