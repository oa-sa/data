# commons-au/data

Open dataset of support services for vulnerable people in Australia.

Free to access. Free to build on. Free forever.

<!-- PIPELINE_STATUS_START -->
**Last updated**: Not yet populated. Run the pipeline to fetch data.
<!-- PIPELINE_STATUS_END -->

## Structure

```
government/              ← Data from government open data portals
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

**Want data from a specific state?** Browse the [`government/`](government/) folder.

**Want to know where the data came from?** Check the `SOURCES.md` in each folder.

## Schema

Every record follows the same structure. See [SCHEMA.md](SCHEMA.md) for the full field reference.

## How This Data Is Updated

An automated pipeline fetches data from Australian government open data portals, standardises it, and pushes it here. See [commons-au/pipeline](https://github.com/commons-au/pipeline).

## Using This Data

Government-sourced data carries Creative Commons Attribution licenses — see the `SOURCES.md` files for details. Each record also embeds its source metadata (`source_organisation`, `source_license`, `source_url`) so attribution travels with the data.

## Related

- [commons-au/landscape](https://github.com/commons-au/landscape) — Research on Australian open data portals
- [commons-au/pipeline](https://github.com/commons-au/pipeline) — The ETL pipeline that builds this dataset
