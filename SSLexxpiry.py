import ssl
import socket
from datetime import datetime

DOMAIN = "example.com"
PORT = 443

def get_ssl_expiry(domain, port):
    context = ssl.create_default_context()
    with socket.create_connection((domain, port)) as sock:
        with context.wrap_socket(sock, server_hostname=domain) as ssock:
            cert = ssock.getpeercert()
            expiry_date_str = cert['notAfter']
            expiry_date = datetime.strptime(expiry_date_str, '%b_
