# Import Python modules
import sys
import socket
from datetime import datetime

# Vulnerability database
vulnerability_database = {
    "OpenSSH 7.2P2": "CVE-2016-6210: Username Enumeration",
    "OS4ED openSIS v7.0": "CVE-2025-22925: SQL Injection",
    "FoxCMS 1.2.5": "CVE-2025-29306: Remote Code Execution",
    "Microsoft Windows 11": "CVE-2024-21338: Kernel Privelege Escalation",
}
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

                # Does the banner match vulerability database
                for vuln_database in vulnerability_database:
                    if vuln_database in banner:
                        print ("Vulnerability found: {}".format(vulnerability_database[vuln_database]))
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
