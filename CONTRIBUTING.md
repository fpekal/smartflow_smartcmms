- Branch `main` - stabilna wersja, odpalona na serwerze
- Branch `next` - wersja w trakcie rozwoju

Tworzymy pull requesty do brancha `next`. Następnie wymagane jest dodanie chociaż jednego
reviewera i zgoda z jego strony na dodanie tego kodu.
Pushować na `main` może tylko @fpekal, bo przez użycie GitHub Actions wszyscy mieliby
możliwość odpalania dowolnego kodu na serwerze jako root. *Too bad*

Dodatkowo żeby coś pushować na `next`, to musi to przejść testy. (Nawet nie pozwoli bez przejścia testów)

Więc: pushujecie zmianę na swojego brancha, czekacie aż skończy się automatyczny test,
dodajecie pull requesta do `next` z reviewerem,
reviewer sprawdza kod, akceptuje zmiany, mergeujecie do `next`.
A @fpekal co jakiś czas będę mergeował na `main` i wtedy będzie się uruchamiać na serwerze.

Na swoich branchach możecie robić co chcecie.
