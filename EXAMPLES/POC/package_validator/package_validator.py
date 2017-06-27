"""Create/validate/save a package based on a directory and a metadata file."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import json
import logging
import os
import re
import sys

THIS_FILE = os.path.abspath(__file__)
THIS_SCRIPT = os.path.basename(THIS_FILE)
THIS_PATH = os.path.dirname(THIS_FILE)
TOOL_PATH = os.path.dirname(THIS_PATH)

if THIS_PATH not in sys.path:
    sys.path.append(THIS_PATH)

if TOOL_PATH not in sys.path:
    sys.path.insert(0, TOOL_PATH)

try:
    import log_help
    import md_structure
    import md_parser
    import upload_file
    import param_help
except Exception:
    raise

try:
    import libs_external  # TOOL_PATH/libs_external/  # noqa
    import libs_tanium  # TOOL_PATH/libs_tanium/  # noqa
except Exception:
    raise

try:
    import pytan
    import pytan.binsupport
    import taniumpy
except Exception:
    raise


def make_abs(path, prefix):
    """Make path absolute with prefix if it is not."""
    ret = os.path.join(prefix, path) if not os.path.isabs(path) else path
    return ret


class PkgVal(object):
    """Find or create and validate packages from a directory of files containing a metadata json file.

    handler : instantiated handler object
    """

    def __init__(self, handler, **kwargs):
        """Constructor."""
        self.LOG = logging.getLogger("PkgVal")
        self.handler = handler
        self.uploader = upload_file.UploadFile(handler=handler)
        self.mdparser = md_parser.MetaDataParser(structure=md_structure.md_structure)

    def start(self, md_path):
        """Start workflow."""
        m = "Starting Package Validator for metadata file '{}'".format
        self.LOG.info(m(md_path))

        md = self.mdparser.from_json_file(json_path=md_path)

        cmd_params = re.findall("\$\d+", md["command"])
        md_params = md.get("parameters", [])

        if len(cmd_params) != len(md_params):
            m = "Command '{}' in metadata refers to {} parameters, but {} parameters defined in metadata!".format
            raise Exception(m(md["command"], len(cmd_params), len(md_params)))

        try:
            obj = self.handler.get("package", name=md["name"])[0]
            obj._FOUND = True
        except Exception:
            obj = taniumpy.PackageSpec()
            obj.name = md["name"]
            obj._FOUND = False
        finally:
            f = "found" if obj._FOUND else "did not find, will create"
            m = "{} {}".format
            self.LOG.info(m(self._pi(obj), f))

        obj = self.val_attr(obj=obj, md=md, attr="command")
        obj = self.val_attr(obj=obj, md=md, attr="command_timeout")
        obj = self.val_attr(obj=obj, md=md, attr="expire_seconds")
        obj = self.val_attr(obj=obj, md=md, attr="display_name")
        obj = self.val_attr(obj=obj, md=md, attr="hidden_flag", bool2int=True)
        obj = self.val_files(obj=obj, md=md, md_path=md_path)
        obj = self.val_params(obj=obj, md=md)

        obj_found = getattr(obj, "_FOUND", False)
        obj_changed = getattr(obj, "_CHANGED", False)

        if obj_found:
            if obj_changed:
                obj = self.handler.session.save(obj)
                m = "Updated existing {} via Tanium API".format
                self.LOG.info(m(self._pi(obj)))
            else:
                m = "No changes made to existing {} via Tanium API".format
                self.LOG.info(m(self._pi(obj)))
        elif not obj_found:
            obj = self.handler.session.add(obj)
            m = "Created new {} via Tanium API".format
            self.LOG.info(m(self._pi(obj)))

        m = "Finished Package Validator for metadata file '{}'".format
        self.LOG.info(m(md_path))
        return obj

    def val_params(self, obj, md):
        """Validate params in obj against md."""
        md_params = md.get("parameters", [])

        current_pd_raw = obj.parameter_definition or "{}"
        try:
            current_pd = json.loads(current_pd_raw)
        except Exception as e:
            m = "Failed to load JSON parameter definition {} from {}, error: {}".format
            raise Exception(m(current_pd_raw, obj, e))
        current_params = current_pd.get("parameters", []) or []
        current_pnames = [x["key"] for x in current_params]

        ph = param_help.ParamHelper()
        new_pd = ph.build_param_def(params=md_params)
        new_params = new_pd.get("parameters", []) or []
        new_pnames = [x["key"] for x in new_params]
        new_pd_raw = json.dumps(new_pd)

        if current_pd_raw != new_pd_raw:
            m = "Removing {} parameters from {} ({})".format
            self.LOG.info(m(len(current_params), self._pi(obj), ", ".join(current_pnames)))
            m = "Adding {} parameters to {} ({})".format
            self.LOG.info(m(len(new_params), self._pi(obj), ", ".join(new_pnames)))
            obj.parameter_definition = new_pd_raw
            obj._CHANGED = True
        return obj

    def val_files(self, obj, md, md_path):
        """Validate files in obj against md."""
        md_dir = os.path.dirname(md_path)
        for md_file in md["files"]:
            path = make_abs(md_file, md_dir)
            obj, do_upload = self.check_remove_file(obj, path)
            if do_upload:
                obj._CHANGED = True
                obj.files = obj.files if obj.files is not None else taniumpy.PackageFileList()

                upload_obj = self.uploader.upload_file(path=path)

                file_obj = taniumpy.PackageFile()
                file_obj.name = os.path.basename(path)
                file_obj.hash = upload_obj.hash
                file_obj.size = os.path.getsize(path)

                obj.files.append(file_obj)
                m = "Added {} to {}".format
                self.LOG.info(m(self._fi(file_obj), self._pi(obj)))
        return obj

    def check_remove_file(self, obj, path):
        """Check if basename of path is one of the files in obj.files."""
        md_file = os.path.basename(path)
        obj_files = obj.files if obj.files is not None else taniumpy.PackageFileList()
        found = [(idx, x) for idx, x in enumerate(obj_files) if x.name == md_file]

        if found:
            idx, file_obj = found[0]
            md_sha_hash = upload_file.sha256_file(path)
            if md_sha_hash != file_obj.hash:
                m = "Removing {} from {} (hash mis-match, will re-upload)".format
                self.LOG.info(m(self._fi(file_obj), self._pi(obj)))
                del(obj.files.file[idx])
                do_upload = True
            else:
                do_upload = False
        else:
            do_upload = True
        return obj, do_upload

    def _fi(self, o, extra=[["hash", ""], ["source", ""]]):
        """Object info string for file object o."""
        ret = self._oi(o=o, extra=extra)
        return ret

    def _pi(self, o, extra=[["last_update", ""]]):
        """Object info string for package object o."""
        ret = self._oi(o=o, extra=extra)
        return ret

    def _oi(self, o, attrs=[["name", ""], ["id", ""]], extra=[]):
        """Object info string for object o."""
        oc = o.__class__.__name__
        oa = ["{}: '{}'".format(x, getattr(o, x, y)) for x, y in attrs]
        oe = ["{}: '{}'".format(x, getattr(o, x, y)) for x, y in extra]
        ret = "{} {}".format(oc, ", ".join(oa + oe))
        return ret

    def val_attr(self, obj, md, attr, **kwargs):
        """Validate that value for attr in obj matches value for attr in md."""
        md_val = md.get(attr, None)
        obj_val = getattr(obj, attr)
        bool2int = kwargs.get("bool2int", False)

        if md_val in [None, ""]:
            m = "Attribute '{}' not defined in metadata, skipping validation against object".format
            self.LOG.info(m(attr))
        else:
            md_val = int(md_val) if bool2int else md_val
            if obj_val == md_val:
                m = "Attribute '{}' matches metadata value, not changing".format
                self.LOG.info(m(attr))
            else:
                m = "Attribute '{}' does not match metadata value, updating '{}' to '{}'".format
                self.LOG.info(m(attr, obj_val, md_val))
                setattr(obj, attr, md_val)
                obj._CHANGED = True
        return obj


def run_argparse():
    """Parse command line arguments."""
    arg_setup = getattr(pytan.binsupport, 'setup_pytan_shell_argparser')
    parser = arg_setup(doc=__doc__)
    # parser.add_argument(
    #     '-m',
    #     '--minutes',
    #     required=False,
    #     action='store',
    #     dest='minutes',
    #     type=int,
    #     default=5,
    #     help='Only return clients that have registered in the last minutes',
    # )
    args = parser.parse_args()
    return parser, args


if __name__ == "__main__":
    log = log_help.setup_logging()
    log_help.log_control(name="urllib3.connectionpool", loud=False)

    parser, args = run_argparse()
    handler = pytan.binsupport.process_handler_args(parser=parser, args=args)

    debug = False
    log_level = logging.DEBUG if debug else logging.INFO
    log.setLevel(log_level)
    # TODO(BLAH)

    pkg_dir = "tdc_client"
    pkg_path = os.path.join(os.path.dirname(THIS_PATH), pkg_dir)
    pkg_win_json = os.path.join(pkg_path, "METADATA_WIN.json")
    pv = PkgVal(handler=handler)
    pkg = pv.start(md_path=pkg_win_json)
