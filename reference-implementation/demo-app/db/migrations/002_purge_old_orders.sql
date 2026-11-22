-- Fictional migration for the demo app.
-- Permanently deletes every order placed before 2020. This script takes no backup.
DELETE FROM orders WHERE placed_at < '2020-01-01';
