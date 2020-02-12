"""Uses brand new features of Python 3"""
from concurrent.futures import ThreadPoolExecutor
import os
import socket
import sys
import time
from subprocess import check_output


__version__ = "1.0.5"


def checkCores():
    """
    Gets the total number of cores and returns sensible default for threads
    """
    multiplier = 4  # set this to whatever you want
    operatingsystem = check_output("uname", shell=True)
    if "Darwin" in str(operatingsystem):
        cores = int(check_output("sysctl -n hw.ncpu", shell=True)) * multiplier
    else:
        cores = int(check_output("egrep 'cpu cores' /proc/cpuinfo | uniq | egrep -o '[0-9]'")) * multiplier
    return cores

def checkMacs(ip_address):
    """
    checks if mac address found from nmap that matches raspberry pi
    Accepts: ip_address var as string
    Returns: nothing
    Prints: found ip of pi if found
    """
    data = check_output(f"nmap -sP {ip_address}", shell=True)
    if ("B8:27:EB" in str(data)) or ("DC:A6:32" in str(data)):
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
    # get current ip hopefully and convert to /24
    currentip = (([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0]
    currentip = currentip.rsplit('.', 1)[0] + '.0/24'
    # set sensible default cores count or override from argv below
    thread_count = checkCores()
    limit = 1
    if not os.geteuid() == 0:
        sys.exit('This script must be run as root (or with \'sudo\')!')
    if len(sys.argv) > 1:
        thread_count = int(sys.argv[1])
    currentnum = 1
    userinput = input(
        f'What net to check? (default {currentip}): ') or currentip
    start_time = time.time()
    print(f'\nChecking for delicious pi around {userinput}...')
    if userinput.endswith('/24'):
        limit = 255
    if limit == 1:
        checkip = userinput.rsplit('.', 1)[0] + f'.{currentnum}'
        checkMacs(checkip)
        print("--- %s seconds ---" % (time.time() - start_time))
        sys.exit(0)
    ip_list = []
    # nice way to fill up the list with the full range
    ip_list.extend([userinput.rsplit('.', 1)[0] +
                    f'.{i}' for i in range(limit)])
    # multi-threading the modern way ;)
    with ThreadPoolExecutor(max_workers=thread_count) as executor:
        {executor.submit(checkMacs, ip) for ip in ip_list}
    # always print the time it took to complete
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    print(logo)
    main()
