from ultralytics import YOLO
import cv2

model=YOLO("models/best.pt")

# cap=cv2.VideoCapture(r"input data\08fd33_4.mp4")
# while True:
#     sec,image=cap.read()
#     results=model(image,stream=True)
#     for result in results:
#         boxes=result.boxes
#         for box in boxes:
#             x1,y1,x2,y2=box.xyxy[0]
#             x1,y1,x2,y2=int(x1),int(y1),int(x2),int(y2)
#             cv2.rectangle(image,(x1,y1),(x2,y2),color=(0,0,255),thickness=3)
#     cv2.namedWindow('image', cv2.WINDOW_NORMAL)   
#     cv2.resizeWindow('image', 800, 600)   
#     cv2.imshow("image",image)
#     cv2.waitKey(1)
result=model.predict(r"input data\08fd33_4.mp4",save=True)
# print(result)
            

# print("hello world")