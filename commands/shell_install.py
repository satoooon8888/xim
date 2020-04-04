from shell import GithubFile, GithubContentsInfoProvider, fetch_files_on_server, fetch_file_content, ShellFileSystem
from typing import List
from utils import RequestResponseError, CommandFailedError, RequestError
from os_wrap import get_shell_extension, get_raw_shell_file_api_url, \
	get_shells_repository_content_api_url
from const_setting import shells_path
import logger
import argparse


def shell_install(args: argparse.Namespace) -> None:
	file_name: str = args.shell_name + get_shell_extension()
	url: str = get_shells_repository_content_api_url()
	try:
		files: List[GithubFile] = fetch_files_on_server(url)
	except RequestResponseError as e:
		logger.error("Request Status {} failed.".format(e.status_code))
		raise CommandFailedError()
	except RequestError as e:
		logger.error("Request failed. URL: {}".format(e.url))
		logger.error(str(e.error))
		raise CommandFailedError()

	provider: GithubContentsInfoProvider = GithubContentsInfoProvider(files)
	if provider.exists(file_name):
		content_url: str = get_raw_shell_file_api_url() + "/" + file_name
		content: str = fetch_file_content(content_url)
		file_system = ShellFileSystem(shells_path)
		file_system.save(file_name, content)
		logger.info("Install success")
	else:
		logger.error("Not found shell file")
