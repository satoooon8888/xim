class Logger:
	def __init__(self) -> None:
		pass

	@staticmethod
	def error(text: str) -> None:
		print("Error: ".format(text))

	@staticmethod
	def warning(text: str) -> None:
		print("Warn: {}".format(text))

	@staticmethod
	def info(text: str) -> None:
		print("Xim: {}".format(text))
