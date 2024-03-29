import subprocess
from datetime import datetime

def get_memory_usage():
    output = subprocess.run(["free", "-m"], capture_output=True, text=True)
    used_mem = output.stdout.split("\n")[1].split()[2]
    return int(used_mem)


memory_usage = get_memory_usage()
if memory_usage > 3000:
    with open("logs.txt", "a") as log:
        log.write("\nmemory usage is: ", memory_usage , "server restarted at: ", datetime.now())
    subprocess.run(["shutdown", "-r", "now"])