EXTRA_DIST = setup.py

clean:
	$(PYTHON) $(top_srcdir)/src/setup.py clean --all

install-exec-local:
	$(PYTHON) $(top_srcdir)/src/setup.py install --prefix $(DESTDIR)/$(prefix) --install-layout=deb

