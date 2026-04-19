"""
Build the combined dataset from all sources (gov/ + osm/).

Reads all CSVs from gov/ and osm/, merges them into:
- combined/services.csv
- combined/services.json
- combined/services.db (SQLite with indexes)
- combined/SOURCES.md

This script runs inside the data repo itself.
"""

import csv
import json
import os
import sqlite3
import glob
from collections import defaultdict
from datetime import date

REPO_ROOT = os.path.join(os.path.dirname(__file__), "..")
COMBINED_DIR = os.path.join(REPO_ROOT, "combined")

SCHEMA_FIELDS = [
    "id", "name", "description", "category", "address", "suburb", "state",
    "postcode", "latitude", "longitude", "phone", "email", "website",
    "hours", "eligibility", "cost", "source_id", "source_name",
    "source_organisation", "source_jurisdiction", "source_license",
    "source_url", "source_date", "quality", "duplicate_of",
]


import re

_DUP_STOPWORDS = {
    "the", "inc", "incorporated", "ltd", "limited", "pty", "co", "and",
    "australia", "australian",
}


def _norm_name(name):
    s = (name or "").lower()
    s = re.sub(r"[^a-z0-9 ]", " ", s)
    tokens = [t for t in s.split() if t and t not in _DUP_STOPWORDS]
    return " ".join(tokens)


def _completeness_score(record):
    """Higher = more complete. Used to pick a primary among duplicates."""
    score = 0
    for field in ("address", "phone", "email", "website", "latitude", "description", "hours"):
        if record.get(field, "").strip():
            score += 1
    if record.get("quality") == "complete":
        score += 2
    elif record.get("quality") == "partial":
        score += 1
    return score


def mark_duplicates(records):
    """
    Detect cross-source duplicates using (normalised_name, postcode) and
    (normalised_name, lat/lng rounded to ~100m) as keys.

    Writes record["duplicate_of"] = primary_id for non-primary copies.
    Does not remove rows — preserves provenance.
    """
    by_pc = {}
    by_geo = {}
    # First pass: bucket records
    for r in records:
        name_norm = _norm_name(r.get("name", ""))
        if not name_norm:
            continue
        pc = r.get("postcode", "").strip()
        if pc:
            by_pc.setdefault((name_norm, pc), []).append(r)
        try:
            lat = round(float(r["latitude"]), 3)
            lng = round(float(r["longitude"]), 3)
            by_geo.setdefault((name_norm, lat, lng), []).append(r)
        except (ValueError, KeyError, TypeError):
            pass

    def resolve(group):
        # Only mark duplicates when more than one source is involved
        sources = {r["source_id"] for r in group}
        if len(sources) < 2:
            return
        primary = max(group, key=_completeness_score)
        for r in group:
            if r["id"] != primary["id"] and not r.get("duplicate_of"):
                r["duplicate_of"] = primary["id"]

    for group in by_pc.values():
        if len(group) > 1:
            resolve(group)
    for group in by_geo.values():
        if len(group) > 1:
            resolve(group)

    marked = sum(1 for r in records if r.get("duplicate_of"))
    print(f"  Marked {marked} duplicate records (kept in dataset with duplicate_of pointer)")


def read_all_csvs():
    """Read all CSVs from gov/ and osm/ directories."""
    all_records = []

    # Gov sources
    gov_csvs = glob.glob(os.path.join(REPO_ROOT, "gov", "**", "*.csv"), recursive=True)
    for path in sorted(gov_csvs):
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                all_records.append(row)
        basename = os.path.basename(path)
        print(f"  gov: {basename} ({sum(1 for _ in open(path)) - 1} records)")

    # OSM sources
    osm_csvs = glob.glob(os.path.join(REPO_ROOT, "osm", "*.csv"))
    for path in sorted(osm_csvs):
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # OSM CSVs have different column names — map them
                mapped = map_osm_record(row)
                all_records.append(mapped)
        basename = os.path.basename(path)
        print(f"  osm: {basename} ({sum(1 for _ in open(path)) - 1} records)")

    return all_records


OSM_SOCIAL_FACILITY_CATEGORIES = {
    "food_bank": "food",
    "soup_kitchen": "food",
    "shelter": "housing",
    "clothing_bank": "personal_care",
    "counselling": "mental_health",
    "outreach": "community",
    "group_home": "housing",
    "nursing_home": "health",
    "workshop": "employment",
}


def map_osm_record(row):
    """Map an OSM CSV record to our standard schema."""
    amenity = row.get("amenity", "")
    office = row.get("office", "")
    sf_type = row.get("social_facility", "")

    # Category
    if sf_type in OSM_SOCIAL_FACILITY_CATEGORIES:
        category = OSM_SOCIAL_FACILITY_CATEGORIES[sf_type]
    elif amenity == "community_centre":
        category = "community"
    elif office in ("ngo", "charity"):
        category = "community"
    else:
        category = "community"

    # Description
    parts = []
    if sf_type:
        parts.append(sf_type.replace("_", " ").title())
    elif amenity:
        parts.append(amenity.replace("_", " ").title())
    elif office:
        parts.append(office.upper())
    sf_for = row.get("social_facility_for", "")
    if sf_for:
        parts.append(f"for {sf_for}")
    description = " ".join(parts)

    name = row.get("name", "")
    if not name:
        return {"name": ""}  # Will be skipped

    # Quality
    has_location = bool(row.get("addr_street", "").strip() or row.get("lat", "").strip())
    has_contact = bool(row.get("phone", "").strip() or row.get("website", "").strip() or row.get("email", "").strip())
    if has_location and has_contact:
        quality = "complete"
    elif has_location or has_contact:
        quality = "partial"
    else:
        quality = "minimal"

    return {
        "id": "",  # Will be assigned during merge
        "name": name,
        "description": description,
        "category": category,
        "address": row.get("addr_street", ""),
        "suburb": row.get("addr_suburb", ""),
        "state": row.get("state", ""),
        "postcode": row.get("addr_postcode", ""),
        "latitude": row.get("lat", ""),
        "longitude": row.get("lon", ""),
        "phone": row.get("phone", ""),
        "email": row.get("email", ""),
        "website": row.get("website", ""),
        "hours": row.get("opening_hours", ""),
        "eligibility": "",
        "cost": "",
        "source_id": "osm_social_facilities",
        "source_name": "OpenStreetMap Social Facilities",
        "source_organisation": "OpenStreetMap contributors",
        "source_jurisdiction": "national",
        "source_license": "ODbL",
        "source_url": "https://www.openstreetmap.org",
        "source_date": date.today().isoformat(),
        "quality": quality,
    }


