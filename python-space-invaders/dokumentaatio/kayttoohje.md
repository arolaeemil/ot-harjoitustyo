# Käyttöohje

Lataa projektin viimeisimmän [releasen](https://github.com/arolaeemil/ot-harjoitustyo/releases) lähdekoodi.

## Ohjelman käynnistys

Ennen ohjelman käyttöä asenna riippuvuudet käyttämällä komentoa:

```bash
poetry install
```
Ennen pelaamista tee database hupputulosten kirjanpito varten käyttämällä komentoa:

```bash
poetry run invoke build
```
Nyt ohjelman käynnistys onnistuu komennolla:

```bash
poetry run invoke start
```
Peli kysyy alkuun 2 parametria. Toinen on vaikeustaso ja toinen äänien päälläolo. Vastaa näihin komentoriville tulostuvien ohjeiden mukaisesti.
Mahdollisessa ongelmatilanteessa kannattaa yrittää suorittaa src/game.py, jos jokin estää edellisen komennon toiminnan. Pelin toiminta vaatii mahdollisuuden avata pygame-ikkuna.

## Pelin pelaaminen

Alusta ohjataan käyttämällä nuolinäppäimiä. Alus kykenee ampumaan spacebarista. Iloisia pelihetkiä.

## Äänet

Peliin on lisätty ääniominaisuuksia, mutta niitten toimintaa eri laitteistoilla ei voidaa taata, joten ne on poistettu käytöstä ellei niitä erikseen valitse päälläoleviksi. Haluttaessa ääniominaisuudet peliin saa alkukyselyn kautta.
