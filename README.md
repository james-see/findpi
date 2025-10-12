# findpi

## What

Find all the Raspberry Pi devices on your network really fast using multithreading in Python 3.8+ and find them fast. Supports all Raspberry Pi models including Pi 5, Pi 4, Pi 3, Pi Zero 2 W, and more.

## Stats

Ok, so to compare this to just running nmap vs. findpi:

|               | run 1       | run 2       | run 3       | average    |
|---------------|-------------|-------------|-------------|------------|
| nmap v7.80    | 6.007 total | 5.679 total | 4.633 total | 5.44 total |
| findpi v1.2.0 | 2.899 total | 2.682 total | 2.696 total | 2.76 total |

## Why

I was sick of waiting forever for the arp / nmap commands to work single-threaded.

Also, arp only works for devices you have seen previously, so you could easily miss things.

## Features

- **Multi-threaded scanning** for fast network discovery
- **CIDR notation support** - scan any subnet size (e.g., `/24`, `/16`, `/25`)
- **All Raspberry Pi models supported** - Pi 1, 2, 3, 4, 5, Zero, Zero W, Zero 2 W, Pi 400
- **Modern Python 3.8+** with improved error handling
- **Cross-platform** - works on Linux, macOS, and Windows

## Installation

```bash
# Using uv (recommended)
uv pip install findpi

# Using pip
pip3 install findpi
```

## Usage

`sudo findpi` use multithreading to get the job done.

***NOTE: Must Use SUDO***

The application asks you what ip address or range you want to select. The default tries to figure out your current network and set it as default.

### Examples

```bash
# Scan default network (auto-detected)
sudo findpi

# Scan specific /24 network
sudo findpi
# What net to check? (default 192.168.1.0/24): 192.168.1.0/24

# Scan larger subnet
sudo findpi
# What net to check? (default 192.168.1.0/24): 10.0.0.0/16

# Scan specific IP
sudo findpi
# What net to check? (default 192.168.1.0/24): 10.2.2.113

# Custom thread count
sudo findpi -c 32
```

Output example:
```bash
What network do you want to check? (192.168.1.0/24):
Checking for delicious pi around 192.168.1.0/24...
Found pi: 192.168.1.113
Found pi: 192.168.1.117
Found pi: 192.168.1.119
Found pi: 192.168.1.137
--- 2.45 seconds ---
```

## Supported Raspberry Pi Models

- **Raspberry Pi 1** - b8:27:eb MAC prefix
- **Raspberry Pi 2** - b8:27:eb MAC prefix
- **Raspberry Pi 3** - b8:27:eb, dc:a6:32 MAC prefixes
- **Raspberry Pi 4** - e4:5f:01, dc:a6:32 MAC prefixes
- **Raspberry Pi 5** - dc:a6:32 MAC prefix
- **Raspberry Pi Zero** - b8:27:eb MAC prefix
- **Raspberry Pi Zero W** - dc:a6:32 MAC prefix
- **Raspberry Pi Zero 2 W** - dc:a6:32 MAC prefix
- **Raspberry Pi 400** - e4:5f:01 MAC prefix

## Troubleshooting

1. If you set the threads too high for your system (should be a factor of number of cores) you will start to see timeout errors like the following `QUITTING! dnet: Failed to open device en0`. The mitigation is to lower the number of threads or leave it at the default.

2. For large subnets (like /16), the scan may take a long time. Consider using a smaller subnet or specific IP ranges.

3. If you get permission errors, make sure you're running with sudo or as root.
