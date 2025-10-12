"""Uses brand new features of Python 3"""
import argparse
import threading
import psutil
from concurrent.futures import ThreadPoolExecutor
import os
import socket
import sys
import time
import platform
from getmac import get_mac_address
try:
    from __version__ import __version__
except ModuleNotFoundError:
    from findpi.__version__ import __version__


def getInput(currentip, thread_count):
    """
    Get user input ip address or use default.
    Supports CIDR notation for different subnet sizes.
    """
    userinput = input(
        f'What net to check? (default {currentip}): ') or currentip
    start_time = time.time()
    print(f'\nChecking for delicious pi around {userinput}...')

    # Parse CIDR notation
    if '/' in userinput:
        network_part, cidr_part = userinput.split('/')
        try:
            cidr = int(cidr_part)
        except ValueError:
            print("Invalid CIDR notation, defaulting to /24")
            network_part = userinput
            cidr = 24
    else:
        # Assume /24 if no CIDR provided
        network_part = userinput
        cidr = 24

    if cidr < 24:
        print(f"Warning: Large subnet /{cidr} may take a long time to scan")
    elif cidr > 30:
        print(f"Small subnet /{cidr} - checking single host")

    # Calculate number of hosts to scan
    host_bits = 32 - cidr
    limit = 2 ** host_bits - 2  # Exclude network and broadcast addresses

    if limit <= 0:
        # Single host scan
        checkMacs(network_part)
        print("--- %s seconds ---" % (time.time() - start_time))
        return

    # Generate IP list
    base_ip = network_part.rsplit('.', 1)[0]
    start_host = 1 if cidr >= 24 else 0  # Start from .1 for /24+, .0 for larger subnets
    ip_list = [f"{base_ip}.{i}" for i in range(start_host, limit + start_host + 1)]

    # Multi-threading the modern way ;)
    with ThreadPoolExecutor(max_workers=thread_count) as executor:
        {executor.submit(checkMacs, ip) for ip in ip_list}
        executor.shutdown(wait=False)
    # Always print the time it took to complete
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
    # os.getuid() seems to be only in linux/unix systems, if platform is 'Windows' just skip the check sudo
    if platform.system() == 'Windows':
        return
    
    if not os.geteuid() == 0:
        sys.exit(
            'This script must be run as root (or with \'sudo\' or \'doas\' etc.)!')


def getip():
    """
    Get current IP address and convert to /24 subnet.
    Returns the current network in CIDR notation.
    """
    try:
        # Try to get IP from hostname resolution
        hostname_ips = socket.gethostbyname_ex(socket.gethostname())[2]
        for ip in hostname_ips:
            if not ip.startswith("127."):
                return ip.rsplit('.', 1)[0] + '.0/24'
    except (socket.gaierror, IndexError):
        pass

    # Fallback: connect to external DNS server to get local IP
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 53))
            local_ip = s.getsockname()[0]
            return local_ip.rsplit('.', 1)[0] + '.0/24'
    except (OSError, IndexError):
        pass

    # Final fallback
    return "192.168.1.0/24"


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
        mac_lower = str(macaddress.lower())
        # Raspberry Pi MAC address prefixes for all models
        pi_prefixes = [
            "b8:27:eb",  # Raspberry Pi 1, 2, 3, Zero (original)
            "dc:a6:32",  # Raspberry Pi 3, Zero W, Pi 5, Zero 2 W
            "e4:5f:01",  # Raspberry Pi 4, 400
        ]
        if any(prefix in mac_lower for prefix in pi_prefixes):
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
