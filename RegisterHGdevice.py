import socket
from zeroconf import ServiceInfo, Zeroconf

# Function to get the current IP address
def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't have to be reachable
        s.connect(('10.254.254.254', 1))
        ip_address = s.getsockname()[0]
    except Exception:
        ip_address = '127.0.0.1'
    finally:
        s.close()
    return ip_address

# Get the current IP address
ip_address = get_ip_address()

# Define the service info
desc = {'version': '0.10.0', 'service': 'example'}
info = ServiceInfo(
    "_http._tcp.local.",
    "example._http._tcp.local.",
    addresses=[socket.inet_aton(ip_address)],
    port=8000,
    properties=desc,
    server="example.local.",
)

# Advertise the service
zeroconf = Zeroconf()
print(f"Registering service on {ip_address}...")
zeroconf.register_service(info)

try:
    input("Press enter to exit...\n\n")
finally:
    print("Unregistering service...")
    zeroconf.unregister_service(info)
    zeroconf.close()
