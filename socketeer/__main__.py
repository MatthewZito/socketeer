from argparse import ArgumentParser

from .observer import observer
from .utils.io import log

if __name__ == '__main__':
    try:
        observer.poll()

    except KeyboardInterrupt as ex:
        log(
            level='warn', 
            message='Execution cancelled by user'
        )

    except Exception as ex:
        log(
            level='error',
            message=ex
        )
