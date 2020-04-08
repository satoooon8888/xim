from setuptools import setup, find_packages

setup(
	name="xim",
	version="1.0.0",
	install_requires=["requests"],
	entry_points={
		"console_scripts": [
			"xim = xim.main:main"
		]
	},
	packages=find_packages(),

)