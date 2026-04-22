# Markdown Generator

This directory contains helper scripts for creating publication and talk markdown files for the site.

## Python Scripts

The `.py` files are command-line scripts that generate markdown entries in the collections used by the site.

### CSV or TSV to publications

Run:

```bash
python3 publications.py publications.csv
```

The input file must contain the expected headers documented in `publications.py`.

### BibTeX to publications

Run:

```bash
python3 pubsFromBib.py publications.bib
```

Useful options:

```bash
python3 pubsFromBib.py path/to/publications.bib --out-dir ../_publications --overwrite
python3 pubsFromBib.py path/to/publications.bib --default-category manuscripts
python3 pubsFromBib.py publications.bib --replace-all
```

The script uses BibTeX entry types to infer categories:

- `article` -> `manuscripts`
- `inproceedings` and `conference` -> `conferences`
- `incollection`, `book`, and `inbook` -> `books`

It reads standard BibTeX fields such as `title`, `author`, `year`, `month`, `day`, `journal`, `booktitle`, `publisher`, `url`, `doi`, `abstract`, and `note`, then creates markdown files in `_publications`.

If you want to fully rebuild the publications collection from the BibTeX source of truth, use:

```bash
python3 pubsFromBib.py publications.bib --replace-all
```

## Jupyter Notebooks

The notebooks are older interactive alternatives for generating markdown from structured publication or talk data.
