import argparse

from commands.current import current
from commands.proxy_add import proxy_add
from commands.proxy_delete import proxy_delete
from commands.proxy_list import proxy_list
from commands.proxy_set import proxy_set
from commands.shell_install import shell_install
from commands.shell_list import shell_list
from commands.shell_search import shell_search
from commands.shell_uninstall import shell_uninstall

from config import ConfigJSONFileStream
from proxy import ProxiesJSONFileStream

from const_setting import config_path, config_default, proxies_default, proxies_path

from utils import CommandFailedError

import sys
import logger

"""
xim current
xim proxy set [proxy_name]
xim proxy add [proxy_name]
xim proxy delete [proxy_name]
xim proxy list
xim shell install [shell_name]
xim shell uninstall [shell_name]
xim shell search
xim shell list
"""


def get_parser() -> argparse.ArgumentParser:
	parser = argparse.ArgumentParser(
		description="""
		Xim is easy proxy changer.
		See https://github.com/satoooon8888/xim
		"""
	)
	parser.set_defaults(handler=lambda x: parser.print_help())
	subparser = parser.add_subparsers()

	# current
	p_current = subparser.add_parser(
		"current",
		help="Show current setting proxy name",
		description="Show current setting proxy name"
	)
	p_current.set_defaults(handler=current)

	# proxy
	p_proxy = subparser.add_parser(
		"proxy",
		help="See xim proxy -h."
	)
	p_proxy.set_defaults(handler=lambda args: p_proxy.print_help())
	p_proxy_sub = p_proxy.add_subparsers()

	# proxy set
	p_proxy_set = p_proxy_sub.add_parser(
		"set",
		help="Set proxy to app with named proxy setting.",
		description="Set proxy to app with named proxy setting."
	)
	p_proxy_set.add_argument("proxy_name", type=str)
	p_proxy_set.set_defaults(handler=proxy_set)

	# proxy add
	p_proxy_add = p_proxy_sub.add_parser(
		"add",
		help="Save named proxy setting with inputted urls",
		description="Save named proxy setting with inputted urls"
	)
	p_proxy_add.add_argument("proxy_name", type=str)
	p_proxy_add.set_defaults(handler=proxy_add)

	# proxy delete
	p_proxy_delete = p_proxy_sub.add_parser(
		"delete",
		help="Delete named proxy setting",
		description="Delete named proxy setting"
	)
	p_proxy_delete.add_argument("proxy_name", type=str)
	p_proxy_delete.set_defaults(handler=proxy_delete)

	# proxy list
	p_proxy_list = p_proxy_sub.add_parser(
		"list",
		help="Show named proxy settings",
		description="Show named proxy settings"
	)
	p_proxy_list.set_defaults(handler=proxy_list)

	# shell
	p_shell = subparser.add_parser(
		"shell",
		help="See xim shell -h",
	)
	p_shell.set_defaults(handler=lambda args: p_shell.print_help())
	p_shell_sub = p_shell.add_subparsers()

	# shell install
	p_shell_install = p_shell_sub.add_parser(
		"install",
		help="Install shell to set proxy from github (proxy depend HTTPS_PROXY)",
		description="Install shell to set proxy from github (proxy depend HTTPS_PROXY)"
	)
	p_shell_install.add_argument("shell_name", type=str, help="e.g. \"HTTP_PROXY\" \"npm,git\"")
	p_shell_install.set_defaults(handler=shell_install)

	# shell uninstall
	p_shell_uninstall = p_shell_sub.add_parser(
		"uninstall",
		help="Uninstall shell",
		description="Uninstall shell"
	)
	p_shell_uninstall.add_argument("shell_name", type=str)
	p_shell_uninstall.set_defaults(handler=shell_uninstall)

	# shell search
	p_shell_search = p_shell_sub.add_parser(
		"search",
		help="Search github for shell to set proxy",
		description="Search github for shell to set proxy"
	)
	p_shell_search.add_argument("shell_name", type=str)
	p_shell_search.set_defaults(handler=shell_search)

	# shell list
	p_shell_list = p_shell_sub.add_parser(
		"list",
		help="Show installed shell list",
		description="Show installed shell list"
	)
	p_shell_list.set_defaults(handler=shell_list)

	return parser


def main() -> None:
	config_stream: ConfigJSONFileStream = ConfigJSONFileStream(config_path)
	proxies_stream: ProxiesJSONFileStream = ProxiesJSONFileStream(proxies_path)
	if not config_stream.exists():
		logger.warning("can't find xim.config.json. create default setting")
		config_stream.save(config_default)
	if not proxies_stream.exists():
		logger.warning("can't find xim_proxies.json. create default setting")
		proxies_stream.save(proxies_default)

	parser: argparse.ArgumentParser = get_parser()
	args: argparse.Namespace = parser.parse_args()

	if hasattr(args, 'handler'):
		# intellijで何故かargs.handlerがstrとされる
		try:
			# noinspection PyCallingNonCallable
			args.handler(args)
		except CommandFailedError:
			sys.exit(1)
		else:
			sys.exit(0)
	else:
		logger.error("Undefined command")
		parser.print_help()
		sys.exit(1)


if __name__ == "__main__":
	main()
