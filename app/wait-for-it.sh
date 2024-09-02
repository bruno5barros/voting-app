#!/bin/sh

set -e

host="$1"
shift
cmd="$@"

until curl "$host/health/" | grep -q '"status": "ok"'; do
  >&2 echo "Health check not available - waiting...$host"
  sleep 3
done

>&2 echo "Health check available - executing command"
exec $cmd
