"""Uses brand new features of Python 3"""
import argparse
import threading
import psutil
from concurrent.futures import ThreadPoolExecutor
import os
import socket
import sys
import time
from getmac import get_mac_address
try:
    from __version__ import __version__
except ModuleNotFoundError:
    from findpi.__version__ import __version__


def getInput(currentip, thread_count):
    """
    Get user input ip address or use default.
    """
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
        executor.shutdown(wait=False)
    # always print the time it took to complete
    print("--- %s seconds ---" % (time.time() - start_time))


def prep():
    """
    Get the args and set them.
    """
    parser = argparse.ArgumentParser(description='Ways to run findpi.')
    parser.add_argument('-c', '--cores', type=int,
                        help='cores to use for threads', dest="cores")
    parser.add_argument('-v', '--version', action='version',
                        version=__version__)
    args = parser.parse_args()
    return args


def checksudo():
    if not os.geteuid() == 0:
        sys.exit(
            'This script must be run as root (or with \'sudo\' or \'doas\' etc.)!')


def getip():
    """
    get current ip hopefully and convert to /24
    """
    currentip = (([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(
        ("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0]
    currentip = currentip.rsplit('.', 1)[0] + '.0/24'
    return currentip


def checkCores():
    """
    Gets the total number of cores and returns sensible default int for threads
    """
    multiplier = 4  # set this to whatever you want
    try:
        cores = psutil.cpu_count() * multiplier
    except:
        print('Cannot get cores info, defaulting to 4')
        cores = 4
    return cores


def ThreadId(ipaddress, macaddress):
    """
    The thread function that gets called from checkMacs to ensure timeout.
    """
    macaddress = get_mac_address(ip=ipaddress)
    if macaddress:
        if ("b8:27:eb" in str(macaddress.lower())) or ("dc:a6:32" in str(macaddress.lower())):
            print(f'Found pi: {ipaddress}')


def checkMacs(ip_address):
    """
    Checks if mac address found using get_mac_address threaded function.
    Accepts: ip_address var as string
    Returns: nothing
    Prints: found ip of pi if found
    """
    macaddress = str()
    th = threading.Thread(target=ThreadId, args=(ip_address, macaddress))
    th.start()
    th.join(timeout=0.5)
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
    """
    Main function that runs everything.
    """
    args = prep()
    checksudo()
    currentIP = getip()
    if not args.cores:
        thread_count = checkCores()
    else:
        thread_count = args.cores
    getInput(currentIP, thread_count)


if __name__ == "__main__":
    print(logo)
    main()
