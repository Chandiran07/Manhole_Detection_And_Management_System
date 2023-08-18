import cv2
from cvzone.SerialModule import SerialObject
from twilio.rest import Client
import keys as k
client = Client(k.account_sid,k.auth_token)
#img = cv2.imread('manhole_open.jpeg')
cap = cv2.VideoCapture(0)
cap.set(3,648)
cap.set(4,480)
classNames=['manhole_closed','manhole_open']
'''
classFile = 'coco.names'
with open(classFile,'rt') as f:
    classNames = f.read().rstrip('n').split('n')
'''
configPath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
weigthsPath = 'frozen_inference_graph.pb'
ESP =SerialObject('COM3')
net = cv2.dnn_DetectionModel(weigthsPath,configPath)
net.setInputSize(250,320)
net.setInputScale(1.0/130)
net.setInputMean((130, 130,130))
net.setInputSwapRB(True)
while True:

    success,img = cap.read()
    classIds, confs, bbox = net.detect(img, confThreshold=0.5)

    if len(classIds)!=0:
        for classID,confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):

            if classID==85 :
                cv2.rectangle(img, box, color=(0, 0, 255), thickness=2)
                cv2.putText(img,classNames[0].upper(),(box[0]+10,box[1]+30),
                        cv2.FONT_HERSHEY_COMPLEX,1,(0,0,0),2)
                print(classIds, bbox)
                ESP.sendData([0])
                '''
                msg = client.messages.create(
                    body='MANHOLE IS CLOSED',
                    from_=k.twilio_number,
                    to=k.target_number
                )
                '''
            elif classID==70:
                cv2.rectangle(img, box, color=(0, 0, 255), thickness=2)
                cv2.putText(img, classNames[1].upper(), (box[0] + 10, box[1] + 30),
                            cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
                print(classIds, bbox)
                ESP.sendData([1])
                msg = client.messages.create(
                    body='MANHOLE IS OPEN',
                    from_=k.twilio_number,
                    to=k.target_number
                )

    cv2.imshow('OUTPUT',img)
    cv2.waitKey(1)
