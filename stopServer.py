import os
import signal
from pathlib import Path

import utils


def stop():
    path = Path("famdb.pid")
    if path.exists():
        file = open("famdb.pid")
        pid = int(list(file)[0])
        serverRunning = utils.isPidRunning(pid)
        if serverRunning:
            os.kill(pid, signal.SIGKILL)
            os.remove("famdb.pid")
            return
        else:
            print('FATAL:PID file detected, but no running process found')
    return
