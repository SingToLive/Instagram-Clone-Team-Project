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


def mainInfo(Info):
    token_receive = request.cookies.get('mytoken')
    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    if Info == "user_info":
        user_info = db.users.find_one({"user_email": payload['id']})
        return user_info
    elif Info == "feeds":
        user_id = db.users.find_one({"user_email": payload['id']})['_id']
        user_followingInfo = db.users.find_one({"_id": user_id})
        feeds = []
        for following in user_followingInfo["following"]:
            following_feed = db.feeds.find({"user_id": following})
            following_id = db.users.find_one({"_id": following}, {"user_email":0, "user_pw":0})
            print(following_id)
            print(type(following_id))
            key_toChange = following_id.pop("_id")
            following_id["follower_id"] = key_toChange
            for feed in following_feed:
                # 시간
                time_pass = past_time_cal(feed['feed_time'])
                #댓글리스트
                feed_info = feed["_id"]
                comments_info = db.comments.find({"feed_id": str(feed_info)})
                comment_info = {}
                i = 0
                for info in comments_info:
                    comment_time = past_time_cal(info['comment_time'])
                    commenter_img = db.users.find_one({"_id":info["user_id"]})["user_picture"]
                    info.update({"commenter_img":commenter_img})
                    info.update(comment_time)
                    comment_info[i] = info
                    i+=1
                comment_dic = {}
                comment_dic["comments"] = comment_info
                feed.update(comment_dic)
                #팔로잉
                feed.update(following_id)
                #게시글 시간
                feed.update(time_pass)
                feeds.append(feed)
        return feeds
    elif Info == "user_recommend":
        user_id = db.users.find_one({"user_email": payload['id']})['_id']
        user_followingInfo = db.users.find_one({"_id": user_id})
        user_recommend = list(db.users.find({"_id": {'$nin': user_followingInfo['following']}}))
        return user_recommend

def past_time_cal(time):
    time_pass = {}
    # a = datetime.now() - feed['feed_time']
    a = datetime.now() - time
    if a.days > 0:
        time_pass['time'] = a.days
        time_pass['unit'] = "일 전"
    else:
        if a.seconds // 3600 > 0:
            time_pass['time'] = a.seconds // 3600
            time_pass['unit'] = "시간 전"
        elif a.seconds // 60 > 0:
            time_pass['time'] = a.seconds // 60
            time_pass['unit'] = "분 전"
        else:
            time_pass['time'] = a.seconds
            time_pass['unit'] = "초 전"
    return time_pass