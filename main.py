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
from utils import TerminateError

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
	parser = argparse.ArgumentParser(description="Xim is a proxy manager tool.")
	subparser = parser.add_subparsers()

	# current
	p_current = subparser.add_parser("current", help="show current proxy")
	p_current.set_defaults(handler=current)

	# proxy
	p_proxy = subparser.add_parser("proxy", help="see xim proxy -h")
	p_proxy.set_defaults(handler=lambda args: p_proxy.print_help())
	p_proxy_sub = p_proxy.add_subparsers()

	# proxy set
	p_proxy_set = p_proxy_sub.add_parser("set", help="set your proxy")
	p_proxy_set.add_argument("proxy_name", type=str)
	p_proxy_set.set_defaults(handler=proxy_set)

	# proxy add
	p_proxy_add = p_proxy_sub.add_parser("add", help="add inputted proxy")
	p_proxy_add.add_argument("proxy_name", type=str)
	p_proxy_add.set_defaults(handler=proxy_add)

	# proxy delete
	p_proxy_delete = p_proxy_sub.add_parser("delete", help="delete proxy")
	p_proxy_delete.add_argument("proxy_name", type=str)
	p_proxy_delete.set_defaults(handler=proxy_delete)

	# proxy list
	p_proxy_list = p_proxy_sub.add_parser("list", help="show proxy list")
	p_proxy_list.set_defaults(handler=proxy_list)

	# shell
	p_shell = subparser.add_parser("shell", help="see xim shell -h")
	p_shell.set_defaults(handler=lambda args: p_shell.print_help())
	p_shell_sub = p_shell.add_subparsers()

	# shell install
	p_shell_install = p_shell_sub.add_parser("install", help="install shell to set proxy from github")
	p_shell_install.add_argument("shell_name", type=str)
	p_shell_install.set_defaults(handler=shell_install)

	# shell uninstall
	p_shell_uninstall = p_shell_sub.add_parser("uninstall", help="uninstall shell")
	p_shell_uninstall.add_argument("shell_name", type=str)
	p_shell_uninstall.set_defaults(handler=shell_uninstall)

	# shell search
	p_shell_search = p_shell_sub.add_parser("search", help="search a shell from github")
	p_shell_search.add_argument("shell_name", type=str)
	p_shell_search.set_defaults(handler=shell_search)

	# shell list
	p_shell_list = p_shell_sub.add_parser("list", help="show installed shell list")
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
			args.handler(args)
		except TerminateError:
			logger.error("terminated.")
	else:
		parser.print_help()


if __name__ == "__main__":
	main()
