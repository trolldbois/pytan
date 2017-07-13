from __future__ import absolute_import, division, print_function, unicode_literals

import argparse
import os
import sys


TRUE_STR = ("yes", "y", "true", "t", "1")
FAIL_STR = ("no", "n", "false", "f", "0")

'''
from argparse import ArgumentDefaultsHelpFormatter as ArgFormatter
from argparse import RawDescriptionHelpFormatter as RawFormatter

class CustomArgFormat(ArgFormatter, RawFormatter):
    """Multiple inheritance Formatter class for :class:`argparse.ArgumentParser`.

    If a :class:`argparse.ArgumentParser` class uses this as it's Formatter class, it will show
    the defaults for each argument in the `help` output
    """
    pass
'''


class ShellParser(argparse.ArgumentParser):

    def __init__(self, *args, **kwargs):
        self.script = kwargs.pop('script', __name__)

        # if 'formatter_class' not in kwargs:
        #     kwargs['formatter_class'] = CustomArgFormat

        argparse.ArgumentParser.__init__(self, *args, **kwargs)

    def exit(self, status=0, message=None):
        if message:
            self._print_message(message, sys.stdout)
        os._exit(status)

    def _print_message(self, message, file=None):
        if message:
            if file is None:
                file = sys.stdout
            file.write(message)

    def error(self, message):
        self.print_help()
        message = '\n!! Argument Parsing Error in "{}": {}\n'.format(self.script, message)
        self.exit(2, message)

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


def add_arg_group(parser, group_name, group_opts):
    grp = parser.add_argument_group(group_name)
    for opt_name, opts in sorted(group_opts.items(), key=lambda x: x[1].get("priority", 1)):
        default = opts.get("default", "")
        suppress = opts.get("suppress", False)
        required = opts.get("required", False)
        dest = opts.get("dest", opt_name)
        short = opts.get("short", True)
        long_opt = "--{}".format(opt_name)
        helps = opts.get("help", "No help provided!")
        choices = opts.get("choices", [])

        args = []
        if short is True:
            short_opt = "-{}".format(opt_name[0])
            args.append(short_opt)
        elif short:
            short_opt = "-{}".format(short)
            args.append(short_opt)
        args.append(long_opt)

        kwargs = {}
        kwargs['default'] = argparse.SUPPRESS if suppress else default
        kwargs['required'] = required
        kwargs['dest'] = dest

        if helps:
            choices_txt = ""
            if choices:
                choices_txt = ", ".join(choices)
                choices_txt = " [valid choices: {}]".format(choices_txt)

            default_txt = "[default: '{}']".format(default)

            help_txt = "{} {}{}".format(helps, default_txt, choices_txt)
            help_txt = help_txt.replace("%", "%%")
            kwargs['help'] = help_txt

        if choices:
            kwargs['choices'] = choices

        if isinstance(default, bool):
            kwargs['type'] = str2bool

        elif isinstance(default, int):
            kwargs['type'] = int

        # print("adding arg to group {!r} opts: {!r}, {!r}".format(name, opts, add_opts))
        grp.add_argument(*args, **kwargs)


def make_base_parser(script, doc, opts):
    base = ShellParser(script=script, description=doc, add_help=False)

    for group_name, group_opts in opts.items():
        add_arg_group(base, group_name, group_opts)
    return base


def make_parser(script, doc, version, opts):
    base = make_base_parser(script, doc, opts)
    parser = ShellParser(script=script, description=doc, parents=[base], add_help=False)
    parser.add_argument('--version', action='version', version=version)
    parser.add_argument('--help', action='help')
    return parser
