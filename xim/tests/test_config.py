from xim.config import ConfigJSONFileStream, Config
from xim.utils import TmpFile


def test_config():
	with TmpFile("./tmp.json") as f:
		stream = ConfigJSONFileStream(f.name)
		saving_config: Config = {"current_proxy": "foo"}
		stream.save(saving_config)
		loaded_config = stream.load()
		assert saving_config == loaded_config
