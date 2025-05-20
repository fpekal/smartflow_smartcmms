## Przegląd plików
- compose.yaml - ustawia jakie obrazy dockera mają się uruchomić na produkcji. Ustawiane tam są bazy danych. *Raczej* nic tam nie trzeba zmieniać
- Makefile - są tam takie handy skrypty do uruchomienia i wyłączenia baz danych podczas lokalnego testowania aplikacji
- .env.template - szablon pliku .env, który trzeba utworzyć, jak chce się u siebie lokalnie uruchomić bazy danych używając `make run-db`
- .env.test - uzupełniony plik .env używany podczas testowania aplikacji na serwerze

## Skrypty
- make run-db - uruchomienie bazy danych
- make down - wyłączenie bazy danych

## Serwer
- https://smartcmms.everest.stream/api - Backend
- https://smartcmms.everest.stream - Frontend
