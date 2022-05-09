# Käyttöohje

Lataa projektin viimeisimmän [releasen](https://github.com/arolaeemil/ot-harjoitustyo/releases) lähdekoodi.

## Ohjelman käynnistys

Ennen ohjelman käyttöä asenna riippuvuudet käyttämällä komentoa:

```bash
poetry install
```
Nyt ohjelman käynnistys onnistuu komennolla:

```bash
poetry run invoke start
```

Mahdollisessa ongelmatilanteessa kannattaa yrittää suorittaa src/game.py, jos jokin estää edellisen komennon toiminnan. Pelin toiminta vaatii mahdollisuuden avata pygame-ikkuna.

## Pelin pelaaminen

Alusta ohjataan käyttämällä nuolinäppäimiä. Alus kykenee ampumaan spacebarista. Iloisia pelihetkiä.
