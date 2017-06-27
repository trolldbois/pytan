#!/usr/bin/env python -i
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
"""Provides an interactive console with pytan available as handler."""
__author__ = 'Jim Olsen <jim.olsen@tanium.com>'
__version__ = '2.2.0'

pytan_path = "/github/pytan-master/lib"

import os  # noqa
import sys  # noqa

my_file = os.path.abspath(sys.argv[0])
my_name = os.path.splitext(os.path.basename(my_file))[0]
my_dir = os.path.dirname(my_file)
parent_dir = os.path.dirname(my_dir)
lib_dir = os.path.join(parent_dir, 'lib')
path_adds = [lib_dir, pytan_path]
[sys.path.append(aa) for aa in path_adds if aa not in sys.path]

try:
    import pytan  # noqa
    import pytan.binsupport  # noqa
    import taniumpy  # noqa
except Exception:
    raise


def handle_cgs(handler, obj, kwargs):
    """Example PreAddAction callback that modifies the target_group of an Action if computer group names are supplied.

    callbacks = {}
    callbacks["PreAddAction"] = handle_cgs
    deploy_action(package="blah", cg_names=["ip has 192.168", "has tanium app"], action_filters=["Computer Name, that contains:a"], callbacks=callbacks)
    """
    cgs = kwargs.get("cg_names", [])
    cg_objs = [handler.get("group", name=x)[0] for x in cgs]
    cg_listobj = taniumpy.GroupList()
    [cg_listobj.append(x) for x in cg_objs]

    if cg_objs:
        tg_obj = taniumpy.Group()
        tg_obj.sub_groups = cg_listobj
        tg_obj.and_flag = 0
        if obj.target_group is not None:
            tg_obj.sub_groups.append(obj.target_group)
        obj.target_group = tg_obj
    return obj


if __name__ == "__main__":
    pytan.binsupport.version_check(reqver=__version__)

    setupmethod = getattr(pytan.binsupport, 'setup_pytan_shell_argparser')
    responsemethod = getattr(pytan.binsupport, 'process_pytan_shell_args')

    parser = setupmethod(doc=__doc__)
    args = parser.parse_args()

    handler = pytan.binsupport.process_handler_args(parser=parser, args=args)
    response = responsemethod(parser=parser, handler=handler, args=args)
    callbacks = {}
    callbacks["PreAddAction"] = handle_cgs

    v = handler.deploy_action(
        package="Distribute Copy Tools",
        cg_names=["ip has 192.168", "has tanium app"],
        action_filters=["Computer Name, that contains:a", "Computer Name, that contains:c"],
        callbacks=callbacks,
        run=True,
        get_results=False,
        action_options=["or"],
    )
    po = v["poller_object"]
    m = "Resolved target group to: {}".format
    print(m(po.target_group.text))
    """
    Will output line as follows (note target has action filters AND computer groups):

    Resolved target group to:  ( Tanium Client IP Address starting with "192.168.1" or Running Applications containing "tanium" or ( Computer Name containing "a" or Computer Name containing "c" ) )
    """
