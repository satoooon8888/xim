import os


class TmpFile:
	def __init__(self, path):
		self.file = open(path, "w")

	def __enter__(self):
		return self.file

	def __exit__(self, exc_type, exc_val, exc_tb):
		self.file.close()
		os.remove(self.file.name)
