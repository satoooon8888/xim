import argparse

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


def get_parser():
	parser = argparse.ArgumentParser(description="Xim is a Proxy Manager Tool.")
	subparser = parser.add_subparsers()
	# current
	p_current = subparser.add_parser("current", help="show current proxy")

	# proxy
	p_proxy = subparser.add_parser("proxy")
	p_proxy_sub = p_proxy.add_subparsers()

	# proxy set
	p_proxy_set = p_proxy_sub.add_parser("set", help="set your proxy")
	p_proxy_set.add_argument("proxy_name", type=str)

	# proxy add
	p_proxy_add = p_proxy_sub.add_parser("add", help="add input proxy")
	p_proxy_add.add_argument("proxy_name", type=str)

	# proxy delete
	p_proxy_delete = p_proxy_sub.add_parser("delete", help="delete proxy")
	p_proxy_delete.add_argument("proxy_name", type=str)

	# proxy list
	p_proxy_list = p_proxy_sub.add_parser("list", help="show proxy list")

	# shell
	p_shell = subparser.add_parser("shell")
	p_shell_sub = p_shell.add_subparsers()

	# shell install
	p_shell_install = p_shell_sub.add_parser("install")

	# shell uninstall
	p_shell_uninstall = p_shell_sub.add_parser("uninstall")

	# shell search
	p_shell_search = p_shell_sub.add_parser("search")

	# shell list
	p_shell_list = p_shell_sub.add_parser("list")

	return parser


def main() -> None:
	parser = get_parser()
	args = parser.parse_args()
	if args.subcommand in ["current"]:
		pass
	if args.subcommand in ["proxy"]:
		if args.subcommand.subcommand in ["set"]:
			pass
		if args.subcommand.subcommand in ["add"]:
			pass
		if args.subcommand.subcommand in ["delete"]:
			pass
		if args.subcommand.subcommand in ["list"]:
			pass
	if args.subcommand in ["shell"]:
		if args.subcommand.subcommand in ["install"]:
			pass
		if args.subcommand.subcommand in ["uninstall"]:
			pass
		if args.subcommand.subcommand in ["search"]:
			pass
		if args.subcommand.subcommand in ["list"]:
			pass


if __name__ == "__main__":
	main()
