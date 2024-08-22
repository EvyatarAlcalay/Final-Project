import os.path
import os
import threading
import time

import cv2
import torch
import numpy as np
from ultralytics import YOLOWorld
from gtts import gTTS
from playsound import playsound
from Line import Line
from Vertex import Vertex

class LivePicture:
    #system constants
    ROOT = "Hang The Picture According To The Istructions"
    DETECTION_MODEL = "yolov8s-worldv2.pt"
    FINISH_TIME = 5.0
    #target circle
    RADIUS_OF_TARGET_CIRCLE = 5
    RED = (0,0,204)
    ERROR_RANGE = 0.05
    ERROR_PIXEL = 5
    #constants of text to speech
    TURN_RIGHT = "move right"
    TURN_LEFT = "move left"
    TURN_DOWN = "move down"
    TURN_UP = "move up"
    TILT_LEFT = "tilt left"
    TILT_RIGHT = "tilt right"
    REACH_DESTINATION = "stop!"
    #bbox constans
    OBJECTS_TO_DETECT = ["picture", "card", "poster", "postcard", "paper"]
    GREEN = (51, 153, 51)
    #text color
    BLUE = (255,0,0)
    #device
    DEVICE_INTERNAL = 0
    DEVICE_EXTERNAL = 1

    
    def __init__(self, target_point, wall_corner_points_vertex, direction = Line.HORIZONTAL):
        """
        initialize the Live picture window.
        :param yolo_model_path: the name of the model
        :param target_point: the point we aim to hang it the picture
        """
        # Initialize the YOLO model
        self.model = YOLOWorld(LivePicture.DETECTION_MODEL, verbose=False)
        
        # Check if GPU is available and use it if possible (for improving performance)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        self.model.set_classes(LivePicture.OBJECTS_TO_DETECT)

        #the point we want to hang there th picture
        self.target_point = target_point

        # selected points on the wall
        self.wall_corner_points_vertex = wall_corner_points_vertex

        # hang direction text (move left, move right, etc...)
        self.hang_directions = ""

        #detected line for tilting
        self.longest_line = []
        self.debug = False

        #last detected objects and the detection time :[ [x, y, time.time()]...]
        self.last_detected = []

        # setup picture durection (horizonlat or vertical)
        self.direction = direction
        print("direction", self.direction)

        # application exit
        self.end_run = False
        self.done = False
        self.timer = None        

    
    def detect_objects(self, frame):
        """
        :param frame: the current frame of the video
        :return: the objects which were detected
        """
        # Run the YOLO model on the frame
        results = self.model(frame, verbose=False)
        return results

    def detect_edges(self, region_of_interests, low_threshold=100, high_threshold=200):
        """
        This function is using an algorithm (named canny) to detect the edge of the picture
        :param region_of_interests: param to Canny
        :param low_threshold: param to Canny
        :param high_threshold: param to Canny
        :return: the corners of the picture
        """
        # Use Canny edge detection
        edges = cv2.Canny(region_of_interests, low_threshold, high_threshold)
        return edges
    
    def create_tts(self,text):
        """
        This function is creating TTS and play it
        :param text: The text that you want to convert to audio
        """
        language = 'en' # Language in which you want to convert
        if not os.path.isfile(f"./audio/{text}.mp3"):
            myobj = gTTS(text=text, lang=language, slow=False) #initialize
            myobj.save(f"./audio/{text}.mp3") # Saving the converted audio in a mp3 file
        playsound(f"./audio/{text}.mp3")  # Playing the converted file

    def direct_each_frame(self,processed_frame, center_point_bbox, y_left, y_right):
        """
        This function in each frame tell what to do: move left, move up, stop an etc.
        :param center_point_bbox: the center point of the bbox we created along the picture
        :param y_left: the left side of the longer line of the picture
        :param y_right: the right side of the longer line of the picture
        :return: how to move (with sound and text)
        """
        # if current position was detected, do nothing
        if self.done == True: return
        text = ""
        tts_sound = ""
        if self.debug: print("direction" , center_point_bbox, y_left, y_right)
        p_left, _1, p_right, _2 = self.wall_corner_points_vertex
        #text to speech - MOVING
        if center_point_bbox.x < self.target_point.x*(1-LivePicture.ERROR_RANGE):
            tts_sound = LivePicture.TURN_RIGHT
            text = LivePicture.TURN_RIGHT
        elif center_point_bbox.x > self.target_point.x*(1+LivePicture.ERROR_RANGE):
            tts_sound = LivePicture.TURN_LEFT
            text = LivePicture.TURN_LEFT
        elif center_point_bbox.y < self.target_point.y*(1-LivePicture.ERROR_RANGE):
            tts_sound = LivePicture.TURN_DOWN
            text = LivePicture.TURN_DOWN
        elif center_point_bbox.y > self.target_point.y*(1+LivePicture.ERROR_RANGE):
            tts_sound = LivePicture.TURN_UP
            text = LivePicture.TURN_UP
        #text to speech - TILTING
        elif y_left > y_right+LivePicture.ERROR_PIXEL:  # y_left/y_right > p_left.y/p_right.y *1.02: 
            if self.direction == Line.VERTICAL:
                tts_sound = LivePicture.TILT_LEFT
                text = LivePicture.TILT_LEFT    
            else:
                tts_sound = LivePicture.TILT_RIGHT
                text = LivePicture.TILT_RIGHT
        elif y_left < y_right-LivePicture.ERROR_PIXEL:  #y_left/y_right * 1.2 < p_left.y/p_right.y:
            if self.direction == Line.VERTICAL:
                tts_sound = LivePicture.TILT_RIGHT
                text = LivePicture.TILT_RIGHT
            else:
                tts_sound = LivePicture.TILT_LEFT
                text = LivePicture.TILT_LEFT
        else:
            tts_sound = LivePicture.REACH_DESTINATION
            text = LivePicture.REACH_DESTINATION
            self.done = True

        self.hang_directions = text
        if self.hang_directions != "":
            cv2.putText(processed_frame, self.hang_directions, (50, 70), cv2.FONT_HERSHEY_SIMPLEX,
                        2, LivePicture.BLUE, 3)        
        self.create_tts(tts_sound)

        #exit after finish
        if self.done == True and self.timer == None:
            self.timer = threading.Timer(interval=LivePicture.FINISH_TIME, function=self.end_program)
            self.timer.start()


    def end_program(self):
        """
        end program
        :return: boolean
        """
        self.end_run = True

    def detect_line_direction(self, x1, y1, x2, y2, tolerance=10):
        """_summary_

        Args:
            x1 (_type_): x of left line point 
            y1 (_type_): y of left line point 
            x2 (_type_): x of right line point 
            y2 (_type_): y of right line point 
            tolerance (int, optional): _description_. Defaults to 10.

        Returns:
            _type_: Line constance horizontal, vertical or uknown 
        """
        if abs(y2-y1) <= tolerance :return Line.HORIZONTAL
        if abs(x2-x1) <= tolerance :return Line.VERTICAL
        return Line.UNKNOWN

    def find_longest_cv_line(self, edges):
        """
        this function is finding the long line of the picture we detect
        :param edges: the corners of the picture
        :return: the longest line
        """
        longest_line = None
        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=50, minLineLength=20, maxLineGap=10)
        if lines is None:
            return None
        
        #filter lines
        orthogonal_lines = []  #lines which are horizontals or verticals
        for line in lines:
            x1, y1, x2, y2 = line[0]
            direction = self.detect_line_direction(x1, y1, x2, y2)
            if self.direction == Line.HORIZONTAL and direction == Line.HORIZONTAL:
                orthogonal_lines.append(line)
            elif self.direction == Line.VERTICAL and direction == Line.VERTICAL:
                orthogonal_lines.append(line)

        if len(orthogonal_lines) == 0: return None
        longest_line = max(orthogonal_lines, key=lambda line: np.linalg.norm([line[0][2]-line[0][0], line[0][3]-line[0][1]]))
      
        return longest_line
    
    def process_frame(self, frame):
        """
        analyze the detection and activate the directions according to the analyze
        :param frame: the frame of the video
        :return: the frame
        """
        results = self.detect_objects(frame)
        count = 0
        for detection in results:
            boxes = detection.boxes
            for box in boxes:
                
                x_min = int(box.xyxy[0][0].item())
                y_min = int(box.xyxy[0][1].item())
                x_max = int(box.xyxy[0][2].item())
                y_max = int(box.xyxy[0][3].item())

                width_box = int(box.xywh[0][2].item())
                height_box = int(box.xywh[0][3].item())
                center_point_bbox = Vertex(x_min+width_box/2, y_min+height_box/2)
                
                now = time.time() * 1000
                skip_detection = False
                object_found = False
                
                # check if it was detected
                for d in self.last_detected:
                    if d[0] == center_point_bbox.x and d[1] == center_point_bbox.y:
                        object_found = True
                        if now - d[2] >= 10:
                            skip_detection = True
                        else:
                            d[2] = now
                if skip_detection == True:
                    continue
                if object_found == False:
                    self.last_detected.append([center_point_bbox.x, center_point_bbox.y, now])
                    
                count = count + 1
                #print("class id", box.cls.item(), "class name = ", LivePicture.OBJECTS_TO_DETECT[int(box.cls.item())])
                
                # Extract the region of interest (ROI)
                region_of_interest = frame[y_min:y_max, x_min:x_max]
                gray_region_of_interest = cv2.cvtColor(region_of_interest, cv2.COLOR_BGR2GRAY)

                # Detect edges
                edges = self.detect_edges(gray_region_of_interest)

                # find the longest line
                longest_line = self.find_longest_cv_line(edges)
                # Draw contours on the ROI
                if longest_line is not None:
                    x1, y1, x2, y2 = longest_line[0]
                    self.longest_line = longest_line[0]

                    if self.direction == Line.HORIZONTAL:
                        self.direct_each_frame(frame, center_point_bbox, y1, y2)
                    else:   #vertical picture
                        self.direct_each_frame(frame, center_point_bbox, x1, x2)
                    if self.debug: cv2.line(frame,(int(x1),int(y1)),(int(x2),int(y2)),thickness=2,color=(0,0,0))
                    
                cv2.rectangle(frame, (int(x_min), int(y_min)),
                              (int(x_max), int(y_max)), LivePicture.GREEN, 2)
                # Overlay the region_of_interest with edges and contours back to the frame
                frame[y_min:y_max, x_min:x_max] = region_of_interest

        if count == 0:
            self.hang_directions = "cannot detect"
        cv2.circle(frame,(self.target_point.x,self.target_point.y),LivePicture.RADIUS_OF_TARGET_CIRCLE,LivePicture.RED,
                       8,cv2.FILLED, 0)
        return frame


