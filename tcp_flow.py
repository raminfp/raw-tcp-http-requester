import struct
import socket


def calculate_checksum(msg):
    s = 0
    # Loop taking 2 characters at a time
    for i in range(0, len(msg), 2):
        if (i + 1) < len(msg):
            w = (msg[i] << 8) + msg[i + 1]
        else:
            w = (msg[i] << 8)
        s = s + w

    s = (s >> 16) + (s & 0xffff)
    s = ~s & 0xffff

    return s


class TCPPacket:
    def __init__(self, src_ip, dst_ip, src_port, dst_port, seq=0, ack_seq=0, flags=0):
        self.src_ip = src_ip
        self.dst_ip = dst_ip
        self.src_port = src_port
        self.dst_port = dst_port
        self.seq_num = seq
        self.ack_num = ack_seq
        self.data_offset = 5
        self.flags = flags
        self.window = 2920
        self.checksum = 0
        self.urgent_ptr = 0

    def pack(self):
        data_offset_reserved = (self.data_offset << 4) + 0
        flags = self.flags

        # First build the TCP header without checksum
        tcp_header = struct.pack(
            '!HHLLBBHHH',
            self.src_port,
            self.dst_port,
            self.seq_num,
            self.ack_num,
            data_offset_reserved,
            flags,
            self.window,
            0,
            self.urgent_ptr
        )

        # Build pseudo header for checksum calculation
        source_address = socket.inet_aton(self.src_ip)
        dest_address = socket.inet_aton(self.dst_ip)
        placeholder = 0
        protocol = socket.IPPROTO_TCP
        tcp_length = len(tcp_header)

        psh = struct.pack('!4s4sBBH',
                          source_address,
                          dest_address,
                          placeholder,
                          protocol,
                          tcp_length
                          )

        # Calculate checksum
        checksum = calculate_checksum(psh + tcp_header)

        # Rebuild TCP header with checksum
        tcp_header = struct.pack(
            '!HHLLBBHHH',
            self.src_port,
            self.dst_port,
            self.seq_num,
            self.ack_num,
            data_offset_reserved,
            flags,
            self.window,
            checksum,
            self.urgent_ptr
        )

        return tcp_header
