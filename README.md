# Üdvözlőkártya – statikus hanglejátszó

Mobil-első statikus weboldal egyedi audio lejátszóval, GitHub Pages hosztolással és QR-kód deep linkekkel.

**Publikus URL (előnézet):** https://sevcsik.github.io/greeting-cards/

## Projektstruktúra

```text
public/                 # GitHub Pages site root
  index.html
  css/styles.css
  js/{config,player,main}.js
  assets/audio/*.m4a
  assets/img/cover.jpg
source/                 # Forrás média (WAV + háttérkép)
scripts/                # Build és QR generáló scriptek
qrcodes/                # Generált QR-kód PNG-k
site.config.json        # Publikus base URL a QR-kódokhoz
.github/workflows/      # GitHub Pages deploy
```

## Média optimalizálás

1. Tedd a hangfájlokat a `source/audio/` mappába (`eva.m4a`, `margo.m4a`, `lilla.m4a`, `kati.m4a`).
2. Tedd a borítóképet a `source/img/` mappába (`cover.jpg` ajánlott).
3. Futtasd:

```bash
python3 scripts/convert-audio.py
python3 scripts/copy-background.py
```

Az ffmpeg a forrás `.m4a` fájlokat webre készített assetekké másolja a `public/assets/audio/` mappába.

## QR-kódok

Állítsd be a `site.config.json` fájlban a GitHub felhasználónevet, repo nevet és a végleges `baseUrl` értéket, majd:

```bash
pip install qrcode[pil]
python3 scripts/generate-qrcodes.py
```

Generált fájlok:

- `qrcodes/main.png` → oldal gyökere
- `qrcodes/track-1.png` … `track-4.png` → `?track=1` … `?track=4` deep linkek

## Deep linkek

| URL | Viselkedés |
|-----|------------|
| `/` | Alap oldal, kézi sávválasztás |
| `/?track=1` | 1. sáv betöltése és automatikus indítás |
| `/?track=2` | 2. sáv |
| `/?track=3` | 3. sáv |
| `/?track=4` | 4. sáv |

## GitHub Pages

A `.github/workflows/deploy.yml` workflow a `main` branch push után feltölti a `public/` mappát a `gh-pages` branch-re.

**Repo beállítás (egyszeri):** Settings → Pages → Build and deployment → Source: **Deploy from a branch** → Branch: `gh-pages` / `/ (root)`.

## Helyi előnézet

```bash
cd public
python3 -m http.server 8080
```

Nyisd meg: http://localhost:8080

## Megjegyzés a csatolt fájlokról

A projekt a feltöltött `Éva.m4a`, `Margó.m4a`, `Lilla.m4a` és `Kati.m4a` hangfájlokat használja.
