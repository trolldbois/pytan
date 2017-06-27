"""Extension for Pytan to enable uploading a local file to the Tanium Platform API."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import base64
import hashlib
import logging
import os
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


CHUNK_SIZE = 64 * 1024


class UploadFile(object):
    """Custom extension class to provide the ability to upload a file to the Tanium API.

    handler : instantiated handler object
    """

    def __init__(self, handler, **kwargs):
        """Constructor."""
        self.LOG = logging.getLogger("UploadFile")
        self.handler = handler

    def upload_data(self, data, **kwargs):
        """Upload data to tanium api."""
        kwargs["name"] = kwargs.get("name", "<unknown>")
        kwargs["hash"] = kwargs.get("hash", sha256_hash(data))
        kwargs["size"] = kwargs.get("size", len(data))
        kwargs["hsize"] = b2h(kwargs["size"])
        kwargs["overwrite"] = kwargs.get("overwrite", False)
        kwargs["obj"] = self.start(**kwargs)
        kwargs["pos"] = 0
        for part in chunkify(data):
            kwargs["part"] = part
            kwargs["obj"] = self._send_part(**kwargs)
            kwargs["pos"] += len(part)
        self.finish(**kwargs)
        return kwargs["obj"]

    def upload_file(self, path, **kwargs):
        """Upload a file to tanium api via streaming."""
        path = os.path.expanduser(path)
        path = os.path.abspath(path) if not os.path.isabs(path) else path

        if not os.path.isfile(path):
            m = "File to upload to Tanium API '{}' not found!".format
            raise Exception(m(path))

        kwargs["name"] = path
        kwargs["size"] = os.path.getsize(path)
        kwargs["hsize"] = b2h(kwargs["size"])
        kwargs["overwrite"] = kwargs.get("overwrite", True)
        kwargs["obj"] = self.start(**kwargs)

        hasher = hashlib.sha256()

        kwargs["pos"] = 0
        with open(path, "rb") as fh:
            for part in read_chunks(fh):
                hasher.update(part)
                kwargs["part"] = part
                kwargs["obj"] = self._send_part(**kwargs)
                kwargs["pos"] += len(part)

        kwargs["hash"] = hasher.hexdigest()
        self.finish(**kwargs)
        return kwargs["obj"]

    def finish(self, **kwargs):
        """Finisher for uploading a file/str."""
        if kwargs["hash"] != kwargs["obj"].hash:
            m = "Uploaded file '{name}' hash '{obj.hash}' does not match locally computed hash '{hash}'!".format
            raise Exception(m(**kwargs))

        m = "Finished Upload for file '{name}' with hash '{hash}' ({hsize})".format
        self.LOG.info(m(**kwargs))

    def start(self, **kwargs):
        """Starter for uploading a file/str."""
        m = "Starting Upload for '{name}' ({hsize})".format
        self.LOG.info(m(**kwargs))
        kwargs["obj"] = taniumpy.UploadFile()
        kwargs["obj"].file_size = kwargs["size"]
        kwargs["obj"].force_overwrite = int(kwargs["overwrite"])
        kwargs["obj"] = self._upload_api(**kwargs)
        m = "Received Initial UploadFile for '{name}': {obj}".format
        self.LOG.debug(m(**kwargs))
        return kwargs["obj"]

    def _send_part(self, **kwargs):
        kwargs["psize"] = len(kwargs["part"])
        kwargs["obj"].bytes = base64.b64encode(kwargs["part"])
        kwargs["obj"].file_size = kwargs["size"]
        kwargs["obj"].start_pos = kwargs["pos"]
        kwargs["obj"].part_size = kwargs["psize"]
        kwargs["hpsize"] = b2h(kwargs["psize"])
        kwargs["hpos"] = b2h(kwargs["pos"])
        m = "Sending {obj} for '{name}' ({hpsize} chunk) ({hpos} out of {hsize})".format
        self.LOG.debug(m(**kwargs))
        kwargs["obj"] = self._upload_api(**kwargs)
        kwargs["_c"] = bool(kwargs["obj"].file_cached)
        m = "Received {obj} response for '{name}' cached: {_c}, hash: {obj.hash} - {obj.percent_complete}%".format
        self.LOG.debug(m(**kwargs))
        return kwargs["obj"]

    def _upload_api(self, obj, **kwargs):
        """Send obj to Tanium API using the UploadFile command and return the result."""
        object_list = obj.toSOAPBody(minimal=True)
        command = "UploadFile"
        request_body = self.handler.session._build_body(command=command, object_list=object_list)
        response_body = self.handler.session._get_response(request_body=request_body)
        ret = taniumpy.BaseType.fromSOAPBody(body=response_body)
        return ret


def sha256_hash(data):
    """Return sha 256 hash for data."""
    hasher = hashlib.sha256()
    hasher.update(data)
    ret = hasher.hexdigest()
    return ret


def sha256_file(path):
    """Return sha 256 hash for file."""
    hasher = hashlib.sha256()
    with open(path) as fh:
        for part in read_chunks(fh):
            hasher.update(part)
    ret = hasher.hexdigest()
    return ret


def chunkify(item, size=CHUNK_SIZE):
    """Generator that yields spliced items of item no greater than size."""
    return (item[i:i + size] for i in range(0, len(item), size))


def read_chunks(fh, size=CHUNK_SIZE):
    """Generator that reads a file like fh and yields chunks of size."""
    chunk = fh.read(size)
    while chunk:
        yield chunk
        chunk = fh.read(size)


def b2h(n):
    """Convert bytes int into human friendly string format.

    >>> b2h(10000)
    '9.8 KB'
    >>> b2h(100001221)
    '95.4 MB'
    """
    t = "{0:.2f} {1}".format
    symbols = ("KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    prefix = {s: 1 << (i + 1) * 10 for i, s in enumerate(symbols)}
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return t(value, s)
    return t(n, "B")


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
    uf = UploadFile(handler=handler)
    path = "../../WINPY/py.exe"

    # streaming chunks from file (memory efficient!)
    z1 = uf.upload_file(path=path)

    # load the whole file:
    with open(path, "rb") as fh:
        data = fh.read()

    z2 = uf.upload_data(data=data, name=path)

    same_hash = z2.hash == z1.hash
    log.info("hashes the same: {}".format(same_hash))
