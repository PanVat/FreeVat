# Python
FROM python:3.12-slim

# Proměnné prostředí
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Nastavení pracovního adresáře
WORKDIR /app

# Instalace systémových balíčků (build-essential, libpq-dev a netcat)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Instalace závislostí
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kód
COPY . .

# *** NOVÉ KROKY PRO ENTRYPOINT SKRIPT ***
# Přidání spouštěcího skriptu a nastavení oprávnění
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Port, na kterém aplikace poběží
EXPOSE 8000

# Nastavení entrypointu a CMD
# ENTRYPOINT spustí náš skript
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

# CMD je to, co entrypoint skript spustí na závěr (exec "$@")
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]