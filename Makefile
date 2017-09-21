PREFIX ?= /usr/local
ALTPREFIX ?= $(HOME)/.local
DESTDIR ?=
BINDIR ?= /bin
MANDIR ?= /share/man

all:
	@echo "Passphrase by HacKan (https://hackan.net)"
	@echo "Commands for this makefile:"
	@echo "	install altinstall uninstall altuninstall lint"

install:
	@install -v -d "$(DESTDIR)$(PREFIX)$(MANDIR)/man1" && install -m 0644 -v man/passphrase.1 "$(DESTDIR)$(PREFIX)$(MANDIR)/man1/passphrase.1"
	@install -v -d "$(DESTDIR)$(PREFIX)$(BINDIR)/"
	install -v -d "$(DESTDIR)$(PREFIX)$(BINDIR)/" && install -m 0755 -v src/passphrase.py "$(DESTDIR)$(PREFIX)$(BINDIR)/passphrase"

uninstall:
	@rm -vrf \
		"$(DESTDIR)$(PREFIX)$(BINDIR)/passphrase" \
		"$(DESTDIR)$(PREFIX)$(MANDIR)/man1/passphrase.1"

altinstall:
	@install -v -d "$(DESTDIR)$(ALTPREFIX)$(MANDIR)/man1" && install -m 0644 -v man/passphrase.1 "$(DESTDIR)$(ALTPREFIX)$(MANDIR)/man1/passphrase.1"
	@install -v -d "$(DESTDIR)$(ALTPREFIX)$(BINDIR)/"
	install -v -d "$(DESTDIR)$(ALTPREFIX)$(BINDIR)/" && install -m 0755 -v src/passphrase.py "$(DESTDIR)$(ALTPREFIX)$(BINDIR)/passphrase"

altuninstall:
	@rm -vrf \
		"$(DESTDIR)$(ALTPREFIX)$(BINDIR)/passphrase" \
		"$(DESTDIR)$(ALTPREFIX)$(MANDIR)/man1/passphrase.1"

lint:
	flake8 ./src

.PHONY: install altinstall uninstall altuninstall lint
