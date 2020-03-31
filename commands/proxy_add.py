from proxy import ProxiesJSONFileStream, Proxies, Proxy
import argparse
from utils import input_with_default
from const_setting import proxies_path
import logger


def create_proxy_from_input() -> Proxy:
	name: str = input("proxy name: ")
	http: str = input_with_default("http: ", prefill="http://")
	guessed_next_url = "https://" + http.split("http://")[1]
	https: str = input_with_default("https: ", prefill=guessed_next_url)
	guessed_next_url = "ftp://" + http.split("http://")[1]
	ftp: str = input_with_default("ftp: ", prefill=guessed_next_url)
	guessed_next_url = "ssh://" + http.split("http://")[1]
	ssh: str = input_with_default("ssh: ", prefill=guessed_next_url)
	return Proxy(name, http, https, ftp, ssh)


def proxy_add(args: argparse.Namespace) -> None:
	proxy: Proxy = create_proxy_from_input()
	stream: ProxiesJSONFileStream = ProxiesJSONFileStream(proxies_path)
	proxies: Proxies = stream.load()
	proxies.add(proxy)
	stream.save(proxies)
	logger.info("add inputted proxy")
