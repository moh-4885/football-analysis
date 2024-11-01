import cv2
import os 
def read_video(video_path):
    
    if not os.path.exists(video_path):
        print(f"Error: File '{video_path}' not found.")
        return []

    cap = cv2.VideoCapture(video_path)
    frames = []

    while True:
        sec, frame = cap.read()
        if not sec:  
            break
        frames.append(frame)
    # print(frames)
    cap.release() 
    return frames

def save_video(video_frames, out_path):
    if not video_frames:
        print("Error: No video frames to save.")
        return

    frame_height, frame_width = video_frames[0].shape[:2]

    # print(frame_height,frame_width)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(out_path, fourcc, 30, (frame_width, frame_height))

    for frame in video_frames:
        # print("1")
        out.write(frame)
   
    out.release() 
    print(f"Video saved to {out_path}")