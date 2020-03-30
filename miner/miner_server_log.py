import sys, os
from datetime import datetime
import threading


class MinerServerLog():
	id = None
	dir = None
	p_warnings = True
	w_warnings = True
	p_info = True
	w_info = True
	p_debug = False
	w_debug = True


	def set_up(id, dir):
		MinerServerLog.id = id
		MinerServerLog.dir = dir
		MinerServerLog.log_file = os.path.join(MinerServerLog.dir, "log.server.txt")


	def warning(msg):
		if MinerServerLog.p_warnings:
			print("Miner {} WARNING: {}".format(MinerServerLog.id, msg))
		if MinerServerLog.w_warnings:
			MinerServerLog.write_tf(MinerServerLog.get_str().format("WARNING", msg))


	def info(msg):
		if MinerServerLog.p_info:
			print("Miner {}: {}".format(MinerServerLog.id, msg))
		if MinerServerLog.w_info:
			MinerServerLog.write_tf(MinerServerLog.get_str().format("INFO", msg))


	def debug(msg):
		if MinerServerLog.p_debug:
			print("Miner {}: {}".format(MinerServerLog.id, msg))
		if MinerServerLog.w_debug:
			MinerServerLog.write_tf(MinerServerLog.get_str().format("DEBUG", msg))


	def get_str():
		dt = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
		return "[{}] [{}] Miner {}-{}: {}\n".format(dt, "{}", MinerServerLog.id, threading.get_ident(), "{}")


	def write_tf(msg):
		if MinerServerLog.id is not None and MinerServerLog.dir is not None:
			with open(MinerServerLog.log_file, "a") as f:
				f.write(msg)
		else:
			print("WARNING: Log not saved, log must be setup first")