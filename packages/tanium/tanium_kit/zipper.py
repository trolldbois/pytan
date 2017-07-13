from __future__ import absolute_import, division, print_function, unicode_literals

import datetime
import logging
import os
import re
import zipfile

LOG = logging.getLogger(__name__.split(".")[-1])

DEFAULT_SKIPS = [
    r"{zip_file}",
    r"\.DS_Store",
    r"\.com\.apple.*",
]

ZIP_ADD = "Zipping {} '{}' as '{}'".format
ZIP_SKIP = "Skipping {} '{}', matches pattern '{}'".format
ZIP_MAKE = "{} ZIP '{}' of source path '{}'".format
ZIP_PATTERNS = "Skip patterns: {}".format


def skip_check(p, t, skips):
    for s in skips:
        if re.findall(s, p):
            LOG.info(ZIP_SKIP(t, p, s))
            return True
    return False


def zip_walk(zf, src_path, **kwargs):
    dest_path = kwargs.get("dest_path", "")
    skips = kwargs.get("skips", [])
    compress_type = kwargs.get("compress_type", 0)

    basename = os.path.dirname(src_path)

    for dirname, subdirs, files in os.walk(src_path):
        if dest_path:
            dest_dir = dirname.replace(src_path, "")
            dest_dir = dest_dir.lstrip(os.path.sep)
            dest_dir = os.path.join(dest_path, dest_dir)
        else:
            dest_dir = dirname.replace(basename, "")

        dest_dir = dest_dir.lstrip(os.path.sep)

        if skip_check(dirname, "directory", skips):
            continue

        LOG.info(ZIP_ADD("directory", dirname, dest_dir))
        zf.write(filename=dirname, arcname=dest_dir, compress_type=compress_type)

        for filename in files:
            src_file = os.path.join(dirname, filename)
            dest_file = os.path.join(dest_dir, filename)

            if skip_check(src_file, "file", skips):
                continue

            LOG.debug(ZIP_ADD("file", src_file, dest_file))
            zf.write(filename=src_file, arcname=dest_file, compress_type=compress_type)

    return zf


def mkzip(zip_path, src_path, **kwargs):
    dest_path = kwargs.get("dest_path", "")
    skips = kwargs.get("skips", [])
    compress = kwargs.get("compress", True)
    remove_old = kwargs.get("remove_old", True)
    zip_path = os.path.abspath(zip_path)

    if compress:
        try:
            import zlib  # noqa
            compress_type = zipfile.ZIP_DEFLATED
        except:
            compress_type = zipfile.ZIP_STORED
    else:
        compress_type = zipfile.ZIP_STORED

    ret = {
        "zip_path": zip_path,
        "zip_file": os.path.basename(zip_path),
        "src_path": src_path,
        "dest_path": dest_path,
    }

    all_skips = skips + [x.format(**ret) for x in DEFAULT_SKIPS]
    all_skips = [x for x in all_skips if x]
    skip_text = ", ".join(["'{}'".format(x) for x in all_skips])

    if remove_old and os.path.isfile(zip_path):
        m = "REMOVING OLD ZIP '{}'"
        m = m.format(zip_path)
        LOG.warning(m)

    LOG.info(ZIP_MAKE("Creating", zip_path, src_path))
    LOG.info(ZIP_PATTERNS(skip_text))

    with zipfile.ZipFile(zip_path, "w") as zf:
        zip_walk(
            zf=zf,
            src_path=src_path,
            dest_path=dest_path,
            skips=all_skips,
            compress_type=compress_type,
        )

    LOG.info(ZIP_MAKE("Created", zip_path, src_path))
    return ret


def zip_info(zip_path, details=False):
    zf = zipfile.ZipFile(zip_path)
    for info in zf.infolist():
        if details:
            LOG.info('Archived filename: {}'.format(info.filename))
            LOG.info('\tComment: {}'.format(info.comment))
            LOG.info('\tModified: {}'.format(datetime.datetime(*info.date_time)))
            LOG.info('\tSystem: {} (0 = Windows, 3 = Unix)'.format(info.create_system))
            LOG.info('\tZIP version: {}'.format(info.create_version))
            LOG.info('\tCompressed: {} bytes'.format(info.compress_size))
            LOG.info('\tUncompressed: {} bytes'.format(info.file_size))
        else:
            LOG.info('Archived filename: {}'.format(info.filename))
    zf.close()
