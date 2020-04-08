import json
from typing import TypedDict
import os


class Config(TypedDict):
	current_proxy: str


class ConfigJSONFileStream:
	def __init__(self, path: str) -> None:
		self.path = path

	def load(self) -> Config:
		with open(self.path, "rt") as f:
			config: Config = json.load(f)
		return config

	def save(self, config: Config) -> None:
		with open(self.path, "wt") as f:
			json.dump(config, f)

	def exists(self) -> bool:
		return os.path.exists(self.path)
