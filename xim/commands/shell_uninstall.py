from xim.shell import ShellFileSystem
from xim.os_wrap import get_shell_extension
import argparse
from xim import logger
from xim.utils import CommandFailedError
from xim.const_setting import shells_path


def shell_uninstall(args: argparse.Namespace) -> None:
	file_name: str = args.shell_name + get_shell_extension()
	file_system: ShellFileSystem = ShellFileSystem(shells_path)
	if file_system.exists(file_name):
		file_system.delete(file_name)
		logger.info("Successfully uninstall")
	else:
		logger.error("Not found shell file")
		raise CommandFailedError()
