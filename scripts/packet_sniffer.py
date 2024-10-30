import sys
from scapy.all import sniff,IP
import json
from datetime import datetime


PACKET_LOG_FILE = "packet_activity.json"

def packet_callback(packet):
	if packet.haslayer(IP):
		packet_data = {
		"timestamp" : datetime.now().isoformat(),
		"source ip" : packet[IP].src,
		"destination ip":packet[IP].dst,
		"protocol": packet[IP].proto,
		"length": len(packet),
	}


	try:
		with open(PACKET_LOG_FILE,"r+") as file:
			try:
				logs = json.load(file)
			except:
				logs = []
			logs.append(packet_data)
			file.seek(0)
			json.dump(logs,file,indent=4)
	except FileNotFoundError:
		with open(PACKET_LOG_FILE,'w') as file:
			json.dump(logs,file,indent=4)
	print("Packet Data Stored")
		
def start(filter_str ):
	print(f"starting packet sniffing with filter {filter_str}")
	sniff(prn=packet_callback,filter=filter_str,store=0)


def main():
	if len(sys.argv) != 2:
		print("Use python packet_sniffer.py <filter>")

	filter_str = sys.argv[1]

	start(filter_str)

if __name__ == "__main__":
	main()
