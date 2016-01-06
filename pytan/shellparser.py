import sys
import argparse

from argparse import ArgumentDefaultsHelpFormatter as ArgFormatter
from argparse import RawDescriptionHelpFormatter as RawFormatter

TRUE_STR = ("yes", "true", "t", "1")
FAIL_STR = ("no", "false", "f", "0")


class CustomArgFormat(ArgFormatter, RawFormatter):
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


def str2bool(v):
    if v.lower() in TRUE_STR:
        result = True
    elif v.lower() in FAIL_STR:
        result = False
    else:
        err = "{!r} not a valid choice, must be one of {} for true, or one of {} for false"
        err = err.format(v, ', '.join(TRUE_STR), ', '.join(FAIL_STR))
        raise argparse.ArgumentTypeError(err)
    return result


def add_arg_group(parser, name, opt_dict, defaults={}):
    grp = parser.add_argument_group(name)
    for k, v in opt_dict.items():
        hd = defaults.get(k, '')

        opts = []
        opts.append('--' + k)

        if v.get('short'):
            opts.append('-' + v['short'])

        add_opts = {}
        add_opts['default'] = argparse.SUPPRESS
        add_opts['required'] = False
        add_opts['dest'] = k

        if v.get('help', ''):
            h = '{} (default: {!r})'.format(v['help'], hd)
            h = h.replace('%', '%%')
            add_opts['help'] = h

        if v.get('choices', []):
            add_opts['choices'] = v['choices']

        if isinstance(hd, int):
            add_opts['type'] = int
        elif isinstance(hd, bool):
            add_opts['type'] = str2bool

        # print("adding arg to group {!r} opts: {!r}, {!r}".format(name, opts, add_opts))
        grp.add_argument(*opts, **add_opts)
