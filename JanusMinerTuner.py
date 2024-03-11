import subprocess
import re

def get_core_info():
    try:
        args = "wmic cpu get NumberOfCores,NumberOfLogicalProcessors"
        
        # Run the command and capture its output
        output = subprocess.check_output(args, shell=True).decode().split('\n')
        
        # Extract the number of cores and logical processors from the second line
        parts = output[1].strip().split()
        if len(parts) == 2:
            core_count = int(parts[0])
            logical_processor_count = int(parts[1])
            return core_count, logical_processor_count
        
    except (subprocess.CalledProcessError, ValueError, IndexError):
        pass
    
    print("Failed to retrieve CPU core information.")
    return None, None

if __name__ == "__main__":
    core_count, logical_processor_count = get_core_info()
    if core_count is not None and logical_processor_count is not None:
        print("Number of CPU Cores:", core_count)
        print("Number of Logical Processors:", logical_processor_count)
    else:
        core_count = 8
        logical_processor_count = 16

    threadStart = 2
    threadEnd = logical_processor_count * 4
    pattern = r'\d+\.\d+'
    
    for i in range(threadStart, threadEnd+1, 2):
        args = 'janusminer-windows -h us.acc-pool.pw -p 12000 -u af80d9a79c09dca66c7da9f7e6f5cfd6f48804d46c785eac --gpus="0,1" -t ' + str(i)+ ' -q 2'
        print(args)

        process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        statusCounter = 0
        averageHash = 0
        for line in process.stdout:
            print(line)
            currentHash = 0
            if b"Total hashrate (CPU):" in line:
                statusCounter += 1
                currentHash = float(line.decode().split('(CPU): ')[1].split(' ')[0])

                if "kh/s" in line.decode():
                    currentHash = currentHash * 1000
                if "mh/s" in line.decode():
                    currentHash = currentHash * 1000000
                if "gh/s" in line.decode():
                    currentHash = currentHash * 1000000000
                if "th/s" in line.decode():
                    currentHash = currentHash * 1000000000000
                print (currentHash)
                
                averageHash = averageHash + currentHash
                print(averageHash)
                runningHash = averageHash / statusCounter
                print(runningHash)
                
