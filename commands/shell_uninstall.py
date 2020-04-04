from shell import ShellFileSystem
from os_wrap import get_shell_extension
import argparse
import logger
from utils import CommandFailedError
from const_setting import shells_path


def shell_uninstall(args: argparse.Namespace) -> None:
	file_name: str = args.shell_name + get_shell_extension()
	file_system: ShellFileSystem = ShellFileSystem(shells_path)
	if file_system.exists(file_name):
		file_system.delete(file_name)
		logger.info("Successfully uninstall.")
	else:
		logger.error("Not found shell file.")
		raise CommandFailedError()
