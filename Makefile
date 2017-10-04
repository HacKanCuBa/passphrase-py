SHELL=/bin/bash

PREFIX ?= /usr/local
ALTPREFIX ?= $(HOME)/.local
DESTDIR ?=
BINDIR ?= /bin
MANDIR ?= /share/man
TMPDIR := $(shell mktemp -d --tmpdir "passphrase.XXXXXXXXXX")

all:
	@echo "Passphrase by HacKan (https://hackan.net)"
	@echo "Commands for this makefile:"
	@echo "	install altinstall uninstall altuninstall package-install lint clean"

clean:
	@rm -vrf \
		build/ \
		dist/ \
		passphrase.egg-info/ \
		passphrase/__pycache__/ \
		passphrase/passphrase.egg-info/

package-install:
	python3 setup.py install

install-common:
	mkdir $(TMPDIR)/src/
	cp -f passphrase/*.py $(TMPDIR)/src/
	cp -f passphrase/*.json $(TMPDIR)/src/
	@sed -i 's/from .passphrase import Passphrase/from passphrase import Passphrase/g' "$(TMPDIR)/src/__main__.py"
	@sed -i "s/from .secrets import randbelow/from secrets import randbelow/; s/from .calc import entropy_bits as calc_entropy_bits/from calc import entropy_bits as calc_entropy_bits/; s/from .calc import entropy_bits_nrange as calc_entropy_bits_nrange/from calc import entropy_bits_nrange as calc_entropy_bits_nrange/; s/from .calc import password_len_needed as calc_password_len_needed/from calc import password_len_needed as calc_password_len_needed/; s/from .calc import words_amount_needed as calc_words_amount_needed/from calc import words_amount_needed as calc_words_amount_needed/;" "$(TMPDIR)/src/passphrase.py"
	@if command -v zip 2> /dev/null; then \
		zip -j -r $(TMPDIR)/passphrase.zip $(TMPDIR)/src/*; \
	elif python3 -c 'from sys import version_info; assert (version_info >= (3, 5)), "Python 3.5+ required"' 2> /dev/null; then \
		python3 -m zipapp "$(TMPDIR)/src" && \
			mv "$(TMPDIR)/src.pyz" "$(TMPDIR)/passphrase.zip"; \
	else \
		echo "No zip command found and Python seems < 3.5, bailing out..." && \
			exit 1; \
	fi; \
	echo '#!/usr/bin/env python3' | cat - "$(TMPDIR)/passphrase.zip" > "$(TMPDIR)/passphrase"
	@chmod +x "$(TMPDIR)/passphrase"

install: install-common
	@install -v -d "$(DESTDIR)$(PREFIX)$(MANDIR)/man1" && install -m 0644 -v man/passphrase.1 "$(DESTDIR)$(PREFIX)$(MANDIR)/man1/passphrase.1"
	@install -v -d "$(DESTDIR)$(PREFIX)$(BINDIR)/"
	install -v -d "$(DESTDIR)$(PREFIX)$(BINDIR)/" && install -m 0755 -v "$(TMPDIR)/passphrase" "$(DESTDIR)$(PREFIX)$(BINDIR)/passphrase"

uninstall:
	@rm -vrf \
		"$(DESTDIR)$(PREFIX)$(BINDIR)/passphrase" \
		"$(DESTDIR)$(PREFIX)$(MANDIR)/man1/passphrase.1"

altinstall: install-common
	@install -v -d "$(DESTDIR)$(ALTPREFIX)$(MANDIR)/man1" && install -m 0644 -v man/passphrase.1 "$(DESTDIR)$(ALTPREFIX)$(MANDIR)/man1/passphrase.1"
	@install -v -d "$(DESTDIR)$(ALTPREFIX)$(BINDIR)/"
	install -v -d "$(DESTDIR)$(ALTPREFIX)$(BINDIR)/" && install -m 0755 -v "$(TMPDIR)/passphrase" "$(DESTDIR)$(ALTPREFIX)$(BINDIR)/passphrase"

altuninstall:
	@rm -vrf \
		"$(DESTDIR)$(ALTPREFIX)$(BINDIR)/passphrase" \
		"$(DESTDIR)$(ALTPREFIX)$(MANDIR)/man1/passphrase.1"

lint:
	flake8 .

.PHONY: install altinstall uninstall altuninstall lint clean