def write_csv(records, path):
    """Write records to CSV."""
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=SCHEMA_FIELDS)
        writer.writeheader()
        for record in records:
            row = {field: record.get(field, "") for field in SCHEMA_FIELDS}
            writer.writerow(row)
    print(f"  Written: {path} ({len(records)} records)")


def write_json(records, path):
    """Write records to JSON."""
    output = [{field: record.get(field, "") for field in SCHEMA_FIELDS} for record in records]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"  Written: {path} ({len(records)} records)")


def write_sqlite(records, path):
    """Write records to SQLite database."""
    if os.path.exists(path):
        os.remove(path)

    conn = sqlite3.connect(path)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE services (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            category TEXT,
            address TEXT,
            suburb TEXT,
            state TEXT,
            postcode TEXT,
            latitude REAL,
            longitude REAL,
            phone TEXT,
            email TEXT,
            website TEXT,
            hours TEXT,
            eligibility TEXT,
            cost TEXT,
            source_id TEXT,
            source_name TEXT,
            source_organisation TEXT,
            source_jurisdiction TEXT,
            source_license TEXT,
            source_url TEXT,
            source_date TEXT,
            quality TEXT,
            duplicate_of TEXT
        )
    """)

    cursor.execute("CREATE INDEX idx_state ON services(state)")
    cursor.execute("CREATE INDEX idx_category ON services(category)")
    cursor.execute("CREATE INDEX idx_quality ON services(quality)")
    cursor.execute("CREATE INDEX idx_suburb ON services(suburb)")
    cursor.execute("CREATE INDEX idx_postcode ON services(postcode)")

    for record in records:
        row = {field: record.get(field, "") for field in SCHEMA_FIELDS}
        for field in ("latitude", "longitude"):
            try:
                row[field] = float(row[field]) if row[field] else None
            except ValueError:
                row[field] = None

        cursor.execute(
            f"INSERT OR IGNORE INTO services ({', '.join(SCHEMA_FIELDS)}) VALUES ({', '.join('?' * len(SCHEMA_FIELDS))})",
            [row[f] for f in SCHEMA_FIELDS],
        )

    conn.commit()
    conn.close()
    print(f"  Written: {path} ({len(records)} records)")


def write_sources(path):
    """Build SOURCES.md from all SOURCES.md files in gov/ and osm/."""
    lines = [
        "# Data Sources and Attribution",
        "",
        "This dataset is built from Australian government open data and OpenStreetMap.",
        "",
    ]

    # Collect all SOURCES.md content
    for sources_file in sorted(glob.glob(os.path.join(REPO_ROOT, "gov", "**", "SOURCES.md"), recursive=True)):
        with open(sources_file) as f:
            content = f.read().strip()
            # Extract just the attribution lines
            for line in content.split("\n"):
                if line.startswith("- **"):
                    lines.append(line)

    # Add OSM attribution
    osm_sources = os.path.join(REPO_ROOT, "osm", "SOURCES.md")
    if os.path.exists(osm_sources):
        lines.append(f"- **OpenStreetMap contributors**, National, *Social Facilities, Community Centres, NGOs, Charities*, "
                      f"Sourced on {date.today().strftime('%d %B %Y')}, "
                      f"[openstreetmap.org](https://www.openstreetmap.org). License: ODbL")

    lines.append("")
    lines.append(f"Last updated: {date.today().isoformat()}")
    lines.append("")

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  Written: {path}")


def main():
    os.makedirs(COMBINED_DIR, exist_ok=True)

    print("Reading all sources...")
    records = read_all_csvs()

    # Filter out empty names
    records = [r for r in records if r.get("name", "").strip()]

    # Assign IDs to records that don't have one (OSM)
    osm_counter = 0
    for record in records:
        if not record.get("id", "").strip():
            record["id"] = f"osm_social_facilities_{osm_counter:04d}"
            osm_counter += 1

    print(f"\nTotal: {len(records)} records")

    print("\nDetecting cross-source duplicates...")
    mark_duplicates(records)

    print("\nWriting combined output...")
    write_csv(records, os.path.join(COMBINED_DIR, "services.csv"))
    write_json(records, os.path.join(COMBINED_DIR, "services.json"))
    write_sqlite(records, os.path.join(COMBINED_DIR, "services.db"))
    write_sources(os.path.join(COMBINED_DIR, "SOURCES.md"))

    print("\nDone.")


if __name__ == "__main__":
    main()
