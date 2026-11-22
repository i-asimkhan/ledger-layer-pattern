-- Fictional migration for the demo app.
CREATE TABLE orders (
    id        INTEGER PRIMARY KEY,
    customer  TEXT NOT NULL,
    placed_at TEXT NOT NULL
);
