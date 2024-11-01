import sys
sys.path.append("../")
from utils import get_distence,get_center
class Playerball():
    def __init__(self):
        self.max_player_distence=70
    def assign_player_ball(self,players_track,ball):
        ball_x_center,ball_y_center=get_center(ball)
        min_distence=99999
        assigned_player=-1
        for player_id ,player in players_track.items():
            player_box=player["boxes"]
            left_distence=get_distence((player_box[0],player_box[-1]),(ball_x_center,ball_y_center))
            right_distence=get_distence((player_box[2],player_box[-1]),(ball_x_center,ball_y_center))
            distence=min(left_distence,right_distence)
            if distence< self.max_player_distence:
                if distence<min_distence:
                    min_distence=distence
                    assigned_player=player_id
        return assigned_player
                