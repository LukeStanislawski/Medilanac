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
		"""
		Used to set up log parameters

		id: miner ID to be displayed in logs
		dir: dir to write log file to
		"""
		MinerServerLog.id = id
		MinerServerLog.dir = dir
		MinerServerLog.log_file = os.path.join(MinerServerLog.dir, "miner_server.log")


	def warning(msg):
		"""
		Used to log a warning

		msg: Message to log
		"""
		if MinerServerLog.p_warnings:
			print("Miner {} WARNING: {}".format(MinerServerLog.id, msg))
		if MinerServerLog.w_warnings:
			MinerServerLog.write_tf(MinerServerLog.get_str().format("WARNING", msg))


	def info(msg):
		"""
		Used to log at normal level

		msg: Message to log
		"""
		if MinerServerLog.p_info:
			print("Miner {}: {}".format(MinerServerLog.id, msg))
		if MinerServerLog.w_info:
			MinerServerLog.write_tf(MinerServerLog.get_str().format("INFO", msg))


	def debug(msg):
		"""
		Used to log at debug level

		msg: Message to log
		"""
		if MinerServerLog.p_debug:
			print("Miner {}: {}".format(MinerServerLog.id, msg))
		if MinerServerLog.w_debug:
			MinerServerLog.write_tf(MinerServerLog.get_str().format("DEBUG", msg))


	def get_str():
		"""
		Defines the standard string format that is used for log messages
		"""
		dt = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
		return "[{}] [{}] Miner {}-{}: {}\n".format(dt, "{}", MinerServerLog.id, threading.get_ident(), "{}")


	def write_tf(msg):
		"""
		writes a message to the log file
		
		msg: Message to log
		"""
		if MinerServerLog.id is not None and MinerServerLog.dir is not None:
			with open(MinerServerLog.log_file, "a") as f:
				f.write(msg)
		else:
			print("WARNING: Log not saved, log must be setup first")