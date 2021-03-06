import os
from typing import TextIO, List
import shutil


class CommandFailedError(Exception):
	pass


class HaveNotImplOSError(Exception):
	pass


class RequestResponseError(Exception):
	def __init__(self, url: str, status_code: int):
		self.url: str = url
		self.status_code: int = status_code


class RequestError(Exception):
	def __init__(self, url: str, error: Exception):
		self.url: str = url
		self.error: Exception = error


class TmpFile:
	def __init__(self, path) -> None:
		self.file = open(path, "w")

	def __enter__(self) -> TextIO:
		return self.file

	def __exit__(self, exc_type, exc_val, exc_tb) -> None:
		self.file.close()
		os.remove(self.file.name)


class TmpDirectory:
	def __init__(self, path: str) -> None:
		self.path = path
		os.mkdir(path)

	def __enter__(self) -> None:
		pass

	def __exit__(self, exc_type, exc_val, exc_tb) -> None:
		shutil.rmtree(self.path)


def input_with_default(prompt: str, prefill: str = "") -> str:
	# https://stackoverflow.com/questions/2533120/show-default-value-for-editing-on-python-input-possible/2533134
	# https://stackoverflow.com/questions/5403138/how-to-set-a-default-editable-string-for-raw-input/20351345
	if os.name == "posix":
		# noinspection PyUnresolvedReferences
		import readline

		readline.set_startup_hook(lambda: readline.insert_text(prefill))
		try:
			return input(prompt)
		finally:
			readline.set_startup_hook()
	elif os.name == "nt":
		from msvcrt import getch, putch

		def putstr(b):
			b = list(map(lambda x: x.encode(), b))
			for c in b:
				putch(c)

		putstr(prompt)

		if prefill is None:
			data = []
		else:
			data = list(prefill)
			putstr(data)
		while True:
			c = getch()
			if c in b'\r\n':
				break
			elif c == b'\003':  # Ctrl-C
				putstr('\r\n')
				raise KeyboardInterrupt
			elif c == b'\b':  # Backspace
				if data:
					putstr('\b \b')  # Backspace and wipe the character cell
					data.pop()
			elif c in b'\0\xe0':  # Special keys
				getch()
			else:
				putch(c)
				data.append(c.decode())
		putstr('\r\n')
		return ''.join(data)
	else:
		raise HaveNotImplOSError()


def remove_extension(file_name: str) -> str:
	return "".join(file_name.split(".")[0:-1])


def get_file_list(path: str) -> List[str]:
	files: List[str] = os.listdir(path)
	files_file: List[str] = [f for f in files if os.path.isfile(os.path.join(path, f))]
	return files_file
