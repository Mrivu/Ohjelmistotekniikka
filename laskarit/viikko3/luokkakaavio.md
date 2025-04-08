```mermaid
 classDiagram
    Monopolipeli "1" -- "2" Noppa
    Monopolipeli "1" -- "1" Pelilauta
    Pelilauta "1" -- "40" Ruutu
    Ruutu "1" -- "1" Ruutu : seuraava
    Ruutu "1" -- "0..8" Pelinappula
    Pelinappula "1" -- "1" Pelaaja
    Pelaaja "2..8" -- "1" Monopolipeli
    Ruutu "1" -- "1" Vankila
    Ruutu "1" -- "1" Lähtö
    Ruutu "1" -- "1" Mene Vankilaan
    Ruutu "1" -- "1" Vapaa pysäköinty
    Ruutu "6" -- "6" Sattuma tai Yhteismaa
    Ruutu "8" -- "8" Asemat tai laitokset
    Ruutu "22" -- "22" Katu
    Ruutu "1" -- "1" Toiminto
    Sattuma ja/tai Yhteismaa "6" -- "1...99" Kortti
    Kortti "1" -- "1..99" Toiminto
    Katu "1" -- "1..5" Talo
    Katu "1" -- "1" Pelaaja
    Raha "0...99999" -- "1" Pelaaja
```
