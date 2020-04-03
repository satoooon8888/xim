from config import Config
from proxy import Proxies, Proxy

config_path: str = "./xim.config.json"
proxies_path: str = "./xim_proxies.json"
shells_path: str = "./shells"
un_setting_current_proxy = "__un_setting__"
config_default: Config = {"current_proxy": un_setting_current_proxy}
proxies_default: Proxies = Proxies([Proxy("noproxy", "", "", "", "")])
content_api_shells_repository_root: str = "https://api.github.com/repos/satoooon8888/xim_shells/contents/"
raw_file_api_shells_repository_root: str = "https://raw.githubusercontent.com/satoooon8888/xim_shells/master/"
windows_shells_dirname: str = "windows_shells"
linux_shells_dirname: str = "linux_shells"
windows_shells_extension: str = ".bat"
linux_shells_extension: str = ".sh"
