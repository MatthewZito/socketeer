def log(**kwargs):
  level, message = kwargs.values()

  prefix = '[-]' if level == 'error' else \
    '[!]' if level == 'warn' else \
    '[+]' if level == 'success' else \
    '[*]'

  print(f'\n{prefix} {message}')

