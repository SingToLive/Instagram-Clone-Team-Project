from flask import Flask, render_template, request, jsonify, redirect
import hashlib
import datetime
import jwt
from pymongo import MongoClient
client = MongoClient('localhost',27017)
db = client.sijosijo

SECRET_KEY = 'SPARTA'

app = Flask(__name__)

# 로그인메인
@app.route('/')
def home():
    return render_template('SignUpPage.html')

# 회원가입API
@app.route('/api/signup', methods=['POST'])
def signup():

    email_receive = request.form['email_give']
    name_receive = request.form['name_give']
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    pw_receive = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    doc = {
        'user_email': email_receive,
        'user_name': name_receive,
        'user_id': id_receive,
        'user_pw': pw_receive
    }

    if not (email_receive and name_receive and id_receive and pw_receive):
        return jsonify({'result': 'fail', 'msg': '모두 입력해주세요!'})

    else:
        db.users.insert_one(doc)
        return jsonify({'result': 'success', 'msg': '회원가입 되었습니다!'})

@app.route('/login')
def login():
    return render_template('LoginPage.html')

# @app.route('/signup')
#
# # 로그인API
# @app.route('/api/login', methods=['POST'])
# def login():
#     email_receive = request.form['email_give']
#     pw_receive = request.form['pw_give']
#
#     pw_receive = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()
#
#     doc = {
#         'user_email': email_receive,
#         'user_pw': pw_receive
#     }
#
#     db.users.find_one(doc)
#
#     if doc is not None:
#         paylod = {
#             'user_email': email_receive,
#             'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=5)
#         }
#         token = jwt.encode(paylod, SECRET_KEY, algorithm='HS256')
#
#         return jsonify({'result': 'success', 'token': token, 'msg': '로그인되었습니다!'})
#     else:
#         return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})
#
#
# @app.route('/api/nick', methods=['GET'])
# def api_valid():
#     token_receive = request.cookies.get('mytoken')
#
#     try:
#         payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
#         print(payload)
#
#         doc = db.user.find_one({'user_email': payload['user_email']}, {'_user_email': 0})
#         return jsonify({'result': 'success', 'user_id': doc['user_id']})
#     except jwt.ExpiredSignatureError:
#         # 위를 실행했는데 만료시간이 지났으면 에러가 납니다.
#         return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})
#     except jwt.exceptions.DecodeError:
#         return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})



if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
