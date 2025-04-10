- Branch `main` - stabilna wersja, odpalona na serwerze
- Branch `next` - wersja w trakcie rozwoju

**ZAKAZ** force pusha na `next`.
Pushować na `main` może tylko @fpekal, bo przez użycie GitHub Actions byłaby
możliwość odpalania dowolnego kodu na serwerze.
Dodatkowo żeby coś pushować na `next` to musi to przejść testy.

Więc: pushujecie zmianę na swojego brancha, czekacie aż skończy się automatyczny test, pushujecie na `next`.
A ja co jakiś czas będę mergeował na `main` i wtedy będzie się uruchamiać na serwerze.

Na swoich branchach możecie robić co chcecie.
