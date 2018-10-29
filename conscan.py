"""Uses brand new features of Python 3"""

from concurrent.futures import ThreadPoolExecutor, as_completed
import sys
import time
from subprocess import check_output
start_time = time.time()

def checker(ip_address):
    # Your actual program here. Using threading.Lock() if necessary
    data = check_output(f"nmap -sP {ip_address}", shell=True)
    if "B8:27:EB" in str(data):
        print(f'Found pi: {ip_address}')
    else:
        return
    return 


def main():
    # create as many threads as you want and set from terminal as parameter
    thread_count = 48
    if len(sys.argv) > 1:
        thread_count = int(sys.argv[1])
    currentnum = 1
    macme = input('What network do you want to check? (10.2.2.0/24): ')
    if macme == '':
        macme = '10.2.2.0/24'
    if macme.endswith('/24'):
        limit = 255
    else:
        limit = 1
    if limit == 1:
        checkip = macme.rsplit('.', 1)[0] + f'.{currentnum}'
        data = check_output(f"nmap -sP {checkip}", shell=True)
        if "B8:27:EB" in str(data):
            print(f'Found pi: {macme}')
        else:
            pass
        print("--- %s seconds ---" % (time.time() - start_time))
        exit()
    else:
        ip_list = []
        while currentnum <= limit:
            checkip = macme.rsplit('.', 1)[0] + f'.{currentnum}'
            ip_list.append(checkip)
            currentnum = currentnum + 1
    with ThreadPoolExecutor(max_workers = thread_count) as executor: 
        futures = {executor.submit(checker, ip) for ip in ip_list}

        # as_completed() gives you the threads once finished
        for f in as_completed(futures):
            # Get the results 
            rs = f.result()
    print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == "__main__":
    main()
