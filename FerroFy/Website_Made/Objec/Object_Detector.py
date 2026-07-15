import cv2
from ultralytics import YOLO

class Object_Detector:
    def __init__(self, Model_Name='yolov8n.pt'):
        self.Model = YOLO(Model_Name)
    
    def Process_Frame(self, Frame):
        Results = self.Model(Frame, verbose=False)
        Annotated_Frame = Results[0].plot()
        
        return Annotated_Frame
