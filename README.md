# Open Australian Services Archive (OASA)

[![DOI](https://zenodo.org/badge/1208538497.svg)](https://doi.org/10.5281/zenodo.19564281)

Open dataset of support services across Australia.

Free to access. Free to build on. Free forever.

<!-- PIPELINE_STATUS_START -->
**Last updated**: 17 April 2026 | **24497 services** from **5 state(s)** gov data + **1989** OSM records
<!-- PIPELINE_STATUS_END -->

## Structure

```
gov/                     ← Data from government open data portals
├── federal/             ← Federal datasets (data.gov.au)
├── vic/                 ← Victoria
├── nsw/                 ← New South Wales
├── qld/                 ← Queensland
│   └── SOURCES.md       ← Attribution per state

combined/                ← All data merged into one file
├── services.csv         ← Full dataset as CSV
├── services.json        ← Full dataset as JSON
└── SOURCES.md           ← Full attribution list
```

## Quick Start

**Want everything?** Download [`combined/services.csv`](combined/services.csv).

**Want data from a specific state?** Browse the [`gov/`](gov/) folder.

**Want to know where the data came from?** Check the `SOURCES.md` in each folder.

## Schema

Every record follows the same structure. See [SCHEMA.md](SCHEMA.md) for the full field reference.

## How This Data Is Updated

An automated pipeline fetches data from Australian government open data portals, standardises it, and pushes it here. See [oa-sa/pipeline](https://github.com/oa-sa/pipeline).

## Using This Data

Government-sourced data carries Creative Commons Attribution licenses - see the `SOURCES.md` files for details. Each record also embeds its source metadata (`source_organisation`, `source_license`, `source_url`) so attribution travels with the data.

## Related

- [oa-sa/landscape](https://github.com/oa-sa/landscape) - Research on Australian open data portals
- [oa-sa/pipeline](https://github.com/oa-sa/pipeline) - The ETL pipeline that builds this dataset
