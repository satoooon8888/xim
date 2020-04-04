from config import ConfigJSONFileStream, Config
from const_setting import config_path, un_setting_current_proxy
import logger


def current(args) -> None:
	stream = ConfigJSONFileStream(config_path)
	config: Config = stream.load()
	current_proxy: str = config["current_proxy"]
	if current_proxy == un_setting_current_proxy:
		logger.info("haven't set proxy yet")
		return
	logger.info("current set proxy: {}".format(current_proxy))
