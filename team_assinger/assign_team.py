from sklearn.cluster import KMeans
class Teamassign():
    def __init__(self):
        self.team_colors={}
        self.players_team={}
    def get_cluster_model(self,image):
        kmeans=KMeans(n_clusters=2,init="k-means++",random_state=0)
        reshpaed_image=image.reshape(-1,3)
        kmeans.fit(reshpaed_image)
        return kmeans
        pass
    def get_player_color(self,frame,box):
        cropped_frame=frame[int(box[1]):int(box[3]),int(box[0]):int(box[2])]
        first_half=cropped_frame[0:int(cropped_frame.shape[0]//2),:]
        #get the cluster model
        kmeans=self.get_cluster_model(first_half)

        clusterd_image=kmeans.labels_.reshape(first_half.shape[0],first_half.shape[1])
        cornor_label=[clusterd_image[0,0],clusterd_image[-1,0],clusterd_image[0,-1],clusterd_image[-1,-1]]
        background_label=max(set(cornor_label),key=cornor_label.count)
        player_label=1-background_label
        player_shirt_color=kmeans.cluster_centers_[player_label]
        return player_shirt_color
        
        
    def get_team_color(self,frame,player_track):
        players_color=[]
        for _,player in player_track.items():
            box=player["boxes"]
            player_color=self.get_player_color(frame,box)
            players_color.append(player_color)
        # print(players_color)
        kmeans=kmeans=KMeans(n_clusters=2,init="k-means++",random_state=42)
        kmeans.fit(players_color)
        self.kmeans=kmeans
        self.team_colors[1]=kmeans.cluster_centers_[0]
        self.team_colors[2]=kmeans.cluster_centers_[1]
    def get_player_team(self,frame,player_box,player_id):
        if player_id in self.players_team:
            return self.players_team[player_id]
        
        if player_id==84 or player_id==125:
            team_id=2
            self.players_team[player_id]=team_id
            return team_id
        player_shirt_color=self.get_player_color(frame,player_box)
        team_id=self.kmeans.predict(player_shirt_color.reshape(1,-1))[0]
        team_id+=1
        self.players_team[player_id]=team_id
        return team_id