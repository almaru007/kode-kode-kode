# Cross-Channel Marketing Attribution & Cohort Engine

An end-to-end data pipeline evaluating multi-touch attribution (MTA), true return on ad spend (ROAS), and customer lifetime value (LTV) across digital paid acquisition channels.

## The Business Problem
Native ad platforms (Meta, Google, TikTok) operate as "walled gardens," each relying on isolated click/view windows that claim duplicate credit for downstream conversions. This project models first-party tracking data to:
1. Reconcile platform-reported ROAS against real first-party ledger revenue.
2. Quantify conversion overlap between top-of-funnel prospecting and bottom-of-funnel branded search.
3. Track cohort retention and LTV maturation across acquisition sources.

## Data Pipeline
* **`generate_data.py`**: Simulates 10,000 distinct user journeys, daily media investments, and transaction lifecycles incorporating realistic privacy attribution loss.
* **`data/`**: Relational tables (`ad_spend.csv`, `touchpoints.csv`, `transactions.csv`).
* **`schema_documentation.md`**: Formal data dictionary and relational mapping.

## Setup
```bash
pip install -r requirements.txt
python generate_data.py