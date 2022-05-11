from pymongo import MongoClient
import jwt
import datetime as dt
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import timedelta
from datetime import datetime
import certifi
from bson.objectid import ObjectId

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
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"user_email": payload['id']})
        user_id = db.users.find_one({"user_email": payload['id']})['_id']
        user_followingInfo = db.users.find_one({"_id": user_id})
        feeds = []



        user_recommend = list(db.users.find({"_id": {'$nin': user_followingInfo['following']}}))
        for following in user_followingInfo["following"]:
            following_feed = db.feeds.find({"user_id": following})
            following_id = db.users.find_one({"_id": following}, {"_id":0, "user_email":0, "user_pw":0})
            for feed in following_feed:
                time_pass = {}
                a = datetime.now() - feed['feed_time']
                if a.days > 0:
                    time_pass['time'] = a.days
                    time_pass['unit'] = "일 전"
                else:
                    if a.seconds//3600 > 0:
                        time_pass['time'] = a.seconds//3600
                        time_pass['unit'] = "시간 전"
                    elif a.seconds//60 > 0:
                        time_pass['time'] = a.seconds//60
                        time_pass['unit'] = "분 전"
                    else:
                        time_pass['time'] = a.seconds
                        time_pass['unit'] = "초 전"
                feed.update(following_id)
                feed.update(time_pass)
                feeds.append(feed)
        return render_template('MainPage.html', users=user_info, feeds=feeds, recommends=user_recommend)

    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))

    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))

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
    following_receive = []
    follower_receive = []


    pw_receive = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()
    
    doc = {
        'user_email': email_receive,
        'user_name': name_receive,
        'user_id': id_receive,
        'user_pw': pw_receive,
        'user_picture': "../static/img/default_user.png",
        'following' : following_receive,
        'follower' : follower_receive
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


# 게시물 업로드 API
@app.route('/api/feedup', methods=['POST'])
def FeedUpReceive():
    token_receive = request.cookies.get('mytoken')
    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    user_info = db.users.find_one({"user_email": payload['id']})
    picture_receive = (request.form.getlist('picture_give'))
    contents_receive = request.form['contents_give']
    userID_receive = user_info['_id']

    doc = {
        'feed_picture': picture_receive,
        'feed_contents': contents_receive,
        'user_id': userID_receive,
        'feed_time': dt.datetime.utcnow()
    }
    db.feeds.insert_one(doc)
    return jsonify({'result': 'success', 'msg': '게시물이 업로드 되었습니다.'})

# 댓글 업로드 API
@app.route('/api/commentup', methods=['POST'])
def CommentUpReceive():
    token_receive = request.cookies.get('mytoken')
    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    user_info = db.users.find_one({"user_email": payload['id']})

    contents_receive = request.form['contents_give']
    feedID_receive = request.form['feedID_give']
    userID_receive = user_info['_id']
    userName_receive = user_info['user_id']

    doc = {
        'comment_contents': contents_receive,
        'comment_time': dt.datetime.utcnow(),
        'feed_id' : feedID_receive,
        'user_id': userID_receive,
        'user_name' : userName_receive
    }
    db.comments.insert_one(doc)
    return jsonify({'result': 'success', 'msg': '댓글이 등록되었습니다.'})

# MyPage API
@app.route('/api/mypage', methods=['POST'])
def MyPageReceive():


    userID_receive = ObjectId(request.form['userID_give'])
    print(userID_receive)
    user_info = db.users.find_one({"_id": userID_receive})

    print(user_info)

    return render_template('MyPage.html', user=user_info)

# 팔로우 API
@app.route('/api/follow', methods=['POST'])
def FollowReceive():
    token_receive = request.cookies.get('mytoken')
    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    user_info = db.users.find_one({"user_email": payload['id']})

    follower_receive = ObjectId(request.form['follower_give'])
    user_id = ObjectId(user_info['_id'])
    user_following = db.users.find_one({"_id": user_id})
    followingInfo=user_following['following']
    followingInfo.append(follower_receive)
    print(followingInfo)
    user_follower = db.users.find_one({"_id": follower_receive})
    followerInfo = user_follower['follower']
    followerInfo.append(user_id)
    print(followerInfo)
    print(db.users)
    db.users.update_one(
        {"_id": user_id},
        {"$set": {"following": list(followingInfo)}}
    )
    print(db.users)

    db.users.update_one(
        {"_id": follower_receive},
        {"$set": {"follower": list(followerInfo)}}
    )

    return jsonify({'result': 'success'})


# @app.route("/login", methods=["GET", "POST"])
@app.route("/signin", methods=["POST"])
def login_page():
    if request.method == "POST":
        user_id = request.form["user_id"]
        user_password = request.form["user_password"]
        user_password = hashlib.sha256(user_password.encode('utf-8')).hexdigest()
        id = db.users.find_one({"user_email": user_id})
        if id == None:
            return jsonify({'result': "fail", 'msg': '가입되지 않은 이메일입니다!'})
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
