#!/bin/bash

CONTENT=$(
  cat <<EOF
version: '3'

services:
EOF
)

DEV=$(
  cat <<EOF

  postgresql:
    container_name: "postgresql"
    image: postgres:15
    restart: always
    env_file:
      - ./.env
    ports:
      - "5432:5432"
    volumes:
      - ./postgres-data:/var/lib/postgresql/data/

  redis:
    container_name: redis
    image: redis
    restart: always
    command: [sh, -c, "redis-server"]
    ports:
      - "6379:6379"

  backend:
    container_name: "backend"
    build: .
    command: python -m app
    restart: always
    env_file:
      - ./.env
    ports:
      - 8000:8000

volumes:
  postgres-data:
EOF
)

PROD=$(
  cat <<EOF

  postgresql:
    container_name: "postgresql"
    image: postgres:15
    restart: always
    env_file:
      - ./.env
    ports:
      - "5432:5432"
    volumes:
      - ../postgres-data:/var/lib/postgresql/data/

  redis:
    container_name: redis
    image: redis
    restart: always
    command: [sh, -c, "redis-server"]
    ports:
      - "6379:6379"

  backend:
    container_name: "backend"
    build: .
    command: python -m app
    restart: always
    env_file:
      - ./.env
    ports:
      - 8000:8000

volumes:
  postgres-data:
EOF
)

RED='\033[0;31m'
GREEN='\033[0;32m'

[ "$#" -eq 1 ] || {
  printf "%b%s" "$RED" "Ошибка. Необходимо ввести 1 аргумент."
  exit 1
}

arg="$1"
case "$arg" in
dev) CONTENT+=$DEV ;;
prod) CONTENT+=$PROD ;;
*)
  printf "%b%s" "$RED" "Ошибка. Недопустимый аргумент."
  exit 1
  ;;
esac

cat <<EOF >docker-compose.yml
$CONTENT
EOF

printf "%b%s" "$GREEN" "docker-compose.sh успешно сгенерирован."
