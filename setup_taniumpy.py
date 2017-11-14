from setuptools import setup

setup(name='taniumpy',
      version='2.2.2',
      package_dir={'taniumpy': 'lib/taniumpy'},
      packages=['taniumpy', 'taniumpy.object_types',],
      requires=[
            "asn1crypto",
            "certifi",
            "cffi",
            "chardet",
            "cryptography",
            "idna",
            "pycparser",
            "pyOpenSSL",
            "requests",
            "six",
            "urllib3",
            "xmltodict",
      ],
      )
