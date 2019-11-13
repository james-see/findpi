# find pi

## What

Find all the raspberry pi devices on your network really fast using multithreading in Python 3.x and find them fast. 

## Why

I was sick of waiting forever for the arp / nmap commands to work single-threaded. 

Also, arp only works for devices you have seen previously, so you could easily miss things.

## Usage

`sudo python3 conscan.py` use multithreading to get the job done

***NOTE: Must Use SUDO***

The application asks you what ip address or range you want to select. The default is `10.2.2.0/24`. Examples are `192.168.1.0/24`, etc. If you want to check just one ip address, you can put that in as well, like `10.2.2.113` for instance.

`sudo finder.py 32` or `sudo conscan.py 32` the number at the end is the number of threads to use, with the default being 64 will return the following:

```bash
What network do you want to check? (10.2.2.0/24):
Found pi: 10.2.2.113
Found pi: 10.2.2.117
Found pi: 10.2.2.119
Found pi: 10.2.2.137
```

Enjoy!
