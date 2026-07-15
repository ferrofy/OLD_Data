import customtkinter as Ctk
import cv2
from Object_Detector import Object_Detector
from Camera_View import Camera_View

class Main_App(Ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("AI Object Detection")
        self.geometry("900x700")
        
        Ctk.set_appearance_mode("dark")
        Ctk.set_default_color_theme("blue")
        
        self.Camera_Component = Camera_View(self)
        self.Camera_Component.pack(fill="both", expand=True)
        
        self.Detector = Object_Detector()
        
        self.Cap = cv2.VideoCapture(0)
        
        self.Update_Loop()
        
    def Update_Loop(self):
        Ret, Frame = self.Cap.read()
        
        if Ret:
            Processed_Frame = self.Detector.Process_Frame(Frame)
            self.Camera_Component.Update_Frame(Processed_Frame)
            
        self.after(10, self.Update_Loop)
        
    def On_Closing(self):
        self.Cap.release()
        self.destroy()

if __name__ == "__main__":
    App = Main_App()
    App.protocol("WM_DELETE_WINDOW", App.On_Closing)
    App.mainloop()
