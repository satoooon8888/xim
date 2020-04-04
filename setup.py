from setuptools import setup

setup(
	install_requires=["requests"],
	entry_points={
		"console_scripts": [
			"xim = main:main"
		]
	}
)