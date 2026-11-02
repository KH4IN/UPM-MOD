# Decisiones tomadas sin Ricardo

Cada entrada indica la opción elegida, el motivo y las alternativas. Ricardo puede cambiar cualquiera.

| Fecha | Decisión | Motivo | Alternativas |
|---|---|---|---|
| 2026-11-02 | Partir de la etiqueta `v1.3.0` de Project Alice | Es la versión ya probada con UPM | Partir de `main`, con más mejoras pero sin probar |
| 2026-11-02 | Compilar con MSVC 2022, igual que el proyecto original | Evita diferencias de compilador | Clang |
| 2026-11-02 | La religión de la URSS, vacía en UPM, pasa a `orthodox` | Es la de su cultura principal; UPM no define ateísmo | Crear una religión atea |
| 2026-11-02 | `core = MAG` en Magdeburgo pasa a `add_core` | Es la lectura literal de la clave | `remove_core` |
| 2026-11-02 | No se cambian los 130 usos de `FROM` en eventos aleatorios | No hay país de origen, así que no se sabe qué quería el autor | Sustituirlos por `THIS` |
| 2026-11-02 | Andhra pasa de la etiqueta `AND` a `ADH` | Alice la confunde con la condición `AND`, y son pocos archivos | Dejarla sin arreglar; enseñar a Alice a distinguirlas |
| 2026-11-02 | Una condición sobre algo inexistente pasa a `always = no` | Siempre es falsa; Alice la tiraba y la condición de alrededor se cumplía siempre | Borrar el evento entero |
| 2026-11-02 | Los textos sin traducir se ven en inglés | Es el arreglo mínimo y ya no se pierde información | Traducir ya los 1.345 textos que faltan, previsto para la fase 6 |
| 2026-11-02 | Los precios sin tope no se corrigen en la fase 1 | Limitarlos cambia toda la economía, y eso lo rehace la fase 4a | Poner ya un tope provisional |
| 2026-11-02 | Las 6 garantías de `Guarantees.txt` siguen sin cargarse | Alice no entiende esa clave y su efecto es pequeño | Añadirla al motor |
| 2026-11-02 | Máximo de 96 opciones por evento | UPM usa 84 y la lista se puede desplazar | Partir el evento en varios |
| 2026-11-02 | La fecha pasa a `int32_t` con signo | Las restas de fechas siguen dando negativos, como antes | `uint32_t`, que haría que esas restas dieran números enormes |
| 2026-11-02 | Regimientos, barcos y construcciones de tierra pasan a 65.000 filas con identificadores de 32 bits | Con 32.000, el jugador dejaría de poder reclutar hacia 2115 | Quedarse en 32.000 y solo evitar el cierre; cambiar el generador de tablas |
| 2026-11-02 | La construcción de regimientos para en 60.000 y quedan 5.000 filas para rebeldes y movilización | Los regimientos siguen a la población, así que cualquier tope se llena antes de 2250 | Subir el tope sin freno, que solo retrasa el cierre |
| 2026-11-02 | Fábricas a 32.000 en vez de 65.000 | Bastan para el pico medido de 17.252 y mantienen sus identificadores de 16 bits | Pasarlas a 32 bits, con más memoria y más cambios |
| 2026-11-02 | Ejércitos a 16.000 y rutas comerciales a 160.000 | Duplican lo necesario; las rutas llegaron a 82.380 | Añadirles también un freno, que por ahora no hace falta |
| 2026-11-02 | La partida guardada pasa a la versión 46 | El cambio de identificadores altera el formato; las partidas antiguas no cargan | Convertir las partidas antiguas, que nadie necesita todavía |
| 2026-11-02 | Cerca del tope, el botón de reclutar solo se desactiva, sin explicarlo | Con la partida ya llena de regimientos, es un caso muy raro | Añadir un texto de ayuda, que se puede hacer en la fase 6 |
| 2026-11-02 | No se cambia `colonial_recruitment` ni el crecimiento mundial | Es un valor del juego base, y el 2 % anual se rehace en la fase 4a | Bajar el modificador ya, que apenas cambia el total |
| 2026-11-02 | La comparación con `v2game.exe` se aplaza a la fase 4a | No funciona sin ventana, tardaría horas y la fase 4a rehace la economía | Hacerla ahora, sobre una economía que va a cambiar |
| 2026-11-02 | `upm-alice` conserva `LLVM-C.dll` y `LLVM-C.lib` en su historial | Son del proyecto original, hacen falta para compilar, el repo es privado y quitarlos obliga a reescribir la historia y separarla de Alice | Reescribir la historia sin ellos |
| 2026-11-02 | Los archivos de texto del UPM siguen sin subirse a `UPM-MOD` | El repo es público y contienen texto derivado del juego; solo van las herramientas que los corrigen | Subirlos tras revisar qué partes se pueden publicar |
