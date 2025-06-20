# FreeVat

**FreeVat** je webová aplikace, která umožňuje uživatelům nahrávat, zobrazovat a mazat 3D modely. Aplikace je postavena na
moderních technologiích a poskytuje uživatelům jednoduché a intuitivní rozhraní při prohlížení 3D modelů. Všechny
modely, které zde uživatelé nahrají, budou veřejně přístupné a bude si je moct stáhnout úplně kdokoli a používat na
úplně cokoli. Je to takové zdrojákoviště 3D objektů, ke kterým má přístup úplně každý.

## Z čeho se aplikace skládá?

### Front-end
- `HTML & CSS` - Základní struktura a stylování
- `Three.js` - Práce s 3D grafikou na webu
- `Tailwind CSS` - Moderní a responzivní design

### Back-end
- `Django` - Celá aplikace je postavena na Djangu
- `PostgreSQL` - Databázový systém
- `Django Rest Framework` - REST API pro komunikaci mezi frontendem a backendem
- `OAuth` - Přihlašování uživatelů a správa přístupových dat
- `Docker` - Kontejnerizace aplikace pro snadné nasazení a škálování

Všechny instalované závislosti jsou uvedeny v souborech `requirements.txt` a `package.json`.

## Kde jsem se inspiroval?
- Poliigon: https://www.poliigon.com/
- Sketchfab: https://sketchfab.com/
- 3DViewerMax: https://3dviewermax.com/
- 3DViewerOnline: https://www.3dvieweronline.com/
- Printables: https://www.printables.com/
- CGTrader: https://www.cgtrader.com/
- Thingiverse: https://www.thingiverse.com/
- Turbosquid: https://www.turbosquid.com/
- ClaraIO: https://clara.io/
- PolyHaven: https://polyhaven.com/
- BlendSwap: https://www.blendswap.com/
- Free3D: https://free3d.com/

## Možné názvy?
- `3Vat`
- `ThreeVat`
- `FreeVat` (finální)

## Co od aplikace očekávám?

- Ukládání 3D modelů do databáze a provádět s nima základní CRUD operace
- Prohlížení objektů v 360° - posouvání, zoomování i rotace
- Registrace, přihlašování a mazání uživatelských účtů
- Zobrazování základních informací o modelech (počet ploch, velikost souboru..)
- Více jazyků na výběr - čeština / angličtina
- Vyhledávání 3D modelů podle názvu, případně podle velikosti