def run_YOLO(target_point, wall_corner_points_vertex, direction):
    """
    This Function run the live picture
    """
    
    detector = LivePicture(target_point, wall_corner_points_vertex, direction)

    # Capture video from the webcam
    video = cv2.VideoCapture(LivePicture.DEVICE_EXTERNAL)

    while True:
        ret, frame = video.read()
        if not ret:
            break

        # Process the frame to detect objects and edges
        processed_frame = detector.process_frame(frame)

        if detector.hang_directions != "":
            cv2.putText(processed_frame, detector.hang_directions, (50, 70), cv2.FONT_HERSHEY_SIMPLEX,
                        2, LivePicture.BLUE, 3)
        if detector.debug and len(detector.longest_line) == 4:
            x1, y1, x2, y2 = detector.longest_line
            cv2.line(frame,(int(x1),int(y1)),(int(x2),int(y2)),thickness=2,color=(0,0,0))
        # Display the processed frame
        cv2.imshow(LivePicture.ROOT, processed_frame)

        # Break the loop if 'q' is pressed
        if detector.end_run or cv2.waitKey(1) & 0xFF == ord('q') or cv2.waitKey(1) & 0xFF == ord('q') :
            break

    # Release the video capture object
    video.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    run_YOLO(Vertex(439, 142), [(385, 139), (582, 15), (394, 478), (639, 475)], Line.VERTICAL)
    