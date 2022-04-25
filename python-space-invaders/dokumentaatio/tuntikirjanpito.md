# Työaikakirjanpito, Ohjelmistotekniikan harjoitustyö
## Työpäivät
**29.3**
Yhteensä 2 tuntia.
Vaatimusmäärittelyn laatiminen.
Yleistä suunnittelua koskien projektin ohjelmoinnin aloittamista.


**2.4**

Yhteensä 7 tuntia.
Ohjelmoinnin varsinainen aloitus. Toteutettu perustoiminnallisuus ilman vihollisia. Pelaajalla nyt alus, joka voi liikkua ja ampua, ei voi poistua kentältä.
Säätämistä gitin, poetryn, invoken jne. kanssa. Koska Ubuntu for Windows niin ongelmia oli aika paljon saada halutut asiat toimimaan projektin kanssa.

**5.4**

Yhteensä 1 tuntia.
Dokumenttien kuntoon laittoa ja testausta etätyöaseman kautta. Tässä ongelmia poetryn ja pythonin versioiden kanssa. Lopulta saatu toimimaan siten, että luotan siihen että toimii kun tarkastaja yrittää.

**10.4**
Yhteensä 9 tuntia.
Lisätty paljon toiminnallisuutta koskien vihollisia. Alkutoimenpiteet pisteidenlaskua ja pelaajan elämiä varten tehty. Korjattu pylintin antamia virheitä, joita oli paljon. Laajennettu testejä. Tehty luokkakaaviota. Päivitetty dokumentaatiota. Lisätty task-komentoja. Testattu etäyhteyden kautta.

**22.4**
Yhteensä 7 tuntia.
Mietitty miten vihollisten spawnaus tullaan tekemään ja toteutettu se. Lisätty ääniefektit. Lisätty uusi vihollistyyppi. Laajennettu hieman puhtaasti graafisia efektejä. Vihollistyyppi ja graafiset efektit eivät omia uusia luokkiaan vaan vanhoja ja levelin koodia muokattiin mahdollistamaan erilaisten asioiden kutsu näistä luokista. Selkeytetty pelin nopeuden säätämistä tarvittaessa, oli alunperin varsin hankalaa saada haltutut suhteelliset muutokset haluttuihin asioihin.

**25.4**
Yhteensä 4 tuntia.
Laajennettu testejä ja hiouttu lisättyjä ominaisuuksia. Testeissä ongelma äänien mukaanotossa, saatu toimimaan kun ajaa pytest VSC:llä. Ei kuitenkaan siten että toimisi taskina WLS kanssa. Päädytty ratkaisuun, jossa äänet voi poistaa käytöstä muuttamalla levelin sounds parametriä, jotta testit saadaan toimimaan. Päänvaivaa aiheutti myös miten saada input komentojen oikeellisuus testattua pytestillä. Tähän ei saatu ratkaisua.
