import os
runs=0
while True:
    c=os.popen("python3 server.py").read()
    if "KeyboardInterrupt" in c:
        exit()
    runs+=1
    print(runs)
