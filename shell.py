import requests
from const_setting import content_api_shells_repository_root, windows_shells_dirname, linux_shells_dirname, \
	raw_file_api_shells_repository_root
import os
import subprocess
from typing import List, TypedDict
from utils import remove_extension, HaveNotImplOSError


class GithubFileLink(TypedDict):
	self: str
	git: str
	html: str


class GithubFile(TypedDict):
	name: str
	path: str
	sha: str
	size: int
	url: str
	html_url: str
	git_url: str
	download_url: str
	type: str
	_links: GithubFileLink


def get_shells_dirname() -> str:
	dirname: str
	if os.name == "nt":
		dirname = windows_shells_dirname
	elif os.name == "posix":
		dirname = linux_shells_dirname
	else:
		raise HaveNotImplOSError()
	return dirname


def fetch_files_on_server() -> List[GithubFile]:
	location: str = content_api_shells_repository_root + get_shells_dirname()
	files: List[GithubFile] = requests.get(location).json()
	return files


class GithubContentsInfoProvider:
	def __init__(self, contents: List[GithubFile]) -> None:
		self.contents: List[GithubFile] = contents

	def list(self) -> List[str]:
		content_name_list: List[str] = []
		for i in range(len(self.contents)):
			content_name_list.append(self.contents[i]["name"])
		return content_name_list

	def search(self, file_name: str) -> List[str]:
		content_name_list: List[str] = []
		for i in range(len(self.contents)):
			content_name = remove_extension(self.contents[i]["name"])
			if file_name in content_name:
				content_name_list.append(self.contents[i]["name"])
		return content_name_list

	def exists(self, file_name: str) -> bool:
		for i in range(len(self.contents)):
			if file_name == self.contents[i]["name"]:
				return True
		return False

	@staticmethod
	def fetch_file_content(shell_name: str) -> str:
		file_url: str = raw_file_api_shells_repository_root + "/" + get_shells_dirname() + "/" + shell_name
		content: str = requests.get(file_url).content.decode("utf-8")
		return content


class ShellFilesSystem:
	def __init__(self, path: str) -> None:
		self.path: str = path

	def exists(self, shell_name: str) -> bool:
		file_path = self.path + "/" + shell_name
		return os.path.exists(file_path)

	def run(self, shell_name: str, args: List[str]) -> subprocess.CompletedProcess:
		file_path: str = self.path + "/" + shell_name
		proc: subprocess.CompletedProcess = subprocess.run([file_path, *args])
		return proc

	def load(self, shell_name: str) -> str:
		file_path: str = self.path + "/" + shell_name
		with open(file_path, "rt") as f:
			return f.read()

	def save(self, shell_name: str, content: str) -> None:
		file_path: str = self.path + "/" + shell_name
		with open(file_path, "wt") as f:
			f.write(content)
