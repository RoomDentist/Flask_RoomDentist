import cv2

def detect(image, imageNum):
    # dentalImage = cv2.imread(image) # 이미지 읽어오기
    cv2.imwrite(f"./images/{imageNum}_result.jpg", image)
    
    print("Success")
    return {"Gold": 5, "Amalgam": 10, "Cavity": 3}