# Less Is a Different Kind of More

*Scarcity as a Mode of Innovation*: a working paper, and a companion to *The Widening Edge*.

> The light bulb needed a power grid. The bottle light needed a roof and the sun.

When people lack the resources an existing solution takes for granted, they
sometimes rethink the problem from scratch, and sometimes the result is cheaper,
simpler and more widely useful than the original. This paper argues that
scarcity doesn't produce *more* innovation. It produces a *different kind*.
It also asks when that happens and when scarcity simply means going without.

The paper is built like software. Every number in the prose and every chart
comes from a script, and one command rebuilds the PDF from public data.

## Build

Requirements: Python 3.11+, TeX Live with LuaLaTeX, biber and latexmk
(on Ubuntu: `texlive-luatex texlive-latex-extra texlive-pictures
texlive-bibtex-extra texlive-fonts-extra texlive-science biber latexmk`).

```sh
make setup     # Python dependencies (pandas, wbgapi, requests, matplotlib)
make all       # fetch → process → stats → scarcity-paper.pdf
make final     # clean build that fails on any placeholder, TODO or bad citation
```

Other targets: `make data`, `make figures`, `make pdf`, `make clean`,
`make distclean` (also drops cached downloads and fonts).

The typefaces (Source Serif 4, Source Sans 3; SIL Open Font License) are
fetched from pinned Adobe releases and checked against SHA-256 hashes by
`scripts/fetch_fonts.py`, so local and CI builds set the same type.

## Layout

```
data/raw/         untouched downloads (git-ignored; fetch scripts recreate them)
data/manual/      figures hand-copied from reports: value, unit, year, source_key, page
data/processed/   tidy CSVs read directly by pgfplots
data/SOURCES.md   every dataset: URL, access date, licence, notes
scripts/          fetch_*.py, process_*.py, export_stats.py, check_final.py
generated/        stats.tex: one \newcommand per number used in the prose
paper/            main.tex, preamble/, sections/, figures/, references.bib
```

## Rules the repository follows

- **No number is typed into the prose.** Text says `\sspElecAccess{}`, and
  `scripts/export_stats.py` defines it from processed data with consistent rounding.
- **Charts read the CSVs.** Figures are pgfplots and TikZ, so they share the
  document's fonts and palette.
- **Nothing is invented.** Anything not yet verified appears as a visible
  `\placeholder{...}` and is listed in `TODO.md`.
- **Counterpoints are part of the argument.** Every section of the case for
  carries at least one Counterpoint box.

## CI

`.github/workflows/build.yml` builds the PDF on every push and uploads it as
an artifact. On a `v*` tag it also runs `make final` and attaches the PDF to
the release.
