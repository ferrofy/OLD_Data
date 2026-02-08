import subprocess
import sys

Files = [
    ["Advanvce Calculator" , "Advance_Calculator"],
    ["ChatBot" , "ChatBot"],
    ["Mouse Tracker" , "Mouse_Tracker"],
    ["QR Code Maker" , "QR_Code"],
    ["Spammer" , "Spammer"],
    ["Video Converter" , "Video_Converter"],
    ["Worm" , "Worm"],
    ["YT PlayList" , "YT_Playlist_Info"],
]

while True:

    print("\nTYPE THE NUMBER FOR THE FILE YOU WANT TO RUN\n")

    for Index in range(len(Files)):
        print(f"[{Index}] ---> {Files[Index][0]}")

    print("[999] ---> Exit")

    File_To_Run = int(input("What You Want To Run ---> "))

    if File_To_Run == 999:
        print("Exiting....")
        break

    if 0 <= File_To_Run < len(Files):
        subprocess.run([sys.executable, f"{Files[File_To_Run][1]}/Main.py"])
    else:
        print("Wrong Input.... Try Again...")

