SRC=graph_inference
MAKEFILE_DOCS=Makefile.docs

docs:
	make -f $(MAKEFILE_DOCS)

test:
	py.test --cov-report term-missing --cov $(SRC)
