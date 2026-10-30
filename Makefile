# Less Is a Different Kind of More — build pipeline.
#
#   make setup    install Python dependencies
#   make data     fetch raw sources (cached) and process them into tidy CSVs
#   make figures  data + generated/stats.tex (pgfplots reads the CSVs directly)
#   make pdf      compile scarcity-paper.pdf with LuaLaTeX via latexmk
#   make all      everything above
#   make final    clean build, then fail on placeholders, TODOs or bad citations
#   make clean    remove LaTeX build products (keeps cached downloads)
#   make distclean  also remove cached downloads

PYTHON  ?= python3
LATEXMK ?= latexmk
PDF     := scarcity-paper.pdf

# Reproducible PDFs: fixed timestamps and IDs.
export SOURCE_DATE_EPOCH ?= $(shell git log -1 --format=%ct 2>/dev/null || echo 0)
export FORCE_SOURCE_DATE := 1

FETCH   := $(sort $(wildcard scripts/fetch_*.py))
PROCESS := $(sort $(wildcard scripts/process_*.py))

.PHONY: all setup data fetch process figures stats pdf final clean distclean

all: pdf

setup:
	$(PYTHON) -m pip install pandas wbgapi requests matplotlib

fetch:
	@for s in $(FETCH); do echo "== $$s"; $(PYTHON) $$s || exit 1; done

process: fetch
	@for s in $(PROCESS); do echo "== $$s"; $(PYTHON) $$s || exit 1; done

data: process

stats: data
	$(PYTHON) scripts/export_stats.py

figures: stats

pdf: figures
	cd paper && $(LATEXMK) -r ../.latexmkrc main.tex
	cp paper/build/main.pdf $(PDF)

final:
	cd paper && $(LATEXMK) -r ../.latexmkrc -C main.tex
	$(MAKE) pdf
	$(PYTHON) scripts/check_final.py

clean:
	cd paper && $(LATEXMK) -r ../.latexmkrc -C main.tex
	rm -rf paper/build $(PDF)

distclean: clean
	rm -rf data/raw/*
	touch data/raw/.gitkeep
