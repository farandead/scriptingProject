import psutil
import time
from datetime import datetime
import sys
import json

LOG_FILE = 'system_monitor.log'


def log_system_matrics():
	data = {
		"Timestap":datetime.now().isoformat(),
		"CPU Usage":psutil.cpu_percent(interval=1),
		"Memory Usage":psutil.virtual_memory().percent,
		"Disk Usage":psutil.disk_usage('/').percent,
		"Network Sent": round(psutil.net_io_counters().bytes_sent /(1024 **2),2)	,
		"Network Recived":round(psutil.net_io_counters().bytes_recv /(1024 **2)),

	}

	
	try:
		with open(LOG_FILE,"r+") as file:
			try:
				logs = json.load(file)
			except json.decoder.JSONDecodeError:
				logs = []
			logs.append(data)
			file.seek(0)
			json.dump(logs,file,indent=4)
			print("System Data Logged")
	except FileNotFoundError:
		with open(LOG_FILE,'w') as file:
			json.dump([data],file,indent=4)


		
def main():
	log_system_matrics()

if __name__ == "__main__":
	log_system_matrics()
	

