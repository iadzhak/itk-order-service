#!/bin/bash

set -e

echo 'Запускаю миграции'
alembic upgrade head
echo 'Запускаю сервер'
python -m bin.main