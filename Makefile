all:
	@echo "Passphrase by HacKan (https://hackan.net)"
	@echo "Commands for this makefile:"
	@echo "	lint"

lint:
	flake8 ./src

.PHONY: lint
