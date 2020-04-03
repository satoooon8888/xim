from shell import fetch_files_on_server, GithubContentsInfoProvider, GithubFile
from os_wrap import get_shells_repository_content_api_url
from typing import List
from utils import remove_extension, RequestResponseError, CommandFailedError, RequestError
import logger
import argparse


def shell_search(args: argparse.Namespace) -> None:
	url: str = get_shells_repository_content_api_url()
	try:
		files: List[GithubFile] = fetch_files_on_server(url)
	except RequestResponseError as e:
		logger.error("Response {} Status failed.".format(e.status_code))
		raise CommandFailedError()
	except RequestError as e:
		logger.error("Request failed. URL: {}".format(e.url))
		logger.error(str(e.error))
		raise CommandFailedError()

	provider: GithubContentsInfoProvider = GithubContentsInfoProvider(files)
	match_shell_names: List[str] = provider.search(args.shell_name)
	number_matched = len(match_shell_names)
	if number_matched > 0:
		logger.info("Matched {} shell file.".format(number_matched))
		for name in match_shell_names:
			logger.info(remove_extension(name))
	else:
		logger.error("Not matched shell file.")
