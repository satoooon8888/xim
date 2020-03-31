import os


class TmpFile:
	def __init__(self, path):
		self.file = open(path, "w")

	def __enter__(self):
		return self.file

	def __exit__(self, exc_type, exc_val, exc_tb):
		self.file.close()
		os.remove(self.file.name)


def input_with_default(prompt: str, prefill: str = ""):
	# https://stackoverflow.com/questions/2533120/show-default-value-for-editing-on-python-input-possible/2533134
	# https://stackoverflow.com/questions/5403138/how-to-set-a-default-editable-string-for-raw-input/20351345
	if os.name == "posix":
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


class TerminateError(Exception):
	pass
