from shell import fetch_files_on_server, GithubContentsInfoProvider, GithubFile
from typing import List
from utils import remove_extension
import logger


def shell_search(args):
	files: List[GithubFile] = fetch_files_on_server()
	provider: GithubContentsInfoProvider = GithubContentsInfoProvider(files)
	match_shell_names: List[str] = provider.search(args.shell_name)
	number_matched = len(match_shell_names)
	if number_matched > 0:
		print("Matched {} shell file.".format(number_matched))
		for name in match_shell_names:
			print(remove_extension(name))
	else:
		logger.error("Not matched shell file.")
