from xim.shell import fetch_files_on_server, GithubContentsInfoProvider, GithubFile
from xim.os_wrap import get_shells_repository_content_api_url
from typing import List
from xim.utils import remove_extension, RequestResponseError, CommandFailedError, RequestError
from xim import logger
import argparse


def shell_search(args: argparse.Namespace) -> None:
	if args.shell_name != "" and args.all is True:
		logger.error("Can't use both shell_name and --all")
		raise CommandFailedError()
	if args.shell_name == "" and args.all is False:
		logger.error("Required shell_name arguments. See xim shell search -h")
		raise CommandFailedError()
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
	if not args.all:
		match_shell_names: List[str] = provider.search(args.shell_name)
	else:
		match_shell_names: List[str] = provider.list()
	number_matched = len(match_shell_names)
	if number_matched > 0:
		logger.info("Matched {} shell file.".format(number_matched))
		for name in match_shell_names:
			logger.info(remove_extension(name))
	else:
		logger.error("Not matched shell file")
