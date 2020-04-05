import argparse
from proxy import ProxiesJSONFileStream, Proxies
from const_setting import proxies_path


def proxy_list(args: argparse.Namespace):
	stream: ProxiesJSONFileStream = ProxiesJSONFileStream(proxies_path)
	proxies: Proxies = stream.load()
	log = ""
	longest_name_length = 0
	for proxy in proxies:
		longest_name_length = max(longest_name_length, len(proxy.name))
	longest_name_length += 1  # split
	for proxy in proxies:
		log += proxy.name + " " * (longest_name_length - len(proxy.name)) + "http : " + proxy.http + "\n"
		log += " " * longest_name_length + "https: " + proxy.https + "\n"
		log += "\n"
	print(log)
