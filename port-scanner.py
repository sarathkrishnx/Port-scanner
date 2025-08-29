import socket
from ftplib import FTP

port_services = {
    20: "FTP (Data)",
    21: "FTP (Control)",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    3306: "MySQL",
    3389: "RDP",
    8080: "HTTP-Alt / Proxy"
}
domains = [".com", ".org", ".net", ".in", ".edu", ".gov", ".io"]


def banner_grab_http(hostip, port):
    s = socket.socket()
    hostname = socket.gethostbyname(hostip)
    s.connect((hostip, port))
    request = f" HEAD / HTTP/1.1\r\nHost:{hostname}\r\n\r\n"
    s.send(request.encode())
    reply = s.recv(4096).decode(errors="ignore")
    s.close()
    return reply


def banner_grabbing_ftp(hostip, port):
    s = socket.socket()
    s.connect((hostip, port))
    reply = s.recv(4096).decode(errors="ignore")
    s.close()
    return reply


def check_anonymous_ftp(hostip, port):
    try:
        f = FTP()
        f.connect(hostip, port, timeout=7)
        ftp_response = f.login(user="anonymous", passwd="test@example.com")
        f.quit()
        if ftp_response.startswith('230'):
            return "Login Success "
        else:
            return "Login Failed "
    except Exception as e:
        return f"FTP Error:{e}"


def banner_grabbing_ssh(hostip, port):
    s = socket.socket()
    s.connect((hostip, port))
    banner = s.recv(4096).decode(errors="ignore")
    s.close()
    return banner


def banner_grabbing_smtp(hostip, port):
    s = socket.socket()
    s.connect((hostip, port))
    banner = s.recv(4096).decode(errors="ignore")
    return banner


def multi(start, end, host):
    for p in range(start, end + 1):
        s = socket.socket()
        s.settimeout(1)
        conn = s.connect_ex((host, p))
        s.close()

        if conn == 0:
            if p in port_services and p in [80, 8080, 443]:
                banner = banner_grab_http(host, p)
                print("\n==============================")
                print(f"Port: {p}")
                print(f"Service: {port_services[p]}")
                print(f"Status : Open")
                print("Banner:")
                print(banner.strip())
                print("==============================\n")

            elif p in port_services and p == 21:
                try:
                    banner = banner_grabbing_ftp(host, p)
                    print("\n==============================")
                    print(f"Port: {p}")
                    print(f"Service: {port_services[p]}")
                    print(f"Status : Open")
                    print("Banner:")
                    print(banner.strip())
                    
                    print("checking Anonymous login...")
                    print(check_anonymous_ftp(host, p))
                    print("==============================\n")
                except Exception as e:
                    print(f"port {p} : open, couldn't grab banner")

            elif p in port_services and p == 22:
                try:
                    banner = banner_grabbing_ssh(host, p)
                    print("\n==============================")
                    print(f"Port: {p}")
                    print(f"Service: {port_services[p]}")
                    print(f"Status : Open")
                    print("Banner:")
                    print(banner.strip())
                    print("==============================\n")
                except Exception as e:
                    print(f"port {p} : open, couldn't grab banner")

            elif p in port_services and p == 25:
                try:
                    banner = banner_grabbing_smtp(host, p)
                    print("\n==============================")
                    print(f"Port: {p}")
                    print(f"Service: {port_services[p]}")
                    print(f"Status : Open")
                    print("Banner:")
                    print(banner.strip())
                    print("==============================\n")
                except Exception as e:
                    print(f"port {p} : open, couldn't grab banner")

            else:
                print("\n==============================")
                print(f"Port: {p}")
                print(f"Service: {port_services[p]}")
                print(f"Status : Open")
                print("==============================\n")
        else:
            print(f"Port {p} : closed ")


def single(hostip):
    port = int(input("Enter Port to scan : "))
    s = socket.socket()
    s.settimeout(1)
    conn = s.connect_ex((hostip, port))

    if conn == 0:
        if port in port_services and port in [80, 8080, 443]:
            banner = banner_grab_http(hostip, port)
            print("\n==============================")
            print(f"Port: {port}")
            print(f"Service: {port_services[port]}")
            print("Banner:")
            print(banner.strip())
            print("==============================\n")
        elif port in port_services and port == 21:
            banner = banner_grabbing_ftp(hostip, port)
            print("\n==============================")
            print(f"Port: {port}")
            print(f"Service: {port_services[port]}")
            print("Banner:")
            print(banner.strip())
            print("==============================\n")
            print("checking Anonymous login...")
            print(check_anonymous_ftp(hostip, port))
        elif port in port_services and port == 22:
            print(f"Port {port}: open, services: {port_services[port]}")
        else:
            print(f"Port is open")
    else:
        print(f"Port is closed")

    s.close()


def ask():
    host = input("Enter target's IP Address : ").strip()
    usr_rep = input(f"Do you want to scan a single port scan or multiple port scan ? (single ( S )/multiple ( M ))")
    startp = None
    endp = None

    if usr_rep in ['multiple', 'M', 'm']:
        print("Enter starting and ending range of port : ")
        startp = int(input("Enter starting port : "))
        endp = int(input("Enter ending port : "))
        multi(startp, endp, host)
    else:
        single(host)

    return startp, endp, host


startp, endp, hostip = ask()
