from .task_runner import task_runner

if __name__ == "__main__":
  try:
    task_runner.poll()
  except Exception as ex:
    print("An exception occurred ", ex)