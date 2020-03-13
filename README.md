# findpi

## What

Find all the raspberry pi devices on your network really fast using multithreading in Python 3.x and find them fast.

## Stats

Ok, so to compare this to just running nmap vs. findpi:

|               | run 1       | run 2       | run 3       | average    |
|---------------|-------------|-------------|-------------|------------|
| nmap v7.80    | 6.007 total | 5.679 total | 4.633 total | 5.44 total |
| findpi v1.0.3 | 2.899 total | 2.682 total | 2.696 total | 2.76 total |

## Why

I was sick of waiting forever for the arp / nmap commands to work single-threaded.

Also, arp only works for devices you have seen previously, so you could easily miss things.

## Usage

`pip3 install findpi` then `sudo findpi` use multithreading to get the job done.

***NOTE: Must Use SUDO***

The application asks you what ip address or range you want to select. The default tries to figure out your current network and set it as default. Examples are `192.168.1.0/24`, etc. If you want to check just one ip address, you can put that in as well, like `10.2.2.113` for instance.

`sudo findpi -c 32` the number at the end is the number of threads to use, with the default being 4 times whatever cores findpi discovers about your machine, will return the following:

```bash
What network do you want to check? (10.2.2.0/24):
Found pi: 10.2.2.113
Found pi: 10.2.2.117
Found pi: 10.2.2.119
Found pi: 10.2.2.137
```

## Troubleshooting

1. If you se the threads too high for your system (should be a factor of number of cores) you will start to see timeout errors like the following `QUITTING! dnet: Failed to open device en0`. The mitigation is to lower the number of threads or leave it at the default.
