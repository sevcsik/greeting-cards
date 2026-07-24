# Üdvözlőkártya – statikus hanglejátszó

Mobil-első statikus weboldal egyedi audio lejátszóval, GitHub Pages hosztolással és QR-kód deep linkekkel.

**Publikus URL:** https://sevcsik.github.io/greeting-cards/

## Projektstruktúra

```text
index.html              # Főoldal (GitHub Pages)
css/, js/, assets/        # Lejátszó statikus fájlok
.nojekyll                 # Jekyll kikapcsolása
source/                   # Forrás média
scripts/                  # Build scriptek
qrcodes/                  # QR-kód PNG-k
```

## GitHub Pages

Minden a **`main` branch gyökerén** van. Beállítás: Settings → Pages → **`main`** / **`/ (root)`**.

## Helyi előnézet

```bash
python3 -m http.server 8080
```

## Deep linkek

- `/?track=Éva néni`, `/?track=Margó`, `/?track=Lilla`, `/?track=Kati`
