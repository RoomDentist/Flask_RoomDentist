import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage

from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin
from OpenSSL import SSL
import datetime as dt
import logging, ssl

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)
api = Api(app)


if __name__ == '__main__':
    # Firebase 세팅 정보
    cred = credentials.Certificate("/home/bixbycrew/workspace/RoomDentist/roomdentist-firebase-adminsdk-43dh8-cb3091c532.json")
    PROJECT_ID = "roomdentist"
    firebase_admin.initialize_app(cred, {
        'storageBucket': f"{PROJECT_ID}.appspot.com"
    })

    # 버킷은 바이너리 객체의 상위 컨테이너이다. 버킷은 Storage에서 데이터를 보관하는 기본 컨테이너이다.
    bucket = storage.bucket() # 기본 버킷 사용
    print(" * Firebase 설정 완료")

    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    cert = '/home/bixbycrew/workspace/Cert/cert.pem'
    pkey = '/home/bixbycrew/workspace/Cert/privkey.pem'
    chainkey = '/home/bixbycrew/workspace/Cert/fullca.pem'
    context.load_verify_locations('/home/bixbycrew/workspace/Cert/fullca.pem')
    context.load_cert_chain(cert, pkey)
    app.run(debug=True, host='0.0.0.0', port=6000, ssl_context=context)
