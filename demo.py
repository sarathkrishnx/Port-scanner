import socket
from ftplib import FTP
import threading

port_services={
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


def banner_grab_http(hostip,port):
    
    
    s=socket.socket()
    hostname=socket.gethostbyname(hostip)
    s.connect((hostip,port))
    request = f" HEAD / HTTP/1.1\r\nHost:{hostname}\r\n\r\n"
    s.send(request.encode())
    
    reply=s.recv(4096).decode(errors="ignore")
    s.close()
    return reply

def banner_grabbing_ftp(hostip,port):
    
    s=socket.socket()
    s.connect((hostip,port))
    reply=s.recv(4096).decode(errors="ignore")
    s.close()
    return reply
    
        
    
def check_anonymous_ftp(hostip,port):
    
    try:
        f=FTP()
        f.connect(hostip,port,timeout=7)
        ftp_response=f.login(user="anonymous",passwd="test@example.com")
        f.quit()
        if ftp_response.startswith('230'):
            return "Login Success "
        else:
            return "Login Failed "
        
        
    
        
    except Exception as e:
        return f"FTP Error:{e}"
    
def banner_grabbing_ssh(hostip,port):
    
    s=socket.socket()
    s.connect((hostip,port))
    
    banner=s.recv(4096).decode(errors="ignore")
    s.close()
    
    return banner

def banner_grabbing_smtp(hostip,port):
    s=socket.socket()
    s.connect((hostip,port))
    banner=s.recv(4096).decode(errors="ignore")
    return banner
    
    
    
        


def multi(start, end, host):
    results = []  

    for p in range(start, end+1):
        s = socket.socket()
        s.settimeout(1)
        conn = s.connect_ex((host, p))

        if conn == 0:
            result = {
                "port": p,
                "service": port_services.get(p, "Unknown"),
                "status": "Open",
                "banner": "",
                "anonymous": None
            }

            
            if p in [80, 8080, 443]:
                result["banner"] = banner_grab_http(host, p)

            
            elif p == 21:
                result["banner"] = banner_grabbing_ftp(host, p)
                result["anonymous"] = check_anonymous_ftp(host, p)

            
            elif p == 22:
                try:
                    s.send(b"\n")
                    reply = s.recv(1024).decode(errors="ignore").strip()
                    result["banner"] = reply
                except:
                    result["banner"] = "No banner"

            results.append(result)

        else:
            results.append({
                "port": p,
                "service": port_services.get(p, "Unknown"),
                "status": "Closed",
                "banner": "",
                "anonymous": None
            })

        s.close()

    
    for r in results:
        print("\n==============================")
        print(f"Port: {r['port']}")
        print(f"Service: {r['service']}")
        print(f"Status : {r['status']}")
        if r['banner']:
            print("Banner:")
            print(r['banner'])
        if r['anonymous'] is not None:
            print("Anonymous Login:", r['anonymous'])
        print("==============================")




def single(hostip):
    
    port = int(input("Enter Port to scan : "))
    s=socket.socket()
    s.settimeout(1)
    conn = s.connect_ex((hostip,port))


    if conn == 0:
        if port in port_services and port in [80,8080,443]:
            banner = banner_grab_http(hostip, port)
            print("\n==============================")
            print(f"Port: {port}")
            print(f"Service: {port_services[port]}")
            print("Banner:")
            print(banner.strip())
            print("==============================\n")
        elif port in port_services and port == 21 :
            banner=banner_grabbing_ftp(hostip,port)
            print("\n==============================")
            print(f"Port: {port}")
            print(f"Service: {port_services[port]}")
            print("Banner:")
            print(banner.strip())
            print("==============================\n")
            print("checking Anonymous login...")
            print(check_anonymous_ftp(hostip,port))
            
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
    thread_number = 5
    
    if usr_rep in ['multiple','M','m'] :
        print("Enter starting and ending range of port : " )
        startp=int(input("Enter starting port : " ))
        endp=int(input("Enter ending port : " ))
        
        
        
        
        totalport = endp - startp + 1
        chunk_size = totalport // thread_number
        
        
        
        Threads = []
        
        for i in range (thread_number):
            
            thread_start = startp + i * chunk_size
            
            if i == thread_number - 1:
                
                thread_end = endp
            else:
                
                thread_end = thread_start + chunk_size - 1
                
                
            t = threading.Thread(target=multi,args=(thread_start,thread_end,host))
            t.start()  
            
          
            Threads.append(t)
        for t in Threads:
            t.join()
                  
                 
                 
        
        '''
        thread2 = threading.Thread(target=multi,args=(thread_start,thread_end,host))
        thread3 = threading.Thread(target=multi,args=(thread_start,thread_end,host))
        
        thread1.start()
        thread2.start()
        thread3.start()
        
        thread1.join()
        thread2.join()
        thread3.join()
'''
        
    else:
    
        single(host)
        
    return startp,endp,host
        
startp,endp,hostip = ask()



'''
print("flag1")
thread1 = threading.Thread(target=multi,args=(startp,endp,hostip))
thread2 = threading.Thread(target=multi,args=(startp,endp,hostip))
thread3 = threading.Thread(target=multi,args=(startp,endp,hostip))

print("flag2")

thread1.start()
thread2.start()
thread3.start()




thread1.join()
thread2.join()
thread3.join()

print("flag3")
'''

    
        

