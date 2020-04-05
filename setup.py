from setuptools import setup

setup(
	name="xim",
	version="1.0.0",
	install_requires=["requests"],
	entry_points={
		"console_scripts": [
			"xim = main:main"
		]
	}
)