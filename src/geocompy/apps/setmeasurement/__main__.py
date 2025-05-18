from .cli import build_parser


parser = build_parser()
args = parser.parse_args()
args.func(args)
