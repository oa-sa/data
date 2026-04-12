# Contributing

This dataset grows through two channels:

1. **Government open data** — pulled automatically by the [pipeline](https://github.com/commons-au/pipeline)
2. **Community contributions** — submitted by people who know services that aren't in any government database

This guide is about the second one.

## Who Can Contribute

Anyone. Case workers, volunteers, community organisations, or anyone who knows about a support service that should be listed.

## What To Submit

A service that helps vulnerable people and isn't already in the dataset. This includes:

- Food banks, free meals, community kitchens
- Emergency accommodation, shelters
- Free or low-cost health services
- Mental health and counselling services
- Legal aid and community legal centres
- Employment and training programs
- Financial counselling and emergency relief
- Domestic and family violence support
- Drug and alcohol services
- Disability support services
- Community centres, drop-in spaces
- Free WiFi, public computers
- Anything else that helps someone in need

## How To Submit

### Option 1: Open a GitHub Issue

[Create a new issue](../../issues/new) with the following information:

- **Name**: Name of the service or organisation
- **Description**: What they provide
- **Category**: See [SCHEMA.md](SCHEMA.md) for the list of categories
- **Address**: Street address, suburb, state, postcode
- **Phone**: Contact number
- **Website**: If they have one
- **Hours**: When they're open
- **Eligibility**: Who can access the service
- **Cost**: Free, low-cost, etc.

Include as much as you know. Partial information is still valuable.

### Option 2: Submit a Pull Request

If you're comfortable with GitHub:

1. Fork this repository
2. Add your record(s) to `data/services.csv`
3. Follow the schema in [SCHEMA.md](SCHEMA.md)
4. Set `source_id` to `community`
5. Set `source_name` to `Community contribution`
6. Submit a pull request

### Option 3: Email

If GitHub isn't your thing, that's fine. Reach out with the details and we'll add it.

## Guidelines

- **Accuracy**: Only submit services you know exist and are currently operating
- **No personal information**: Don't include names of staff or clients
- **Public services only**: Only list services that are open to the public or specific eligible groups
- **Keep it current**: If you know a listed service has closed or changed, let us know

## Verification

Community-submitted records are reviewed before being added. We may reach out to confirm details.
