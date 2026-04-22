#!/usr/bin/env python3

import argparse
import os
import re
import sys
from calendar import month_abbr, month_name
from pathlib import Path


CATEGORY_BY_TYPE = {
    "article": "manuscripts",
    "inproceedings": "conferences",
    "conference": "conferences",
    "proceedings": "conferences",
    "incollection": "books",
    "book": "books",
    "inbook": "books",
}


HTML_ESCAPE_TABLE = {
    "&": "&amp;",
    '"': "&quot;",
    "'": "&apos;",
}


def html_escape(text: str) -> str:
    return "".join(HTML_ESCAPE_TABLE.get(char, char) for char in text)


def clean_text(text: str) -> str:
    return text.replace("{", "").replace("}", "").replace("\\", "").strip()


def slugify(text: str) -> str:
    slug = clean_text(text).lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug[:90]


def parse_month(raw_month: str | None) -> str:
    if not raw_month:
        return "01"
    value = clean_text(raw_month).strip().lower()
    if value.isdigit():
        return f"{int(value):02d}"
    short_lookup = {name.lower(): index for index, name in enumerate(month_abbr) if name}
    full_lookup = {name.lower(): index for index, name in enumerate(month_name) if name}
    if value[:3] in short_lookup:
        return f"{short_lookup[value[:3]]:02d}"
    if value in full_lookup:
        return f"{full_lookup[value]:02d}"
    return "01"


def parse_day(raw_day: str | None) -> str:
    if not raw_day:
        return "01"
    digits = re.sub(r"\D", "", raw_day)
    if not digits:
        return "01"
    return f"{int(digits):02d}"


def split_top_level(text: str, delimiter: str) -> list[str]:
    parts = []
    current = []
    brace_depth = 0
    quote_open = False
    index = 0
    delimiter_len = len(delimiter)

    while index < len(text):
        chunk = text[index : index + delimiter_len]
        char = text[index]
        if char == '"' and (index == 0 or text[index - 1] != "\\"):
            quote_open = not quote_open
        elif char == "{" and not quote_open:
            brace_depth += 1
        elif char == "}" and not quote_open and brace_depth > 0:
            brace_depth -= 1

        if brace_depth == 0 and not quote_open and chunk == delimiter:
            parts.append("".join(current).strip())
            current = []
            index += delimiter_len
            continue

        current.append(char)
        index += 1

    if current:
        parts.append("".join(current).strip())
    return parts


def unquote_bib_value(value: str) -> str:
    value = value.strip().rstrip(",")
    if value.startswith("{") and value.endswith("}"):
        value = value[1:-1]
    elif value.startswith('"') and value.endswith('"'):
        value = value[1:-1]
    return clean_text(value)


def parse_bibtex_entries(text: str) -> list[dict]:
    entries = []
    index = 0
    while True:
        start = text.find("@", index)
        if start == -1:
            break
        type_end = text.find("{", start)
        if type_end == -1:
            break
        entry_type = text[start + 1 : type_end].strip().lower()
        depth = 1
        pos = type_end + 1
        while pos < len(text) and depth > 0:
            if text[pos] == "{":
                depth += 1
            elif text[pos] == "}":
                depth -= 1
            pos += 1
        body = text[type_end + 1 : pos - 1].strip()
        index = pos
        if "," not in body:
            continue
        bib_id, raw_fields = body.split(",", 1)
        fields = {}
        for field in split_top_level(raw_fields, ","):
            if "=" not in field:
                continue
            key, value = field.split("=", 1)
            fields[key.strip().lower()] = unquote_bib_value(value)
        entries.append({"id": bib_id.strip(), "type": entry_type, "fields": fields})
    return entries


def format_authors(entry: dict) -> str:
    authors = []
    raw_authors = entry["fields"].get("author", "")
    for author in split_top_level(raw_authors, " and "):
        authors.append(author.strip())
    return "; ".join(authors)


def select_venue(fields: dict[str, str]) -> str:
    for key in ["journal", "booktitle", "publisher", "school"]:
        if key in fields and fields[key].strip():
            return clean_text(fields[key])
    return "Unknown venue"


def build_excerpt(fields: dict[str, str], title: str) -> str:
    for key in ["abstract", "note"]:
        if key in fields and fields[key].strip():
            return clean_text(fields[key])[:220]
    return f"{title}."


