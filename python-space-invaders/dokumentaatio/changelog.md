# Changelog
## Muutokset
**Viikko 3**

Aloitettu pelin ohjelmointi.

Pelissä on nyt alus, jota voi ohjata ylös, alas, vasemmalle ja oikealla.

Pelikentällä on taustakuva ja reunat.

Alus ei voi poistua pelikentältä.

Alus voi ampua ammuksia, jotka liikkuvat. Ammuksia ei voi ampua loputtoman nopeasti.

Luotu testit testaamaan aluksen liikkumista, pelikentän rajojen toimivuutta aluksen kannalta ja ampumistoimintoa.

**Viikko 4**

Peliin lisätty vihollisia. Viholliset voivat ampua takaisin.

Pelaajan ammus voi osua vihollisiin, vihollisten ammukset voivat osua pelaajaan.

Pistelaskuri on olemassa. Pelaajan elämäpalkki on olemassa. Peli loppuu kun palkki tyhjenee.

Viholliset liikkuvat oikealle tai vasemmalle, nopeus vaihtelee, eivät voi mennä kentän ulkopuolelle.

Viholliset spawnaavat sallituissa rajoissa satunnaisesti. Ampuvat sallituissa rajoissa satunnaisin väliajoin.

Tuhottu vihollinen räjähtää, efekti puhtaasti graafinen.

**Viikko 5**

Lisätty toinen tyyppi vihollisia, liikkuvat enemmän ja myös kohti pelaajaa, eivät ammu. Nyt törmäys vihollisen kanssa vähentää pelaajan elämiä.

Lisätty spawnaustoiminto. Vihollisia tulee lisää jos niitä on jäljellä liian vähän. Tällä hetkellä tämä jatkuu loputtomiin.

Lisätty pisteidenlasku tekstitiedostoon. Peli hakee lopuksi edellisen parhaan tuloksen tai kertoo uudesta parhaasta tuloksesta.

Lisätty hyvin yksinkertaiset ääniefektit ampumiseen ja osumiin. Nämä eivät vielä toimi testien kanssa taskien kautta eivätkä kaikilla laitteistolla, joten ne on alustavasti asetettu pois käytöstä. Lisää tietoa README:ssa.

Lisätty graafisia efektejä, uudet viholliset spawnaavat "portaaleista." Nyt myös vihollisten ammukset räjähtävät osuessaan pelaajaan.

**Viikko 6**

Lisätty ajoittainen pomovastustaja. Pomovastustajalla nyt oma luokka, oma kuva ja omat syntyportaali ja kuolemisräjähdys. Pomo liikkuu hitaasti ja kestää useita osumia. Normaalivihollisten lisääntyminen menee tauolle pomon ollessa elossa. Pomon ajoittainen olemassaolo vaikuttanut hieman muihin toimintoihin, jotta ruutu ei ylitäyty vihollisista ja vaikkeustaso sellainen että pomoja pääsee kohtaamaan. Peli tällä hetkellä kuitenkin loputon, pomoja syntyy uusia.
