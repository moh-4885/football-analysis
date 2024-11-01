def get_center(bbox):
    x1, y1, x2, y2 = bbox

    return int((x1+x2)/2), int((y1+y2)/2)

def get_width(bbox):
    x1, _, x2, _ = bbox
    return x2 - x1

def get_height(bbox):
    _, y1, _, y2 = bbox
    return y2 - y1
def get_distence(p1,p2):
    return((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)**0.5

def dimensions(p1,p2):
    return p1[0]-p2[0],p1[1]-p2[1]
def get_foot(bbox):
    x1, y1, x2, y2 = bbox
    return int((x1+x2)/2),int(y2)
    