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

## Äänet

Peliin on lisätty ääniominaisuuksia, mutta niitten toimintaa eri laitteistoilla ei voidaa taata, joten ne on poistettu käytöstä jaossa olevassa koodissa. Haluttaessa ääniominaisuudet peliin täytyy level.py -tiedoston parametri self.sound_on muuttaa arvoon 1 arvosta 0 ja mahdollisesti poistaa "#" game.py tiedoston pygame.mixer.init() kohdasta. Myöskään automaattitestit eivät tällä hetkellä tue ääniominaisuuksia. Äänien käyttöönottoa voi yrittää, mutta teknistä tukea tähän ei tällä hetkelle ole saatavilla.
