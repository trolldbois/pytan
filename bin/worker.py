"""pass."""
__author__ = 'Jim Olsen <jim.olsen@tanium.com>'
__version__ = '4.0.0'

import os
import sys

try:
    import pytan  # noqa
except Exception as e:
    print("ERROR: Unable to import pytan package, error: '{}'".format(e))
    print("Full PYTHONPATH: {}".format(', '.join(sys.path)))
    sys.exit(99)


def get_shell_name():
    """pass."""
    try:
        shell_name = sys.argv.pop(1)
    except:
        print("ERROR: Missing the first argument in the format of 'shell:SCRIPT_NAME'")
        sys.exit(99)

    if shell_name.startswith('shell:'):
        shell_name = shell_name.replace('shell:', '')
    else:
        err = "ERROR: First argument {!r} does not begin with 'shell:' followed by SCRIPT_NAME"
        err = err.format(shell_name)
        print(err)
        sys.exit(99)

    return shell_name


if __name__ == "__main__":
    shell_name = get_shell_name()

    # set the first argument to the name of the script that called us
    sys.argv[0] = shell_name

    # find the worker from shell_name without the extension
    worker_basename = os.path.splitext(shell_name)[0]
    worker_module = "pytan.shell.{}".format(worker_basename)

    __import__(worker_module)
    module = eval(worker_module)
    worker = module.Worker()

    version_check = worker.version_check(__version__)
    console = worker.interactive_check()
    check = worker.check()
    setup = worker.setup()
    args = worker.parse_args()
    handler = worker.get_handler()
    result = worker.get_result()
    exec(worker.get_exec())
