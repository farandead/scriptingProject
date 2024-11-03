import subprocess
import re
import time
import logging

TCPDUMP_INTERFACE = "eth0"
TCPDUMP_FILE = "/var/log/tcpdump.log"
MALICIOUS_IP_THRESHOLD  = 10
CHECK_INTERVAL = 20
BLOCKED_IPS_FILE = "/var/log/blocked_ips.log"


logging.basicConfig(filename=BLOCKED_IPS_FILE,level=logging.INFO,format="%(asctime) - %(message)s")


def start_tcpdump():
	cmd = [
	"sudo","tcpdump","-i",TCPDUMP_INTERFACE, "-nn","-q","-l","-A",
	"-w",TCPDUMP_FILE
	]
	
	subprocess.Popen(cmd)


def analyse_tcp_dump():
	ip_counts = {}

	
	try:
		with open(TCPDUMP_FILE,"r") as file:
			lines = file.readlines()
			print(lines)
	except FileNotFoundError:
		print("tcpdump log file not found")

		return ip_counts
	
	ip_regex = re.compile(r'(\d+\.\d+\.\d+\.\d+)')	
	for line in lines:
		line = line.decode("utf-8",errors="ignore")
		match = ip_regex.searh(lines)
		if match:
			
			ip =match.group(1)
			ip_counts[ip] = ip_counts.get(ip_counts[ip],0) +1
			
	return {ip:count for ip,count in ip_counts.items() if count>= MALCIOUS_IP_THRESHOLD}



def block_ip(ip):
	try:
		subprocess.run(["sudo","iptables","-A","INPUT","-s",ip,"-j","DROP"],check=True)
		logging.info(f"BLOCKED IP = {ip}")
		print(f"BLOCKED IP = {ip}")
	except :
		print("Failed to bock the IP: {}")


def main():
	#start the tcp dump
	start_tcpdump()
	while True:
		time.sleep(CHECK_INTERVAL)

		sus_ips = analyse_tcp_dump()
		
		if sus_ips:
			for ip in sus_ips:
				block_ip(ip)

		with open(TCPDUMP_FILE,"w") as f:
			f.truncate(0)
			print("Saving the file")

if __name__ == "__main__":
	main()
	#analyse the tcp dump for the interval
	#if there is supsecious ip block it 
	

