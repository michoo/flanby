# Flanby

It's a tool to monitoring machine status, open ports and possible vuln. 
It's like flan from cloudflare but it's integrated in a nice server


## cve
https://github.com/CVEProject
https://vulners.com/cve/CVE-2019-14513

## nice to read
https://github.com/MyKings/python-masscan
https://github.com/robertdavidgraham/masscan/wiki/rate

## install masscan
sudo apt install masscan
if sudo permission needed to run masscan, you can check same issues from tshark, tcpdump,...
sudo setcap cap_net_raw,cap_net_admin+eip /usr/bin/masscan

https://github.com/robertdavidgraham/masscan

## scripts nmap
https://github.com/vulnersCom/nmap-vulners
nmap -oX - -sV --script=/home/fred/workspace/projects/python/flanby/scripts/vulners.nse 192.168.1.1



## inspiration
https://github.com/GoSecure/freshonions-torscraper
https://github.com/cloudflare/flan