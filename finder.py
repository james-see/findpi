"""Get ip addresses of Raspberry Pi devices on network super fast using threading."""
"""
Author: James Campbell
Date: 29 October 2018
"""

import queue
import threading
from subprocess import check_output
import sys, os
import time
start_time = time.time()

#define a worker function
def worker(queue_item):
    queue_full = True
    while queue_full:
        try:
            #get your data off the queue, and do some work
            ip_address = queue_item.get(False)
            try:
                data = check_output(f"nmap -sP {ip_address}", shell=True)
            except Exception as e:
                print('errored')
                return

            # pi at time of writing has these first three for Mac Address
            if "B8:27:EB" in str(data):
                print(f'Found pi: {ip_address}')
            queue_item.task_done()

        except queue.Empty:
            queue_full = False

            



def main():
    # create as many threads as you want and set from terminal as parameter
    thread_count = 64
    if not os.geteuid() == 0:
        sys.exit('This script must be run as root (or with \'sudo\')!')
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
            print(f'{macme} is not a pi device')
        print("--- %s seconds ---" % (time.time() - start_time))
        exit()
    else:
        ip_list = []
        while currentnum <= limit:
            checkip = macme.rsplit('.', 1)[0] + f'.{currentnum}'
            ip_list.append(checkip)
            currentnum = currentnum + 1
    ip_queue = ip_list
    q = queue.Queue()
    for ip in ip_queue:
        q.put(ip)

    for i in range(thread_count):
        t = threading.Thread(target=worker, args = (q,))
        t.start()
    q.join()
    print("--- %s seconds ---" % (time.time() - start_time))
if __name__ == "__main__":
    main()
    
    
