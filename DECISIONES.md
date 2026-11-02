# Decisiones tomadas sin Ricardo

Cada entrada indica la opción elegida, el motivo y las alternativas. Ricardo puede cambiar cualquiera.

| Fecha | Decisión | Motivo | Alternativas |
|---|---|---|---|
| 2026-11-02 | Partir de la etiqueta `v1.3.0` de Project Alice | Es la versión ya probada con UPM | Partir de `main`, con más mejoras pero sin probar |
| 2026-11-02 | Compilar con MSVC 2022, igual que el proyecto original | Evita diferencias de compilador | Clang |
| 2026-11-02 | La fecha pasa a `int32_t` con signo | Las restas de fechas siguen dando negativos, como antes | `uint32_t`, que haría que esas restas dieran números enormes |
