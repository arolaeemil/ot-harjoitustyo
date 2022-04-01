```mermaid
 classDiagram
	Pelaaja "2-8" -- "1" Peli
	Pelilauta "1" -- "1" Pelilauta
	Ruutu "40" -- "1" Pelilauta
	Pelaaja "1" -- "1" Pelinappula
	Peli "1" -- "2" Noppa
	Pelinappula "1" -- "1" Ruutu
	class Peli{
	pelaajat
	}
	class Pelaaja{
	pelinappula
	}
	class Pelilauta{
	}
	class Ruutu{
	seuraava_ruutu
	ruudun_tyyppi
	}
	class Pelinappula{
	pelaaja
	sijainti_ruutu
	}
	class Noppa{
	}
```
