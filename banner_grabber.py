# Import Python modules
import sys
import socket
from datetime import datetime

# Define a target
if len(sys.argv) == 2:
    # Translate hostname to IPv4
    target = socket.gethostbyname(sys.argv[1])
else:
    target = "127.0.0.1"

# Show scanning information
print("-" * 45)
print("Scan Target: " + target)
print("Scan started at: " + str(datetime.now()))
print("=" * 45)

# Run the Scan
try:
    for port in range(1, 1023):
        # Create a socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)

        # Attempt to grab the banner
        result = s.connect_ex((target, port))
        if result == 0:
            print("Port {} is open".format(port))
            try:
                s.send(b'HEAD / HTTP/1.1\r\nHost: localhost\r\n\r\n')
                banner = s.recv(1023)
                print("Banner: {}".format(banner.decode().strip()))
            except:
                print("Banner for port {} not found".format(port))
        s.close()


# Interrupt a scan
except KeyboardInterrupt:
    print("\nScan halted by user")
    sys.exit()

except socket.gaierror:
    print("\nHostname could not be resolved.")
    sys.exit()

except socket.error:
    print("\nCouldn't connect to server.")
    sys.exit()
