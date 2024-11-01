import pickle as pkl
import cv2
import numpy as np 
import sys
sys.path.append("../")
from utils import get_distence,dimensions
import os
class CameraMovementEstimatot():
    def __init__(self,frame):
        self.min_distence=5
        gray_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        mask=np.zeros_like(gray_frame)
        mask[:,0:20]=1
        mask[:,900:1050]=1
        
        self.lk_params = dict(
            winSize = (15,15),
            maxLevel = 2,
            criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT,10,0.03)
        )

        
        self.features = dict(
            maxCorners = 100,
            qualityLevel = 0.3,
            minDistance =3,
            blockSize = 7,
            mask = mask
        )
        
    def adjust_camera_movement(self,tracks,camera_movement_per_frame):
        for track_name,track in tracks.items():
            for frame_number,frame_trackes in enumerate(track):
                for track_id,track_info in frame_trackes.items():
                    position=tracks[track_name][frame_number][track_id]["position"]
                    camera_mov=camera_movement_per_frame[frame_number]
                    position_adjusted=(position[0]-camera_mov[0],position[1]-camera_mov[1])
                    tracks[track_name][frame_number][track_id]["position_adjusted"]=position_adjusted
        
    def get_camera_mov(self,frames,read_from_stub=False,stub_path=None):
        if read_from_stub and stub_path is not None and os.path.exists(stub_path):
            with open(stub_path,"rb") as f :
                camera_mov=pkl.load(f)
            return camera_mov
        camera_mov=[[0,0]]*len(frames)
        old_gray=cv2.cvtColor(frames[0],cv2.COLOR_BGR2GRAY)
        old_features=cv2.goodFeaturesToTrack(old_gray,**self.features)
        for frame_number in range(1,len(frames)):
            frame_gray=cv2.cvtColor(frames[frame_number],cv2.COLOR_BGR2GRAY)
            new_features,_,_=cv2.calcOpticalFlowPyrLK(old_gray,frame_gray,old_features,None,**self.lk_params)
            
            max_distence=0
            camera_mov_x,camera_mov_y=0,0
            for i ,(old,new) in enumerate(zip(old_features,new_features)):
                new_feature_point=new.ravel()
                old_feature_point=old.ravel()
                distence=get_distence(new_feature_point,old_feature_point)
                if distence>max_distence:
                    max_distence=distence
                    camera_mov_x,camera_mov_y=dimensions(old_feature_point,new_feature_point)
            if max_distence>self.min_distence:
                camera_mov[frame_number]=(camera_mov_x,camera_mov_y)
                old_features=cv2.goodFeaturesToTrack(frame_gray,**self.features)
            old_gray=frame_gray.copy()
        if stub_path is not None:
            with open(stub_path,"wb") as f :
                pkl.dump(camera_mov,f)
        return camera_mov
    def draw_camera_mov(self,frames,camera_mov):
        out_frames=[]
        for frame_num,frame in enumerate(frames):
            frame=frame.copy()
            overlay=frame.copy()
            cv2.rectangle(overlay,(0,0),(500,100),(255,255,255),-1)
            alpha=0.6
            cv2.addWeighted(overlay,alpha,frame,1-alpha,0,frame)
            camera_mov_x,camera_mov_y=camera_mov[frame_num]
            cv2.putText(frame,f"X Movement {camera_mov_x:.2f}",(10,30), cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),3)
            cv2.putText(frame,f"Y Movement {camera_mov_y:.2f}",(10,60), cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),3)
            out_frames.append(frame)
        return out_frames
        
            
                    
                
                
            
        