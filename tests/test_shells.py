from utils import TmpFile, TmpDirectory
from shell import *
import os


def test_shells():
	if os.name == "nt":
		with TmpDirectory("./test_shells"):
			with TmpFile("./test_shells/test_shell.bat") as f:
				with open("./test_shells/test_shell.bat", "wt") as ff:
					ff.write("foobar")
				system = ShellFilesSystem("test_shells")
				assert system.exists("test_shell") is True
				assert system.exists("foobar") is False
				assert system.load("test_shell") == "foobar"
				system.save("test_shell2", "foo")
				assert system.load("test_shell2") == "foo"
	else:
		raise HaveNotImplOSError()
