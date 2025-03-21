## Przegląd plików
- compose.yaml - ustawia jakie obrazy dockera mają się uruchomić na produkcji. Ustawiane tam są bazy danych. *Raczej* nic tam nie trzeba zmieniać
- compose-test.yaml - to samo, co compose.yaml, tylko że do testów na serwerze
- Dockerfile - instaluje się tam pakiety potrzebne do wybudowania/uruchomienia aplikacji. Dodatkowo jest tam zdefiniowane jak mają się uruchomić testy na serwerze
- .env.template - szablon pliku .env, który trzeba utworzyć, jak chce się u siebie lokalnie uruchomić bazy danych używając `make run-db`
- .env.test - uzupełniony plik .env używany podczas testowania aplikacji na serwerze
- Makefile - są tam takie handy skrypty do uruchomienia i wyłączenia baz danych podczas lokalnego testowania aplikacji


## Skrypty
- make run-db - uruchomienie bazy danych
- make down - wyłączenie bazy danych


## TLDR
Potrzebujecie biblioteki lub jakiegoś narzędzia? Dockerfile  
Potrzebujecie dodatkowego działającego w tle programu? compose.yaml  
