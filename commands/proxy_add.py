from proxy import ProxiesJSONFileStream, Proxies, Proxy
import argparse
from utils import input_with_default, CommandFailedError
from const_setting import proxies_path, un_setting_current_proxy
import logger


def create_proxy_from_input(name: str) -> Proxy:
	http: str = input_with_default("http: ", prefill="http://")
	guessed_next_url = "https://" + http.split("http://")[1]
	https: str = input_with_default("https: ", prefill=guessed_next_url)
	guessed_next_url = "ftp://" + http.split("http://")[1]
	ftp: str = input_with_default("ftp: ", prefill=guessed_next_url)
	guessed_next_url = "ssh://" + http.split("http://")[1]
	ssh: str = input_with_default("ssh: ", prefill=guessed_next_url)
	return Proxy(name, http, https, ftp, ssh)


def proxy_add(args: argparse.Namespace) -> None:
	stream: ProxiesJSONFileStream = ProxiesJSONFileStream(proxies_path)
	proxies: Proxies = stream.load()

	name: str = args.proxy_name
	if name == "":
		logger.error("Empty argument is invalid")
		raise CommandFailedError()
	if name == un_setting_current_proxy:
		logger.error("Sorry, this name is already used by system. put a else name")
		raise CommandFailedError()
	if proxies.exists(name):
		logger.error("This name is already used")
		raise CommandFailedError()
	proxy: Proxy = create_proxy_from_input(name)
	proxies.add(proxy)
	stream.save(proxies)
	logger.info("add inputted proxy")
