import subprocess

args = 'janusminer-windows -h us.acc-pool.pw -p 12000 -u af80d9a79c09dca66c7da9f7e6f5cfd6f48804d46c785eac --gpus="0,1" -t 36 -q 16'

while 1:

    process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    for line in process.stdout:
        print(line)
        if b"Thread#0: 0.000000 h/s" in line:
            process.terminate()

    for line in process.stderr:
        print(line)
