-- Ciste database schema (CIS-0-3). Money is integer cents, dates are ISO 8601 text.
-- IBANs and card numbers are stored in full; masking happens at the tool boundary (CIS-2-4).

PRAGMA foreign_keys = ON;

CREATE TABLE customers (
    id        TEXT PRIMARY KEY,
    name      TEXT NOT NULL,
    email     TEXT NOT NULL,
    tier      TEXT NOT NULL CHECK (tier IN ('retail', 'premium')),
    joined_on TEXT NOT NULL
);

-- Each Customer has exactly one Account.
CREATE TABLE accounts (
    id            TEXT PRIMARY KEY,
    customer_id   TEXT NOT NULL UNIQUE REFERENCES customers (id),
    iban          TEXT NOT NULL UNIQUE,
    balance_cents INTEGER NOT NULL,
    opened_on     TEXT NOT NULL
);

CREATE TABLE cards (
    id         TEXT PRIMARY KEY,
    account_id TEXT NOT NULL REFERENCES accounts (id),
    number     TEXT NOT NULL UNIQUE,
    last4      TEXT NOT NULL,
    kind       TEXT NOT NULL CHECK (kind IN ('debit', 'virtual', 'credit')),
    status     TEXT NOT NULL CHECK (status IN ('active', 'frozen')),
    expires_on TEXT NOT NULL
);

CREATE TABLE fee_catalogue (
    id           TEXT PRIMARY KEY,
    name         TEXT NOT NULL,
    amount_cents INTEGER NOT NULL,
    ft_section   TEXT NOT NULL
);

-- amount_cents is positive for money out. A Fee has fee_id and no merchant;
-- a Merchant charge is the reverse.
CREATE TABLE transactions (
    id           TEXT PRIMARY KEY,
    account_id   TEXT NOT NULL REFERENCES accounts (id),
    card_id      TEXT REFERENCES cards (id),
    kind         TEXT NOT NULL CHECK (kind IN ('merchant_charge', 'fee')),
    amount_cents INTEGER NOT NULL,
    merchant     TEXT,
    fee_id       TEXT REFERENCES fee_catalogue (id),
    entry_mode   TEXT CHECK (entry_mode IN ('chip_pin', 'contactless', 'online')),
    posted_on    TEXT NOT NULL,
    description  TEXT NOT NULL,
    CHECK (
        (kind = 'fee' AND fee_id IS NOT NULL AND merchant IS NULL)
        OR (kind = 'merchant_charge' AND fee_id IS NULL AND merchant IS NOT NULL)
    )
);

-- UNIQUE (transaction_id) makes a second Refund of the same Fee impossible.
CREATE TABLE refunds (
    id             TEXT PRIMARY KEY,
    transaction_id TEXT NOT NULL UNIQUE REFERENCES transactions (id),
    amount_cents   INTEGER NOT NULL,
    status         TEXT NOT NULL CHECK (status IN ('approved', 'rejected')),
    created_on     TEXT NOT NULL
);

CREATE TABLE disputes (
    reference      TEXT PRIMARY KEY,
    transaction_id TEXT NOT NULL REFERENCES transactions (id),
    status         TEXT NOT NULL,
    reason_code    TEXT NOT NULL,
    report_json    TEXT NOT NULL,
    created_on     TEXT NOT NULL
);

CREATE TABLE escalations (
    id          TEXT PRIMARY KEY,
    customer_id TEXT NOT NULL REFERENCES customers (id),
    reason      TEXT NOT NULL,
    created_on  TEXT NOT NULL
);
