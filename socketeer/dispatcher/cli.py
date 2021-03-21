from argparse import ArgumentParser

parser = ArgumentParser()

parser.add_argument(
	'--host',
	help='dispatch srv host',
	default='localhost',
	action='store'
)

parser.add_argument(
	'--port',
	help='dispatch srv port',
	default='9000',
	action='store'
)

def get_args():
    return parser.parse_args()
