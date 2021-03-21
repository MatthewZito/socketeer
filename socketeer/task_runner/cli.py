from argparse import ArgumentParser

from ..utils.constants import RANGE_INIT as port_range

parser = ArgumentParser()

parser.add_argument(
    '--host',
    help='task runner thread host',
    default='localhost',
    action='store'
)

parser.add_argument('--port',
    help=f'task runner thread port; by default >= {port_range}',
    action='store'
)

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