def build_url(fields: dict[str, str]) -> str:
    if fields.get("url"):
        return fields["url"].strip()
    if fields.get("doi"):
        return f"https://doi.org/{clean_text(fields['doi'])}"
    return ""


def build_citation(authors: str, title: str, venue: str, year: str) -> str:
    return f"{authors} ({year}). \"{title}.\" <i>{venue}</i>."


def markdown_body(fields: dict[str, str], authors: str, venue: str, year: str, doi: str, url: str) -> str:
    lines = []
    if fields.get("abstract"):
        lines.append(clean_text(fields["abstract"]))
        lines.append("")
    elif fields.get("note"):
        lines.append(clean_text(fields["note"]))
        lines.append("")
    lines.append(f"Authors: {authors}")
    lines.append("")
    lines.append(f"Venue: {venue} ({year})")
    if doi:
        lines.append(f"DOI: {doi}")
    if url:
        lines.append("")
        lines.append(f"[Access paper here]({url}){{:target=\"_blank\"}}")
    return "\n".join(lines)


def create_markdown(entry: dict, default_category: str) -> tuple[str, str]:
    fields = entry["fields"]
    title = clean_text(fields["title"])
    year = clean_text(fields.get("year", "1900"))
    month = parse_month(fields.get("month"))
    day = parse_day(fields.get("day"))
    date = f"{year}-{month}-{day}"
    category = CATEGORY_BY_TYPE.get(entry["type"].lower(), default_category)
    venue = select_venue(fields)
    authors = format_authors(entry)
    doi = clean_text(fields.get("doi", ""))
    url = build_url(fields)
    slug = slugify(title)
    citation = build_citation(authors, title, venue, year)
    excerpt = build_excerpt(fields, title)
    body = markdown_body(fields, authors, venue, year, doi, url)

    md_filename = f"{date}-{slug}.md"
    md = [
        "---",
        f'title: "{html_escape(title)}"',
        "collection: publications",
        f"category: {category}",
        f"permalink: /publication/{slug}",
        f"excerpt: '{html_escape(excerpt)}'",
        f"date: {date}",
        f"venue: '{html_escape(venue)}'",
    ]
    if url:
        md.append(f"paperurl: '{url}'")
    md.append(f"citation: '{html_escape(citation)}'")
    md.append("---")
    md.append("")
    md.append(body)
    md.append("")
    return md_filename, "\n".join(md)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate _publications markdown files from a BibTeX file."
    )
    parser.add_argument("bibfile", help="Path to the input .bib file")
    parser.add_argument(
        "--out-dir",
        default="../_publications",
        help="Output directory for markdown files, default: ../_publications",
    )
    parser.add_argument(
        "--default-category",
        default="manuscripts",
        choices=["books", "manuscripts", "conferences"],
        help="Fallback category when the BibTeX entry type is unknown",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing markdown files with the same name",
    )
    parser.add_argument(
        "--replace-all",
        action="store_true",
        help="Delete existing markdown files in the output directory before regenerating everything",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    bib_path = Path(args.bibfile)
    if not bib_path.exists():
        print(f"BibTeX file not found: {bib_path}", file=sys.stderr)
        return 1

    out_dir = (Path(__file__).resolve().parent / args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    if args.replace_all:
        removed = 0
        for file_path in out_dir.glob("*.md"):
            file_path.unlink()
            removed += 1
        print(f"Removed {removed} existing markdown files from {out_dir}")

    bibdata = parse_bibtex_entries(bib_path.read_text(encoding="utf-8"))

    created = 0
    skipped = 0
    for entry in bibdata:
        bib_id = entry["id"]
        if "title" not in entry["fields"]:
            print(f"Skipping {bib_id}: missing title", file=sys.stderr)
            skipped += 1
            continue

        filename, content = create_markdown(entry, args.default_category)
        destination = out_dir / os.path.basename(filename)
        if destination.exists() and not args.overwrite:
            print(f"Skipping existing file: {destination.name}")
            skipped += 1
            continue

        destination.write_text(content, encoding="utf-8")
        print(f"Wrote {destination.name}")
        created += 1

    print(f"Done. Created {created} files, skipped {skipped}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
