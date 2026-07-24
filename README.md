# Üdvözlőkártya – statikus hanglejátszó

Mobil-első statikus weboldal egyedi audio lejátszóval, GitHub Pages hosztolással és QR-kód deep linkekkel.

**Publikus URL (előnézet):** https://sevcsik.github.io/greeting-cards/

## Projektstruktúra

```text
public/                 # GitHub Pages site root
  index.html
  css/styles.css
  js/{config,player,main}.js
  assets/audio/*.mp3
  assets/img/background.jpg
source/                 # Forrás média (WAV + háttérkép)
scripts/                # Build és QR generáló scriptek
qrcodes/                # Generált QR-kód PNG-k
site.config.json        # Publikus base URL a QR-kódokhoz
.github/workflows/      # GitHub Pages deploy
```

## Média optimalizálás

1. Tedd a 4 darab `.wav` fájlt a `source/audio/` mappába (`track1.wav` … `track4.wav` sorrendben).
2. Tedd a háttérképet a `source/img/` mappába (`background.jpg` ajánlott).
3. Futtasd:

```bash
python3 scripts/convert-audio.py
python3 scripts/copy-background.py
```

Az ffmpeg 128 kbps stereo MP3-at készít a `public/assets/audio/` mappába.

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

A `.github/workflows/deploy.yml` workflow a `main` branch push után:

1. Konvertálja a forrás hangfájlokat (ha vannak).
2. Feltölti a `public/` mappát GitHub Pages-re.

**Repo beállítás:** Settings → Pages → Build and deployment → Source: **GitHub Actions**.

## Helyi előnézet

```bash
cd public
python3 -m http.server 8080
```

Nyisd meg: http://localhost:8080

## Megjegyzés a csatolt fájlokról

Ha a saját `.wav` és háttérkép fájljaid még nem kerültek a `source/` mappába, másold be őket, futtasd újra a konverziós scripteket, majd a QR generátort.
