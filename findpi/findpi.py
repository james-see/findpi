"""Uses brand new features of Python 3"""
from concurrent.futures import ThreadPoolExecutor
import os
import sys
import time
from subprocess import check_output
start_time = time.time()

__version__ = "1.0.1"


def checker(ip_address):
    """
    checks if mac address found from nmap that matches raspberry pi
    Accepts: ip_address var as string
    Returns: nothing
    Prints: found ip of pi if found
    """
    data = check_output(f"nmap -sP {ip_address}", shell=True)
    if "B8:27:EB" in str(data):
        print(f'Found pi: {ip_address}')
    else:
        return
    return


logo = """
  ______ _____ _   _ _____  _____ _____
 |  ____|_   _| \ | |  __ \|  __ \_   _|
 | |__    | | |  \| | |  | | |__) || |
 |  __|   | | | . ` | |  | |  ___/ | |
 | |     _| |_| |\  | |__| | |    _| |_
 |_|    |_____|_| \_|_____/|_|   |_____|

"""


def main():
    # create as many threads as you want and set from terminal as parameter
    thread_count = 48
    limit = 1
    if not os.geteuid() == 0:
        sys.exit('This script must be run as root (or with \'sudo\')!')
    if len(sys.argv) > 1:
        thread_count = int(sys.argv[1])
    currentnum = 1
    userinput = input(
        'What net to check? (default 10.2.2.0/24): ') or '10.2.2.0/24'
    print(f'\nChecking for delicious pi around {userinput}...')
    if userinput.endswith('/24'):
        limit = 255
    if limit == 1:
        checkip = userinput.rsplit('.', 1)[0] + f'.{currentnum}'
        checker(checkip)
        print("--- %s seconds ---" % (time.time() - start_time))
        sys.exit(0)
    ip_list = []
    ip_list.extend([userinput.rsplit('.', 1)[0] +
                    f'.{i}' for i in range(limit)])
    with ThreadPoolExecutor(max_workers=thread_count) as executor:
        {executor.submit(checker, ip) for ip in ip_list}
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    print(logo)
    main()
