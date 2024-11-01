from utils import save_video,read_video
from trackers import Tracker
from team_assinger import Teamassign
from assign_player_ball import Playerball
from camera_movement import CameraMovementEstimatot
from view_transformer import ViewTransformer
from speed_and_distence_estimator import SpeedDistence
# import json
import cv2
def main():
    frames=read_video("input data/08fd33_4.mp4")
    tracker=Tracker("models/best.pt")
    tracked=tracker.get_object_track(frames,read_from_stub=True,stub_path="stubs/tracker.pkl")
    
    ball_tracked=tracked["ball"]
    # print(ball_tracked)
    tracked["ball"]=tracker.ball_interpolation(ball_tracked)
    tracker.add_position_track(tracked)
    
 
    # get camera Movement between frames         
    cammera_mov_estim=CameraMovementEstimatot(frames[0])   
    camera_movs_per_frame=cammera_mov_estim.get_camera_mov(frames,read_from_stub=True,stub_path="stubs/camera_movement.pkl")  
    cammera_mov_estim.adjust_camera_movement(tracked,camera_movs_per_frame)
    
    #transform the positon relative to the court
    transformer=ViewTransformer()
    transformer.add_transformed_point(tracked)
    
    SpeedDistenceEstimator=SpeedDistence()
    SpeedDistenceEstimator.get_speed_distence(tracked)
    # print(tracked["player"])
    frames=SpeedDistenceEstimator.draw_speed_distence_anotation(frames,tracked)
    

    frames=cammera_mov_estim.draw_camera_mov(frames,camera_movs_per_frame)
    #get each player team 
    assigner=Teamassign()
    assigner.get_team_color(frames[0],tracked["player"][0])
    for frame_number,players_in_frame in enumerate(tracked["player"]):
        for player_id,player in players_in_frame.items():
            player_team=assigner.get_player_team(frames[frame_number],player["boxes"],player_id)
            tracked["player"][frame_number][player_id]["team"]=player_team
            tracked["player"][frame_number][player_id]["team_color"]=assigner.team_colors[player_team]
       
    playerball=Playerball()      
    ball_control=[2]
    for frame_num,frame_players in enumerate(tracked["player"]):
        ball_box=tracked["ball"][frame_num][1]["bbox"]
        player_with_ball=playerball.assign_player_ball(frame_players,ball_box)
        if player_with_ball !=-1:
            tracked["player"][frame_num][player_with_ball]["has_ball"]=True
            ball_control.append(tracked["player"][frame_num][player_with_ball]["team"])
        else :
            ball_control.append(ball_control[-1])
            
            
    anotated_frames=tracker.draw_anotations(frames,tracked,ball_control)
     
    save_video(anotated_frames,"out_data/out_video.avi")
    
    
    
    
    # for k,v in assigner.team_colors.items():
    #     print(f"team {k} is assigned to color {v}")

    # this code is to croppe image
    # for track_id,player in  tracked["player"][0].items():
    #     boxes=player["boxes"]
    #     frame=frames[0]
    #     cropped_frame=frame[int(boxes[1]):int(boxes[3]),int(boxes[0]):int(boxes[2])]
    #     cv2.imwrite("out_data/cropped_image.jpg",cropped_frame)
    #     break
    
if __name__=="__main__":
    main()