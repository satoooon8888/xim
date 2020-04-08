from xim.utils import TmpFile, TmpDirectory
from xim.shell import *


def test_shells():
	with TmpDirectory("./test_shells"):
		with TmpFile("./test_shells/test_shell.bat"):
			with open("./test_shells/test_shell.bat", "wt") as ff:
				ff.write("foobar")
			system = ShellFileSystem("test_shells")
			assert system.exists("test_shell.bat") is True
			assert system.exists("foobar.bat") is False
			assert system.load("test_shell.bat") == "foobar"
			system.save("test_shell2.bat", "foo")
			assert system.load("test_shell2.bat") == "foo"


def test_provider():
	shells: List[GithubFile] = [{
		"name": "foo.bat",
		"path": "",
		"sha": "",
		"size": 0,
		"url": "",
		"html_url": "",
		"git_url": "",
		"download_url": "",
		"type": "",
		"_links": {
			"self": "",
			"git": "",
			"html": ""
		}
	}]
	provider = GithubContentsInfoProvider(shells)
	assert provider.exists("foo.bat") is True
	assert provider.exists("bar.bat") is False
	assert provider.list() == ["foo.bat"]
	assert provider.search("f") == ["foo.bat"]
	assert provider.search("b") == []
