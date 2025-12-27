## Požadavky

- `Python 3.10` nebo [novější](https://www.python.org/)
- `PostgreSQL 14` nebo [novější](https://www.postgresql.org/)
- `Node.js` [nejnovější](https://nodejs.org/)

## Postup

### 1. Naklonování repozitáře

```
git clone https://github.com/PanVat/FreeVat.git
cd FreeVat
```

---

### 2. Vytvoření virtuálního prostředí

#### Windows

```
python -m venv .venv
.\venv\Scripts\activate
```

#### Linux

```
python3 -m venv .venv
source .venv/bin/activate
```

---

### 3. Instalace potřebných balíčků

```
pip install -r requirements.txt
npm install
```

---

### 4. Vytvoření databáze

#### V PostgreSQL terminálu

```
CREATE DATABASE freevat;
```

---

### 5. Nastavení konfiguračního souboru

- Přejmenujte soubor `.env.example` na `.env`
- Nastavte si přístupové klíče pro `Django` a `OAuth`

---

### 6. Spuštění migrací

```
python manage.py migrate
```

---

### 7. Vytvoření superuživatele

```
python manage.py createsuperuser
```

---

### 8. Kompilace překladů

```
python manage.py compilemessages
```

---

### 9. Spuštění serveru

```
npm run dev
python manage.py runserver
```

- Do prohlížeče zadejte `localhost:8000`