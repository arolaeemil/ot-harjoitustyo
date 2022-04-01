```mermaid
 sequenceDiagram
    participant Main
    participant Machine
    participant Fueltank
    participant Engine
    Main->>Machine: __init__
    Machine->>Fueltank: __init__
    Machine->>Fueltank: fill
    Machine->>Engine: __init__
    Main->>Machine: drive
    Machine->>Engine: start
    Machine->>Engine: is_running
    
```
