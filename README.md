# Projekt Analizy Danych - ASI LAB2
## Opis Projektu
Projekt służy do analizy i przetwarzania danych użytkowników. Dane są generowane za pomocą skryptu `generator_danych.py`, a następnie czysczone i zamieszczane w Google Sheet.

## Funkcjonalności
1. Wygenerowanie danych:
   - Dane są generowane poprzez uruchomienie skryptu `generator_danych.py`, znajdującym się [tutaj](https://github.com/PJATK-ASI-2024/Lab2---Obr-bka-danych/blob/main/README.md). Skrypt actions uruchamiany jest automatycznie przy każdym pushu na main.
2. Przetwarzanie danych:
   - Rekordy w których ilość brakujących wartości przekracza połowę kolumn są usunięte
   - Wartości brakujące w kolumnach "Wiek" i "Średnie zarobki" są uzupełniane medianą.
   - Wartości brakujące w kolumnie "Cel Podróży" są uzupełniane najczęściej występującą wartością.
   - Ostatecznie, wszystkie pozostałe rekordy z brakującymi wartościami zostają usunięte
3. Uzupełnienie danych w Arkuszu Google:
   - Arkusz Google "ASI LAB2" jest całkowicie czyszczony, a następnie dane są uzupełniane. W celu obsługi błędów związanych z limitem odwołań do API, zapytania są pięciokrotnie powtarzane co 60 sekund w przypadku wyjątku.