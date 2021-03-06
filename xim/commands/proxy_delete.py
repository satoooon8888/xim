import argparse
from xim.proxy import ProxiesJSONFileStream, Proxies
from xim.const_setting import proxies_path
from xim import logger


def proxy_delete(args: argparse.Namespace) -> None:
	name: str = args.proxy_name
	stream: ProxiesJSONFileStream = ProxiesJSONFileStream(proxies_path)
	proxies: Proxies = stream.load()
	if proxies.exists(name):
		proxies.delete(name)
	else:
		logger.error("not found this name")
	stream.save(proxies)
	logger.info("add inputted proxy")
