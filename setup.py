from setuptools import setup

setup(name='taniumpy',
      version='2.2.2',
      package_dir={'taniumpy': 'lib/taniumpy'},
      packages=['taniumpy', 'taniumpy.object_types',],
      )

setup(name='pytan',
      version='2.2.2',
      package_dir={'pytan': 'lib/pytan'},
      packages=['pytan'],
      )