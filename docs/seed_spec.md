# Seed-data specification

What `python -m ciste.db.seed` builds into `ciste.db` (CIS-0-3). The seed is deterministic: it uses `random.Random(SEED)` with `SEED = 20261031` and a fixed "today" of **2026-10-31**, never the system clock. Running it twice must give an identical `iterdump()`.

Everything is fictional. IBANs and card numbers are synthetic and stored in full (masking is added in CIS-2-4).

## 1. Conventions

- **IDs**: `C001`–`C020` (Customers), `A001`–`A020` (Accounts; `A0nn` belongs to `C0nn`), `K001`… (Cards), `T00001`… (Transactions), `F-…` (Fee catalogue entries), `R001`… (Refunds), `D-0001`… (Dispute references), `E001`… (Escalations). Edge-case rows get fixed IDs (section 5).
- **Money**: integer cents in `*_cents` columns; euro only.
- **Dates**: ISO 8601 text. Transactions run from **2026-08-01 to 2026-10-31** (3 months).
- **IBAN**: `IE` + two check digits (valid mod 97) + `CSTE` + 14 digits, 22 characters.
- **Card number**: 16 digits, BIN prefix `400099`, Luhn-valid. `last4` is stored too.
- **Tier**: `retail` or `premium`, on the Customer.

## 2. Tables

| Table | Columns |
|---|---|
| `customers` | `id`, `name`, `email`, `tier` (`retail`/`premium`), `joined_on` |
| `accounts` | `id`, `customer_id` (unique), `iban` (unique), `balance_cents`, `opened_on` |
| `cards` | `id`, `account_id`, `number` (unique), `last4`, `kind` (`debit`/`virtual`/`credit`), `status` (`active`/`frozen`), `expires_on` |
| `fee_catalogue` | `id`, `name`, `amount_cents`, `ft_section` (e.g. `FT-3.2`) |
| `transactions` | `id`, `account_id`, `card_id` (nullable), `kind` (`merchant_charge`/`fee`), `amount_cents` (positive = money out), `merchant` (null for Fees), `fee_id` (null for Merchant charges), `entry_mode` (`chip_pin`/`contactless`/`online`/null), `posted_on`, `description` |
| `refunds` | `id`, `transaction_id` (**unique**), `amount_cents`, `status` (`approved`/`rejected`), `created_on` |
| `disputes` | `reference`, `transaction_id`, `status`, `reason_code`, `report_json`, `created_on` |
| `escalations` | `id`, `customer_id`, `reason`, `created_on` |

Constraints the seed relies on:

- `refunds.transaction_id` is unique, so a second Refund of the same Fee is impossible.
- A `fee` transaction has `fee_id` set and `merchant` null; a `merchant_charge` is the reverse. Enforce with a `CHECK`.
- Each Customer has exactly one Account.

## 3. Fee catalogue

Amounts match `docs/fees_and_terms.md`.

| ID | Name | Amount | `ft_section` |
|---|---|---|---|
| `F-OVERDRAFT` | Unarranged overdraft | €65.00 | FT-3.2 |
| `F-CARD-REPL` | Card replacement | €10.00 | FT-4.2 |
| `F-CARD-EXPRESS` | Express card delivery | €25.00 | FT-4.3 |
| `F-INTL` | International transfer | €15.00 | FT-5.1 |
| `F-RECALL` | International transfer recall | €175.00 | FT-5.2 |
| `F-RETURNED` | Returned payment | €12.00 | FT-6.1 |

## 4. Customers

20 Customers: 12 retail, 8 premium. Names are Irish and fictional. Each has one Account and 2–3 Cards. Unless an edge case says otherwise, Cards are `active`, balances are positive, and there is no Refund, Dispute or Escalation.

| ID | Name | Tier | Cards | Notes |
|---|---|---|---|---|
| C001 | Aoife Brennan | retail | 2 debit | Retail Fee > €50 (E2) |
| C002 | Cian Murphy | retail | 2 debit, 1 virtual | Duplicate Merchant charge (E1) |
| C003 | Niamh Doyle | retail | 2 debit | Frozen Card (E5) |
| C004 | Seán Kavanagh | retail | 2 debit | Chip-and-PIN transaction (E6) |
| C005 | Ciara Walsh | retail | 2 debit, 1 virtual | Small Fee, refundable (E7) |
| C006 | Oisín Byrne | retail | 2 debit | Already-refunded Fee (E4) |
| C007 | Gráinne Ryan | retail | 2 debit | Prior Escalation (E8) |
| C008 | Darragh Nolan | retail | 2 debit | Regular spender, no incidents |
| C009 | Saoirse Quinn | retail | 2 debit, 1 virtual | Regular spender, no incidents |
| C010 | Eoghan Hayes | retail | 2 debit | Returned payment Fees (E9) |
| C011 | Róisín Gallagher | retail | 2 debit | Low balance, dips below zero once |
| C012 | Fionn Daly | retail | 2 debit | Regular spender, no incidents |
| C013 | Éabha Fitzpatrick | premium | 2 debit, 1 credit | Premium Fee > €150 (E3) |
| C014 | Tadhg Sullivan | premium | 2 debit, 1 credit | Premium Fee between €50 and €150 (E10) |
| C015 | Sinéad McCarthy | premium | 2 debit, 1 credit | Open Dispute (E11) |
| C016 | Conor Lynch | premium | 2 debit | Heavy international transfers |
| C017 | Orla Brady | premium | 2 debit, 1 virtual | Regular spender, no incidents |
| C018 | Pádraig Moran | premium | 2 debit, 1 credit | Regular spender, no incidents |
| C019 | Clodagh Fahy | premium | 2 debit | Regular spender, no incidents |
| C020 | Rónán Keane | premium | 2 debit, 1 virtual | Regular spender, no incidents |

