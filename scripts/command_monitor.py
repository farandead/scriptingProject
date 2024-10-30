from scapy.all import ARP,Ether,srp
import json
from datetime import datetime
import os
import time

history_file = "/home/kali/.bash_history" 
log_file = os.path.expanduser("~/command_log.json")


def get_command_history():
	with open(history_file,'r') as file:
		return file.readlines()


def log_commands(commands):
	log_data = []
	if os.path.exits(log_file):
		with open(log_file,'r') as json_file:
			log_data = json.load(json_file)

	for command in commands:
		entry = {
		"timestamp" : datetime.now().isoformat(),
		"command": command.strip()
		}
		log_data.append(entry)

	with open(log_file,'w') as json_file:
		json.dump(log_data,json_file,indent=4)
	print("Dumped")
def monitor_history():
	last_position = 0
	while True:
		commands = get_command_history()
		if len(commands) > last_position:
			new_commands = commands[last_postion:]
			log_commands(new_commands)
			last_position = len(commands)
		time.sleep(5)

if __name__ == "__main__":
	print("Monitoring")
	monitor_history()

