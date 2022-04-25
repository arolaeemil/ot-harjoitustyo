# Ohjelmistotekniikka, harjoitustyö
## Space invaders

Sovellus on peli, joka on valmiina melko space invaders-tyyppinen sisältäen aluksen jota voi ohjata kaksiulotteisessa kentässä ja vihollisia, joita voi tuhota aluksen ammuksilla.
Pelissä on nyt kahdentyyppisiä vihollisia, joita ilmestyy lisää tuhottaessa sekä pistelaskuri. Pelaaja voi myös tuhoutua jos viholliset osuvat alukseen tai se törmää vihollisiin liian monta kertaa.
Pelin lopullinen versio mahdollisesti sisältää pomovastustajan ja erinäisiä peliin vaikuttuvia muita lisäominaisuuksia.

**Pelin toimivuus**

Peli on tarkoitettu toimivaksi Pythonin versiolla 3.8. Muut versiot saattavat toimia, mutta tätä ei taata. Pelissä on käytetty pygame-kirjastoa.

**Kehitysvaiheen aikainen käyttö**

Peli voidaan käynnistää Ubuntulla komentorivillä komennolla "poetry run invoke start". Ennen tätä on suoritettava "poetry install" ennen ensimmäistä käynnistystä riippuvuuksien asentamiseksi. Jos käynnistyksessä ilmenee ongelmia voi pelin yrittää käynnistää ajamalla src/game.py. Peliä varten avautuu pygame-ikkuna, jos tämän avaaminen ei ole mahdollista ei peliä voi pelata.
Haluttaessa ääniominaisuudet peliin täytyy level.py -tiedoston parametri self.sound_on muuttaa arvoon 1 arvosta 0. Huomioitavaa että tämänhetkiset automaattitestit eivät tue äänien olemassaoloa.

**Dokumentaatio**

[Changelog](https://github.com/arolaeemil/ot-harjoitustyo/blob/master/python-space-invaders/dokumentaatio/changelog.md)

[Työaikakirjanpito](https://github.com/arolaeemil/ot-harjoitustyo/blob/master/python-space-invaders/dokumentaatio/tuntikirjanpito.md)

[Vaatimusmäärittely](https://github.com/arolaeemil/ot-harjoitustyo/blob/master/python-space-invaders/dokumentaatio/vaatimusmaarittely.md)

[Arkkitehtuuri](https://github.com/arolaeemil/ot-harjoitustyo/blob/master/python-space-invaders/dokumentaatio/arkkitehtuuri.md)

**Testaus**

Olemassa olevat testit voi ajaa komennolla "poetry run invoke test"

**Testikattavuus**

Testikattavuusraportin saa aikaan komennolla "poetry run invoke coverage-report"
Raportin löytää tämän jälkeen htmlcov-hakemistosta.
