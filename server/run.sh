#!/usr/bin/env bash
# Start the local PostgreSQL cluster (if needed) and the Health Kitchen server (app, accounts, admin and API) on http://localhost:8099
set -e
PG=/usr/lib/postgresql/16/bin
DATA=${HK_PGDATA:-$HOME/.local/share/health-kitchen/pgdata}
PORT=${HK_PGPORT:-5440}
$PG/pg_ctl -D "$DATA" status >/dev/null 2>&1 || $PG/pg_ctl -D "$DATA" -o "-p $PORT -k /tmp" -l "$DATA/../pg.log" start
cd "$(dirname "$0")"
exec ${HK_PY:-$HOME/.venvs/hk/bin/python} -m uvicorn app:app --host 0.0.0.0 --port ${HK_PORT:-8099}
