"""Generate a skeleton bibliography note from a cite-key (and optional DOI).

Emits `Bibliography/Primary/<cite_key>.md` or `Bibliography/Secondary/<cite_key>.md`
with the full YAML schema documented in `Bibliography/README.md`. Optional `--from-doi`
auto-fills title / authors / year / journal / volume / issue / pages via the Crossref
REST API (https://api.crossref.org/works/<doi>) — no API key required.

Usage:
    uv run python Literature/Bibliography/scaffold_bib_note.py \\
        --cite-key dirac1928_quantum_electron --type primary

    uv run python Literature/Bibliography/scaffold_bib_note.py \\
        --cite-key dirac1928_quantum_electron --type primary \\
        --from-doi 10.1098/rspa.1928.0023

    uv run python Literature/Bibliography/scaffold_bib_note.py \\
        --cite-key foo2024_bar --type secondary --dry-run
"""

import argparse
import json
import sys
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen

import yaml

BIB_DIR = Path(__file__).resolve().parent
CROSSREF_URL = "https://api.crossref.org/works/{doi}"
USER_AGENT = "phd-life-bibliography-scaffold/0.1 (mailto:morris.trey.j@gmail.com)"


def fetch_crossref(doi: str) -> dict:
    """Hit Crossref for a DOI and return its `message` dict."""
    url = CROSSREF_URL.format(doi=quote(doi, safe="/.()-"))
    req = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(req, timeout=15) as resp:
        payload = json.loads(resp.read().decode("utf-8"))
    return payload.get("message", {})


def metadata_from_crossref(msg: dict) -> dict:
    """Translate a Crossref `message` into the bibliography YAML schema."""
    out: dict = {}

    title = msg.get("title")
    if isinstance(title, list) and title:
        out["title"] = title[0]

    authors = []
    for a in msg.get("author", []):
        given = a.get("given", "").strip()
        family = a.get("family", "").strip()
        if given and family:
            authors.append(f"{given} {family}")
        elif family:
            authors.append(family)
        elif a.get("name"):
            authors.append(a["name"])
    if authors:
        out["authors"] = authors

    year_parts = (
        msg.get("issued", {}).get("date-parts")
        or msg.get("published-print", {}).get("date-parts")
        or msg.get("published-online", {}).get("date-parts")
    )
    if year_parts and year_parts[0]:
        out["year"] = year_parts[0][0]

    journal = msg.get("container-title")
    if isinstance(journal, list) and journal:
        out["journal"] = journal[0]

    for k_in, k_out in (("volume", "volume"), ("issue", "issue"), ("page", "pages")):
        if msg.get(k_in):
            out[k_out] = msg[k_in]

    if msg.get("DOI"):
        out["doi"] = msg["DOI"]
    if msg.get("URL"):
        out["url"] = msg["URL"]

    # Map Crossref type → our `kind`.
    cr_type = msg.get("type", "")
    out["kind"] = {
        "journal-article": "article",
        "book": "book",
        "book-chapter": "book",
        "proceedings-article": "inproceedings",
        "dissertation": "thesis",
        "posted-content": "preprint",
        "dataset": "dataset",
    }.get(cr_type, "article")

    return out


def default_frontmatter(cite_key: str, type_: str) -> dict:
    """The full schema with empty defaults, in a stable field order."""
    return {
        "cite_key": cite_key,
        "title": "",
        "authors": [],
        "year": None,
        "type": type_,
        "kind": "article",
        "tags": [],
        "journal": "",
        "volume": "",
        "issue": "",
        "pages": "",
        "doi": "",
        "url": "",
        "arxiv_id": "",
        "pdf_status": "pending",
        "pdf_path": "",
        "reading_note": "",
        "human_reviewed": False,
    }


# Render fields in this order regardless of dict insertion quirks.
FIELD_ORDER = list(default_frontmatter("x", "primary").keys())


def render_note(fm: dict) -> str:
    ordered = {k: fm.get(k) for k in FIELD_ORDER}
    yaml_block = yaml.safe_dump(
        ordered, sort_keys=False, allow_unicode=True, default_flow_style=False
    )
    body = (
        "\n<!-- Summary written after reading the source. What it claims, what's "
        "load-bearing\n     for my work, how it connects to [[other_cite_key]] notes. -->\n"
    )
    return f"---\n{yaml_block}---\n{body}"


def main() -> int:
    p = argparse.ArgumentParser(description="Scaffold a bibliography cite-card.")
    p.add_argument("--cite-key", required=True, help="firstauthorYYYY_slug")
    p.add_argument("--type", choices=["primary", "secondary"], required=True)
    p.add_argument("--from-doi", help="Crossref DOI to auto-fill metadata")
    p.add_argument("--dry-run", action="store_true", help="print instead of writing")
    p.add_argument("--force", action="store_true", help="overwrite if it exists")
    args = p.parse_args()

    fm = default_frontmatter(args.cite_key, args.type)

    if args.from_doi:
        try:
            fm.update(metadata_from_crossref(fetch_crossref(args.from_doi)))
        except Exception as e:  # network/JSON errors shouldn't abort the scaffold
            print(f"warning: Crossref lookup failed ({e}); writing empty stub", file=sys.stderr)
            fm["doi"] = args.from_doi

    text = render_note(fm)

    subdir = "Primary" if args.type == "primary" else "Secondary"
    out_path = BIB_DIR / subdir / f"{args.cite_key}.md"

    if args.dry_run:
        print(f"# would write: {out_path}\n")
        print(text)
        return 0

    if out_path.exists() and not args.force:
        print(f"error: {out_path} exists (use --force to overwrite)", file=sys.stderr)
        return 1

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(text, encoding="utf-8")
    print(f"wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
