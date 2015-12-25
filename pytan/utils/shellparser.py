import sys
import argparse

from argparse import ArgumentDefaultsHelpFormatter as A1 # noqa
from argparse import RawDescriptionHelpFormatter as A2 # noqa


class CustomArgFormat(A1, A2):
    """Multiple inheritance Formatter class for :class:`argparse.ArgumentParser`.

    If a :class:`argparse.ArgumentParser` class uses this as it's Formatter class, it will show
    the defaults for each argument in the `help` output
    """
    pass


class ShellParser(argparse.ArgumentParser):
    """Custom :class:`argparse.ArgumentParser` class which does a number of things:

        * Uses :class:`pytan.utils.CustomArgFormat` as it's Formatter class, if none was passed in
        * Prints help if there is an error
        * Prints the help for any subparsers that exist
    """
    def __init__(self, *args, **kwargs):
        self.my_file = kwargs.pop('my_file', __name__)

        if 'formatter_class' not in kwargs:
            kwargs['formatter_class'] = CustomArgFormat

        argparse.ArgumentParser.__init__(self, *args, **kwargs)

    def error(self, message):
        self.print_help()
        print('\n!! Argument Parsing Error in "{}": {}\n'.format(self.my_file, message))
        sys.exit(2)

    def print_help(self, **kwargs):
        super(ShellParser, self).print_help(**kwargs)
        subparsers_actions = [
            action for action in self._actions
            if isinstance(action, argparse._SubParsersAction)
        ]
        for subparsers_action in subparsers_actions:
            print("")
            for choice, subparser in subparsers_action.choices.items():
                print(subparser.format_help())
