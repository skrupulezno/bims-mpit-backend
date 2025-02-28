#!/bin/bash
DB_NAME="mpit"
DB_USER="user"
DB_HOST="localhost"
BACKUP_DIR="/backups/"
DATE=$(date +%Y%m%d)
BACKUP_FILE="${BACKUP_DIR}/${DB_NAME}_${DATE}.dump"

if [ ! -d "$BACKUP_DIR" ]; then
    mkdir -p "$BACKUP_DIR"
fi

pg_dump -U "$DB_USER" -h "$DB_HOST" -F c -b -v -f "$BACKUP_FILE" "$DB_NAME"

if [ $? -eq 0 ]; then
    echo "Backup успешно создан: $BACKUP_FILE"
else
    echo "Ошибка создания backup" >&2
fi

# Добавить в cron 
# chmod +x /backup.sh
# crontab -e
# 0 2 * * * /путь/к/скрипту/backup.sh