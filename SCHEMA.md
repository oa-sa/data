# Data Schema

Every record in `services.csv` and `services.json` follows this schema.

## Service Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | Unique identifier. Format: `{source_id}_{index}` for government data, `community_{index}` for community contributions |
| `name` | string | Yes | Name of the service or organisation |
| `description` | string | No | What the service provides. Plain language. |
| `category` | string | Yes | Primary service category (see categories below) |
| `address` | string | No | Street address |
| `suburb` | string | No | Suburb or locality |
| `state` | string | Yes | Australian state or territory: ACT, NSW, NT, QLD, SA, TAS, VIC, WA |
| `postcode` | string | No | 4-digit Australian postcode |
| `latitude` | number | No | Latitude in decimal degrees (e.g. -37.8136) |
| `longitude` | number | No | Longitude in decimal degrees (e.g. 144.9631) |
| `phone` | string | No | Phone number |
| `email` | string | No | Email address |
| `website` | string | No | Website URL |
| `hours` | string | No | Opening hours in human-readable format |
| `eligibility` | string | No | Who can access the service (e.g. "No restrictions", "Health care card holders") |
| `cost` | string | No | Cost of the service (e.g. "Free", "Low-cost", "Gold coin donation") |

## Source Metadata Fields

These fields track where each record came from.

| Field | Type | Description |
|-------|------|-------------|
| `source_id` | string | Identifier for the data source |
| `source_name` | string | Name of the dataset |
| `source_organisation` | string | Government agency or organisation that published the data |
| `source_jurisdiction` | string | State/territory or "federal" |
| `source_license` | string | License identifier (e.g. CC-BY-4.0) |
| `source_url` | string | URL to the original dataset |
| `source_date` | string | Date the data was sourced (YYYY-MM-DD) |
| `quality` | string | Record completeness: `complete` (has location + contact), `partial` (has one), `minimal` (has neither) |
| `duplicate_of` | string | If set, the `id` of another record that represents the same service. Populated only when a duplicate is detected across sources. |

## Quality

Each record is scored based on how useful it is for someone trying to find or contact a service:

| Quality | Meaning | Typical % |
|---------|---------|-----------|
| `complete` | Has location (address or coordinates) AND contact info (phone, website, or email) | ~84% |
| `partial` | Has either location OR contact info, but not both | ~15% |
| `minimal` | Has neither - just a name and category | ~1% |

## Categories

| Category | Description |
|----------|-------------|
| `food` | Food banks, free meals, food parcels, community kitchens |
| `housing` | Emergency accommodation, social housing, homelessness support |
| `health` | GPs, clinics, hospitals, dental, pharmacies |
| `mental_health` | Counselling, psychiatric services, crisis support |
| `alcohol_drugs` | Drug and alcohol services, needle exchanges, rehabilitation |
| `legal` | Legal aid, community legal centres, courts |
| `financial` | Emergency relief, financial counselling, Centrelink, material aid |
| `employment` | Job services, training, resume help, work programs |
| `education` | English classes, literacy, TAFE, vocational training |
| `disability` | Disability support, NDIS, accessibility services |
| `family` | Family services, domestic violence support, child protection |
| `community` | Community centres, recreation, social groups |
| `information` | Information and referral services |
| `transport` | Transport assistance |
| `personal_care` | Showers, laundry, clothing, personal hygiene |
| `technology` | Free WiFi, public computers, digital literacy |
| `other` | Services that don't fit other categories |
