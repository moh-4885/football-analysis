import cv2
import numpy as np 

class ViewTransformer():
    def __init__(self):
        court_width=68
        court_length=23.32
        self.pixel_vertices = np.array([[110, 1035], 
                               [265, 275], 
                               [910, 260], 
                               [1640, 915]],dtype=np.float32)
        
        self.target_vertices = np.array([
            [0,court_width],
            [0, 0],
            [court_length, 0],
            [court_length, court_width]
        ],dtype=np.float32)
        self.precpective_transformers=cv2.getPerspectiveTransform(self.pixel_vertices,self.target_vertices)
    def transform_point(self,point):
        x,y=int(point[0]),int(point[1])
        is_in=cv2.pointPolygonTest(self.pixel_vertices,(x,y),False) >0
        if not is_in:
            return None
        reshaped_point=point.reshape(-1,1,2)
        new_position=cv2.perspectiveTransform(reshaped_point,self.precpective_transformers)
        return new_position.reshape(-1,2)
        
    def add_transformed_point(self,tracks):
        for track_name,track in tracks.items():
            for frame_number,frame_track in enumerate(track):
                for track_id,track_info in frame_track.items():
                    adjusted_point=track_info["position_adjusted"]
                    point=np.array(adjusted_point,dtype=np.float32)
                    transformed_point=self.transform_point(point)
                    if transformed_point is not None:
                        transformed_point=transformed_point.squeeze().tolist()
                        
                    tracks[track_name][frame_number][track_id]["transformed_point"]=transformed_point
                        