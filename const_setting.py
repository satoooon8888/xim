from config import Config
from proxy import Proxies, Proxy

config_path: str = "./xim.config.json"
proxies_path: str = "./xim_proxies.json"
config_default: Config = {"current_proxy": "__un_setting__"}
proxies_default: Proxies = Proxies([Proxy("noproxy", "", "", "", "")])