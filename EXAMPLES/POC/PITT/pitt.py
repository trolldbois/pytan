'''Post Install Tanium Tool'''

import os

from localconfig import config as cp

from pytan import binsupport

__author__ = 'Jim Olsen <jim.olsen@tanium.com>'
__version__ = '2.1.9'

if __name__ == "__main__":
    binsupport.version_check(reqver=__version__)
    setupmethod = getattr(binsupport, 'setup_pytan_shell_argparser')
    parser = setupmethod(doc=__doc__)

    parser.add_argument(
        '--config_file',
        required=True,
        default='pitt.ini',
        action='store',
        dest='config_file',
        help='Path to PITT Configuration File',
    )

    args = parser.parse_args()
    handler = binsupport.process_handler_args(parser=parser, args=args)
    responsemethod = getattr(binsupport, 'process_pytan_shell_args')
    response = responsemethod(parser=parser, handler=handler, args=args)

    cf = args.config_file
    if not os.path.isfile(cf):
        m = "CONFIG: Unable to find file '{}'".format
        raise Exception(m(args.config_file))

    m = "CONFIG: Loading file: '{}'".format
    handler.mylog.debug(m(cf))

    try:
        cp.read(cf)
    except Exception as e:
        m = "CONFIG: Failed to read ini file: {}, {}".format
        raise Exception(m(cf, e))

    # parsed_items = {s: {k: v for k, v in cp.items(s)} for s in cp}
    # m = "CONFIG: parsed values from config file '{}': {}".format
    # self.mylog.debug(m(cf, self.jsonify(parsed_items)))
