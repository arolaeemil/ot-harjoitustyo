# Ohjelmistotekniikka, harjoitustyö
## Space invaders

Sovellus on peli, joka on melko space invaders-tyyppinen sisältäen aluksen jota voi ohjata kaksiulotteisessa kentässä ja vihollisia, joita voi tuhota aluksen ammuksilla.
Pelissä on nyt kahdentyyppisiä vihollisia, joita ilmestyy lisää tuhottaessa sekä pistelaskuri. Välillä ilmestyy myös haastavampia pomovastustajia. Pelaaja voi myös tuhoutua jos viholliset osuvat alukseen tai se törmää vihollisiin liian monta kertaa. Tulevaisuudessa peli voisi sisältää myös esimerkiksi erilaisia aseita alukselle.

**Pelin toimivuus**

Peli on tarkoitettu toimivaksi Pythonin versiolla 3.8. Muut versiot saattavat toimia, mutta tätä ei taata. Pelissä on käytetty pygame-kirjastoa.

**Pelin valmistelu ja pelaaminen**

Peli voidaan käynnistää Ubuntulla komentorivillä komennolla "poetry run invoke start". Ennen tätä on suoritettava "poetry install" ennen ensimmäistä käynnistystä riippuvuuksien asentamiseksi. Jos käynnistyksessä ilmenee ongelmia voi pelin yrittää käynnistää ajamalla src/game.py. Peliä varten avautuu pygame-ikkuna, jos tämän avaaminen ei ole mahdollista ei peliä voi pelata.
Peliin on lisätty ääniominaisuuksia, mutta niitten toimintaa eri laitteistoilla ei voidaa taata, joten ne on poistettu käytöstä jaossa olevassa koodissa. Haluttaessa ääniominaisuudet peliin täytyy level.py -tiedoston parametri self.sound_on muuttaa arvoon 1 arvosta 0 ja mahdollisesti poistaa "#" game.py tiedoston pygame.mixer.init() kohdasta. Myöskään automaattitestit eivät tällä hetkellä tue ääniominaisuuksia. Äänien käyttöönottoa voi yrittää, mutta teknistä tukea tähän ei tällä hetkelle ole saatavilla.
 
**Dokumentaatio**

[Changelog](https://github.com/arolaeemil/ot-harjoitustyo/blob/master/python-space-invaders/dokumentaatio/changelog.md)

[Työaikakirjanpito](https://github.com/arolaeemil/ot-harjoitustyo/blob/master/python-space-invaders/dokumentaatio/tuntikirjanpito.md)

[Vaatimusmäärittely](https://github.com/arolaeemil/ot-harjoitustyo/blob/master/python-space-invaders/dokumentaatio/vaatimusmaarittely.md)

[Arkkitehtuuri](https://github.com/arolaeemil/ot-harjoitustyo/blob/master/python-space-invaders/dokumentaatio/arkkitehtuuri.md)

[Käyttöohje](https://github.com/arolaeemil/ot-harjoitustyo/blob/master/python-space-invaders/dokumentaatio/kayttoohje.md)

**Testaus**

Sovelluksen testit voi ajaa komennolla "poetry run invoke test"

**Testikattavuus**

Testikattavuusraportin saa aikaan komennolla "poetry run invoke coverage-report"
Raportin löytää tämän jälkeen htmlcov-hakemistosta.
