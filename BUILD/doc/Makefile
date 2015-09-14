# Makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
PAPER         =
BUILDDIR      = build
REALBUILDDIR  = ../../doc
STATIC_DOCDIR = static_doc

# User-friendly check for sphinx-build
ifeq ($(shell which $(SPHINXBUILD) >/dev/null 2>&1; echo $$?), 1)
$(error The '$(SPHINXBUILD)' command was not found. Make sure you have Sphinx installed, then set the SPHINXBUILD environment variable to point to the full path of the '$(SPHINXBUILD)' executable. Alternatively you can add the directory with the executable to your PATH. If you don't have Sphinx installed, grab it from http://sphinx-doc.org/)
endif

# Internal variables.
PAPEROPT_a4     = -D latex_paper_size=a4
PAPEROPT_letter = -D latex_paper_size=letter
ALLSPHINXOPTS   = -d $(BUILDDIR)/doctrees $(PAPEROPT_$(PAPER)) $(SPHINXOPTS) source
# the i18n builder cannot share the environment and doctrees with the others
I18NSPHINXOPTS  = $(PAPEROPT_$(PAPER)) $(SPHINXOPTS) source
VERSION         = $(shell cat ../../lib/pytan/__init__.py|grep __version__|cut -d\' -f2)


.PHONY: help clean html dirhtml singlehtml pickle json htmlhelp qthelp devhelp epub latex latexpdf text man changes linkcheck doctest coverage gettext

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  html       to make standalone HTML files"
	@echo "  htmlzip       to make standalone HTML files into a zipped archive"
	@echo "  latex      to make LaTeX files, you can set PAPER=a4 or PAPER=letter"
	@echo "  latexpdf   to make LaTeX files and run them through pdflatex"
	@echo "  linkcheck  to check all external links for integrity"
	@echo "  coverage   to run coverage check of the documentation (if enabled)"
	@echo "  all        to run clean htmlzip coverage latexpdf"

clean:
	rm -rf $(BUILDDIR)/*
	rm -rf $(REALBUILDDIR)/html/*
	rm -rf $(REALBUILDDIR)/pdf/*

cleanbuild:
	rm -rf $(BUILDDIR)/*

html:
	mkdir -p $(BUILDDIR)/
	mkdir -p $(REALBUILDDIR)/html/PyTan-$(VERSION)-HTML_DOC

	@echo "Re-building source/taniumpy"
	sphinx-apidoc -f -T -M -o source/taniumpy ../../lib/taniumpy/
	perl -pi -e "s/taniumpy package/TaniumPy Package/" source/taniumpy/taniumpy.rst

	$(SPHINXBUILD) -b html $(ALLSPHINXOPTS) $(REALBUILDDIR)/html/PyTan-$(VERSION)-HTML_DOC
	cp $(REALBUILDDIR)/console.wsdl $(REALBUILDDIR)/html/PyTan-$(VERSION)-HTML_DOC/console.wsdl

	@echo
	@echo "Build finished. The HTML pages are in $(REALBUILDDIR)/html/PyTan-$(VERSION)-HTML_DOC"

htmlzip:
	mkdir -p $(BUILDDIR)/
	mkdir -p $(REALBUILDDIR)/html/PyTan-$(VERSION)-HTML_DOC

	@echo "Re-building source/taniumpy"
	sphinx-apidoc -f -T -M -o source/taniumpy ../../lib/taniumpy/
	perl -pi -e "s/taniumpy package/TaniumPy Package/" source/taniumpy/taniumpy.rst

	$(SPHINXBUILD) -b html $(ALLSPHINXOPTS) $(REALBUILDDIR)/html/PyTan-$(VERSION)-HTML_DOC

	cp $(REALBUILDDIR)/console.wsdl $(REALBUILDDIR)/html/PyTan-$(VERSION)-HTML_DOC/console.wsdl
	cd $(REALBUILDDIR)/html/ ; zip -9rm PyTan-$(VERSION)-HTML_DOC.zip PyTan-$(VERSION)-HTML_DOC/

	@echo
	@echo "Build finished. The HTML pages are in $(REALBUILDDIR)/html/PyTan-$(VERSION)-HTML_DOC.zip"

latex:
	$(SPHINXBUILD) -b latex $(ALLSPHINXOPTS) $(BUILDDIR)/latex
	@echo
	@echo "Build finished; the LaTeX files are in $(BUILDDIR)/latex."
	@echo "Run \`make' in that directory to run these through (pdf)latex" \
	      "(use \`make latexpdf' here to do that automatically)."

latexpdf:
	mkdir -p $(BUILDDIR)/
	mkdir -p $(REALBUILDDIR)/pdf/

	$(SPHINXBUILD) -b latex $(ALLSPHINXOPTS) $(BUILDDIR)/latex
	@echo "Running LaTeX files through pdflatex..."
	$(MAKE) -C $(BUILDDIR)/latex all-pdf

	cp $(BUILDDIR)/latex/PyTan.pdf $(REALBUILDDIR)/pdf/PyTan-$(VERSION).pdf
	@echo
	@echo "pdflatex finished; the PDF file is in $(REALBUILDDIR)/pdf/PyTan-$(VERSION).pdf"

linkcheck:
	$(SPHINXBUILD) -b linkcheck $(ALLSPHINXOPTS) $(BUILDDIR)/linkcheck
	@echo
	@echo "Link check complete; look for any errors in the above output " \
	      "or in $(BUILDDIR)/linkcheck/output.txt."

coverage:
	$(SPHINXBUILD) -b coverage $(ALLSPHINXOPTS) $(BUILDDIR)/coverage
	@echo "Testing of coverage in the sources finished, look at the " \
	      "results in $(BUILDDIR)/coverage/python.txt."


all: clean htmlzip coverage latexpdf

alldirty: htmlzip coverage latexpdf
