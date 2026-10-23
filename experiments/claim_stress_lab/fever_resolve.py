"""Resolve selected FEVER evidence sentence IDs against the official wiki-pages.zip.

This is evidence extraction only, NOT independent quote-defect labeling.
Streams each JSONL member and stores only requested pages. No dependencies.
"""
import argparse
import json
import zipfile
from pathlib import Path


def wanted_references(claims_path, limit=30):
    wanted = {}
    with Path(claims_path).open(encoding="utf-8") as stream:
        for line in stream:
            if not line.strip():
                continue
            record = json.loads(line)
            for group in record.get("evidence", []):
                for entry in group:
                    if isinstance(entry, list) and len(entry) >= 4 and isinstance(entry[2], str) and type(entry[3]) is int:
                        wanted.setdefault(entry[2], set()).add(entry[3])
            limit -= 1
            if limit == 0:
                break
    return wanted


def resolve(claims_path, wiki_zip, limit=30):
    wanted = wanted_references(claims_path, limit)
    found = {}
    with zipfile.ZipFile(wiki_zip) as archive:
        for name in archive.namelist():
            if not name.endswith(".jsonl"):
                continue
            with archive.open(name) as stream:
                for raw in stream:
                    page = json.loads(raw)
                    title = page.get("id")
                    if title not in wanted:
                        continue
                    sentences = {}
                    for row in page.get("lines", "").splitlines():
                        number, sep, text = row.partition("\t")
                        if sep and number.isdecimal() and int(number) in wanted[title]:
                            sentences[int(number)] = text.split("\t")[0]
                    found[title] = sentences
            if len(found) == len(wanted):
                break
    refs = []
    for title in sorted(wanted):
        for sentence_id in sorted(wanted[title]):
            text = found.get(title, {}).get(sentence_id)
            refs.append({"page": title, "sentence_id": sentence_id, "source_text": text,
                         "resolved": text is not None})
    return {"requested_references": len(refs),
            "resolved_references": sum(r["resolved"] for r in refs),
            "quote_defect_labels_available": False,
            "ready_for_independent_evaluation": False,
            "references": refs}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--claims", type=Path, required=True)
    parser.add_argument("--wiki-zip", type=Path, required=True)
    parser.add_argument("--limit", type=int, default=30)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.limit < 1:
        parser.error("--limit must be positive")
    result = resolve(args.claims, args.wiki_zip, args.limit)
    output = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.write_text(output, encoding="utf-8")
    else:
        print(output)


if __name__ == "__main__":
    main()
