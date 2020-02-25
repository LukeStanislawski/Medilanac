import sys, os
from datetime import datetime

class Log():
	def set_up(self, id, dir):
		self.id = id
		self.dir = dir
		self.log_file = os.path.join(self.dir, "log.txt")

		self.p_warnings = True
		self.w_warnings = True
		self.p_info = True
		self.w_info = True
		self.p_debug = False
		self.w_debug = True


	def warning(self, msg):
		if self.p_warnings:
			print("Miner {} WARNING: {}".format(self.id, msg))
		if self.w_warnings:
			self.write_tf(self.get_str().format("WARNING", msg))


	def info(self, msg):
		if self.p_info:
			print("Miner {}: {}".format(self.id, msg))
		if self.w_info:
			self.write_tf(self.get_str().format("INFO", msg))


	def debug(self, msg):
		if self.p_debug:
			print("Miner {}: {}".format(self.id, msg))
		if self.w_debug:
			self.write_tf(self.get_str().format("DEBUG", msg))


	def get_str(self):
		dt = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
		return "[{}] [{}] Miner {}: {}\n".format(dt, "{}", self.id, "{}")


	def write_tf(self, msg):
		if self.id is not None and self.dir is not None:
			with open(self.log_file, "a") as f:
				f.write(msg)
		else:
			print("WARNING: Log not saved, log must be setup first")
