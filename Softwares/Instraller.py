import subprocess

Command_To_Run = ""

Python_Lib = ["sympy", "numpy", "pandas", "pyautogui", "keyboard", "yt-dlp", "qrcode[pil]","imageio-ffmpeg"]
# C_Files = [["FerroFy\\C\\Basic_Math.c", "FerroFy\\C\\DLL\\Basic_Math.dll"]]

for i in range(len(Python_Lib)):
    print(f"Downloading ----> {Python_Lib[i]} [ Please Wait This May Take While ]")
    Command_To_Run = f"pip install {Python_Lib[i]}"

    Process = subprocess.run(
        Command_To_Run,
        shell=True,
        capture_output=True,
        text=True
    )

    print(f"Done Downloading ----> {Python_Lib[i]}")

# for j in range(len(C_Files)):
#     Source_File = C_Files[j][0]
#     Output_Dll = C_Files[j][1]

    # print(f"Building DLL From ----> {Source_File}")

    # Command_To_Run = f"gcc {Source_File} -shared -o {Output_Dll}"

    # Process = subprocess.run(
    #     Command_To_Run,
    #     shell=True,
    #     capture_output=True,
    #     text=True
    # )
    # print(f"Done Building DLL ----> {Output_Dll}")

print(Process.stdout)
print(Process.stderr)
