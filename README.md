# Raw TCP/HTTP Requester

This project is a low-level networking tool designed to manually craft and send TCP/IP packets, as well as perform basic HTTP requests using raw sockets. Built in Python, it provides a deeper understanding of TCP and HTTP protocols by allowing users to send and receive packets directly, without relying on higher-level libraries.

## Features

* **Custom IP and TCP Packet Creation**: Manually set IP headers and TCP flags, including SYN and ACK flags
* **Raw HTTP GET Requests**: Send HTTP GET requests after establishing a TCP connection using raw packets
* **Binary Data Handling**: Automatically detect and save binary data (e.g., images or files) in responses, with dynamic progress tracking
* **Content Parsing**: Read and display HTTP headers and response content, including handling both text and binary data


![Packet](https://github.com/raminfp/raw-tcp-http-requester/blob/main/image/wireshark.png?raw=true)

## Usage

### Prerequisites

* **Python 3** is required
* **Root/Administrator Permissions**: Raw socket manipulation requires elevated permissions

### Running the Script

1. **Clone the repository**:
```bash
git clone https://github.com/raminfp/raw-tcp-http-requester.git
cd raw-tcp-http-requester
```

2. **Run the script**:
```bash
sudo python3 main.py
```

3. **Enter the Target Host and URL Path** when prompted.

### Example

To initiate a connection and send a request to a server:

```bash
sudo python3 main.py
```

After entering the IP address and path, the tool will:
1. Send a SYN packet
2. Establish a TCP connection and send an HTTP GET request
3. Display the response headers and save binary data if applicable

## Important Notes

* **Permissions**: This script requires root/admin privileges due to the use of raw sockets
* **Testing Purposes Only**: Ensure you have authorization to interact with the target server, as sending raw packets may be flagged as unusual behavior

## License

This project is open-source under the MIT License. Please review `LICENSE` for more information.
