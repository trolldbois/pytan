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
    """Example PreAddQuestion callback that modifies the group of a question if computer group names are supplied.

    callbacks = {}
    callbacks["PreAddQuestion"] = handle_cgs
    handler.ask_manual(
        sensors=["Computer Name", "Operating System", "Folder Contents{folderPath=C:\\Program Files}"],
        cg_names=["ip has 192.168", "has tanium app"],
        callbacks=callbacks)
    """
    cgs = kwargs.get("cg_names", [])
    cg_objs = [handler.get("group", name=x)[0] for x in cgs]
    cg_listobj = taniumpy.GroupList()
    [cg_listobj.append(x) for x in cg_objs]

    if cg_objs:
        tg_obj = taniumpy.Group()
        tg_obj.sub_groups = cg_listobj
        tg_obj.and_flag = 0
        if obj.group is not None:
            tg_obj.sub_groups.append(obj.group)
        obj.group = tg_obj
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
    callbacks["PreAddQuestion"] = handle_cgs

    v = handler.ask_manual(
        sensors=["Computer Name", "Operating System", "Folder Contents{folderPath=C:\\Program Files}"],
        cg_names=["ip has 192.168", "has tanium app"],
        callbacks=callbacks,
        get_results=False,
    )
    qo = v["question_object"]
    m = "Resolved question to: {}".format
    print(m(qo.query_text))
    """
    Will output line as follows (note target has computer groups):

    Resolved question to: Get Computer Name and Operating System and Folder Contents[C:\Program Files] from all machines with ( Tanium Client IP Address starting with "192.168.1" or Running Applications containing "tanium" )
    """
