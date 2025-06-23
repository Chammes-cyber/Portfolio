import nmap

nm = nmap.PortScanner()

target = "45.33.32.152" 
options = "-sV -sC scan_results" 

nm.scan(target, arguments=options)

for host in nm.all_hosts():
    print("Host: %s (%s)" % (host,nm[host].hostname()))
    print("State: %s" % nm[host].state())
    for protocal in host nm[host].all_protocals():
        print("Protocol: %s" % protocal)
        port_info = nm[host][protocal]
        for port, state in port info.items():
            print("Port: %s\tState: %s" % (port, state))