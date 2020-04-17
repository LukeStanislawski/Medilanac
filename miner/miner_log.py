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
		"""
		Used to set up log parameters

		id: miner ID to be displayed in logs
		dir: dir to write log file to
		"""
		MinerLog.id = id
		MinerLog.dir = dir
		MinerLog.log_file = os.path.join(MinerLog.dir, "miner.log")


	def warning(msg):
		"""
		Used to log a warning

		msg: Message to log
		"""
		if MinerLog.p_warnings:
			print("Miner {} WARNING: {}".format(MinerLog.id, msg))
		if MinerLog.w_warnings:
			MinerLog.write_tf(MinerLog.get_str().format("WARNING", msg))


	def info(msg):
		"""
		Used to log at normal level

		msg: Message to log
		"""
		if MinerLog.p_info:
			print("Miner {}: {}".format(MinerLog.id, msg))
		if MinerLog.w_info:
			MinerLog.write_tf(MinerLog.get_str().format("INFO", msg))


	def debug(msg):
		"""
		Used to log at debug level

		msg: Message to log
		"""
		if MinerLog.p_debug:
			print("Miner {}: {}".format(MinerLog.id, msg))
		if MinerLog.w_debug:
			MinerLog.write_tf(MinerLog.get_str().format("DEBUG", msg))


	def get_str():
		"""
		Defines the standard string format that is used for log messages
		"""
		dt = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
		return "[{}] [{}] Miner {}: {}\n".format(dt, "{}", MinerLog.id, "{}")


	def write_tf(msg):
		"""
		writes a message to the log file
		
		msg: Message to log
		"""
		if MinerLog.id is not None and MinerLog.dir is not None:
			with open(MinerLog.log_file, "a") as f:
				f.write(msg)
		else:
			print("WARNING: Log not saved, log must be setup first")


