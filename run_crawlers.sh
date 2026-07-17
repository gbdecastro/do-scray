#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

mkdir -p logs

LOG_FILE="logs/cron_run_crawlers.log"

exec > >(tee -a "$LOG_FILE") 2>&1

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"
}

trap 'log "Execução dos crawlers interrompida com erro."' ERR

log "Iniciando execução dos crawlers"
python3 -m diario_oficial.apps.run_crawlers
log "Execução dos crawlers finalizada"
