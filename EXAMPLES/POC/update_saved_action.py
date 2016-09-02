#!/usr/bin/env python -i
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
'''Provides an interactive console with pytan available as handler'''
__author__ = 'Jim Olsen <jim.olsen@tanium.com>'
__version__ = '2.1.5'

import os
import sys
sys.dont_write_bytecode = True

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

if __name__ == "__main__":
    pytan.binsupport.version_check(reqver=__version__)

    setupmethod = getattr(pytan.binsupport, 'setup_pytan_shell_argparser')
    responsemethod = getattr(pytan.binsupport, 'process_pytan_shell_args')

    parser = setupmethod(doc=__doc__)
    parser.add_argument(
        '--id',
        required=True,
        action='store',
        dest='id',
        default=None,
        help='ID of saved action to retrieve',
    )
    parser.add_argument(
        '--tag',
        required=True,
        action='append',
        dest='tags',
        default=[],
        help='key:value of tag to add',
    )

    args = parser.parse_args()
    tags_to_add = dict([x.split(':') for x in args.tags])

    handler = pytan.binsupport.process_handler_args(parser=parser, args=args)
    response = responsemethod(parser=parser, handler=handler, args=args)

    try:
        saved_action_list = handler.get('saved_action', id=args.id)
    except:
        print('failed to retrieve saved_action id {}'.format(args.id))
        sys.exit(1)

    saved_action = saved_action_list[0]
    print('found saved_action: {}'.format(saved_action))

    if saved_action.metadata is None:
        saved_action.metadata = taniumpy.MetadataList()

    for k, v in tags_to_add.items():
        pre_exists = False
        for m in saved_action.metadata:
            if k == m.name.replace('TConsole.SavedAction.', ''):
                duh = 'overwriting tag {!r} from value {!r} to value {!r}'.format
                print(duh(k, m.value, v))
                # overwrite the value
                m.value = v
                # continue on to next tag to add
                pre_exists = True
                break

        if pre_exists:
            continue

        duh = 'creating new tag {!r} with value {!r}'.format
        print(duh(k, v))

        new_item = taniumpy.MetadataItem()
        new_item.name = 'TConsole.SavedAction.{}'.format(k)
        new_item.value = v
        saved_action.metadata.append(new_item)

    updated_sa = handler.session.save(saved_action)
    print('updated saved_action {}'.format(saved_action))
