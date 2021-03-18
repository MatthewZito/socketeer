import subprocess

from ..cli import get_args

def poll ():
  args = get_args()
  host, port = args.dispatch.split(":")
  repo = args.repository
  print(host, port, repo)
  while True:
    try:
      subprocess.check_output(["./update_repo.sh", repo])
    except OSError as ex:
      pass # TODO
    except subprocess.CalledProcessError as ex:
      raise Exception("Unable to update and observe repository. See: ", ex.output)
