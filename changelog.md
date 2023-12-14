## Zmiany w Kodzie

### 1. Separacja Odpowiedzialności (SoC)
   - Kod został zorganizowany w klasy takie jak `Screen`, `Grid`, `Button`, `FileHandler`, `FileDialogHandler`, `Renderer` i `Game`. Każda klasa ma konkretną odpowiedzialność, co przyczynia się do lepszej organizacji i utrzymania kodu.

### 2. Wzorzec Model-View-Controller (MVC)
   - Klasy `Grid`, `Renderer` i `Game` wspólnie reprezentują wzorzec MVC. `Grid` to model reprezentujący stan gry, `Renderer` to widok odpowiedzialny za renderowanie grafiki, a `Game` działa jako kontroler obsługujący wejście użytkownika i logikę gry.

### 3. Wzorzec Komendy (Command)
   - Klasa `Button` reprezentuje wzorzec Komendy. Enkapsuluje żądanie (`click_action`) jako obiekt, umożliwiając parametryzację klientów różnymi żądaniami i kolejkowanie żądań.

### 4. Wzorzec Strategii (Strategy)
   - Klasy `FileHandler` i `FileDialogHandler` demonstrują wzorzec Strategii. Określają one rodzinę algorytmów (operacje zapisu i odczytu) i umożliwiają ich wymianę, pozwalając kodowi klienta (`GameFileHandler` i `GameTkinterFileDialogHandler`) działać niezależnie od używanych algorytmów.

### 5. Wzorzec Metody Szablonowej (Template Method)
   - Klasa `Game` używa metody szablonowej (`run`), aby zdefiniować szkielet algorytmu. Kroki algorytmu są zdefiniowane w metodach `handle_events`, `update` i `render`, ale niektóre z kroków mogą być przesłaniane przez podklasy (w tym przypadku `Renderer`).

### 6. Wzorzec Obserwatora (Observer)
   - Kod wykorzystuje podejście oparte na zdarzeniach do obsługi wejścia użytkownika. Zdarzenia są obserwowane przez pętlę zdarzeń, a różne komponenty (przyciski) rejestrują zainteresowanie tymi zdarzeniami.

### 7. Wzorzec Metody Fabrycznej (Factory Method)
   - Klasy `GameFileHandler` i `GameTkinterFileDialogHandler` pełnią rolę fabryk do tworzenia konkretnych obiektów obsługi plików (`PickleFileHandler` i `TkinterFileDialogHandler`).

### 8. Zasada Pojedynczej Odpowiedzialności (SRP)
   - Każda klasa ma jedną odpowiedzialność, co sprawia, że kod jest bardziej modularny i łatwiejszy do utrzymania.

### 9. Wstrzykiwanie Zależności (Dependency Injection)
   - Zależności, takie jak obsługa plików i obsługa okna dialogowego, są wstrzykiwane do odpowiednich klas (`Game`, `GameFileHandler` i `GameTkinterFileDialogHandler`). To promuje elastyczność i testowalność.

### 10. Enkapsulacja
   - Właściwości i metody klasy są odpowiednio enkapsulowane, a modyfikatory dostępu są używane do kontrolowania widoczności składników, co jest zgodne z zasadami enkapsulacji.
