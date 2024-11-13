import socket


def handle_chunked_response(sock):
    """
    Handle chunked transfer encoding HTTP response
    """

    def read_chunk():
        # Read the chunk size line
        chunk_size_str = ""
        while True:
            char = sock.recv(1)
            if char == b'\r':
                sock.recv(1)  # Skip \n
                break
            chunk_size_str += char.decode('ascii')
        chunk_size = int(chunk_size_str.strip(), 16)
        return chunk_size
    full_response = b''
    while True:
        chunk_size = read_chunk()
        # Chunk size 0 indicates end of response
        if chunk_size == 0:
            sock.recv(2)
            break
        # Read the chunk data
        chunk_data = b''
        bytes_remaining = chunk_size
        while bytes_remaining > 0:
            chunk = sock.recv(min(bytes_remaining, 8192))
            if not chunk:
                raise ConnectionError("Connection closed while reading chunk")
            chunk_data += chunk
            bytes_remaining -= len(chunk)

        full_response += chunk_data
        sock.recv(2)  # Read chunk's trailing \r\n

    return full_response


def parse_http_response(sock):
    """
    Parse HTTP response including headers and handle different transfer encodings
    """
    # Read status line first
    status_line = b''
    while True:
        char = sock.recv(1)
        if char == b'\r':
            sock.recv(1)  # Skip \n
            break
        status_line += char
    try:
        status_line = status_line.decode('utf-8')
        protocol, status_code, status_text = status_line.split(' ', 2)
        status_code = int(status_code)
    except Exception as e:
        print(f"Error parsing status line: {e}")
        status_code = 0

    # Read headers
    headers = {}
    while True:
        line = b''
        while True:
            char = sock.recv(1)
            if not char:
                raise ConnectionError("Connection closed while reading headers")
            if char == b'\r':
                next_char = sock.recv(1)
                if next_char == b'\n':
                    break
            line += char

        if not line:  # Empty line indicates end of headers
            break

        if b':' in line:
            name, value = line.decode('utf-8', errors='ignore').split(':', 1)
            headers[name.lower().strip()] = value.strip()
    # Handle response body based on transfer encoding
    if headers.get('transfer-encoding', '').lower() == 'chunked':
        response_body = handle_chunked_response(sock)
    elif 'content-length' in headers:
        content_length = int(headers['content-length'])
        response_body = b''
        bytes_received = 0
        while bytes_received < content_length:
            remaining = content_length - bytes_received
            chunk = sock.recv(min(8192, remaining))
            if not chunk:
                break
            response_body += chunk
            bytes_received += len(chunk)
            print(
                f"Downloaded: {bytes_received}/{content_length} bytes ({(bytes_received / content_length) * 100:.1f}%)")
    else:
        # No content length or chunked encoding - read until connection closes
        response_body = b''
        while True:
            try:
                chunk = sock.recv(8192)
                if not chunk:
                    break
                response_body += chunk
                print(f"Received chunk of {len(chunk)} bytes")
            except socket.timeout:
                break

    return status_code, headers, response_body
