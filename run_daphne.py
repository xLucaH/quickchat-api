# Custom script to run daphne/django server using pycharm with debugger.
# Script taken from https://stackoverflow.com/questions/67467155/run-django-in-debug-mode-with-daphne

import sys

if __name__ == '__main__':
    # insert here whatever commands you use to run daphne
    sys.argv = ['daphne', 'quickchat.asgi:application']
    from daphne.cli import CommandLineInterface

    CommandLineInterface.entrypoint()
