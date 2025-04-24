from django.core.management.base import BaseCommand
from smartcmms.models import Form, Activity


class Command(BaseCommand):
    help = 'Loads initial forms and activities into the database'

    def handle(self, *args, **kwargs):
        forms_data = [
            {
                "name": "1.1 Przepompownia PPOŻ v1.csv",
                "activities": [
                    "Sprawdzenie stanu obudowy pompy.",
                    "Ocena stanu przewodów elektrycznych i hydraulicznych.",
                    "Kontrola poziomu oleju i stanu zbiorników paliwa (jeśli dotyczy).",
                    "Uruchomienie pompy i sprawdzenie ciśnienia w systemie.",
                    "Test działania zaworów bezpieczeństwa.",
                    "Sprawdzenie czasu reakcji pompy",
                    "Sprawdzenie stanu baterii (jeśli dotyczy).",
                    "Ocena stanu generatora (jeśli dotyczy).",
                    "Sprawdzenie uszczelek i połączeń.",
                    "Inspekcja filtrów i innych elementów eksploatacyjnych."
                ]
            },
            {
                "name": "1.9 SSP System Sygnalizacji Pożaru -  (czujki dymowe,ROP v1.csv",
                "activities": [
                    "Sprawdzenie stanu centralki alarmowej.",
                    "Ocena stanu czujek pożarowych.",
                    "Kontrola sygnalizatorów akustycznych i optycznych.",
                    "Sprawdzenie przycisków alarmowych.",
                    "Test funkcjonalności centrali alarmowej.",
                    "Sprawdzenie zasilania głównego i awaryjnego.",
                    "Test komunikacji między centralą a czujkami.",
                    "Test wyzwolenia alarmu z różnych czujek pożarowych.",
                    "Test wyzwolenia alarmu z przycisków ręcznych.",
                    "Test działania sygnalizatorów akustycznych i optycznych.",
                    "Symulacja sytuacji alarmowej i ocena reakcji systemu.",
                    "Sprawdzenie działania systemu powiadamiania.",
                    "Kontrola stanu baterii awaryjnych.",
                    "Test działania systemu przekazywania alarmów do jednostki straży pożarnej."
                ]
            },
            {
                "name": "2.1 Transformatory v1.csv",
                "activities": [
                    "Sprawdzenie działania dopływu i wylotu powietrza w komorze",
                    "Ocena stanu czystości, uszkodzeń, zamocowania i obecności korozji",
                    "Kontrola kompletności oświetlenia pomieszczenia",
                    "Sprawdzenie połączeń w razie konieczności poprawienie zomontowania i oczyszczenie",
                    "Sprawdzenie wizualne transformatora",
                    "Sprawdzenie urządzeń zabezpieczających pod względem działania i kompletności",
                    "Przeczyszczenie dla zapewnienia działania instalacji",
                    "Sprawdzenie ciągości uziemienia roboczego",
                    "Sprawdzenie ciągości uziemienia ochronnego"
                ]
            },
            {
                "name": "2.2 Rozdzielnia SN v1.csv",
                "activities": [
                    "Oględziny wzrokowe",
                    "Sprawdzenie kompletności i działania oświetlenia pomieszczenia",
                    "Sprawdzenie pod względem zabrudzenia, uszkodzeń, korozji i zamocowania",
                    "Kontrola urządzeń ochronnych pod względem sprawnoci funkcji mechanicznych i elektrycznych",
                    "Sprawdzenie urządzeń zabezpieczających pod względem działania",
                    "Kontrola kompletności wyposażenia BHP oraz ich legazliacji",
                    "Przeczyszczenie dla zapewnienia działania instalacji",
                    "Sprawdzenie ciagłości uziemienia",
                    "Termowizja rozdzielni "
                ]
            },
            {
                "name": "3.1 CCTV v1.csv",
                "activities": [
                    "Czyszczenie monitorów",
                    "Czyszczenie i test rejestratorów",
                    "Czyszczenie i test kamer ( tryb dzienny i nocny, regulacja obrazu)",
                    "Sprawdzenie poprawności nagrań (tryb dzienny i nocny)",
                    "Pomiar napięć zasilania",
                    "Spradzenie zasilania awaryjnego jeśli występuje"
                ]
            },
            {
                "name": "3.7 System SSWiN v1.csv",
                "activities": [
                    "Sprawdzić stan centrali alarmowej i akumulatorów",
                    "Sprawdzić zdalne powiadamianie (jeśli jest zamontowane)",
                    "Sprawdzić odzwierciedlenie w wizualizacji (jeśli zainstalowano)",
                    "Sprawdzić stan i działanie czujników drzwi",
                    "Sprawdzić działania sygnalizacji optycznej i akustycznej (jeśli zainstalowano)",
                    "Sprawdzić poprawność działania w razie wystąpienia alarmu pożarowego"
                ]
            },
            {
                "name": "4.18 Kurtyny powietrzne v1.csv",
                "activities": [
                    "Sprawdzić stan połączeń elektrycznych",
                    "Sprawdzić zabezpieczenia elektryczne i wysterowania",
                    "Sprawdzić stan i działanie automatyki",
                    "Sprawdzić stan wymiennika (w razie potrzeby oczyścić)",
                    "Sprawdzić czy nagrzewnica jest odpowietrzona (nagrzewnica wodna)",
                    "Sprawdzić stan wlotu powietrza (w razie potrzebny oczyścic)",
                    "Sprawdzić elementy obudowy pod względem zabrudzen i korozji ( w razie potrzeby oczyścić i pomalować)",
                    "Kontrola działania regulatorów temperatury i regulatorów wydajności poiwietrza",
                    "Sprawdzić stan filtrów (w razie potrzebny oczyścić lub wymienić)",
                    "Zmierzyć pobór prądów w silniku",
                    "Sprawdzić elementy obudowy pod względem zabrudzen i korozji ( w razie potrzeby oczyścić i pomalować)"
                ]
            },
            {
                "name": "4.1 Agregaty wody lodowej (Chillery) v1.csv",
                "activities": [
                    "Sprawdzenie wszystkich sekcji urządzenia pod względem działania, wibracji i                zamocowania, elementy poluzowane dokręcić    ",
                    "Sprawdzenie poboru prądu poszczególnych odbiorników (wyniki w załączniku)",
                    "Sprawdzenie poprawności działania grzałki/grzałek",
                    "Sprawdzenie zabezpieczeń ciśnieniowych i zwłok czasowych   ",
                    "Sprawdzenie wartości ciśnień roboczych (wyniki w załączniku)",
                    "Sprawdzenie szczelności układu pod względem czynnika chłodniczego   ",
                    "Sprawdzenie zamocowań połączeń elektrycznych   ",
                    "Sprawdzenie stanu oleju (ciśnienie, poziom, zawartośc kwasu)",
                    "Sprawdzenie działania zaworu rozprężnego i elektromagnetycznego ",
                    "Sprawdzenie stanu urządzeń zabezpieczających pracę sprężarek",
                    "Sprawdzanie silnika (stan łożysk, kierunki obrotów, zanieczyszczenia i korozje)",
                    "Sprawdzenie rur i izolacji rur pod względem zewnętrznych uszkodzeń i nieszczelności",
                    "Sprawdzenie i czyszczenie filtrów mechanicznych w obiegu chłodniczym",
                    "Sprawdzenie pompy (stan dławicy, uszczelnienie wału, smarowanie łożysk)",
                    "Wymiana filtrów ",
                    "Sprawdzanie wentylatora (stan łożysk, praca łopat, zanieczyszczenia i korozje)",
                    "Sprawdzić temperaturę skraplania, schładzania, wyczyścić chłodnicę (skraplacz wodny/ wentylator)",
                    "Sprawdzenie zaworów bezpieczeństwa (dodatkowe zlecenie)"
                ]
            },
            {
                "name": "4.20 Sprężarki v1.csv",
                "activities": [
                    "Poziom oleju: [ok / niski / wysoki / wymaga uzupełnienia]",
                    "Filtry: [czyste / zabrudzone / wymagają wymiany]",
                    "Paski napędowe: [dobry stan / zużyte / wymagają wymiany]",
                    "Łożyska: [dobry stan / wykazują zużycie / wymagają wymiany]",
                    "Uszczelki: [dobry stan / wykazują zużycie / wymagają wymiany]",
                    "Ciśnienie robocze: [wartość ciśnienia, np. 8 bar]",
                    "Temperatura pracy: [wartość temperatury, np. 75°C]",
                    "Poziom hałasu: [np. w normie / powyżej normy]",
                    "Wibracje: [np. w normie / powyżej normy]"
                ]
            },
            {
                "name": "4.4 Centrala Wentylacyjna v1.csv",
                "activities": [
                    "Sprawdzenie czerpni powietrza, anemostatów, czystości i połączeń kanałów",
                    "Sprawdzenie szczelności i działania przepustnic",
                    "Sprawdzenie działania silników (poziom hałasu, łożyska, kierunek obrotu)",
                    "Sprawdzenie działania wentylatora (łożyska, naciąg pasków- jeśli występują)",
                    "Sprawdzenie stanu nagrzewnic, chłodnic i rekuperatorów",
                    "Mycie i dezynfekcja nagrzewnic, chłodnic i rekuperatorów",
                    "Sprawdzenie nastaw i zadziałania zabezpieczeń  (frost, presostat)",
                    "Kontrola działania zaworów trójdrogowych",
                    "Sprawdzenie układu odprowadzania skroplin",
                    "Sprawdzenie nastaw elementów peryferyjnych automatyki i sterowania",
                    "Sprawdzenie stanu szafy zasilającej i automatyki (dokręcenie mocowań, sprawdzenie zabezpieczeń)",
                    "Sprawdzenie stanów filtrów powietrza",
                    "Wymiana filtrów powietrza (zakup filtrów po stronie klienta)",
                    "Sprawdzenie stanu połączeń śrubywch",
                    "Kontrola poprawności działania kanałowej nagrzewnicy elektrycznej oraz pulsera"
                ]
            },
            {
                "name": "4.5 Rooftop v1.csv",
                "activities": [
                    "Sprawdzenie czerpni powietrza, anemostatów, czystości i połączeń kanałów",
                    "Sprawdzenie szczelności i działania przepustnic",
                    "Sprawdzenie działania silników (poziom hałasu, łożyska, kierunek obrotu)",
                    "Sprawdzenie działania wentylatora (łożyska, naciąg pasków- jeśli występują)",
                    "Sprawdzenie stanu nagrzewnic, chłodnic i rekuperatorów",
                    "Mycie i dezynfekcja nagrzewnic, chłodnic i rekuperatorów",
                    "Sprawdzenie nastaw i zadziałania zabezpieczeń  (frost, presostat)",
                    "Kontrola działania zaworów trójdrogowych",
                    "Sprawdzenie układu odprowadzania skroplin",
                    "Sprawdzenie nastaw elementów peryferyjnych automatyki i sterowania",
                    "Sprawdzenie stanu szafy zasilającej i automatyki (dokręcenie mocowań, sprawdzenie zabezpieczeń)",
                    "Sprawdzenie stanów filtrów powietrza",
                    "Wymiana filtrów powietrza (zakup filtrów po stronie klienta)",
                    "Sprawdzenie stanu połączeń śrubywch",
                    "Kontrola poprawności działania kanałowej nagrzewnicy elektrycznej oraz pulsera"
                ]
            },
            {
                "name": "4.9 Kotły v1.csv",
                "activities": [
                    "Sprawdzenie i regulacja automatyki, sygnalizacji i instalacji elektrycznej",
                    "Czyszczenie i płukanie kotła przed i po sezonie grzewczym",
                    "Sprzwdzenie i wymiana elektrod jonizacyjnych i zapłonowych",
                    "Sprzwdzenie i wymiana/czyszczenie filtrów paliwa",
                    "Sprawdzenie stanu palników gazowych/olejowych przed i po sezonie grzewczym",
                    "Sprzwdzenie uszczelnień armatury kotła",
                    "Sprawdzenie działania wentylacji nawiewnej i wywiewnej, czyszczenie kanałów",
                    "Kontrola działania pomp obiegowych w trybie automatycznym i ręcznym",
                    "Sprawdzenie działania termostatu kotła",
                    "Sprawdzenie działania zapłonu",
                    "Sprawdzenie działania urządzeń zabezpieczających (zawory bezp. STB, czujnik minimalnego poziomu wody w kotle)",
                    "Sprawdzenie stanu wody w kotle, ew. uzupełnić",
                    "Sprawdzenie czasu działania zabezpieczenia przed zanikiem ciągu kominowego",
                    "Sprawdzenie działania czujek termometrycznych i manometrycznych",
                    "Konserwacja kotła ( sprawdzenie stanu komory spalania, czyszczenie)",
                    "Sprawdzić działanie pomp obiegowych w trybie automatycznym i ręcznym",
                    "Odpowietrzenie układu, uzupełnienie czynnika"
                ]
            },
            {
                "name": "5.16 Zawory antyskażeniowe.csv",
                "activities": [
                    "Sprawdzenie wizualne poprawności instalacji zaworu (dostępności, wentylacji, zabezpieczenia przed zamarzaniem, itp.)",
                    "Sprawdzenie wizualne samego zaworu (wycieki, korozja powierzchni, itp.)",
                    "Sprawdzenie poprawności działania (szczelności zaworu) za pomocą kurka upustowego"
                ]
            },
            {
                "name": "5.1 Separator ropopochodny v1.csv",
                "activities": [
                    "Sprawdzić połączenia pod kątem szczelności.",
                    "Sprawdzić bezpieczeństwo zamknęcia pokrywy - Dokręcić śruby i sprawdzić uszczelki.",
                    "Zmierzyć grubość wartswy osadu - jeżeli to konieczne zlecić czyszczenie",
                    "Skontrolować zawory automatyczne",
                    "Skontrolować poprawnośc działania pompy (co 2 lata zmienić olej)",
                    "Oczyścić i w razie potrzeby wymienić sito w osadniku wstepnym.",
                    "Sprawdzenie pod kątem czystości i uszkodzeń mechanicznych, w tym pomieszczenie",
                    "Kontrola zamocowań, izolacji i dławików kabli zasilających i sygnalizacyjnych.",
                    "Skontrolować sygnalizacje elektryczną",
                    "Kontrola dziennika eksploatacji i dokonanie wpisu"
                ]
            },
            {
                "name": "5.5 Przepompownia ścieków v1.csv",
                "activities": [
                    "Sprawdzenie stanu urządzeń (oględziny wizualne)",
                    "Sprawdzenie stanu połączeń elektrycznych pod kątem ich zamocowania, w razie potrzeby poprawić",
                    "Test wyłącznika FI",
                    "Pomiar napięcia",
                    "Pomiar prądu",
                    "Pomiar temperatury",
                    "Sprawdzenie stanu uszczelnienia instalacji (obserwacja wycieków)",
                    "Sprawdzenie stanu uszczelnienia zbiornika (obserwacja wycieków)"
                ]
            },
            {
                "name": "5.7 Separator tłuszczu v1.csv",
                "activities": [
                    "Sprawdzić połączenia pod kątem szczelności.",
                    "Sprawdzić bezpieczeństwo zamknęcia pokrywy - Dokręcić śruby i sprawdzić uszczelki.",
                    "Zmierzyć grubość wartswy osadu - jeżeli to konieczne zlecić czyszczenie",
                    "Skontrolować zawory automatyczne",
                    "Skontrolować poprawnośc działania pompy (co 2 lata zmienić olej)",
                    "Oczyścić i w razie potrzeby wymienić sito w osadniku wstepnym.",
                    "Sprawdzenie pod kątem czystości i uszkodzeń mechanicznych, w tym pomieszczenie",
                    "Kontrola zamocowań, izolacji i dławików kabli zasilających i sygnalizacyjnych.",
                    "Skontrolować sygnalizacje elektryczną",
                    "Kontrola dziennika eksploatacji i dokonanie wpisu"
                ]
            },
            {
                "name": "6.1 Doki załadunkowe v1.csv",
                "activities": [
                    "Sprawdzenie oznakowania i instrukcji obsługi",
                    "Sprawdzenie wyłącznika głównego",
                    "Sprawdzenie wspornika serwisowego",
                    "Kontrola wizualna fartucha gumowego, odbojników, uszczelnień",
                    "Kontrola stanu skrzynki sterującej i przycisków",
                    "Kontrola wizualna stanu platformy (powierzchnia, zabezpieczenia boczne, zawiasy)",
                    "Kontrola wizualna jęzora wysuwnego (prowadnice, łożyska)",
                    "Kontrola układu hydraulicznego ramy wsporczej",
                    "Kontrola agregatu ramy (olej hydrauliczny, wycieki, stan połączeń)",
                    "Kontrola przewodów hydraulicznych",
                    "Kontrola siłowników",
                    "Sprawdzenie układu elektrycznego (uziemienie, przewody, osłony przewodów)",
                    "Kontrola i testy zabezpieczeń automatycznych"
                ]
            },
            {
                "name": "6.2 Bramy segmentowe i pomosty v1.csv",
                "activities": [
                    "Wizualne sprawdzenie poprawności i działania bramy",
                    "Sprawdzenie płaszcza bramy",
                    "Sprawdzenie stanu mechanizmów prowadzących bramy",
                    "Sprawdzenie stanu sprężyn wspomagających otwieranie bramy",
                    "Sprawdzenie linek stalowych oraz elementów łączących poszczególne panele",
                    "Sprawdzenie stanu siłownika oraz poprawności działania automatyki",
                    "Sprawdzenie poprawności funkcjonowania awaryjnego otwierania",
                    "Wykonywanie niezbędnych regulacji, smarowania"
                ]
            },
            {
                "name": "6.5 Drzwi przesuwne v1.csv",
                "activities": [
                    "Sprawdzenie barier świetlnych (fotokomórek)",
                    "Sprawdzenie przełącznika programowego",
                    "Kontrola stanu akumulatorów oraz awaryjnego otwarcia drzwi",
                    "Awaryjne otwarcie drzwi (mechaniczne)",
                    "Sprawdzenie działania wyłącznika automatycznego",
                    "Kontrola stanu pasków i kół napędu",
                    "Czyszczenie szyny jezdnej napędu"
                ]
            }
        ]

        for form_data in forms_data:
            form, created = Form.objects.get_or_create(name=form_data['name'])
            if created:
                for activity_name in form_data['activities']:
                    Activity.objects.create(form=form, name=activity_name)
                self.stdout.write(self.style.SUCCESS(f'Added form: {form.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Skipped (already exists): {form.name}'))
