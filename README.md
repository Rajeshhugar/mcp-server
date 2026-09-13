# Expense Tracker MCP server

The server requires a database URL in `DATABASE_URL`.

For local development only:

```powershell
$env:DATABASE_URL = "sqlite:///expenses.db"
uv run python main.py
```

For a Prefect Horizon deployment, create a hosted PostgreSQL database and set its
connection string as the `DATABASE_URL` environment variable in the Horizon
server settings. Do not use a SQLite URL in Horizon: its deployed source
filesystem is not durable writable storage.

For example (the server also accepts the standard `postgresql://...` URL that
most providers show in their dashboard):

```text
postgresql+psycopg://USER:PASSWORD@HOST:5432/DATABASE?sslmode=require
```
