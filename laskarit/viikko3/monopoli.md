```mermaid
 classDiagram
	Pelaaja "2-8" -- "1" Pelilauta
	Ruutu "40" -- "1" Pelilauta
	Pelaaja "1" -- "1" pelinappula
	Pelilauta "1" -- "2" Noppa
	class Pelaaja{
	pelinappula
	}
	class Pelilauta{
	}
	class Ruutu{
	seuraava_ruutu
	}
	class Pelinappula{
	pelaaja
	sijainti_ruutu
	}
	class Noppa{
	}
```
