import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
from firebase_admin import db
import os
import cv2
import json
import datetime
import pytz
from detects import detectFunction

# Firebase 세팅 정보
cred = credentials.Certificate("./roomdentist-firebase-adminsdk-43dh8-cb3091c532.json")
PROJECT_ID = "roomdentist"
firebase_admin.initialize_app(cred, {
    'storageBucket': f"{PROJECT_ID}.appspot.com",
    'databaseURL': 'https://roomdentist-default-rtdb.firebaseio.com/'
})
# 버킷은 바이너리 객체의 상위 컨테이너이다. 버킷은 Storage에서 데이터를 보관하는 기본 컨테이너이다.
bucket = storage.bucket() # 기본 버킷 사용
print(" * Firebase Storage Setting Success")

dir = db.reference().child("users")
print(" * Firebase Realtime Database Setting Success")

def downloadImage(uid, imageNum):
    source_blob_name = f"users/{uid}/{todayDate()}/{imageNum}.png" # 유저의 uid에서 오늘 날짜의 이미지 번호를 소스로 지정
    destination_file_name = f"./images/{uid}/{todayDate()}/{imageNum}.png" # 로컬 폴더의 저장 위치 지정
    createFolder(f"./images/{uid}/{todayDate()}/results")
    blob = bucket.blob(source_blob_name) # blob형태로 다운
    blob.download_to_filename(destination_file_name) # 다운받은 파일을 지정한 로컬 폴더에 저장
    imagePath = f"./images/{uid}/{todayDate()}" # openCV로 다운받은 이미지 불러오기
    dentalResults = detectFunction(imagePath, uid, imageNum) # detect 함수로 이미지와 imageNum 전달 후 결과 이미지 return
    
    uploadDatabase(uid, imageNum, dentalResults)
    return uploadImage(uid, imageNum)

def uploadImage(uid, imageNum):
    source_blob_name = f"users/{uid}/{todayDate()}/results/{imageNum}.png" # Remote 폴더, 유저의 uid에서 오늘 날짜의 이미지 번호를 소스로 지정
    source_file_name = f"./images/{uid}/{todayDate()}/results/{imageNum}.png" # 로컬 폴더의 저장 위치
    blob = bucket.blob(source_blob_name)
    blob.upload_from_filename(source_file_name)
    return True # 성공하면 True return

def uploadDatabase(uid, imageNum, dentalResults):
    dir.child(uid).child("results").child(f"{todayDate()}").child(f"{imageNum}").update(dentalResults)

def todayDate():
    dt_now = datetime.datetime.now(pytz.timezone('Asia/Seoul'))
    return dt_now.date()
 
def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)

    