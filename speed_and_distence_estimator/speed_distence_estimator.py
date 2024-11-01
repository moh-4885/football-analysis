import sys
import cv2
sys.path.append("../")
from utils import get_distence,get_foot
class SpeedDistence():
    def __init__(self):
        self.frame_window=5
        self.frame_rate=30
        
    def get_speed_distence(self,tracks):
        total_distence={}
        for track_name,track in tracks.items():
            if track_name!= "player":
                continue
            
            frames_number=len(track)
            for frame_number in range(0,frames_number,5):
                last_frame=min(frame_number+5,frames_number-1)
                for track_id,track_info in track[frame_number].items():
                    if track_id not in track[last_frame]:
                        continue                  
                    first_position=track[frame_number][track_id]["transformed_point"]
                    last_position=track[last_frame][track_id]["transformed_point"]
                    if last_position is None or first_position is None :
                        continue
                    distence_coverd=get_distence(first_position,last_position)
                    
                    time_elapsed =(last_frame-frame_number)/self.frame_rate
                    speed_meter_per_secound=distence_coverd/time_elapsed
                    speed_km=speed_meter_per_secound*3.6
                    
                    if track_name not in total_distence:
                        total_distence[track_name]={}
                    if track_id not in total_distence[track_name]:
                        total_distence[track_name][track_id]=0
                    total_distence[track_name][track_id]+=distence_coverd
                    for frame_numbe_batch in range(frame_number,last_frame):
                        if track_id not in track[frame_numbe_batch]:
                            continue
                        track[frame_numbe_batch][track_id]["distence"]= total_distence[track_name][track_id]
                        track[frame_numbe_batch][track_id]["speed"]= speed_km
    def draw_speed_distence_anotation(self,video_frames,tracks):
        out_frames=[]
        for frame_number,frame in enumerate(video_frames):
            
            for track_name,track in tracks.items():
                if track_name!="player":
                    continue
                for _,track_info in track[frame_number].items():
                    if "speed" not in track_info:
                        continue
                    speed=track_info.get("speed",None)
                    distence=track_info.get("distence",None)
                    if speed is None or distence is None:
                        continue
                    bbox=track_info.get("boxes")
                    position=get_foot(bbox)
                    position=list(position)
                    position[1]+=40
                    position=tuple(map(int,position))
                    cv2.putText(frame, f"{speed:.2f} km/h",position,cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),2)
                    cv2.putText(frame, f"{distence:.2f} m",(position[0],position[1]+20),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),2)
            out_frames.append(frame)
        return out_frames
                    
                        
                        
                
        