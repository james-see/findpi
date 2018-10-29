# find-pi

## What
Find all the raspberry pi devices on your network really fast using multithreading in Python 3.x and find them fast. 

## Why

I was sick of waiting forever for the arp / nmap commands to work single-threaded. 

Also, arp only works for devices you have seen previously, so you could easily miss things.

## Usage

**Must Use SUDO**

`sudo finder.py 32` the number at the end is the number of threads to use, with the default being 64 will return the following:

```
What network do you want to check? (10.2.2.0/24):
Found pi: 10.2.2.113
Found pi: 10.2.2.117
Found pi: 10.2.2.119
Found pi: 10.2.2.137
```

Enjoy!
