This directory contains a number of scripts used to help automate the release process of pytan.

Nothing in here should be run by anyone unless you know what you are doing.

 * BUILD/build_taniumpy.sh: Will re-generate the lib/taniumpy directory from the taniumpy github repo. Only to be used when we are sure pytan specific changes to taniumpy have been backported to the taniumpy repo, and we know we want to pull in changes from the taniumpy github repo.
 * BUILD/build_bin_scripts.py: Will re-create all scripts in bin/ and winbin/
 * BUILD/build_bin_doc.py: Will create ini files for each script in bin/, then run those using lib/md_doctester.py, which will in turn create a markdown and html file for each script in the bin/ directory under ```BUILD/doc/source/_static/bin_doc```. The Makefile for the doc build process will put these into their proper place
 * BUILD/build_api_examples.py: Will create example python scripts under EXAMPLES/PYTAN_API and SOAP XML examples under EXAMPLES/SOAP_API using the data driven test json files under test/ddt, and will also create ReST documents under ```BUILD/doc/source/examples``` for inclusion into the final doc set
 * BUILD/doc/Makefile: run ```make all``` from in this dir to re-generate the doc/ dir from scratch. This will produce a PDF and HTML set of documentation under the doc/ dir. After doing this, there is some manual work needed to copy the doc/ dir to the pytan.gh-pages repo in order to update the github pages doc set for pytan.
 * BUILD/ARCHIVE/STATICWINBUILD/*.bat: VERY OLD/UNMAINTAINED -- Must be run on a windows system. Will produce a staticly compiled version of a given bin/ script, zip it up, then store the zip file in ZIP_DIST/
