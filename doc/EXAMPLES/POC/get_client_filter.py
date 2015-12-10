#!/usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
'''Gets clients using a filter that only returns clients that have registered within a certain time'''
__author__ = 'Jim Olsen <jim.olsen@tanium.com>'
__version__ = '2.1.6'

# change me to the location of PyTan!
pytan_loc = '~/gh/pytan'

import os
import sys

sys.dont_write_bytecode = True
sys.path.append(os.path.join(os.path.expanduser(pytan_loc), 'lib'))

my_file = os.path.abspath(sys.argv[0])
my_name = os.path.splitext(os.path.basename(my_file))[0]
my_dir = os.path.dirname(my_file)
parent_dir = os.path.dirname(my_dir)
lib_dir = os.path.join(parent_dir, 'lib')
path_adds = [lib_dir]
[sys.path.append(aa) for aa in path_adds if aa not in sys.path]

import pytan
import pytan.binsupport
import taniumpy


def get_clients_filter(handler, minutes=5):
    kwargs = {}
    if minutes:
        cache_filter = taniumpy.CacheFilter()
        cache_filter.field = 'last_registration'
        cache_filter.type = 'Date'
        cache_filter.operator = 'Greater'
        cache_filter.not_flag = False
        last_registration = -(minutes * 60)
        cache_filter.value = pytan.utils.seconds_from_now(last_registration)

        cache_filter_list = taniumpy.CacheFilterList()
        cache_filter_list.append(cache_filter)
        # cache_filter_list_body = cache_filter_list.toSOAPBody()
        kwargs['cache_filters'] = cache_filter_list

    search_spec = taniumpy.SystemStatusList()
    clients = handler.session.find(search_spec, **kwargs)
    return clients


if __name__ == "__main__":
    pytan.binsupport.version_check(reqver=__version__)

    setupmethod = getattr(pytan.binsupport, 'setup_pytan_shell_argparser')
    responsemethod = getattr(pytan.binsupport, 'process_pytan_shell_args')

    parser = setupmethod(doc=__doc__)
    parser.add_argument(
        '-m',
        '--minutes',
        required=False,
        action='store',
        dest='minutes',
        type=int,
        default=5,
        help='Only return clients that have registered in the last minutes',
    )
    args = parser.parse_args()

    handler = pytan.binsupport.process_handler_args(parser=parser, args=args)
    response = responsemethod(parser=parser, handler=handler, args=args)

    clients = get_clients_filter(handler, minutes=args.minutes)
    print clients
