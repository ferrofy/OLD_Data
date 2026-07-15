import customtkinter as Ctk
from PIL import Image, ImageTk
import cv2

class Camera_View(Ctk.CTkFrame):
    def __init__(self, Master, **Kwargs):
        super().__init__(Master, **Kwargs)
        
        self.Title_Label = Ctk.CTkLabel(self, text="Real-Time Object Detection", font=Ctk.CTkFont(size=24, weight="bold"))
        self.Title_Label.pack(padx=20, pady=(20, 10))
        
        self.Video_Label = Ctk.CTkLabel(self, text="")
        self.Video_Label.pack(padx=20, pady=10, fill="both", expand=True)
        
    def Update_Frame(self, Cv_Image):
        Rgb_Image = cv2.cvtColor(Cv_Image, cv2.COLOR_BGR2RGB)
        Pil_Image = Image.fromarray(Rgb_Image)
        Tk_Image = ImageTk.PhotoImage(image=Pil_Image)
        
        self.Video_Label.configure(image=Tk_Image)
        self.Video_Label.image = Tk_Image
