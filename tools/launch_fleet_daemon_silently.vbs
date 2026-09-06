Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = "C:\Users\jibra\Desktop\1\digitalcreatoravi"
WshShell.Run "python tools\fleet_command_server.py", 0, False
