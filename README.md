# Chomsky-normálforma 
* A program Chomsky-normálformára hozza beolvasott nyelvtan.
* Elsőként bekéri a nyelvtant tartalmazó szöveges dokumentumot, melynek a formai követelményei a következők:
  * A fájlban minden egyes sora egy új szimbólumra vonatkoztatott szabályrendszert jelképez.
  * A sor első betűje a szimbólum majd a kettős pont után `|` jellel elválasztva az arra vonatkozó szabályok.
  * A kezdő szimbólum mindig az `S`. 
  * A terminálisok halmaza az angol ábécé kisbetűi, a nem terminálisok halmaza az angol ábécé nagybetűi. 
  * Az epszilon a `_` karakter jelképezi.
  * Példa:
  ```
  S: AB | AAaB | CBA
  A: BB | aBBa | a
  B:  _ | aSB
  C: aA | BC   | d
  ```
* Az átalakítások során megjelennek új nem terminálisok, a `Q()` jelképező álnemterminális, illetve a `[]` hosszcsökkentésnél felhasznált nem terminális szimbólumok.
* A program végén lehetőségünk van megadni szavakat és lekérdezni, hogy tartalmazza-e a nyelvtan. 
* A programot a `0` karakter megadásával tudjuk bezárni.
* A program az **ELTE IK - Formális nyelvek és automaták** nevű tárgyon tanult algoritmus reprezentálására készült 2015/16-2 félévében.
