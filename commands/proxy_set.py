from shell import ShellFileSystem
from proxy import ProxiesJSONFileStream, Proxies, Proxy
from const_setting import proxies_path, shells_path
from utils import CommandFailedError, remove_extension
from typing import List
import subprocess
import argparse
import logger


def proxy_set(args: argparse.Namespace) -> None:
	proxies_stream: ProxiesJSONFileStream = ProxiesJSONFileStream(proxies_path)
	proxies: Proxies = proxies_stream.load()
	if not proxies.exists(args.proxy_name):
		logger.error("Not found given name proxy")
		raise CommandFailedError()
	proxy: Proxy = proxies.get(args.proxy_name)

	shell_system: ShellFileSystem = ShellFileSystem(shells_path)
	shell_names: List[str] = shell_system.list()
	if len(shell_names) == 0:
		logger.error("No installed shell file")
		raise CommandFailedError()

	for name in shell_names:
		logger.info("Setting {}...".format(remove_extension(name)))
		try:
			proc: subprocess.CompletedProcess = shell_system.run(name, proxy.url_list())
			proc.check_returncode()
		except subprocess.CalledProcessError as e:
			logger.error("Shell script did not exit successfully")
			logger.info("Exit Status: {}".format(e.returncode))
			raise CommandFailedError()
		except subprocess.TimeoutExpired as e:
			logger.error("Timeout shell script")
			raise CommandFailedError()
		except KeyboardInterrupt as e:
			logger.error("Keyboard interrupt. ")
			raise CommandFailedError()
		logger.info("Done")
