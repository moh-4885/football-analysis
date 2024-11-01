from ultralytics import YOLO
import supervision as sv
import pickle
import pandas as pd
import os
import cv2
import sys
import numpy as np
sys.path.append("../")
from utils import get_center,get_width,get_foot
class Tracker():
    
    def __init__(self,model_path) :
        self.model=YOLO(model_path)
        self.tracker=sv.ByteTrack()
    def ball_interpolation(self,ball_tracker):
        tracked=[x.get(1,{}).get("bbox",[]) for x in ball_tracker]
        tracked_df=pd.DataFrame(tracked,columns=["x1","y1","x2","y2"])
        tracked_df=tracked_df.interpolate()
        tracked_df=tracked_df.bfill()
        interpolated_object=[{1:{"bbox":x}} for x in tracked_df.to_numpy().tolist()]
        return interpolated_object
        
 

    def detect_frame(self,frames):
        batch_size=20
        detections=[]
        for i in range(0,len(frames),batch_size):
            batch_detections=self.model.predict(frames[i:i+batch_size])
            detections+=batch_detections
            
        return detections
    def get_object_track(self,frames,read_from_stub=False,stub_path=None):
        if read_from_stub and stub_path is not None and os.path.exists(stub_path):
            with open(stub_path,"rb") as f :
                tracker=pickle.load(f)
            return tracker
        #to save the trckes in each frame 
        tracker={"player":[],
                 "referee":[],
                 "ball":[]
                 }
        detections=self.detect_frame(frames)
        # print(detections[0].names)

            
        for frame_number,frame_detection in enumerate(detections):
            class_names=frame_detection.names
            class_names_inv={name:id for id,name in class_names.items()}
            #convert in to a supervision format 
            detection_supervision=sv.Detections.from_ultralytics(frame_detection)
            # bcz goalkeeper detection is not accurate we treat the goalkepper as a player and changing it id to a player id
            for i ,id in enumerate(detection_supervision.class_id):
                if class_names[id]=="goalkeeper":  
                    detection_supervision.class_id[i]=class_names_inv["player"]
            #track the frame 
            detection_tracked=self.tracker.update_with_detections(detection_supervision)
            tracker["player"].append({})
            tracker["referee"].append({})
            tracker["ball"].append({})
            for tracked_detetion in detection_tracked:
                
                boxes=tracked_detetion[0]
                class_id=tracked_detetion[3]
                traked_id=tracked_detetion[4]
                if class_id==class_names_inv["player"]:
                    tracker["player"][frame_number][traked_id]={"boxes":boxes}
                if class_id==class_names_inv["referee"]:
                    tracker["referee"][frame_number][traked_id]={"boxes":boxes}
            for frame_detection in detection_supervision:
                bbox = frame_detection[0].tolist()
                cls_id = frame_detection[3]

                if cls_id == class_names_inv['ball']:
                    tracker["ball"][frame_number][1] = {"bbox":bbox}
        if stub_path is not None :
            with open(stub_path,"wb") as f:
                pickle.dump(tracker,f)
            print("Tracker saved .")
        return tracker
    def add_position_track(self,tracks):
        for track_name,track in tracks.items():
            for frame_number,frame_track in enumerate(track):
                for track_id,track_info in frame_track.items():
                    if track_name=="ball":
                        boxes=track_info.get("bbox")
                        position=get_center(boxes)
                    else :
                        boxes=track_info.get("boxes")
                        position=get_foot(boxes)
                    tracks[track_name][frame_number][track_id]["position"]=position
    def draw_ellipse(self,frame,box,color,track_id=None):
         y2=int(box[3])
         
         x_center,_=get_center(box)
         width=get_width(box)
         cv2.ellipse(frame,center=(x_center,y2),axes=(int(width),int(0.35*width)),angle=0,startAngle=-45,endAngle=245,color=color,thickness=2,lineType=cv2.LINE_4)
         if track_id is not None:   
            rectangle_width=40
            rectangle_height=20
            x1_rect=x_center-rectangle_width//2
            y1_rect=(y2-rectangle_height//2)+15
            x2_rect=x_center+rectangle_width//2
            y2_rect=(y2+rectangle_height//2)+15
            cv2.rectangle(frame,(x1_rect,y1_rect),(x2_rect,y2_rect),color,cv2.FILLED)
            x_text=x1_rect+12
            if track_id>99:
                x_text=x_text-10
            y_text=y1_rect+15
            cv2.putText(frame,f"{track_id}",(int(x_text),int(y_text)),cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,0,0),2)
         
         
         
         return frame 
    def draw_traingle(self,frame,bbox,color):
        y= int(bbox[1])
        x,_ = get_center(bbox)

        triangle_points = np.array([
            [x,y],
            [x-10,y-20],
            [x+10,y-20],
        ])
        cv2.drawContours(frame, [triangle_points],0,color, cv2.FILLED)
        cv2.drawContours(frame, [triangle_points],0,(0,0,0), 2)
        return frame
    def draw_ball_control(self,frame,frame_number,ball_control):
        overlay=frame.copy()
        
        cv2.rectangle(overlay,(1350,850),(1900,970),(255,255,255),-1)
        alpha=0.4
        cv2.addWeighted(overlay,alpha,frame,1-alpha,0,frame)
        team1=ball_control[:frame_number+1].count(1)
        team2=ball_control[:frame_number+1].count(2)
        team1_control=team1/(team1+team2)
        team2_control=team2/(team1+team2)
        cv2.putText(frame,f"Team 1 ball control {team1_control*100:.2f}%",(1400,900),cv2.FONT_HERSHEY_SIMPLEX,1, (0,0,0), 3)
        cv2.putText(frame,f"Team 2 ball control {team2_control*100:.2f}%",(1400,950),cv2.FONT_HERSHEY_SIMPLEX,1, (0,0,0), 3)
        return frame
        
        
    def draw_anotations(self,frames,tracker,ball_control):
        output_frames=[]
        for frame_number,frame in enumerate(frames):
            frame=frame.copy()
            players=tracker["player"][frame_number]
            referees=tracker["referee"][frame_number]
            ball=tracker["ball"][frame_number]
            for player_id , player in players.items():
                color=player.get("team_color",(0,0,255))
                frame=self.draw_ellipse(frame,player["boxes"],color,player_id)
                if player.get("has_ball",False):
                    frame=self.draw_traingle(frame,player["boxes"],(0,0,255))
                
            for _ , referee in referees.items():
                frame=self.draw_ellipse(frame,referee["boxes"],(0,255,255))
                
            for _ , ball in ball.items():
                
                frame=self.draw_traingle(frame,ball["bbox"],(0,255,0))
            frame=self.draw_ball_control(frame,frame_number,ball_control)
            
            output_frames.append(frame)
        return output_frames                
            
        