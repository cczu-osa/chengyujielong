from flask import Flask, make_response, jsonify, render_template, request
from models import Chengyu
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('mysql+mysqlconnector://root:password@localhost/chengyu',
                       encoding='utf-8', echo=False, pool_size=100, pool_recycle=10)
Base = declarative_base()
DBSession = sessionmaker(bind=engine)


app = Flask(__name__)

import json
from handler import AlchemyEncoder


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/search', methods=['GET'])
def test():
    key = request.args.get('key')
    print(key)
    session = DBSession()
    data = session.query(Chengyu).filter(Chengyu.spy == key).all()
    print(data)
    res = {'data':[]}
    for i in data:
        temp = json.dumps(i, cls=AlchemyEncoder)
        temp = json.loads(temp)
        res['data'].append(temp)
    res['status'] = 0
    res['count'] = len(res['data'])
    print(res)
    return render_template('index.html', chengyu=res)
    # return make_response(jsonify(res))


if __name__ == '__main__':
    app.run(port=8000)
    # test()
