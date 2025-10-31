.PHONY: test test-unit test-watch

SHELL := /bin/zsh

test:
	./tests/run.zsh

test-unit: test

test-watch:
	./tests/run.zsh --watch
