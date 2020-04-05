from proxy import *
from utils import TmpFile


def test_proxy_stream():
	with TmpFile("./tmp.json") as f:
		stream = ProxiesJSONFileStream(f.name)
		saving_proxies = Proxies([
			Proxy(
				"test",
				"http://test",
				"https://test"
			)
		])
		stream.save(saving_proxies)
		loaded_proxies = stream.load()
		assert saving_proxies.proxies[0].name == loaded_proxies.proxies[0].name
		assert loaded_proxies.exists("test") is True
		loaded_proxies.add(
			Proxy(
				"test2",
				"http://test",
				"https://test"
			)
		)
		assert loaded_proxies.exists("test2") is True
		loaded_proxies.delete("test2")
		assert loaded_proxies.exists("test2") is False
