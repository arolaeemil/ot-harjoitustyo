# Arkkitehtuurikuvaus

## Rakenne

Ohjelman perusrakenne koostuu luokista game, gameloop ja level. Testausta helpottamaan on tehty luokat clock, renderer ja event_queue, jotta kyseisiä toiminnallisuuksia ei olisi pakko upottaa muihin luokiin hankaloittamaan testaamista.
Pelin käynnistää ja alustaa luokka game ja pelisilmukkana toimii luokka gameloop. Gameloop vastaa pelaajan syötteen käsittelystä. Luokka level vastaa peliobjektien liikuttelusta ja muusta yleisestä pelin tapahtumakulkuun liittyvästä toiminnasta. Levelin tarvitsemat objektit ovat sprites kansiossa. Jokaiselle erityyppisellä objektilla on omat luokkansa, jotka perivät pygamen sprite-luokan. Objektit hakevat oman kuvansa assets-kansiosta.

## Luokkakaavio
```mermaid
 classDiagram
  game "1" -- "1" gameloop
  level "1" -- "1" gameloop
  level "1" -- "1" game
  renderer "1" -- "1"game
  clock "1" -- "1" game
  eventqueu "1" -- "1" game
  
  basicenemy "6" -- "1" level
  boss "1" -- "1" level
  spaceship "1" -- "1" level
  shot "*" -- "1" level
  blob "*" -- "1" level
  blocker "*" -- "1" level
  explosion "*" -- "1" level

```

Huomioita luokista:

Spritejä ovat basicenemy, spaceship, boss, shot, blob, blocker, explosion. 
Basicenemyjä luodaan kahta erilaista tyyppiä ja ne edustavat pelin vihollisia. Boss on haastavampi vihollinen, jolla on enemmän elämiä ja suurempi koko.
Spaceship luokka toimii pelaajan ohjaamana aluksena.
Pelaajan ammukset kuvataan luokalla shot ja vihollisten ammukset luokalla blob. Blocker luokka muodostaa alueen, jolle muut objektit eivät voi mennä, tällä hetkellä kentän reunat. 
Explosion on tällä hetkellä puhtaasti graafinen efekti. Explosion-luokka huolehtii myös blobien räjähdyksestä ja portaaliksi nimetyn efektin syntymisestä kun vihollisia syntyy lisää. 

## Sekvenssikaavio ammuksen syntymisestä, operaation onnistuessa ##

```mermaid
 sequenceDiagram
  participant Player
  participant Gameloop
  participant Level
  participant Clock
  participant Spaceship
  participant Shot

  Player ->> Gameloop: Press "spacebar", Gameloop.shoot = True
  Gameloop ->> Clock: get_ticks()
  Clock -->> Gameloop: time
  Gameloop ->> Level: Level.shoot(level.ship, time)
  Level ->> Ship: Ship.can_shoot(current_time)
  Ship -->> Level: True
  Level ->> Ship: give_coords(), ship.previous_shot_time = current_time
  Ship -->> Level: coordinates(x,y)
  Level ->> Shot: Shot(coords[0], coords[1])
  Shot -->> Level: Shot
  Level ->> Level: level.shots.add(Shot())
  
```
