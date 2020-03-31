from config import Config
from proxy import Proxies, Proxy

config_path: str = "./xim.config.json"
proxies_path: str = "./xim_proxies.json"
un_setting_current_proxy = "__un_setting__"
config_default: Config = {"current_proxy": un_setting_current_proxy}
proxies_default: Proxies = Proxies([Proxy("noproxy", "", "", "", "")])