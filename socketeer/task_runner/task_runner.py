import subprocess
from  os.path import relpath

from ..cli import get_args
from ..utils.constants import \
  ROOT_SCRIPTS_DIR as root, \
  UPDATE_REPO as script


def poll ():
  args = get_args()
  host, port = args.dispatch.split(':')
  repo = args.repository

  script_path = f'{root}/{script}'

  while True:
    try:
      subprocess.check_output([
        script_path, 
        repo
      ])

    except OSError as ex:
      if ex.errno == 2:
        raise FileNotFoundError(f'{relpath(script_path)} was not found')
      raise Exception('An I/O error occurred. See: ', ex)

    except subprocess.CalledProcessError as ex:
      raise Exception('Unable to update and observe repository. See: ', ex.output)
