import os
from re import L
import subprocess as sp

from sqlalchemy import true

websites = ["www.azm.to","www2.solarmovie.to","www.tubitv.com","www.gostream.site","www.123moviesgoto.com",
            "www.amazon.com/adlp/imdbtv-about","www.peacocktv.com","www.moviestars.to","www.streamm4u.com",
            "www.moviesjoy.to","www.vudu.com","www.spacemov.ws","www.crackle.com","www.xumo.tv/channels",
            "www.flixtor.to/home","w.yesmovies123.me"] # sample predefined sites for blocking.

valid = []

def cval(output): # checks if the given IP address is valid or not.
    if output[-9:-1] == "NXDOMAIN":
        return 0
    elif output[-9:-1] == "SERVFAIL":
        return 0
    else:
        id = ""
        for i in range(len(output)):
            if output[i] == "A" and output[i+1] == "d" and output[i+1] == "d" and i != 20:
                k = i+9
                for k in range(i+9,i+26):
                    if output[k] == '\n':
                        break
                    id += output[k]
                break
    return id

altdom = ['.co','.com','.to','.se','.net'] # sample alternate Top Level Domains (TLD) that can be used to check alternate/clone sites.

def blockalt(): # Brute force approach to block the alternate sites.
    l = len(websites)
    for i in range(l):
        temp = websites[i]
        print("[+] CREATING ALTERNATE DOMAINS FOR " + temp)
        for j in range(len(temp) - 1,0,-1):
            if temp[j] == '.':
                temp = temp[:j]
                break
        for j in altdom:
            t = ""
            t += temp
            t += j
            if t not in websites:
                websites.append(t)
                ou = sp.getoutput('nslookup ' + t)
                valid.append(cval(ou))
    print("\n[+] BLOCKING ALTERNATE SITES...")
    for j in range(l,len(websites)):
        if valid[j] != 0 and j!=42 and j!= 45:
            os.system("sudo iptables -A INPUT -s " + valid[j] +" -j DROP")
    print("[+] ALTERNATE SITES BLOCKED.\n")
    
def block_str(st): # Fucntion to block the alternate/clone sites by string matching.
    print("\n[+] BLOCKING ALTERNATE SITES OF " + st)
    os.system("sudo iptables -A OUTPUT -p udp -m string --string \"" + st +"\" --algo kmp -j DROP")
    print("[+] ALTERNATE SITES OF "+ st +" BLOCKED.\n")

def newsite(site): # function to add new site to the blcoked sites list.
    websites.append(site)
    ou = sp.getoutput('nslookup ' + site)
    valid.append(cval(ou))
    if valid[-1] != 0 :
        print("\n[+] BLOCKING " + site)
        os.system("sudo iptables -A INPUT -s " + valid[-1] +" -j DROP")
        print("[+] "+ site +" BLOCKED.\n")

def unblock_newsite(site): # function to unblock a previously blocked site.
    ou = sp.getoutput('nslookup ' + site)
    valid.append(cval(ou))
    if valid[-1] != 0 :
        print("\n[+] UNBLOCKING " + site)
        os.system("sudo iptables -D INPUT -s " + valid[-1] +" -j DROP")
        print("[+] "+ site +" UNBLOCKED.\n")

def newip(ip): # function to blcok a new IP address
    print("\n[+] BLOCKING " + ip)
    os.system("sudo iptables -A INPUT -s " + ip +" -j DROP")
    print("[+] "+ ip +" BLOCKED.\n")
    
def unblock_newip(ip): # function to unblcok a new IP address
    print("\n[+] UNBLOCKING " + ip)
    os.system("sudo iptables -D INPUT -s " + ip +" -j DROP")
    print("[+] "+ ip +" UNBLOCKED.\n")

for j in websites: # stores the IP of the predefined websites
    out = sp.getoutput('nslookup ' + j)
    valid.append(cval(out))

print("[+] FIREWALL INITIATED !\n")
print("[+] BLOCKING VIDEO STREAMING SITES...")
for j in range(len(websites)): # blocking the predefined sites first.
    if valid[j] != 0 :
        os.system("sudo iptables -A INPUT -s " + valid[j] +" -j DROP")
print("[+] VIDEO STREAMING SITES BLOCKED.")

print("\n[+] Enter any of the folowing commands : ")
print(" -> 1 <url of website> : To block a new website for the host machine.")
print(" -> 2 <ip address> : To block a new ip address for the host machine.")
print(" -> 3 <url of website> : To unblock a website for the host machine.")
print(" -> 4 <ip address> : To unblock an ip address for the host machine.")
print(" -> 5 : To block alternate sites of the previously blocked websites by brute force approach.")
print(" -> 6 <string> : To block alternate sites of the previously blocked websites by string matching approach.")
print(" -> 7 : To view the iptable rules for the blocked websites.")
print(" -> EXIT : To close the firewall and restore the iptable rules.\n")

while(true):
    req = input("Command : ")
    if req[0] == "1":
        si = req[2:]
        newsite(si)
    elif req[0] == "2":
        si = req[2:]
        newip(si)
    elif req[0] == "3":
        si = req[2:]
        unblock_newsite(si)
    elif req[0] == "4":
        si = req[2:]
        unblock_newip(si)
    elif req == "5":
        blockalt()
    elif req[0] == "6":
        st = req[2:]
        block_str(st)
    elif req == "7":
        print("[+] THE IPTABLE RULES ARE: ")
        os.system("sudo iptables -L")
    elif req == "EXIT":
        print("[+] SHUTTING DOWN THE FIREWALL...")
        # setting the default policies for each of the built-in chains to ACCEPT
        os.system("sudo iptables -P INPUT ACCEPT")
        os.system("sudo iptables -P FORWARD ACCEPT")
        os.system("sudo iptables -P OUTPUT ACCEPT")
        # flushing the nat and mangle tabels
        os.system("sudo iptables -t nat -F")
        os.system("sudo iptables -t mangle -F")
        # flushing all chains
        os.system("sudo iptables -F")
        # deleting all non-default chains
        os.system("sudo iptables -X")
        break
    else:
        print("[+] INVALID COMMAND !")
    print('\n')