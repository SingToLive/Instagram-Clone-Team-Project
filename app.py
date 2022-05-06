
from flask import Flask, render_template, request, jsonify, session

import hashlib
from pymongo import MongoClient

import certifi

client = MongoClient('mongodb+srv://test:sparta@cluster0.qttfj.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=certifi.where())
db = client.dbsparta

app = Flask(__name__)
app.secret_key = "SPARTA"

# 로그인메인
@app.route('/')
def login():
    # session.pop('user_id')
    if "user_id" in session:
        return render_template('MainPage.html')
    else:
        print('kk')
        return render_template("LoginPage.html")

#메인페이지
@app.route('/MainPage')
def main():
    return render_template('MainPage.html')

#메인페이지
@app.route('/SignInPage')
def SignIn():
    return render_template('SignInPage.html')

# 회원가입API
@app.route('/api/signup', methods=['POST'])
def SignUp():

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


@app.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        user_id = request.form["user_id"]
        user_password = request.form["user_password"]
        user_password = hashlib.sha256(user_password.encode('utf-8')).hexdigest()
        id = db.users.find_one({"user_id": user_id})
        if id == None:
            return jsonify({'result': "fail", 'msg': '가입되지 않은 아이디입니다!'})
        else:
            if id["user_pw"] != user_password:
                return jsonify({'result': "fail", 'msg': '잘못된 비밀번호입니다!'})
            else:
                session['user_id'] = request.form['user_id']
                return jsonify({'result': "success", 'msg': '로그인 되었습니다!'})


# @app.route('/logout/')
# def logout():
#     session.clear()
#     return redirect(url_for('main.index'))

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)