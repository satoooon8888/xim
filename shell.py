import requests
import os
import subprocess
from typing import List, TypedDict
from utils import remove_extension, RequestResponseError, RequestError


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


def fetch_files_on_server(url: str) -> List[GithubFile]:
	try:
		response: requests.Response = requests.get(url)
	except Exception as e:
		raise RequestError(url, e)
	if response.status_code != 200:
		raise RequestResponseError(url, response.status_code)
	files: List[GithubFile] = response.json()
	return files


def fetch_file_content(url: str) -> str:
	content: str = requests.get(url).content.decode("utf-8")
	return content


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
