import subprocess

ps_command = "cd / && mkdir Test"

subprocess.run(
        ["powershell", "-WindowStyle", "Hidden", "-Command", ps_command],
        creationflags=subprocess.CREATE_NO_WINDOW
)