# Progreso

Diario del bucle: fecha, tarea, qué se hizo, resultado de las pruebas y siguiente paso.

## 2026-11-02: preparación

- **Tarea:** preparar repos y compilador.
- **Hecho:** clonados `UPM-MOD` y Project Alice `v1.3.0` en el escritorio.
- **Intento 1 de compilador:** script `portable-msvc` de un tercero, bloqueado por el control de permisos. No se ejecutó.
- **Intento 2 de compilador:** Microsoft Build Tools oficial con `winget`. Se descargó y su hash era correcto, pero terminó con el código 1602: nadie aceptó el aviso de administrador de Windows.
- **Cambio de fechas (sin compilar):** rama `upm/fecha-32-bits` de `upm-alice`. `sys::date` pasa a `int32_t`, con 7 lecturas de 16 bits corregidas en `fif_triggers.cpp`, la de `current-date` en `fif_common.hpp`, relleno explícito en las estructuras afectadas y versión de partida guardada 45.
- **Resultado:** nada compilado ni probado. Bloqueado por el compilador, ver `BLOQUEOS.md`.
- **Siguiente paso:** instalar Build Tools con el aviso aceptado, compilar y probar 1492 más allá de 1671.

## 2026-11-02: fase 1, motor

- **Compilador:** Ricardo instaló Build Tools 17.14. Nuestra versión de Alice compila en unos 5 minutos.
- **Fechas:** hizo falta un relleno más en `diplomatic_messages.hpp`, porque `full_wg` ocupa 12 bytes y no 10. Las fechas de inicio ya salen bien, de 1492 a 2000.
- **Opciones de evento:** los «76 eventos» son un solo evento, el 250999, con 84 opciones para elegir religión. El límite del motor sube de 8 a 96.
- **Erratas de UPM:** `herramientas/upm_alice_fix.py` aplica 677 cambios en la copia de pruebas. Los errores al cargar bajan de 2.842 a 2.073. De ellos, 1.626 son quitar reclamaciones inexistentes.
- **Pruebas sin ventana:** nuevas opciones `-load` y `-until`. Ciclo 2000 → 2003 → guardar → cargar → 2005 sin errores.
- **Campaña desde 1492:** en 75 minutos llegó a 1698, 27 años más allá del antiguo final de 1671, sin cierres. Memoria entre 591 y 658 MB. La cerró el límite de tiempo de la prueba, no un fallo.
- **Partida desde 2000:** se cerró con código 3 hacia 2116, a los 80 minutos, coincidiendo con la creación de un escenario. Causa aún desconocida. El motor ya escribe `crash_stack.txt` al cerrarse de golpe, y la prueba se repite por tramos guardados.
- **Comprobación fallida:** una prueba de guardar y cargar arrancó en 1492 porque `Alice.exe` era anterior a `-load`. Se descartó y hoy ambos ejecutables son la versión nueva.
- **Avisos de UPM:** de 2.073 a 1.798. Reglas nuevas en `upm_alice_fix.py` y `upm_alice_avisos.py`:
  - 49 países con la alfabetización escrita con coma, que se leía como 0.
  - 88 condiciones sobre culturas, países y regiones inexistentes, que Alice tiraba y dejaban la condición siempre cierta. Pasan a `always = no`, salvo tres grupos culturales con un país por error (EE. UU., Francia y Alemania), que pasan a su grupo real.
  - 10 provincias con fechas de solo un año.
  - Andhra pasa de `AND` a `ADH`, porque su etiqueta chocaba con la condición `AND` y su nombre con la palabra «and».
