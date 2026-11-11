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
| 2026-11-02 | `upm-alice` conserva `LLVM-C.dll` y `LLVM-C.lib` en su historial | Son del proyecto original y hacen falta para compilar. La regla de no subir binarios se refiere a nuestros compilados y a archivos del juego. El repo es privado, y quitarlos obligaría a reescribir la historia | Reescribir la historia sin ellos |
| 2026-11-02 | Los archivos de texto del UPM no van a `UPM-MOD`, sino a `UPM-datos`, que es privado | El repo público solo lleva las herramientas que los corrigen, porque esos archivos contienen texto derivado del juego. Ricardo confirmó la subida | Subirlos al público tras revisar qué partes se pueden publicar |
| 2026-11-02 | `UPM-datos` no lleva gráficos, música, modelos ni fuentes del UPM, ni los 641 textos idénticos a los del juego | No siempre se puede comprobar de quién son los binarios, y los idénticos son archivos del juego. El paquete completo sigue en `UPM.zip` | Subir los binarios que se demuestre que son del mod |
| 2026-11-02 | Los últimos partidos de 50 países con una ideología que caducaba en 2000 siguen hasta 2300 | Esos países perdían esa ideología al pasar de 2000; alargar el último partido de cada una es lo mínimo | Escribir partidos nuevos para el siglo XXI, que corresponde a la fecha de 2026 |
| 2026-11-02 | Ejércitos a 32.000 filas | Llegaron a 14.786 de 16.000 desde 1492 y un `create_army` con la tabla llena cierra el juego. Mantiene los identificadores de 16 bits y el formato | Proteger cada `create_army`, con más cambios |
| 2026-11-02 | Freno de población: el crecimiento positivo baja en proporción a la población mundial, con límite de 10.000 M | Es lo más simple que funciona, se ajusta desde `defines.lua` y es provisional hasta la fase 4a. Frena algo también antes de 1900 | Límite por país; empezar a frenar solo a partir de cierta población |
| 2026-11-02 | Tope de precios en 10 veces el coste base | Ataja los precios de millones de los bienes que aún no se fabrican. Solo cubre bienes; salarios y servicios siguen sin tope | Tope por mercancía; tope también en salarios y servicios |
| 2026-11-11 | El freno se queda con sus valores por defecto | `r4` cumple el criterio: 9.575 M en archivos en 2250, índice máximo 85,5 y 47,6 minutos de 2000 a 2100. Ajustarlo a la historia real es trabajo de la fase 4a | Bajar ya el límite de población para acercarlo a la historia |
| 2026-11-11 | Opción `-wars N` de prueba: cada 1 de enero, N países de la IA en paz atacan a un vecino | La IA casi no declara guerras (nunca más de 20 a la vez desde 1492), y la partida larga pide guerras forzadas. Usa los casus belli del propio juego, no declara si la tabla de guerras pasa de 60 de 100 y solo actúa con la opción | Guerras por eventos de prueba en el mod; órdenes por consola, que sin ventana no hay |
