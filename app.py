from pymongo import MongoClient
import jwt
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import certifi

client = MongoClient('mongodb+srv://test:sparta@cluster0.qttfj.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=certifi.where())
db = client.InstarClone

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/profile_pics"
app.secret_key = "SPARTA"
SECRET_KEY = 'SAJOSAJO'

# 로그인메인
@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    print(token_receive)
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        return render_template('MainPage.html')
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))
    # session.pop('user_id')
    # if "user_id" in session:
    #     return render_template('MainPage.html')
    # else:
    #     return render_template("LoginPage.html")

@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('LoginPage.html', msg=msg)

#메인페이지
@app.route('/MainPage')
def main():
    return render_template('MainPage.html')

#마이페이지
@app.route('/MyPage')
def MyPage():
    return render_template('MyPage.html')

#페이지이동
@app.route('/page')
def page():
    name = request.args.get('name')
    return render_template(name+'.html')

#회원가입페이지
@app.route('/SignUpPage')
def SignUp():
    return render_template('SignUpPage.html')

# 회원가입API
@app.route('/api/signup', methods=['POST'])
def SignUpReceive():

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

    id = db.users.find_one({"user_id": id_receive})
    if id == None:
        pass
    else:
        return jsonify({'result': 'fail', 'msg': '중복된 아이디입니다!'})
    if not (email_receive and name_receive and id_receive and pw_receive):
        return jsonify({'result': 'fail', 'msg': '모두 입력해주세요!'})

    else:
        db.users.insert_one(doc)
        return jsonify({'result': 'success', 'msg': '회원가입 되었습니다!'})


# @app.route("/login", methods=["GET", "POST"])
@app.route("/signin", methods=["POST"])
def login_page():
    if request.method == "POST":
        user_id = request.form["user_id"]
        user_password = request.form["user_password"]
        user_password = hashlib.sha256(user_password.encode('utf-8')).hexdigest()
        id = db.users.find_one({"user_email": user_id})
        if id == None:
            return jsonify({'result': "fail", 'msg': '가입되지 않은 아이디입니다!'})
        else:
            if id["user_pw"] != user_password:
                return jsonify({'result': "fail", 'msg': '잘못된 비밀번호입니다!'})
            else:
                # session['user_id'] = request.form['user_id']
                payload = {
                    'id': user_id,
                    'exp': datetime.utcnow() + timedelta(seconds=60 * 10)  # 로그인 10분 유지
                }
                token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
                return jsonify({'result': "success",'token': token, 'msg': '로그인 되었습니다!'})


# @app.route('/logout', methods=["GET"])
# def logout():
#     # session.pop('user_id')
#     return jsonify({'msg': '로그아웃 되었습니다!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
