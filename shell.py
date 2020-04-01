import requests
from const_setting import shell_location, windows_shells_dirname, linux_shells_dirname, windows_shells_extension, \
	linux_shells_extension, shell_raw_location
import os
import subprocess
from typing import List, TypedDict


class HaveNotImplOSError(Exception):
	pass


class GithubContentsLinks(TypedDict):
	self: str
	git: str
	html: str


class GithubContents(TypedDict):
	name: str
	path: str
	sha: str
	size: int
	url: str
	html_url: str
	git_url: str
	download_url: str
	type: str
	_links: GithubContentsLinks


def get_shell_extension() -> str:
	extension: str
	if os.name == "nt":
		extension = windows_shells_extension
	elif os.name == "posix":
		extension = linux_shells_extension
	else:
		raise HaveNotImplOSError()
	return extension


def get_shells_dirname() -> str:
	dirname: str
	if os.name == "nt":
		dirname = windows_shells_dirname
	elif os.name == "posix":
		dirname = linux_shells_dirname
	else:
		raise HaveNotImplOSError()
	return dirname


class ShellsOnServer:
	def __init__(self) -> None:
		self.location: str = shell_location + get_shells_dirname()
		self.shells: List[GithubContents] = requests.get(self.location).json()

	def list(self) -> List[str]:
		shell_name_list = []
		for i in range(len(self.shells)):
			shell_name_list.append(self.shells[i]["name"])
		return shell_name_list

	def search(self, shell_name: str) -> List[str]:
		shell_name_list: List[str] = []
		shell_name += get_shell_extension()
		for i in range(len(self.shells)):
			if shell_name in self.shells[i]["name"]:
				shell_name_list.append(self.shells[i]["name"])
		return shell_name_list

	def exists(self, shell_name: str) -> bool:
		shell_name += get_shell_extension()
		for i in range(len(self.shells)):
			if shell_name == self.shells[i]["name"]:
				return True
		return False

	@staticmethod
	def get_content(shell_name: str) -> str:
		shell_name += get_shell_extension()
		file_url: str = shell_raw_location + "/" + get_shells_dirname() + "/" + shell_name
		content: str = requests.get(file_url).content.decode("utf-8")
		return content


class ShellFilesSystem:
	def __init__(self, path: str) -> None:
		self.path: str = path

	def exists(self, shell_name: str) -> bool:
		file_path = self.path + "/" + shell_name + get_shell_extension()
		return os.path.exists(file_path)

	def run(self, shell_name: str, args: List[str]) -> subprocess.CompletedProcess:
		file_path: str = self.path + "/" + shell_name + get_shell_extension()
		proc: subprocess.CompletedProcess = subprocess.run([file_path, *args])
		return proc

	def load(self, shell_name: str) -> str:
		file_path: str = self.path + "/" + shell_name + get_shell_extension()
		with open(file_path, "rt") as f:
			return f.read()

	def save(self, shell_name: str, content: str) -> None:
		file_path: str = self.path + "/" + shell_name + get_shell_extension()
		with open(file_path, "wt") as f:
			f.write(content)
