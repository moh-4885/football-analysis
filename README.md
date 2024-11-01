## Video Analysis System for Football Analytics
This project is a video analysis system designed to detect and track players, referees, and footballs using the YOLO object detection model. This system integrates various sports analytics concepts to analyze gameplay and provide insights into team and player performance.

## Project Overview
The goal of this project is to develop a comprehensive video analysis tool that addresses key elements in sports analytics. By leveraging the YOLO object detection model, K-means clustering, optical flow, and perspective transformation, the system provides metrics such as ball acquisition percentage, player speed, and distance covered in meters.

## Key Features
- Real-time detection and tracking of players, referees, and footballs.
- Team assignment using K-means clustering on pixel color data.
- Ball possession analysis to calculate ball acquisition percentages.
- Player movement analysis using optical flow.
- Perspective transformation for accurate distance measurement and tracking.
  <br>
  
![Screenshot](screeshot/screenshot.png)

## Model Architecture
This system is based on the YOLO object detection architecture with additional features for sports analytics, including:

- YOLO Backbone: Used for object detection.
- K-means Clustering: Classifies detected players into teams.
- Optical Flow: Analyzes player movement over time.
- Perspective Transformation: Converts pixel distances into real-world measurements (in meters)

## Dataset 
<a href="https://universe.roboflow.com/roboflow-jvuqo/football-players-detection-3zvbc/dataset/1">dataset used in training</a>
<br>
<a href="https://drive.google.com/file/d/1p5zOOXvMuXkOo-Na8OoVy1XOp1T9zb_G/view?usp=sharing">the video used in constraction</a>
