import struct
import socket


class IPPacket:
    def __init__(self, src_ip, dst_ip, protocol=socket.IPPROTO_TCP):
        self.version = 4
        self.ihl = 5
        self.tos = 0
        self.tot_len = 20 + 20  # 20 bytes IP + 20 bytes TCP
        self.id = 54321
        self.frag_off = 0
        self.ttl = 255
        self.protocol = protocol
        self.check = 0
        self.saddr = socket.inet_aton(src_ip)
        self.daddr = socket.inet_aton(dst_ip)

    def pack(self):
        ver_ihl = (self.version << 4) + self.ihl
        ip_header = struct.pack('!BBHHHBBH4s4s',
                                ver_ihl,
                                self.tos,
                                self.tot_len,
                                self.id,
                                self.frag_off,
                                self.ttl,
                                self.protocol,
                                self.check,
                                self.saddr,
                                self.daddr
                                )
        return ip_header
