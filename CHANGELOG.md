# Changelog

All notable changes to this dataset will be documented in this file.

## [Unreleased]

### Removed
- ACNC Registered Charities source (65,078 records). The ACNC register is a
  charity registry, not a services directory: zero contact info beyond a
  website, zero coordinates, boilerplate descriptions, and thousands of
  umbrella-entity duplicates (e.g. diocesan trustee corporations registered
  many times per parish). Including it diluted signal with low-quality
  records. Prioritising data quality over volume. May revisit using the AIS
  Programs dataset later, which is service-shaped.

### Added
- SA GP Plus Locations (8 records)
- SA Private Hospitals (50 records)
- GeoJSON zip fetch support in pipeline

### Changed
- Total records: 89,575 to 24,497 (net: -65,078 ACNC removal, +58 new sources)
- Quality distribution now 84% complete / 16% partial / 0.3% minimal
  (previously 68% / 28% / 4%)
- Coordinate coverage now 39% (previously 11%)

## [v1.0.0] - 2026-04-14

First release of the Open Australian Services Archive (OASA).

### Data
- 24,440 support services across all 8 states and territories
- 25 sources: 24 government open data + OpenStreetMap
- Formats: CSV, JSON, SQLite

### Sources Connected
- Federal: Emergency Relief Provider Outlets, Employment Services, Judicial Courts
- VIC: Melbourne Free Services, Casey Food Relief/Libraries/Maternal Health, Ballarat Food/Community Centres/Kindergartens/Early Learning, Neighbourhood Houses
- QLD: Gov Service Counters, Housing Centres, Housing Finder, BreastScreen, Victim Support, Dispute Resolution, DCCSDS Contacts, Youth Justice, Hep C Centres
- SA: Community Directory, Child and Family Health
- TAS: Service Tasmania Shops
- OSM: Social Facilities, Community Centres, NGOs, Charities

### Quality
- 84% complete (location + contact info)
- 15% partial
- Less than 1% minimal

### Infrastructure
- Automated pipeline (oa-sa/pipeline) for government CKAN data
- Separate OSM pipeline (oa-sa/osm) via Geofabrik extract
- Auto-build workflow in data repo
- Zenodo DOI: 10.5281/zenodo.19564281
