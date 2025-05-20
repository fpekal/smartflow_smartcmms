## Przegląd plików
- compose-test.yaml - to samo, co compose.yaml, tylko że do testów na serwerze
- Dockerfile - instaluje się tam pakiety potrzebne do wybudowania/uruchomienia aplikacji. Dodatkowo jest tam zdefiniowane jak mają się uruchomić testy na serwerze


## Adresy baz danych
Aplikacja powinna się łączyć z bazami danych używając nazw:
- db - baza PostgreSQL
- db-log - baza MongoDB

Przykładowo uruchomienie `ping db-log` powinno powodować ping do kontenera z MongoDB.  
Bazy dla naszej aplikacji dostępne są na domyślnych portach.

## Serwer
- https://smartcmms.everest.stream/api - Backend
- http://everest.stream:8088 - Adminer (gui do edycji PostreSQL)
- http://everest.stream:8089 - Mongo Express (gui do edycji MongoDB)
- everest.stream:5432 - PostgreSQL (do testów lokalnych na prawdziwej bazie danych)
- everest.stream:27017 - MongoDB (do testów lokalnych na prawdziwej bazie danych)


## CI/CD
Wszystkie pushowane zmiany są automatycznie testowane, a zmiany na branchu `main` są dodatkowo automatycznie uruchamiane na serwerze.  
Wykonane testy można sprawdzić na githubie w widoku historii commitów lub w zakładce "Actions".


## TLDR
Potrzebujecie biblioteki lub jakiegoś narzędzia? Dockerfile  
