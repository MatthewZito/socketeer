import socket

def broadcast(host, port, payload):
    """Open a socket conn on given host, port and send the provided payload

    Await the buffered response and return it

    Args:
        host (str): hostname on which socket conn will be opened
        port (int): port on which socket conn will be opened
        payload (str): data to send via socket conn
    """
    s = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    s.connect((host, port))
    s.send(payload)

    response = s.recv(1024)
    s.close()

    return response


def log(**kwargs):
    level, message = kwargs.values()

    prefix = '[-]' if level == 'error' else \
        '[!]' if level == 'warn' else \
        '[+]' if level == 'success' else \
        '[*]'

    print(f'\n{prefix} {message}')
