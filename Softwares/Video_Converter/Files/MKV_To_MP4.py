import os
import subprocess
from tkinter import Tk, filedialog, messagebox
import imageio_ffmpeg

def Find_Ffmpeg():
    Ffmpeg_Path = imageio_ffmpeg.get_ffmpeg_exe()
    if os.path.isfile(Ffmpeg_Path):
        return Ffmpeg_Path
    return None

def Convert():
    Root = Tk()
    Root.withdraw()
    
    Ffmpeg_Path = Find_Ffmpeg()
    
    if Ffmpeg_Path is None:
        messagebox.showerror("Ffmpeg Not Found", "Automatic Ffmpeg Install Failed")
        return
    
    Input_File_Paths = filedialog.askopenfilenames(
        title="Select Mkv Files",
        filetypes=[("MKV Files", "*.mkv")]
    )
    
    if Input_File_Paths == "":
        return
    
    Downloads_Path = os.path.join(os.path.expanduser("~"), "Downloads")
    
    for Input_File_Path in Input_File_Paths:
        File_Name = os.path.splitext(os.path.basename(Input_File_Path))[0]
        Output_File_Path = os.path.join(Downloads_Path, File_Name + ".mp4")
        
        Command = [
            Ffmpeg_Path,
            "-i", Input_File_Path,
            "-c", "copy",
            Output_File_Path
        ]
        
        subprocess.run(Command)
    
    messagebox.showinfo("Success", "All Conversions Completed Successfully")