## 5. Edge cases

Every edge case exists with its fixed ID. Evals refer to them by ID, so they must not move.

| # | Edge case | Customer | Fixed rows |
|---|---|---|---|
| E1 | **Duplicate Merchant charge**: the same merchant, amount, Card and day, posted twice | C002 | `T90001` and `T90002`: "Dunnes Stores", €42.50, same Card, 2026-10-14, `online` |
| E2 | **Retail Fee > €50** (over the retail Refund cap, within the premium cap) | C001 | `T90003`: `F-OVERDRAFT` €65.00, 2026-10-09 |
| E3 | **Premium Fee > €150** (over both Refund caps) | C013 | `T90004`: `F-RECALL` €175.00, 2026-10-02 |
| E4 | **Already-refunded Fee** | C006 | `T90005`: `F-CARD-REPL` €10.00, 2026-09-21, with `R001` approved for €10.00 |
| E5 | **Frozen Card** | C003 | `K005` (a debit Card) has `status` `frozen`; its last transaction is before 2026-10-20 |
| E6 | **Chip-and-PIN transaction** (for the "chip-and-PIN authorised" reason code) | C004 | `T90006`: "Maxol Service Station", €58.00, `chip_pin`, 2026-10-11, on a physical debit Card |
| E7 | **Retail Fee within the cap, not yet refunded** | C005 | `T90007`: `F-CARD-EXPRESS` €25.00, 2026-10-18 |
| E8 | **Prior Escalation** | C007 | `E001`: reason "Customer asked for a human", 2026-09-30 |
| E9 | **Returned payment Fees** | C010 | `T90008`, `T90009`: `F-RETURNED` €12.00, 2026-09-05 and 2026-10-05 |
| E10 | **Premium Fee between €50 and €150** (refundable for premium, not for retail) | C014 | `T90010`: `F-OVERDRAFT` €65.00, 2026-10-22 |
| E11 | **Open Dispute** | C015 | `D-0001` on `T90011` ("Booking.com", €310.00, `online`, 2026-09-12), reason code `not_received`, status `open`, short `report_json`; new Disputes continue from `D-0002` |

The edge cases cover each eval category in CIS-4-1:

- **refund_ok**: E7 (retail), E10 (premium)
- **refund_over_limit**: E2 (retail), E3 (premium)
- **dispute**: E1, E6, E11
- **escalation**: E8
- **already refunded** (a Refund must be refused): E4

E1, E6 and E11 are Merchant charges, which a Refund can never target, so they also test that the agent explains the difference between a Refund and a Dispute.

## 6. Transaction mix

About **500** transactions in total, including the fixed rows (roughly 25 per Customer, with C011 and C016 nearer 35).

- **Merchant charges** (about 94%), drawn with a seeded random choice:

  | Category | Merchants | Typical amount |
  |---|---|---|
  | Groceries | Dunnes Stores, Tesco Ireland, Lidl, SuperValu | €8–€95 |
  | Transport | Leap Card, Irish Rail, Maxol Service Station, Circle K | €3–€70 |
  | Eating out | Insomnia, Supermac's, Bewley's, Boojum | €4–€45 |
  | Subscriptions | Netflix, Spotify, Vodafone Ireland | €8–€60, monthly |
  | Online | Amazon.ie, Zalando, Booking.com | €15–€320 |

  Entry modes: about 55% `contactless`, 25% `chip_pin`, 20% `online`. Subscriptions and Online are always `online`.

- **Fees** (about 6%): drawn from the catalogue, plus the fixed rows above. At most one `F-OVERDRAFT` per Customer per month. "Regular spender, no incidents" Customers get no Fees.
- **Balances**: each Account's `balance_cents` equals its opening balance minus all `amount_cents`. No balance is below zero except C011's, which dips below zero once and gets an `F-OVERDRAFT` Fee.
- **Refunds**: `R001` only (E4). No other Refunds, so the Refund cap can be tested from a clean state.
- **Dates**: spread across the 3 months with a seeded random day. Subscriptions repeat on the same day each month. Rows with the same date are ordered by ID.

## 7. Checks

The seed script's pytest test (CIS-0-3) checks:

- Two runs give an identical hash of `iterdump()` output.
- 20 Customers (12 retail, 8 premium), 20 Accounts, 40–60 Cards, 450–550 transactions.
- Every edge case in section 5 exists with the stated Customer, amount, date and Card state.
- A second `refunds` insert for `T90005` raises `sqlite3.IntegrityError`.
- No Refund exists for a Merchant charge.
- Every Fee transaction's amount equals its catalogue amount, and its `ft_section` exists in `docs/fees_and_terms.md`.
