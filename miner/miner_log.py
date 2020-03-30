import sys, os
from datetime import datetime
import threading

class MinerLog():
	id = None
	dir = None
	p_warnings = True
	w_warnings = True
	p_info = True
	w_info = True
	p_debug = False
	w_debug = True


	def set_up(id, dir):
		MinerLog.id = id
		MinerLog.dir = dir
		MinerLog.log_file = os.path.join(MinerLog.dir, "log.miner.txt")


	def warning(msg):
		if MinerLog.p_warnings:
			print("Miner {} WARNING: {}".format(MinerLog.id, msg))
		if MinerLog.w_warnings:
			MinerLog.write_tf(MinerLog.get_str().format("WARNING", msg))


	def info(msg):
		if MinerLog.p_info:
			print("Miner {}: {}".format(MinerLog.id, msg))
		if MinerLog.w_info:
			MinerLog.write_tf(MinerLog.get_str().format("INFO", msg))


	def debug(msg):
		if MinerLog.p_debug:
			print("Miner {}: {}".format(MinerLog.id, msg))
		if MinerLog.w_debug:
			MinerLog.write_tf(MinerLog.get_str().format("DEBUG", msg))


	def get_str():
		dt = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
		return "[{}] [{}] Miner {}: {}\n".format(dt, "{}", MinerLog.id, "{}")


	def write_tf(msg):
		if MinerLog.id is not None and MinerLog.dir is not None:
			with open(MinerLog.log_file, "a") as f:
				f.write(msg)
		else:
			print("WARNING: Log not saved, log must be setup first")


