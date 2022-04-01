```mermaid
 sequenceDiagram
    participant Metodi
    participant Machine
    participant Fueltank
    participant Engine
    Main->>Machine: Machine()
    Machine->>Fueltank: self.Fueltank()
    Machine->>Fueltank: self.fueltank.fill(40)
    Machine->>Engine: Engine(self.fueltank)
    Main->>Machine: self.drive()
    Machine->>Engine: self.engine.start()
    Machine->>Engine: self.engine.is_running()
    
```
