from xim.shell import GithubFile, GithubContentsInfoProvider, fetch_files_on_server, fetch_file_content, ShellFileSystem
from typing import List
from xim.utils import RequestResponseError, CommandFailedError, RequestError
from xim.os_wrap import get_shell_extension, get_raw_shell_file_api_url, \
	get_shells_repository_content_api_url
from xim.const_setting import shells_path
from xim import logger
import argparse


def shell_install(args: argparse.Namespace) -> None:
	for name in args.shell_name.split(","):
		logger.info("Install {}...".format(name))
		file_name: str = name + get_shell_extension()
		file_system = ShellFileSystem(shells_path)
		if file_system.exists(file_name):
			logger.error("{} shell file already exits.".format(name))
			raise CommandFailedError()
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
			try:
				content_url: str = get_raw_shell_file_api_url() + "/" + file_name
			except RequestResponseError as e:
				logger.error("Request Status {} failed.".format(e.status_code))
				raise CommandFailedError()
			except RequestError as e:
				logger.error("Request failed. URL: {}".format(e.url))
				logger.error(str(e.error))
				raise CommandFailedError()
			content: str = fetch_file_content(content_url)
			file_system.save(file_name, content)
			logger.info("Install success")
		else:
			logger.error("Not found shell file")
