#!/bin/bash
# entrypoint.sh - Spouštěcí skript pro kontejner Django

# Čekání na PostgreSQL (Zajišťuje, že DB je opravdu připravena před spuštěním migrací)
echo "Waiting for postgres..."

while ! nc -z db 5432; do
  sleep 0.1
done

echo "PostgreSQL started"

# Spuštění migrací
echo "Running Django migrations..."
python manage.py migrate --noinput

# Vytvoření superuživatele (z proměnné prostředí)
echo "Creating superuser if it does not exist..."
# Zkontroluje, zda existuje proměnná prostředí pro ADMIN heslo.
if [ -z "$DJANGO_SUPERUSER_USERNAME" ] || [ -z "$DJANGO_SUPERUSER_PASSWORD" ]; then
    echo "WARNING: Superuser environment variables not set. Skipping automatic superuser creation."
else
    # Příkaz pro vytvoření superuživatele, pokud neexistuje (nutné definovat DJANGO_SUPERUSER_EMAIL)
    python manage.py createsuperuser --noinput || true
fi


# Spuštění hlavního příkazu kontejneru (runserver)
echo "Starting Django server..."
exec "$@"