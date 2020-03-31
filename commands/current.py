from config import ConfigJSONFileStream, Config
from const_setting import config_path


def current(args) -> None:
	stream = ConfigJSONFileStream(config_path)
	config: Config = stream.load()
	current_proxy: str = config["current_proxy"]
	if current_proxy == "__un_setting_":
		print("haven't set proxy yet.")
		return
	print("current set proxy: {}".format(current_proxy))
