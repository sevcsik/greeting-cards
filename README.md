# Üdvözlőkártya – statikus hanglejátszó

Mobil-első statikus weboldal egyedi audio lejátszóval, GitHub Pages hosztolással és QR-kód deep linkekkel.

**Publikus URL:** https://sevcsik.github.io/greeting-cards/

## Projektstruktúra

```text
docs/                   # GitHub Pages site (main branch /docs)
  index.html
  css/styles.css
  js/{config,player,main}.js
  assets/audio/*.m4a
  assets/img/cover.jpg
source/                 # Forrás média
scripts/                # Build és QR generáló scriptek
qrcodes/                # Generált QR-kód PNG-k
site.config.json        # Publikus base URL a QR-kódokhoz
.github/workflows/      # Asset build a main branch-en
```

## Média optimalizálás

1. Tedd a hangfájlokat a `source/audio/` mappába (`eva.m4a`, `margo.m4a`, `lilla.m4a`, `kati.m4a`).
2. Tedd a borítóképet a `source/img/` mappába (`cover.jpg` ajánlott).
3. Futtasd:

```bash
python3 scripts/convert-audio.py
python3 scripts/copy-background.py
```

Az ffmpeg a forrás fájlokat a `docs/assets/` mappába készíti.

## QR-kódok

```bash
pip install qrcode[pil]
python3 scripts/generate-qrcodes.py
```

Generált fájlok:

- `qrcodes/main.png` → oldal gyökere
- `qrcodes/track-eva.png`, `track-margo.png`, `track-lilla.png`, `track-kati.png` → név alapú deep linkek

## Deep linkek

| URL | Viselkedés |
|-----|------------|
| `/` | Alap oldal, kézi sávválasztás |
| `/?track=Éva` | Éva hang betöltése és automatikus indítás |
| `/?track=Margó` | Margó hang |
| `/?track=Lilla` | Lilla hang |
| `/?track=Kati` | Kati hang |

## GitHub Pages

Minden a **`main` branch-en** van. A GitHub Pages a `docs/` mappát szolgálja ki.

**Repo beállítás:** Settings → Pages → Source: **Deploy from a branch** → Branch: **`main`** → Folder: **`/docs`**

## Helyi előnézet

```bash
cd docs
python3 -m http.server 8080
```

Nyisd meg: http://localhost:8080
