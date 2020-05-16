import hashlib
import pymysql
import xml.etree.cElementTree as et
import muban
from time import time
from flask import redirect,abort,url_for,Flask,render_template,request

db = pymysql.connect(host="localhost", user="root", \
                     password="genius", database="dict", charset="utf8")
cur = db.cursor()

app = Flask(__name__)

def DoQuery(word):
    sql_sen="select interpret from words where word='%s'"%word
    print(sql_sen)
    try:
        cur.execute(sql_sen)
    except Exception as e:
        print(e)
        db.connect()
        cur.execute(sql_sen)
    interpret=cur.fetchone()
    if interpret:
        result=interpret[0].split("。")
        print("result count is %d"%len(result))
        return result[0]
    else:
        return "找不到这个单词"

@app.route('/')
def index():
    user = { 'nickname': '天才' } # fake user
    posts = [ # fake array of posts
        {
            'author': { 'nickname': 'John' },
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': { 'nickname': 'Susan' },
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template("index.html",
        title = 'Home',
        user = user,
        posts = posts)

@app.route('/wx',methods=['GET','POST'])
def wx():
    if request.method=='GET':
        signiture=request.args.get('signiture')
        timestamp=request.args.get('timestamp')
        echostr=request.args.get('echostr')
        nonce=request.args.get('nonce')
        token='louiswoo'
        if len(request.args)==0:
            return "hello, this is handle view!!!"
        list=[token,timestamp,nonce]
        list.sort()
        s=list[1]+list[0]+list[2]
        hashcode=hashlib.sha1(s.encode('utf8')).hexdigest()
        if hashcode==signiture:
            print(request.data)
            return echostr
        else:
            print('wechat verify failed!')
            return ""

    elif request.method=='POST':
        xmldata=request.data
        print(xmldata)
        xml_rec=et.fromstring(xmldata)

        ToUserName = xml_rec.find('ToUserName').text
        fromUser = xml_rec.find('FromUserName').text
        MsgType = xml_rec.find('MsgType').text
        MsgId = xml_rec.find('MsgId').text

        if MsgType=='text':
            Content = xml_rec.find('Content').text
            intepret=DoQuery(Content)
            if intepret==None:
                intepret='找不到这个单词！'
            ret_str = muban.replay_muban('text') % (fromUser,ToUserName,int(time()),intepret)
            return ret_str

        elif MsgType=='voice':
            Recognition = xml_rec.find('Recognition').text
            ret_str = muban.replay_muban('text') % (fromUser,ToUserName,int(time()),Recognition)
            return ret_str

if __name__=='__main__':
    app.run(host='0.0.0.0',port=80,debug=True)