from setuptools import setup

setup(name='pytan',
      version='2.2.2',
      package_dir={'pytan': 'lib/pytan'},
      packages=['pytan'],
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
            #"enum",
            #"ipaddress",
            #"OpenSSL",
      ],
      )