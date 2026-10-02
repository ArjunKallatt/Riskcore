"""Rebuild research/csv/*.csv from the agent Markdown tables in research/agents/.

Run: python research/build_csv.py
"""
from __future__ import annotations

import csv
import re
from pathlib import Path

ROOT = Path(__file__).parent
AGENTS = ROOT / "agents"
OUT = ROOT / "csv"
URL_RE = re.compile(r"https?://[^\s)\]>|,;\"'`]+")
MD_LINK_RE = re.compile(r"\[([^\]]+)\]\((https?://[^)]+)\)")


def clean(cell: str) -> str:
    cell = MD_LINK_RE.sub(r"\1 (\2)", cell)
    cell = cell.replace("**", "").replace("`", "").replace("<br>", "; ")
    return re.sub(r"\s+", " ", cell).strip()


def tables(path: Path):
    """Yield (section_heading, header, rows) for every Markdown table in a file."""
    heading, block = "", []
    lines = path.read_text(encoding="utf-8").splitlines() + [""]
    for line in lines:
        if line.startswith("#"):
            heading = line.lstrip("#").strip()
        if line.lstrip().startswith("|"):
            block.append(line.strip())
            continue
        if len(block) >= 3 and set(block[1].replace("|", "").strip()) <= set("-: "):
            split = lambda l: [clean(c) for c in l.strip("|").split("|")]
            header = split(block[0])
            rows = [split(l) for l in block[2:]]
            yield heading, header, [r for r in rows if any(r)]
        block = []


def write(name: str, header: list[str], rows: list[list[str]]) -> None:
    with open(OUT / name, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
    print(f"{name}: {len(rows)} rows")


def pick(header, row, *names, default=""):
    low = [h.lower() for h in header]
    for n in names:
        for i, h in enumerate(low):
            if h.startswith(n.lower()) and i < len(row):
                return row[i]
    return default


def commercial():
    out = []
    for agent, segment in (("agent1.md", "Investment"), ("agent2.md", "Lending/credit")):
        for _, header, rows in tables(AGENTS / agent):
            if "Platform" not in header:
                continue
            region = "Global"
            for r in rows:
                name = r[0]
                if name.lower() in ("india", ""):
                    region = "India"
                    continue
                if segment == "Lending/credit":
                    region = "India" if any(k in name for k in (
                        "ICRA", "CRISIL", "Acies", "ECL Square", "Roopya", "Crediwatch", "Lentra",
                        "CredAble", "Kaleidofin", "Perfios", "Nucleus", "CIBIL", "Equifax India",
                        "CRIF", "TCS", "Mphasis", "Aryaa")) else "Global"
                out.append([
                    name, segment, region, pick(header, r, "Category"),
                    pick(header, r, "Key features"), pick(header, r, "Target users"),
                    pick(header, r, "ECL"), pick(header, r, "Stress"),
                    pick(header, r, "Pricing"), pick(header, r, "Link"),
                    pick(header, r, "Verified"), pick(header, r, "Source date"), agent,
                ])
    write("commercial_landscape.csv",
          ["platform", "segment", "region", "category", "key_features", "target_users",
           "handles_ecl", "stress_testing", "pricing", "link", "verification", "source_date",
           "source_file"], out)


def repos():
    out = []
    for section, header, rows in tables(AGENTS / "agent4.md"):
        if "Repo" not in header:
            continue
        for r in rows:
            out.append([
                r[0], section.split(".", 1)[-1].strip(), pick(header, r, "Category"),
                pick(header, r, "Stars"), pick(header, r, "Last updated"),
                pick(header, r, "License"), pick(header, r, "Language"),
                pick(header, r, "Purpose"), pick(header, r, "Maintenance"),
                pick(header, r, "Reuse"), pick(header, r, "How to reuse"),
                pick(header, r, "Link"), pick(header, r, "Verified"),
            ])
    write("open_source_repos.csv",
          ["repo", "group", "category", "stars_2026_10_02", "last_updated", "license",
           "language", "purpose", "maintenance", "reuse_potential", "how_to_reuse", "link",
           "verification"], out)


MUST_READ = {"50", "51", "6", "3", "8", "7", "73", "58"}


def papers():
    out = []
    for section, header, rows in tables(AGENTS / "agent5.md"):
        if "Title" not in header:
            continue
        topic = re.sub(r"^\d+\.\s*", "", section)
        for r in rows:
            num = r[0]
            out.append([
                num, topic, pick(header, r, "Title"), pick(header, r, "Authors"),
                pick(header, r, "Year"), pick(header, r, "Summary"),
                pick(header, r, "Application"), pick(header, r, "Link"),
                pick(header, r, "Verified"), "yes" if num in MUST_READ else "",
            ])
    write("research_papers.csv",
          ["id", "topic", "title", "authors", "year", "summary", "application_to_riskcore",
           "link", "verification", "top5_must_read"], out)


def data_sources():
    out = []
    for section, header, rows in tables(AGENTS / "agent6.md"):
        if "Source" not in header or "Data type" not in header:
            continue
        group = re.sub(r"^\w+\.\s*", "", section)
        for r in rows:
            out.append([
                pick(header, r, "#"), group, pick(header, r, "Source"),
                pick(header, r, "Data type"), pick(header, r, "Coverage"),
                pick(header, r, "Frequency"), pick(header, r, "Cost"), pick(header, r, "API"),
                pick(header, r, "License"), pick(header, r, "Link"),
                pick(header, r, "Verified"),
            ])
    write("data_sources.csv",
          ["id", "group", "source", "data_type", "coverage", "frequency", "cost", "api",
           "license_terms", "link", "verification"], out)


def regulatory():
    out = []
    for section, header, rows in tables(AGENTS / "agent8.md"):
        if "Requirement" not in header:
            continue
        for r in rows:
            out.append([pick(header, r, "#"), pick(header, r, "Requirement"),
                        pick(header, r, "Source doc"), pick(header, r, "Date"),
                        pick(header, r, "Riskcore feature"), pick(header, r, "v1/v2"),
                        pick(header, r, "Link")])
    write("regulatory_feature_map.csv",
          ["id", "requirement", "source_document", "date_status", "riskcore_feature",
           "version", "link_and_evidence"], out)


def bibliography():
    seen: dict[str, set[str]] = {}
    for path in sorted(AGENTS.glob("agent*.md")):
        for url in URL_RE.findall(path.read_text(encoding="utf-8")):
            url = url.rstrip(".")
            seen.setdefault(url, set()).add(path.stem)
    rows = [[u, re.sub(r"^https?://(www\.)?", "", u).split("/")[0], ";".join(sorted(a))]
            for u, a in sorted(seen.items())]
    write("bibliography.csv", ["url", "domain", "cited_by"], rows)


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    commercial()
    repos()
    papers()
    data_sources()
    regulatory()
    bibliography()
