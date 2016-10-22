import subprocess
import sys

import stopServer


def run():
    if len(sys.argv) == 1:
        print("provide start or stop")
        return
    command = sys.argv[1]
    if command == "start":
        subprocess.Popen(["python3", "startServer.py"], stdout=subprocess.DEVNULL)
    if command == "stop":
        stopServer.stop()


run()
