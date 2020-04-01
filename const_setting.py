from config import Config
from proxy import Proxies, Proxy

config_path: str = "./xim.config.json"
proxies_path: str = "./xim_proxies.json"
windows_shells_path: str = "./windows_shells"
linux_shells_path: str = "./linux_shells"
un_setting_current_proxy = "__un_setting__"
config_default: Config = {"current_proxy": un_setting_current_proxy}
proxies_default: Proxies = Proxies([Proxy("noproxy", "", "", "", "")])
shell_location: str = "https://api.github.com/repos/satoooon8888/xim_shells/contents/"
shell_raw_location: str = "https://raw.githubusercontent.com/satoooon8888/xim_shells/master/"
windows_shells_dirname: str = "windows_shells"
linux_shells_dirname: str = "linux_shells"
windows_shells_extension: str = ".bat"
linux_shells_extension: str = ".sh"
