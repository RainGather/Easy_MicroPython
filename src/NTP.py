try:
    import usocket as socket
except:
    import socket
try:
    import ustruct as struct
except:
    import struct
    
import machine
import time

# (date(2000, 1, 1) - date(1900, 1, 1)).days * 24*60*60
NTP_DELTA = 3155673600

host = 'ntp1.aliyun.com'

def http_time():
    pass

def ntp_time():
    NTP_QUERY = bytearray(48)
    NTP_QUERY[0] = 0x1b
    addr = socket.getaddrinfo(host, 123)[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(1)
    res = s.sendto(NTP_QUERY, addr)
    msg = s.recv(48)
    s.close()
    val = struct.unpack('!I', msg[40:44])[0]
    return val - NTP_DELTA

# tz=timezone
def set_ntp_time(tz=8):
    t = ntp_time()
    t += tz * 3600
    tm = time.localtime(t)
    tm = tm[0:3] + (0,) + tm[3:6] + (0,)
    machine.RTC().datetime(tm)
