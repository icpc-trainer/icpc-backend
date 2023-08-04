#!/bin/sh

cmd="$@"

echo "Waiting for postgres..."

while ! nc -z postgresql 5432; do
  sleep 0.1
done

echo "PostgreSQL started"

make migrate heads

exec $cmd
