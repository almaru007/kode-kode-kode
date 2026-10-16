# Relational Data Architecture: Marketing Attribution Pipeline

This schema models multi-channel media investments, granular customer journey touchpoints, and transactional conversion outcomes.

## 1. Entity-Relationship Summary

* **`touchpoints` (1) ─── (N) `ad_spend`**: Connected logically via `(date, channel)` for top-of-funnel efficiency analysis.
* **`touchpoints` (N) ─── (1) `users`**: Multiple site visits per user across the evaluation window.
* **`transactions` (N) ─── (1) `users`**: Tracks conversions and repeat purchase behavior connected via `user_id`.

---

## 2. Table Specifications

### Table: `ad_spend`
Aggregated daily marketing investments and delivery metrics across paid acquisition channels.

| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `date` | `DATE` | Reporting day (`YYYY-MM-DD`). |
| `channel` | `VARCHAR(50)` | Marketing channel (e.g., `Meta Ads`, `Google Search`). |
| `spend_nok` | `NUMERIC(10,2)`| Net ad spend in Norwegian Krone. |
| `impressions` | `INTEGER` | Number of ad views served. |
| `clicks` | `INTEGER` | Clicks registered by the ad platform. |

### Table: `touchpoints`
Session-level event stream tracking user interaction history prior to purchase.

| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `touchpoint_id` | `VARCHAR(20)` | Primary key (`TP_XXXXXXX`). |
| `user_id` | `VARCHAR(20)` | Unique persistent visitor identifier (`USR_XXXXX`). |
| `timestamp` | `TIMESTAMP` | UTC timestamp of session start. |
| `channel` | `VARCHAR(50)` | Channel source attributing the session. |
| `campaign` | `VARCHAR(100)`| Specific tactical campaign name. |
| `session_duration_sec` | `INTEGER` | Time spent on site during the visit. |

### Table: `transactions`
Order-level conversion data from backend order management/payment ledger.

| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `transaction_id`| `VARCHAR(20)` | Primary key (`TX_XXXXXX`). |
| `user_id` | `VARCHAR(20)` | Foreign key matching visitor ID. |
| `timestamp` | `TIMESTAMP` | Exact checkout confirmation timestamp. |
| `gross_revenue_nok`| `NUMERIC(10,2)`| Total order value before returns. |
| `margin_pct` | `NUMERIC(3,2)` | Gross product margin percentage. |
| `is_refunded` | `INTEGER` | Binary flag (`1` = returned, `0` = settled). |