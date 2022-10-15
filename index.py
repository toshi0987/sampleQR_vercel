######### 2022.08.02 ########
###### sample QR Maker Web App v1

######
from flask import Flask, send_file, request, abort, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
import os
import sys
#from requests_oauthlib import OAuth1Session
import json
#from dotenv import load_dotenv
import pandas as pd
import datetime
#import psycopg2
import qrcode


###herokuデプロイ時###
#DATABASE_URL = os.environ['DATABASE_URL']
#conn = psycopg2.connect(DATABASE_URL, sslmode='require')

app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///test.db'#ローカル環境

#["DATABASE_URL"]はheroku側の環境変数
##以下　herokuデプロイ時必須##
"""
uri=os.getenv("DATABASE_URL")
if uri.startswith("postgres://"):
    uri=uri.replace("postgres://","postgresql://",1)
app.config['SQLALCHEMY_DATABASE_URI'] =uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
"""

db = SQLAlchemy(app)


###DB用クラス（csvファイル名一時的保存場所）###
class fileData(db.Model):
    id=db.Column(db.Integer,primary_key=True)#id
    filename=db.Column(db.String(200),nullable=False)#csvファイル名
    
### QRコード作成＆ファイル名返す ###
def makeQR_to_png(keyword,version,error_correction):
    
    d=datetime.datetime.now()
    filename=d.strftime('%Y%m%d-%H%M%S')

    FILE_PNG=filename+"qrcode.png"
    #QRオブジェクト？を作り直し（毎回）
    qr1=qrcode.QRCode(
        version=int(version),
        error_correction=qrcode.constants.ERROR_CORRECT_L
    )
    qr2=qrcode.QRCode(
        version=int(version),
        error_correction=qrcode.constants.ERROR_CORRECT_M
    )
    qr3=qrcode.QRCode(
        version=int(version),
        error_correction=qrcode.constants.ERROR_CORRECT_Q
    )
    qr4=qrcode.QRCode(
        version=int(version),
        error_correction=qrcode.constants.ERROR_CORRECT_H
    )
    ### 条件分岐 ###
    if int(error_correction)==1:
        qr=qr1
    elif int(error_correction)==2:
        qr=qr2
    elif int(error_correction)==3:
        qr=qr3
    else:
        qr=qr4



    qr.add_data(keyword)
    qr.make()
    img=qr.make_image()
    img.save(FILE_PNG)
    return FILE_PNG
    
    
@app.route("/")
def index():
    #return "hello world"
    
    return render_template("index.html")

@app.route("/export",methods=["POST","GET"])
def export_action():
    if request.method=="POST":
        if request.form["keyword"]!='' and request.form["version"]!='' and request.form["error_correction"]!='':
            keyword=request.form["keyword"]
            version=request.form["version"]
            error_correction=request.form["error_correction"]
        else:
            return redirect("/")
    else:
        return redirect("/")
    
    
    
    
    # 現在のディレクトリを取得
    #path = os.path.abspath(__file__)[:-7]
    ###別の関数でpngファイル作成後、filename取得###
    downloadfilename=makeQR_to_png(keyword,version,error_correction)
    
    
    
    return send_file(
        downloadfilename,
        as_attachment=True
    )
    """
    return send_file(
        downloadfilename,
        as_attachment=True,
        attachment_filename=downloadfilename,
    )"""









if __name__ == "__main__":
    #herokuデプロイ時
    #port=os.getenv("PORT")
    #app.run(host="0.0.0.0",port=port)
    ##ローカル環境##
    app.run(debug=False)