SHELL=/bin/bash

PREFIX ?= /usr/local
ALTPREFIX ?= $(HOME)/.local
DESTDIR ?=
BINDIR ?= /bin
MANDIR ?= /share/man

all:
	@echo "Passphrase by HacKan (https://hackan.net)"
	@echo "Commands for this makefile:"
	@echo -e "\tinstall\n\taltinstall\n\tuninstall\n\taltuninstall\n\tpackage-install\n\tpackage-uninstall\n\tdevenvironment\n\tlint\n\ttest\n\tcoverage\n\ttimeit\n\tclean"

clean:
	@rm -vrf \
		build/ \
		dist/ \
		hc_passphrase.egg-info/ \
		passphrase/__pycache__/ \
		passphrase/tests/__pycache__/ \
		cover/ \
		.coverage \
		passphrase/hc_passphrase.egg-info/
	@find . -type f -name "*.pyc" -delete

package-install:
	python3 setup.py install

package-uninstall:
	pip uninstall hc-passphrase

install-common:
	$(eval TMPDIR := $(shell mktemp -d --tmpdir "passphrase.XXXXXXXXXX"))
	mkdir $(TMPDIR)/src/
	cp -f passphrase/*.py $(TMPDIR)/src/
	@sed -i "s/from .passphrase/from passphrase/g; s/from .settings/from settings/g; s/from .secrets/from secrets/g; s/from .aux/from aux/g" "$(TMPDIR)/src/__main__.py"
	@sed -i "s/from .secrets/from secrets/g; s/from .calc/from calc/g; s/from .settings/from settings/g; s/from .aux/from aux/g; s/from .wordlist/from wordlist/g" "$(TMPDIR)/src/passphrase.py"
	@sed -i "s/from .secrets/from secrets/g" "$(TMPDIR)/src/aux.py"
	@sed -i "s/from .random/from random/g" "$(TMPDIR)/src/secrets.py"
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
	@if [[ "$$PATH" != *"$${HOME}/.local/bin"* ]]; then \
		echo 'if [ -d "$$HOME/.local/bin" ]; then' >> "$(HOME)/.profile"; \
		echo '    PATH="$$HOME/.local/bin:$$PATH"' >> "$(HOME)/.profile"; \
		echo 'fi' >> "$(HOME)/.profile"; \
		echo >> "$(HOME)/.profile"; \
		echo "Local bin directory added to PATH. Source your .profile: source $(HOME)/.profile"; \
	fi; \

altuninstall:
	@rm -vrf \
		"$(DESTDIR)$(ALTPREFIX)$(BINDIR)/passphrase" \
		"$(DESTDIR)$(ALTPREFIX)$(MANDIR)/man1/passphrase.1"

lint:
	flake8 --exclude=venv/ .
	pydocstyle -e --match-dir=passphrase .

test:
	nosetests -v

coverage:
	nosetests --with-coverage --cover-erase --cover-package=passphrase --cover-html

timeit:
	python3 -m timeit -n 100 -r 10 -s 'import os' 'os.system("python3 -m passphrase -w6 -m")'

devenvironment:
	@echo "Creating virtualenv"
	@[ -d venv ] || virtualenv -p python3 venv
	@echo "Installing dev dependencies"
	venv/bin/pip install -r requirements-dev.txt
	@echo "Installing passphrase"
	@venv/bin/python3 setup.py --fullname
	@venv/bin/python3 setup.py --description
	@venv/bin/python3 setup.py --url
	venv/bin/python3 setup.py install
	@echo -e '\nAll done. You might want to activate the virtualenv (I can not do it for you): `source venv/bin/activate`'

.PHONY: install altinstall uninstall altuninstall lint test coverage timeit clean devenvironment
