# commons-au/data

Open dataset of support services for vulnerable people in Australia.

Free to access. Free to build on. Free forever.

## Download

The dataset is available in two formats:

- **CSV**: [`data/services.csv`](data/services.csv)
- **JSON**: [`data/services.json`](data/services.json)

Both contain the same data. Use whichever works for you.

## Schema

Every record in the dataset follows the same structure. See [SCHEMA.md](SCHEMA.md) for the full field reference.

| Field | Description |
|-------|------------|
| `id` | Unique identifier |
| `name` | Name of the service |
| `description` | What the service provides |
| `category` | Service type (food, housing, health, legal, etc.) |
| `address` | Street address |
| `suburb` | Suburb |
| `state` | State or territory |
| `postcode` | Postcode |
| `latitude` | Latitude |
| `longitude` | Longitude |
| `phone` | Phone number |
| `email` | Email address |
| `website` | Website URL |
| `hours` | Opening hours |
| `eligibility` | Who can access the service |
| `cost` | Cost (Free, Low-cost, etc.) |

## Data Sources

All government data is used under Creative Commons Attribution licenses. Full attribution is in [SOURCES.md](SOURCES.md).

The dataset is updated weekly by an automated pipeline from [commons-au/pipeline](https://github.com/commons-au/pipeline).

## Contributing

Know a service that isn't listed? See [CONTRIBUTING.md](CONTRIBUTING.md) for how to add it.

## Using This Data

This data is released under [CC0 1.0](LICENSE) — public domain, no restrictions. You can:

- Build an app
- Print it out
- Feed it into a chatbot
- Share it however you want

No permission needed.

**Note**: While the combined dataset is CC0, individual records sourced from government portals carry their original CC-BY licenses and require attribution. See [SOURCES.md](SOURCES.md).

## Related

- [commons-au/landscape](https://github.com/commons-au/landscape) — Research on Australian open data portals and what's available
- [commons-au/pipeline](https://github.com/commons-au/pipeline) — The ETL pipeline that builds this dataset
