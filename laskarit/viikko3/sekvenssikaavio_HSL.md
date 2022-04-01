```mermaid
 sequenceDiagram
    participant Main
    participant Kioksi
    participant Matkakortti
    participant Lataajalaite
    participant Lukijalaita
    participant HKLLaitehallinto
    
    participant rautatietori
    participant ratikka6
    participant bussi244
    
    paricipant kallen kortti
    
    Main->>HKLLaintehallinto: Laitehallinto()
    
    Main->>Lataajalaite: Lataajalaite()
    Main->>Lukijalaita: Lukijalaite()
    Main->>Lukijalaita: Lukijalaite()
    
    Main->>HKLLaitehallinto: lisaa_lataaja(rautatietori)
    Main->>HKLLaitehallinto: lisaa_lukija(ratikka6)
    Main->>HKLLaitehallinto: lisaa_lukija(bussi244)
    
    Main->>Kioski: Kioski()
    participant lippu_luukku
    Main->>Kioski: lippu_luukku.osta_matkakortti("Kalle")
    
    
    
```
