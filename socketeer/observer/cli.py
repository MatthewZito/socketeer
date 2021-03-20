from argparse import ArgumentParser

parser = ArgumentParser()

parser.add_argument(
	'--dispatch',
	help='dispatch host:port',
	default='localhost:9000',
	action='store'
)

parser.add_argument(
	'repository',
	metavar='REPO',
	type=str,
	help='path to the observed repository'
)

def get_args():
  	return parser.parse_args()
