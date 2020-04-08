import os
from xim.const_setting import windows_shells_dirname, linux_shells_dirname, windows_shells_extension, \
	linux_shells_extension, content_api_shells_repository_root, raw_file_api_shells_repository_root
from xim.utils import HaveNotImplOSError


def get_shells_dirname() -> str:
	dirname: str
	if os.name == "nt":
		dirname = windows_shells_dirname
	elif os.name == "posix":
		dirname = linux_shells_dirname
	else:
		raise HaveNotImplOSError()
	return dirname


def get_shell_extension() -> str:
	extension: str
	if os.name == "nt":
		extension = windows_shells_extension
	elif os.name == "posix":
		extension = linux_shells_extension
	else:
		raise HaveNotImplOSError()
	return extension


def get_raw_shell_file_api_url():
	return raw_file_api_shells_repository_root + get_shells_dirname()


def get_shells_repository_content_api_url():
	return content_api_shells_repository_root + get_shells_dirname()


def convert_linux_path_to_running_os_path(path: str) -> str:
	running_os_path: str
	if os.name == "nt":
		running_os_path = path.replace("/", "\\")
	elif os.name == "posix":
		running_os_path = path
	else:
		raise HaveNotImplOSError()
	return running_os_path
