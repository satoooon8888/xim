import json
from typing import List, TypedDict, Iterator
import os

class ProxyDict(TypedDict):
	name: str
	http: str
	https: str
	ftp: str
	ssh: str


class Proxy:
	def __init__(self, name: str, http: str, https: str, ftp: str, ssh: str) -> None:
		self.name = name
		self.http = http
		self.https = https
		self.ftp = ftp
		self.ssh = ssh

	def url_list(self) -> List[str]:
		return [self.http, self.https, self.ftp, self.ssh]


class ConverterToProxyDictAndProxy:
	@staticmethod
	def convert_to_proxy(proxy_dict: ProxyDict) -> Proxy:
		name: str = proxy_dict["name"]
		http: str = proxy_dict["http"]
		https: str = proxy_dict["https"]
		ftp: str = proxy_dict["ftp"]
		ssh: str = proxy_dict["ssh"]
		return Proxy(name, http, https, ftp, ssh)

	@staticmethod
	def convert_to_proxy_dict(proxy: Proxy) -> ProxyDict:
		return {
			"name": proxy.name,
			"http": proxy.http,
			"https": proxy.https,
			"ftp": proxy.ftp,
			"ssh": proxy.ssh
		}


class Proxies:
	def __init__(self, proxies: List[Proxy]) -> None:
		self.proxies = proxies

	def get(self, name: str) -> Proxy:
		for proxy in self.proxies:
			if proxy.name == name:
				return proxy
		raise ValueError("Not found given name proxy")

	def add(self, proxy: Proxy) -> None:
		self.proxies.append(proxy)

	def delete(self, name: str) -> None:
		for i, proxy in enumerate(self.proxies):
			if proxy.name == name:
				self.proxies.pop(i)

	def exists(self, name: str) -> bool:
		for i, proxy in enumerate(self.proxies):
			if proxy.name == name:
				return True
		return False

	def __iter__(self) -> Iterator[Proxy]:
		return iter(self.proxies)


class ProxiesJSONFileStream:
	def __init__(self, path: str) -> None:
		self.path = path

	def load(self) -> Proxies:
		with open(self.path, "rt") as f:
			raw_proxies: List[ProxyDict] = json.load(f)
		proxies: Proxies = Proxies([])
		for i, raw_proxy in enumerate(raw_proxies):
			proxy: Proxy = ConverterToProxyDictAndProxy.convert_to_proxy(raw_proxy)
			proxies.add(proxy)
		return proxies

	def save(self, proxies: Proxies) -> None:
		raw_proxies: List[ProxyDict] = []
		for proxy in proxies:
			raw_proxy: ProxyDict = ConverterToProxyDictAndProxy.convert_to_proxy_dict(proxy)
			raw_proxies.append(raw_proxy)
		with open(self.path, "wt") as f:
			json.dump(raw_proxies, f)

	def exists(self) -> bool:
		return os.path.exists(self.path)
