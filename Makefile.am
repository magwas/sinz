SUBDIRS = src
distclean-local:
	rm -rf INSTALL `find -name Makefile.in` aclocal.m4 autom4te.cache/ configure install-sh missing src/build

check:
	PYTHONPATH=src python -m unittest discover -p '*.py' -s tests
