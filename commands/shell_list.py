from shell import ShellFileSystem
from const_setting import shells_path
from typing import List
from utils import remove_extension
import logger
import argparse


def shell_list(args: argparse.Namespace) -> None:
	file_system: ShellFileSystem = ShellFileSystem(shells_path)
	files: List[str] = file_system.list()
	if len(files) > 0:
		logger.info("Installed {} shell file.".format(len(files)))
		for file in files:
			logger.info(remove_extension(file))
	else:
		logger.info("No installed shell file")
