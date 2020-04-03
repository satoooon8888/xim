from shell import GithubFile, GithubContentsInfoProvider, fetch_files_on_server, fetch_file_content, ShellFilesSystem
from typing import List
from utils import RequestResponseError, CommandFailedError, RequestError
from os_wrap import get_shell_extension, get_shells_dirname, get_raw_shell_file_api_url, \
	get_shells_repository_content_api_url
import logger


def shell_install(args) -> None:
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
		url: str = get_raw_shell_file_api_url() + "/" + file_name
		content: str = fetch_file_content(url)
		shells_path = "./" + get_shells_dirname()
		file_system = ShellFilesSystem(shells_path)
		file_system.save(file_name, content)
		logger.info("Install success.")
	else:
		logger.error("Not found shell file.")
