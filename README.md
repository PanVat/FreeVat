# 🎁FreeVat

**FreeVat** je webová aplikace, která umožňuje uživatelům **nahrávat, zobrazovat, mazat a ukládat 3D modely**. Aplikace je postavena
na
moderních technologiích a poskytuje uživatelům jednoduché a intuitivní rozhraní při prohlížení 3D modelů. Všechny
modely, které zde uživatelé nahrají, budou veřejně přístupné a bude si je moct stáhnout úplně kdokoli a používat na
úplně cokoli. Je to takové zdrojákoviště 3D objektů, do kterého můžou dobrovolníci přispívat svými výtvory, ke kterým bude mít každý přístup.

[![Version](https://img.shields.io/badge/Verze-Alpha_1.0.0-green.svg?logo=github&logoColor=white)](https://github.com/PanVat/FreeVat)
[![Developer](https://img.shields.io/badge/Vývojář-PanVat-blue)](https://github.com/PanVat)
![License](https://img.shields.io/badge/Licence-Open_Source_✅-purple.svg)
---
## 🛠️Technologie

### 🎨Front-end

- `HTML, CSS & JS` - Základní struktura, stylování a logika
- `Three.js` - Práce s 3D grafikou na webu
- `Tailwind CSS` - Moderní a responzivní webový design
- `Adobe Photoshop` - Tvorba grafických prvků

### ⚙️Back-end

- `Django` - Framework pro vývoj webových aplikací v Pythonu
- `Rosetta` - Správa překladů aplikace, vícejazyčnost
- `Crispy Forms` - Tvorba a stylování uživatelských formulářů
- `PostgreSQL` - Výkonný databázový systém pro ukládání dat
- `OAuth` - Přihlašování a registrace uživatelů s účty třetích stran
- `Node.js` - Prostředí pro běh JavaScriptu na serveru
- `Vite` - Buildování a vývoj v reálném čase
---

## 🔧Instalace
- Jak nainstalovat a spustit aplikaci lokálně je uvedeno [zde](docs/INSTALL.md)

---

## 💡Inspirace

- Poliigon - https://www.poliigon.com/
- Sketchfab - https://sketchfab.com/
- 3DViewerMax - https://3dviewermax.com/
- 3DViewerOnline - https://www.3dvieweronline.com/
- Printables - https://www.printables.com/
- CGTrader - https://www.cgtrader.com/
- Thingiverse - https://www.thingiverse.com/
- Turbosquid - https://www.turbosquid.com/
- ClaraIO - https://clara.io/
- PolyHaven - https://polyhaven.com/
- BlendSwap - https://www.blendswap.com/
- Free3D - https://free3d.com/
- Poly Pizza - https://poly.pizza/
---
## 🏁Cíle
- [x] Ukládání 3D modelů do databáze
- [x] Prodádění základních CRUD operací s 3D modely
- [x] Prohlížení objektů v 360° - posouvání, přibližování i rotace
- [x] Podpora základních 3D formátů - `.obj`, `.fbx`, `.usdz`, `.stl` a `.glb`
- [ ] Podpora softwarových formátů - `.blend`, `.max`, `.c4d` a `.ma`
- [x] Registrace, přihlašování a mazání uživatelských účtů
- [x] Zobrazování základních informací o modelech (počet ploch, velikost souboru..)
- [x] Více jazyků na výběr - čeština / angličtina / němčina
- [x] Plně responzivní design pro PC
- [ ] Plně responzivní design pro mobily a tablety
- [ ] Vyhledávání 3D modelů podle názvu, případně podle velikosti
- [x] Řazení modelů podle data přidání, názvu nebo velikosti
- [ ] Nasazení aplikace na Kubernetes
- [ ] Uspokojení Grussmannových očekávání
---
## ⌛Historie

### ✅Červen 2025 - ![Verze](https://img.shields.io/badge/Indev_0.0.1-darkgreen.svg)

- Vytvoření repozitáře a `README.md`
- Určení technologií a cílů projektu
- Pojmenování aplikace (~~`3Vat`~~ -> ~~`ThreeVat`~~ -> `FreeVat`)
- Základní adresářová struktura
- Instalace potřebných balíčků a knihoven
---

### ✅Červenec a Srpen 2025 - ![Verze](https://img.shields.io/badge/Indev_0.0.1-darkgreen.svg)
- Absolutní prokrastinace a nicnedělání
- O projekt jsem ani nezavadil pohledem
---

### ✅Září 2025 - ![Verze](https://img.shields.io/badge/Indev_0.0.5-darkgreen.svg)
- Nahrazení `Bootstrapu` flexibilnějším `Tailwindem`
- Aplikace je nyní v **CZ**, **EN** a **DE**
- Přeinstalace všech balíčků
- Hodiny a hodiny **centrování neposedného divu**
- Stylování záhlaví a navigace
---

### ✅Říjen 2025 - ![Verze](https://img.shields.io/badge/Indev_0.0.7-darkgreen.svg)
- Dokončení záhlaví, navigace a zápatí
- Tyto elementy jsou nyní plně responzivní (alespoň na PC)
- Instalace a nastavení `Three.js`
- Základní implementace 3D vieweru
---

### ✅Listopad 2025 (1/2) - ![Verze](https://img.shields.io/badge/Indev_0.0.9-darkgreen.svg)
- Registrace, přihlašování, odhlašování a mazání uživatelských účtů
- OAuth přihlašování přes `Google` a `GitHub`
- Pokus o zdockerování aplikace (prozatím neúspěšný)
- Čistka kódu a příprava na další vývoj
---

### ✅Listopad 2025 (2/2) - ![Verze](https://img.shields.io/badge/Indev_0.0.9__3-darkgreen.svg)
- Prokrastinace :(
---

### ✅Prosinec 2025 - ![Verze](https://img.shields.io/badge/Pre--Alpha_0.1.0-darkgreen.svg)
- Formulář pro nahrávání uživatelských dat
- Ukládání 3D modelů do databáze
- Zobrazení nahraných modelů na stránce
- Posouvání, přibližování a rotace modelů ve vieweru
- Možnost změny hesla a uživatelských údajů
---

### ✅Leden 2026 - ![Verze](https://img.shields.io/badge/Alpha_1.0.0-darkgreen.svg)
- Zobrazení mřížky s 3D modely
- Prohlížení modelů ve 360°
- Zobrazení základních informací o modelech
- Možnost editace a mazání vlastních modelů
- Psaní uživatelských komentářů
- Dumpy pro jednoduché nahrávání dat
- Vytvoření vlastního loga a faviconu
- Seznam nedostatků je uveden [zde](docs/ISSUES.md)