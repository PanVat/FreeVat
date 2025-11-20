FROM python:3.13-slim

# Nastavení proměnných prostředí
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Pracovní adresář
WORKDIR /app

# Instalace závislostí
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-dev \
    && rm -rf /var/lib/apt/lists/*

# UV
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Kopírování souboru se závislostmi
COPY requirements.txt .

# Stáhnutí Python závislostí
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Zkopírování celého kódu projektu
COPY . .

# Port
EXPOSE 8000

# Spuštění aplikace
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]