# Decisiones tomadas sin Ricardo

Cada entrada indica la opción elegida, el motivo y las alternativas. Ricardo puede cambiar cualquiera.

| Fecha | Decisión | Motivo | Alternativas |
|---|---|---|---|
| 2026-11-02 | Partir de la etiqueta `v1.3.0` de Project Alice | Es la versión ya probada con UPM | Partir de `main`, con más mejoras pero sin probar |
| 2026-11-02 | Compilar con MSVC 2022, igual que el proyecto original | Evita diferencias de compilador | Clang |
| 2026-11-02 | La religión de la URSS, vacía en UPM, pasa a `orthodox` | Es la de su cultura principal; UPM no define ateísmo | Crear una religión atea |
| 2026-11-02 | `core = MAG` en Magdeburgo pasa a `add_core` | Es la lectura literal de la clave | `remove_core` |
| 2026-11-02 | No se cambian los 130 usos de `FROM` en eventos aleatorios | No hay país de origen, así que no se sabe qué quería el autor | Sustituirlos por `THIS` |
| 2026-11-02 | El país con etiqueta `AND` sigue sin arreglar | Alice la confunde con la condición `AND`; renombrarla toca muchos archivos | Renombrar la etiqueta |
| 2026-11-02 | Máximo de 96 opciones por evento | UPM usa 84 y la lista se puede desplazar | Partir el evento en varios |
| 2026-11-02 | La fecha pasa a `int32_t` con signo | Las restas de fechas siguen dando negativos, como antes | `uint32_t`, que haría que esas restas dieran números enormes |
