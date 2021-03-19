from .task_runner import task_runner
from .utils.log import log

if __name__ == '__main__':
  try:
    task_runner.poll()

  except KeyboardInterrupt as ex:
    log(
      level='warn', 
      message='Execution cancelled by user'
    )

  except Exception as ex:
    log(
      level='error', 
      message=f'An exception occurred. See: {ex}'
    )