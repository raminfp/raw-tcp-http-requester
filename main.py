import socket
import time
from http_parser import parse_http_response
from ip_flow import IPPacket
from tcp_flow import TCPPacket


def send_tcp_http_flow(target_host, target_port=80, path="/"):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
    except PermissionError:
        print("Error: This script requires root/admin privileges")
        return
    s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    # Get local IP
    local_ip = socket.gethostbyname(socket.gethostname())
    # 1. Send SYN packet
    ip_header = IPPacket(local_ip, target_host)
    tcp_header = TCPPacket(
        local_ip,
        target_host,
        src_port=18880,
        dst_port=target_port,
        seq=318,
        flags=2
    )
    packet = ip_header.pack() + tcp_header.pack()
    print(f"Sending SYN packet from {local_ip} to {target_host}...")
    s.sendto(packet, (target_host, 0))
    # Wait a bit for SYN-ACK
    time.sleep(1)
    # 2. Send HTTP GET request using regular socket
    print(f"Establishing TCP connection to {target_host}:{target_port}...")
    http_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    http_socket.settimeout(30)  # Set timeout to 30 seconds
    try:
        http_socket.connect((target_host, target_port))
    except Exception as e:
        print(f"Connection failed: {e}")
        return
    http_request = f"GET {path} HTTP/1.1\r\n"
    http_request += f"Host: {target_host}\r\n"
    http_request += "Accept: */*\r\n"
    http_request += "Connection: close\r\n\r\n"

    print(f"Sending HTTP GET request to {path}...")
    http_socket.send(http_request.encode())
    # 3. Send ACK packet
    ip_header = IPPacket(local_ip, target_host)
    tcp_header = TCPPacket(
        local_ip,
        target_host,
        src_port=18880,
        dst_port=target_port,
        seq=396,
        ack_seq=1589,
        flags=16
    )
    packet = ip_header.pack() + tcp_header.pack()
    print("Sending ACK packet...")
    s.sendto(packet, (target_host, 0))
    # 4. Receive and parse HTTP response
    print("Waiting for HTTP response...")
    try:
        status_code, headers, response_body = parse_http_response(http_socket)
        print(f"\nStatus Code: {status_code}")
        print("\nHeaders received:")
        for name, value in headers.items():
            print(f"{name}: {value}")
        content_type = headers.get('content-type', '').lower()
        print(f"\nResponse received (total bytes: {len(response_body)})")
        # Handle different content types
        if 'application/octet-stream' in content_type:
            print("\nDetected binary data, saving to file.dump...")
            with open('file.dump', 'wb') as f:
                f.write(response_body)
            print("Binary file saved successfully to file.dump")
        else:
            try:
                decoded_response = response_body.decode('utf-8', errors='ignore')
                print("\nResponse content:")
                print(decoded_response)
            except Exception as e:
                print(f"Error decoding response: {e}")
                print("Raw response length:", len(response_body))

    except Exception as e:
        print(f"Error during communication: {e}")
    finally:
        # Clean up
        http_socket.close()
        s.close()


if __name__ == "__main__":
    target_host = "x.x.x.x"
    target_port = 8081  # default port
    target_path = input("Please add url PATH: ")
    send_tcp_http_flow(target_host, target_port, target_path)
