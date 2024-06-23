
# Raport z Modelu Przewidywania Wyników EURO 2024

## 1. Wyniki Testowe i Treningowe

- Dokładność modelu w zgadywaniu dokładnych wyników / zwycięzcy meczu:

  ![Dokładność](assets/accuracy.png)
- Przewidywania procentowych szans na dane miejsce drużyny w swojej grupie EURO 2024 na podstawie przeprowadzonych 1000 symulacji fazy grupowej:

  ![Wyniki](assets/results.png)

## 2. Uzasadnienie Wyboru Techniki/Modelu

- Model Poissona został wybrany, ponieważ ilość strzelonych bramek w meczu pokrywa się z dystrybucją Poissona.

  ![Rozkład Bramkowy](assets/goals-scored-plot.png)
  ![Rozkład Bramkowy Drużyny](assets/team-goals-scored-plot.png)
- Dodatkowo, wykorzystano model regresji liniowej, aby lepiej różnicować drużyny o różnym ELO, zwiększając znaczenie czynnika ELO w kontekście przewidywanego wyniku.

  ![Korelacja ELO i Bramki](assets/elo-goals-correlation.png)

## 3. Opis Danych Wejściowych

- Czyszczenie danych z brakującymi wartościami wyników.
- Wyliczane jest ELO dla uczestników każdego meczu od XIX wieku.
- Na bazie ilości strzelonych i straconych goli oraz różnicy ELO między przeciwnikami wyliczana jest relatywna siła ofensywna oraz defensywna uczestników każdego meczu w momencie jego rozgrywania (nowsze mecze mają większą wagę).
- Wartość ELO podczas przekazywania do modelu jest przeskalowana, aby nie dominowała nad siłą ofensywną i defensywną drużyn.
- Do modelu przekazywane są dane z pominięciem bardzo starych wyników, dla których wartość ELO oraz relatywnej siły nie jest jeszcze odpowiednio wyliczona.
- Model wykorzystuje relatywną siłę, wartość ELO oraz wyniki meczów.

## 4. Strategia Podziału Danych

- Dane podzielone na testowe i treningowe.
- Z każdego meczu wyciągane są dwie wartości treningowe: różnica ELO oraz własna siła ofensywna i siła defensywna przeciwnika dla każdego z uczestników meczu, na podstawie których model przewiduje ilość strzelonych goli (float).
- Testowanie modelu odbywa się przez porównanie rzeczywistego wyniku z przewidywanym na podstawie rozkładu Poissona najbardziej prawdopodobnym rezultatem meczu (przy wykorzystaniu współczynnika przewidywanych goli) oraz dodatkowego zróżnicowania go przy użyciu korelacji między różnicą ELO a różnicą strzelonych bramek w meczach.
- Wykorzystanie k-fold Cross-Validation dla lepszych efektów uczenia modelu.

## 5. Analiza Wyników

- Przewidywania pozycji drużyn w swojej grupie wydają się być stosunkowo realistyczne dla osoby zaznajomionej z piłką nożną.
- Przewidywania wyników zdecydowanie wymagają usprawnień; aktualne wyniki testowe nie są w pełni zadowalające, przewidywane dokładne rezultaty są również niedokładne, np. wynik 1-1 pojawia się zbyt często.

## 6. Kolejne Kroki

- Model docelowy do przewidywania wyników turnieju nie powinien być oparty na danych testowych i treningowych, a na całości dostarczonych danych.