- **Evento de 84 opciones:** probado con ventana. La lista se desplaza hasta el final y la opción 82 cambió la religión del país a `iberian_pagan`, leída por consola.
- **Iconos de la lista:** reproducido. En `es-ES/alice.csv` hay 753 textos vacíos que pisaban el inglés cargado antes, entre ellos `ol_unit_standing_text`. El cargador ya no pisa un texto con una entrada vacía. Comprobado en español con la lista de unidades.
- **Partida por tramos:** pasó por 2116 sin cierre, así que el código 3 no se repitió y su causa sigue sin conocerse. Al recargar un tramo apareció otro fallo.
- **Cierres aleatorios de LLVM:** 2 de 16 arranques murieron con `IMAGE_REL_AMD64_ADDR32NB relocation requires an ordered section layout`, más un `0xC0000005` dentro del código generado. Dependía de dónde cayera la memoria en cada arranque, así que podía tocarle a cualquier jugador. Esas relocalizaciones vienen de las tablas de desenrollado, que aquí no hacen falta: las funciones generadas pasan a `nounwind`. Con el arreglo, 48 de 48 arranques correctos y ningún fallo en el registro de Windows.
- **Equilibrio:** dos campañas de 1836 a 1936 sin cierres, 42 minutos cada una, y con forma muy parecida. Población mundial de 257 a 828 M, multiplicada por 3,2; en la realidad fue menos del doble. El PIB nominal se multiplica por cerca de 1.000 entre 1837 y 1917 y luego se hunde; el de EE. UU. se multiplica por 39 en cinco años. Causa: los precios no tienen tope por diseño de Alice. Acero y cemento pasan de una media de 17 y 34 a más de 2.000, con máximos de millones en un mercado. No se parchea: es trabajo de la fase 4a.
- **Multijugador:** anfitrión y cliente en este PC con la nueva opción `-localonly`, que no abre puertos en el router y solo escucha en 127.0.0.1. Lobby, carga, inicio y avance en las dos ventanas hasta el 6 de septiembre de 1492, sin avisos de desincronización en 8 comprobaciones mensuales. No es una partida larga ni entre dos PC: eso queda para la fase 8.
- **Cierre de 2115:** el código 3 se repitió dos veces el 15 de junio de 2115. La pila apunta a `military::create_new_regiment`, llamada desde `economy::resolve_constructions`. La tabla tenía 32.000 filas y crear una fila de más cierra el juego. Los regimientos siguen a la población: de 26.527 en 2100 a 31.825 en 2115. Las rutas comerciales habrían sido las siguientes, hacia 2127.
- **Arreglo:** regimientos, barcos y construcciones de tierra pasan a 65.000 filas. Eso obliga a usar identificadores de 32 bits y cambia el formato de partida a la versión 46, así que las partidas y escenarios anteriores dejan de valer. Ejércitos 16.000, fábricas 32.000 y rutas 160.000. Como cualquier tope acaba llenándose antes de 2250, la construcción para en 60.000 y las últimas 5.000 filas quedan para rebeldes y movilización. Compilado con el escenario nuevo `upm99.bin`.
- **Regresión de 2000 a 2250:** terminó sin cierres, en 173 minutos y con un pico de 770 MB. Seis tramos, guardando y cargando en cada uno. En la versión anterior habría fallado en 2115.
- **El freno actúa:** regimientos más construcciones llegaron a 60.000 en 2187 y se quedaron ahí 60 años, con un máximo de 60.693. Las tablas nunca se llenaron:

  | Tabla | Pico | Tope | % |
  |---|---:|---:|---:|
  | Regimientos | 52.529 | 65.000 | 81 |
  | Fábricas | 17.252 | 32.000 | 54 |
  | Rutas comerciales | 82.380 | 160.000 | 51 |
  | Guerras | 45 | 100 | 45 |
  | Núcleos | 6.616 | 16.000 | 41 |
  | Ejércitos | 6.248 | 16.000 | 39 |
  | Barcos | 20.753 | 65.000 | 32 |
  | Pops | 66.279 | 300.000 | 22 |

  Son datos de una partida desde 2000. Desde 1492, con muchos más países, no se han medido.
- **Población:** de 1.349 M en 2001 a 252.748 M en 2250, un 2 % anual casi constante. El juego lo aguanta, pero es absurdo: pertenece a la fase 4a.
- **Bombay:** India pasa de 1.069 M en 2081 a 11.192 M en 2121, y luego 7 provincias concentran unos 21.000 M. Con el nuevo `province_stats.csv` se vio la causa: el modificador `colonial_recruitment` del evento 14680, que da +1 % de crecimiento **mensual** y +100 % de atracción de inmigrantes durante 20 años. Es un valor del juego base, pensado para colonias pequeñas. Solo explica una parte del total, así que no se cambia ahora.
- **Precios:** el índice medio baja de 65 en 2021 a 14 en 2101 y sube a 95 en 2250. No hay valores no numéricos, y ningún país tiene PIB negativo en los años revisados, uno de cada 20.
- **Formato 46 en multijugador:** anfitrión y cliente en este PC, seis meses de 1492 sin desincronización. No es una partida larga ni entre dos PC.
- **Formato 46 con ventana:** la partida de 2250 se abre desde la lista, se elige China, se juega y sale la pantalla de fin de partida. Unos 3,2 GB de RAM con ventana.
- **Sin probar:** una partida larga jugada a mano con guerras, el multijugador entre dos PC y la comparación con `v2game.exe`.
- **Siguiente paso:** fase 2, correcciones del UPM. Al terminarla, partida completa de 1492 a 2250 como regresión y para medir las tablas.
