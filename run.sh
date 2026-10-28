#!/usr/bin/env bash
# Quick CLI launcher - delegates to run.command
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec "$DIR/run.command" "$@"
