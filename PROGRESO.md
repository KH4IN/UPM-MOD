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

## 2026-11-02: fase 2, estabilidad y topes

- **Correcciones del UPM:** ninguna de las 1.401 etiquetas se queda sin partidos en 2001. 50 archivos perdían una ideología en 2000 y ahora conservan su último partido hasta 2300, con una regla repetible en `upm_alice_fix.py`. No quedan usos de nombres antiguos de tecnologías ni claves del juego base perdidas.
- **Regresión sin freno, de 1492 a 2250 (`r3`):** terminó sin cierres, con 628 minutos en total. Guardó y cargó en cada tramo.

  | Tramo | Minutos | Pico de RAM (MB) |
  |---|---:|---:|
  | 1492 a 1600 | 22,8 | 666 |
  | 1600 a 1700 | 28,7 | 680 |
  | 1700 a 1800 | 52,1 | 731 |
  | 1800 a 1900 | 79,1 | 768 |
  | 1900 a 2000 | 101,7 | 782 |
  | 2000 a 2100 | 118,5 | 789 |
  | 2100 a 2200 | 145,0 | 788 |
  | 2200 a 2250 | 80,0 | 789 |

- **Tablas desde 1492, sin freno:**

  | Tabla | Pico | Tope | % |
  |---|---:|---:|---:|
  | Regimientos | 65.000 | 65.000 | 100 |
  | Ejércitos | 14.786 | 16.000 | 92 |
  | Fábricas | 19.703 | 32.000 | 62 |
  | Rutas comerciales | 93.831 | 160.000 | 59 |
  | Pops | 118.409 | 300.000 | 40 |
  | Núcleos | 5.882 | 16.000 | 37 |
  | Barcos | 19.282 | 65.000 | 30 |

- **Regimientos:** la construcción frena en 60.000, pero rebeldes y movilización agotan la reserva. La tabla está llena casi sin pausa desde 2126, y las construcciones de tierra llegan a 0 en 2222. No hay cierre, pero casi nadie puede reclutar. En 2201 hay 28.463 regimientos rebeldes y 2.998 movilizados, cifras casi fijas durante 3 años. No se ha investigado por qué esos rebeldes no desaparecen.
- **Ejércitos:** el 92 % era peligroso, porque esa tabla no tiene protección si se llena. Pasa a 32.000 filas, sin cambiar el formato: la partida de 2200 carga y sigue hasta 2204 sin cierres.
- **Población sin freno:** 212 M en 1501, 5.450 M en 1833, 82.160 M en 2001, un máximo de 912.490 M en 2211 y 865.475 M en 2250.
- **Precios sin freno:** el índice medio pasa de 18 en 1493 a 3.934 en 1613, 54.704 en 1873, 123 en 2093 y 129 en 2250. Los bienes que aún no se fabrican se disparan: `electric_gear` llega a 4,8 millones en 1873.
- **Freno provisional (rama `upm/freno-provisional`):** a petición de la revisión de la orquestadora, se limita a un valor ajustable el crecimiento mundial y el precio. El crecimiento positivo se multiplica por `1 - población mundial / ALICE_WORLD_POPULATION_LIMIT`, con 10.000 M por defecto. El precio no pasa de `ALICE_PRICE_CAP_MULTIPLIER` veces el coste base, con 10 por defecto. Con 0 se apaga cada uno. El formato de escenario cambia, y `upm101.bin` lo sustituye. Medido con la regresión `r4`: ver más abajo.
- **Comparación de tiempos:** los 52 minutos de 2000 a 2100 salen de una partida que empezaba en 2000 con 1.349 M de personas. La de 1492 llegaba a 2000 con unos 80.000 M, y por eso tardó 118,5. No miden lo mismo.
- **`r4` en pausa:** se paró a las 22:44 del 2026-11-02, a petición de Ricardo para apagar el PC. Va por el 1 de enero de 1617, con el guardado `r4_pausa_1617.bin` en `Documents\Project Alice\saved games`. El guardado se cargó y jugó hasta 1618 sin cierres. Los CSV de `Victoria II + Alice dev` llegan completos a 1617 y siguen en 1618 al retomar.

  | Dato | `r3`, sin freno | `r4`, con freno |
  |---|---:|---:|
  | Tramo de 1492 a 1600 | 22,8 min | 24,6 min |
  | Pico de RAM en ese tramo | 666 MB | 624 MB |
  | Población en 1613 | 360 M | 332 M |
  | Índice de precios en 1613 | 3.934 | 64 |

  Solo cubre 125 de 758 años: aún no dice nada de 2100 ni de 2250. El tope de precios ya se nota; el de población todavía casi no actúa. Para retomar:

  ```powershell
  & "$env:USERPROFILE\Desktop\UPM-MOD\herramientas\pruebas\alice_tramos.ps1" -Esc 'upm101.bin' -Marca 'r4_pausa_1617.bin' -Anos '1700,1800,1900,2000,2100,2200,2250' -Prefijo 'r4' -Stats
  ```

  El tiempo de 1600 a 1700 habrá que sumarlo: 4,6 minutos antes de la pausa más lo que marque el primer tramo.
- **`r4` retomada:** el 2026-11-10 a las 20:54, desde `r4_pausa_1617.bin`.

## 2026-11-11: cierre de la fase 2, regresión con freno (`r4`)

`r4` terminó a las 04:38 sin cierres, de 1492 a 2250, guardando y cargando en cada tramo. Escenario `upm101.bin`, freno con los valores por defecto. Los CSV quedan en `Victoria II + Alice dev` como `*_stats_r4.csv`, y la tabla sale de un script de comparación de la sesión local.

| Tramo | `r3`, sin freno (min) | `r4`, con freno (min) | Pico de RAM `r4` (MB) |
|---|---:|---:|---:|
| 1492 a 1600 | 22,8 | 24,6 | 624 |
| 1600 a 1700 | 28,7 | 34,0 (4,6 + 29,4, por la pausa) | 688 |
| 1700 a 1800 | 52,1 | 50,4 | 656 |
| 1800 a 1900 | 79,1 | 72,3 | 752 |
| 1900 a 2000 | 101,7 | 86,8 | 773 |
| 2000 a 2100 | 118,5 | 90,4 | 758 |
| 2100 a 2200 | 145,0 | 89,8 | 764 |
| 2200 a 2250 | 80,0 | 44,7 | 683 |
| **Total** | **628** | **493** | **773** |

Población en cifras de archivo (las personas son 4 veces más) e índice medio de precios por mercado:

| Año | Población `r3` | Población `r4` | Índice `r3` | Índice `r4` |
|---|---:|---:|---:|---:|
| 1600 | 308 M | 292 M | 4.152 | 70 |
| 1700 | 1.020 M | 825 M | 433 | 19 |
| 1800 | 3.515 M | 2.309 M | 8 | 14 |
| 1900 | 13.536 M | 5.298 M | 1.567 | 18 |
| 2000 | 80.540 M | 8.023 M | 80 | 11 |
| 2100 | 482.217 M | 9.147 M | 134 | 11 |
| 2200 | 909.128 M | 9.466 M | 128 | 10 |
| 2250 | 865.475 M | 9.575 M | 129 | 10 |

- **Población:** se acerca al tope sin pasarlo: 9.575 M en 2250, unos 38.000 M de personas. Cumple el criterio de «decenas de miles de millones como mucho». Sigue siendo mucho más que la historia real (2000 tiene 8.023 M en archivos, unos 32.000 M de personas, frente a unos 6.100 M reales): eso es trabajo de la fase 4a, y el tope se puede bajar en `defines.lua`.
- **Precios:** el índice máximo es 85,5 (en 1570), frente a 72.899 sin freno. El precio más alto de la partida es 1.100 (`aeroplanes` en 1510, diez veces su coste). Los bienes que aún no se fabrican ya no se disparan: `electric_gear` no pasa de 160.
- **Tablas, picos desde 1492:** regimientos 40.762 de 65.000 (63 %; sin freno se llenaba desde 2126), fábricas 19.325 de 32.000 (60 %), rutas 87.085 de 160.000 (54 %), núcleos 34 %, barcos 33 %, ejércitos 7.236 de 32.000 (23 %), pops 62.110 de 300.000 (21 %), guerras 20 de 100.
- **Regimientos rebeldes:** pico de 3.063 (sin freno, 28.463 en 2201) y 1.217 en 2250. Ya no bloquean el reclutamiento, así que no se investiga más ahora.
- **Guerras:** la IA casi no hace guerras: nunca más de 20 a la vez y entre 1 y 8 en los años redondos. Por eso la partida larga en automático necesita guerras forzadas (siguiente punto).
- **Tramo de 2000 a 2100 desde el bookmark de 2000:** 47,6 minutos y 723 MB de pico, frente a 52 sin freno. Población de 1.347 M en 2001 a 4.557 M en 2100. Cumple el criterio. Los CSV quedan como `*_stats_f2000.csv`.
- **Criterio del freno cumplido:** población de 2250 en decenas de miles de millones de personas como mucho, precios acotados y menos de 52 minutos de 2000 a 2100. La casilla queda marcada en `PLAN.md`.
- **Fase 2 cerrada, salvo los topes de un byte**, que se suben cuando la expansión los necesite. Sin probar todavía: partida larga con guerras, multijugador entre dos PC y comparación con `v2game.exe`.
- **Siguiente paso:** la partida larga en automático con guerras forzadas (fase 1, punto pendiente) y después la fase 3, empezando por 1836.

## 2026-11-11: partida larga en automático con guerras forzadas (`g1`)

- **Opción `-wars N`** (rama `upm/guerras-prueba` de `upm-alice`): cada 1 de enero, N países de la IA en paz atacan a un vecino con un casus belli del juego. No declara si ya hay 60 guerras, porque la tabla admite 100. Prueba de 1836 a 1841 con 5 al año: declaró 5, 5, 5, 5 y 4, sin cierres. Hubo 31, 21, 22, 21 y 18 guerras a la vez, frente a 26, 12, 18, 12 y 7 sin la opción.
- **`g1`, de 1836 a 2026 con 5 guerras al año:** sin cierres hasta la pausa. Tramos de 25 años: 6,7, 7,8, 8,7, 10,3 y 12,3 minutos hasta 1961, con un pico de 689 MB.
- **En pausa** el 2026-11-11 a las 06:23, porque Ricardo apaga el PC. Va por el 1 de enero de 1966, con el guardado `g1_pausa_1966.bin` en `Documents\Project Alice\saved games`, que se cargó y jugó hasta 1967 sin cierres. Los CSV vivos de `Victoria II + Alice dev` son de `g1` y siguen al retomar. Para retomar:

  ```powershell
  & "$env:USERPROFILE\Desktop\UPM-MOD\herramientas\pruebas\alice_tramos.ps1" -Esc 'upm101.bin' -Marca 'g1_pausa_1966.bin' -Anos '1986,2011,2026' -Prefijo 'g1' -Stats -Guerras 5
  ```

- **Retomada y terminada** el 2026-11-11: llega al 1 de enero de 2026 sin cierres. Tramos desde 1966: 12,7, 17,5 y 11,7 minutos, con un pico de 685 MB. Se pidieron 5 guerras al año y salieron 309 en 190 años: 136 hasta 1886, 82 hasta 1936, 60 hasta 1986 y 31 hasta 2026. En 50 años no encontró ninguna pareja válida y solo en 16 llegó a las 5. No se ha mirado qué condición las descarta.
- **Referencia sin guerras forzadas (`g2`):** misma partida sin `-wars`, también sin cierres: 12,8, 16,8, 26,1 y 29,8 minutos por tramo, pico de 756 MB. Resumen con `herramientas/pruebas/alice_guerras.py`:

  | Dato, de 1837 a 2026 | `g2`, sin forzar | `g1`, con `-wars 5` |
  |---|---:|---:|
  | Guerras a la vez, media | 3,8 | 7,9 |
  | Países en guerra, media por año | 23,5 | 36,5 |
  | Participantes, media | 26,1 | 40,5 |
  | Batallas de tierra a la vez, media y pico | 1,6 y 15 | 2,9 y 25 |
  | Países en 2026 (234 al empezar) | 123 | 86 |
  | Países que desaparecen y aparecen | 126 y 15 | 168 y 20 |
  | Regimientos en 2026 | 17.580 | 12.518 |
  | Regimientos rebeldes, mayor valor en los años revisados | 302 | 219 |
  | Población en 2026, en archivos | 3.000 M | 3.460 M |

  Las tablas de guerra quedan lejos del tope: 31 guerras de 100, 113 participantes de 3.000 y 31 objetivos de 1.000.
- **Guardar y cargar:** `g1` cargó 8 guardados de tramo y el de la pausa; `g2`, 3.
- **Con ventana:** `g1_2026.bin` se abre desde la lista, se elige España, se entra en la partida, se abren las pestañas de diplomacia y de guerras, y el juego avanza del 1 al 12 de enero con una batalla. 6 capturas en `Victoria II + Alice dev\capturas_g1`; no van al repo.
- **Lo que no prueba:** todo lo jugó la IA. Nadie ha dirigido una guerra a mano, ni se ha probado el multijugador entre dos PC.
- **Realismo, para la fase 4a:** la partida sin forzar acaba en 2026 con 3.000 M en archivos, unos 12.000 M de personas, frente a unos 8.200 M reales. En la partida con guerras, España llega a 111 M en archivos y posee una gran parte de África. Son datos de partida para comparar, no algo que arreglar ahora.

## 2026-11-12: fase 3, 1836, primera tanda de historia

- **Causa de fondo:** el UPM da a cada país un único valor de religión, cultura principal y capital para sus 11 fechas. Ningún archivo de país cambia la religión por fecha. Alice sí lee esos datos dentro de un bloque con fecha, así que un cambio histórico se puede escribir como bloque nuevo al final del archivo, sin tocar las fechas anteriores.
- **Herramienta nueva:** `herramientas/upm_historia.py`, repetible, con el motivo de cada cambio. Solo vale para la copia de Alice. Cambia 54 archivos de `history/countries`:
  - **Religión de Estado, 13 países:** Prusia, Suecia, Dinamarca, Sajonia, Hesse, Mecklemburgo, Nassau, Holstein, Coburgo, Oldemburgo, Brunswick, Fráncfort y Suiza eran católicos en todas las fechas y pasan a protestantes desde la fecha de 1618. Dos comprobaciones hechas aquí: el juego base los da como protestantes en 1836, y la población del propio UPM es protestante en ellos desde su fecha de 1618 (la de 1579 repite la de 1492). Las fechas reales de la Reforma en cada uno son anteriores a 1579 y las cito de memoria, sin consultar fuentes. El bloque cambia también la cultura `zzz_religion_*`, con la que el UPM marca la religión para sus decisiones.
  - **Capital de Prusia:** Berlín desde la fecha de 1701, cuando pasa a ser suya en el UPM. Antes seguía en Königsberg hasta 2000.
  - **Cultura de relleno, 41 países:** 166 archivos tienen de cultura principal `dummy`, y 41 de esos países tienen provincias en alguna fecha: los 6 dominios japoneses, Mónaco, Liechtenstein, Singapur, Catar, Baréin, Perú del Sur, Río Grande del Sur, Entre Ríos y 20 países que solo existen en 2000, entre otros. Con `dummy` ningún habitante es de la cultura del país. Regla: la cultura mayoritaria de su población en su primera fecha con provincias, y lo mismo con la religión si era el relleno `shamanism`. Excepciones escritas en la herramienta: dominios japoneses con `mahayana`, como el shogunato, y Perú del Sur con `south_andean`, como Perú y Bolivia.
- **Comprobado:** el escenario `upm102.bin` se crea con los mismos avisos que `upm101.bin` (282.242 bytes); en la pantalla de elegir país de 1836, Prusia sale con religión protestante; de 1836 a 1846 sin ventana no hay cierres. Repetir la herramienta no cambia nada más. Copia previa de los archivos en `Victoria II - copias de seguridad\2026-11-12 UPM history countries (Alice dev)`. Los archivos están en `UPM-datos`, rama `upm/corregido-alice`.
- **Sin comprobar:** la capital de Prusia en pantalla, las otras 10 fechas de inicio una a una, y si la regla acierta en cada país de 2000. La regla sigue a la población del UPM, que no siempre es la histórica: Tannu Tuva queda como tártara y suní, y Timor como suní.
- **Vistos y sin tocar, para decidir:**
  - Unos 25 países africanos y de Oceanía tienen de religión `shamanism` y su población es `animist` al 100 %, como Oyo, Benín, Ashanti o Zimbabue. Parece una elección del UPM para todos los Estados animistas, no un relleno.
  - `civilized`: el UPM da por civilizados a 90 de 239 países en 1836; el juego base, a 66 de 131. Afganistán, Kokand, Jiva, Túnez, Trípoli, Jodhpur y Gwalior son civilizados en el UPM y no en el base. Afecta al equilibrio de 1836 y cambiarlo por fecha alteraría también 1900 a 2000.
  - 56 capitales ajenas en 1836. Alice no falla: elige sola la provincia propia más poblada. Mónaco y Liechtenstein tienen de capital la provincia 1.
  - Datos sueltos distintos del base: Países Bajos y Brasil con otro gobierno, Francia y Portugal con otro valor nacional, y 14 capitales en otra provincia, entre ellas la otomana (858 en lugar de 860).

## 2026-11-12: fase 3, 1836, equilibrio (a medias: pausa para apagar el PC)

- **Registros nuevos del motor con `-stats`:** `war_stats.csv` (fecha, quién añade el objetivo, contra quién, casus belli) y `decision_stats.csv` (fecha, país, decisión). En la rama `upm/guerras-prueba` de `upm-alice`.
- **Herramienta nueva:** `herramientas/upm_guerras.py` lista las guerras de `history/wars` abiertas en una fecha. En 1836 hay 3: otomanos contra Trípoli, México contra Texas y Brasil contra Río Grande del Sur.
- **Portugal desaparece en 1837:** en la partida sin guerras forzadas, España pasa de 69 a 104 provincias en un año. No es una guerra: el 14 de julio de 1837 la IA de España toma la decisión «Form Iberia» (`form_spain_portugal`, en `decisions/converterUnions.txt`). Su condición pregunta por provincias dentro de un país, Alice la descarta con un aviso y la decisión queda libre. Lo mismo le pasa a `form_poland_lithuania`.
- **Arreglo a medias, SIN subir:** una regla nueva en `upm_alice_fix.py` (cambio local sin confirmar) reescribe las 4 condiciones como «soy A y los núcleos de B son míos o de mi esfera». Quita los 4 avisos de carga y España ya no se anexiona Portugal, pero **no vale**: como Castilla no existe en 1836, la condición sobre sus núcleos se cumple sola y Portugal toma la decisión el 3 de enero de 1836 y pasa a ser `IBR`. Falta exigir que el otro país exista (o que tenga núcleos). La copia de pruebas del mod tiene ya la regla defectuosa aplicada; el original está en `Victoria II - copias de seguridad\2026-11-12 UPM converterUnions (Alice dev)`. El escenario `upm103.bin` lleva ese defecto: el bueno es `upm102.bin`.
- **Tecnología, hallazgo de fondo:** el UPM reparte las 150 tecnologías victorianas en seis tramos de 25, de 1492 a 1914. En 1836 todo país civilizado empieza con 100 (el juego base da entre 13 y 35), incluidas ametralladoras y motor de combustión, y Reino Unido tiene las mismas que el Imperio otomano. Por eso decisiones del juego base ligadas a tecnología salen enseguida: Haussmann, el Concilio Vaticano y el túnel de San Gotardo el 3 de enero de 1836, y el canal de Suez en 1838. Es diseño del mod: se trata en la fase 4.
- **Otros datos de la partida sin forzar:** Alemania, Italia y Japón no se unifican hasta 2002; España llega a 232 provincias; la mitad del salto de 1851 es colonización de África. En tres años, Perú añade 108 veces el mismo objetivo «Acquire core» contra Perú del Sur; sin investigar.
- **Núcleos dudosos en 1836:** Austria reclama 8 de las 13 provincias de Bélgica, y Francia 3 de Prusia.
- **Siguiente paso:** terminar el arreglo de las dos uniones, crear el escenario, comprobar que Portugal sigue siendo `POR` en 1846, subir los archivos a `UPM-datos` y seguir con el repaso de 1836.

## 2026-11-10: preparación de la fase 3, auditoría de las fechas

Hecha con `herramientas/upm_fecha.py` mientras corre `r4`. Solo lee archivos: no cambia el mod. La población de los archivos cuenta 1 de cada 4 personas, como en Victoria 2, así que las cifras en personas son 4 veces las de los archivos. Se comprueba con 2000: 1.342 M en archivos, 5.370 M de personas.

| Fecha | Países | Provincias con dueño | Personas | Capitales ajenas | Provincias pobladas sin dueño |
|---|---:|---:|---:|---:|---:|
| 1492 | 486 | 2.034 | 914 M | 113 | 681 |
| 1579 | 374 | 2.138 | 914 M | 96 | 577 |
| 1618 | 349 | 2.180 | 1.027 M | 95 | 535 |
| 1701 | 293 | 2.356 | 1.027 M | 72 | 359 |
| 1776 | 262 | 2.431 | 1.046 M | 57 | 284 |
| 1803 | 232 | 2.455 | 1.046 M | 55 | 260 |
| 1836 | 239 | 2.505 | 1.046 M | 56 | 210 |
| 1900 | 120 | 2.698 | 2.327 M | 22 | 17 |
| 1936 | 121 | 2.714 | 2.327 M | 14 | 1 |
| 1945 | 117 | 2.714 | 2.327 M | 16 | 1 |
| 2000 | 200 | 2.715 | 5.369 M | 8 | 0 |

- **La población se comparte entre fechas:** solo hay 5 juegos de población para 11 fechas. 1492 usa la misma que 1579, y 1900 la misma que 1936 y 1945.
- **1492 tiene el doble de gente de la cuenta:** 914 M, frente a los 450 a 500 M que suelen estimarse para 1500. Por países tampoco cuadra: Ming 336 M e Inglaterra 14,8 M. Las cifras históricas de referencia están sin contrastar con fuentes; es trabajo de la fase 3.
- **Capitales ajenas:** en 1492, 113 países tienen como capital una provincia que no es suya, por ejemplo la del Yuan del Norte, que es Pekín, de los Ming. No se ha mirado qué hace Alice con ellas.
- **Gobiernos de 1492:** Inglaterra, Lituania, Hungría, Polonia, Suecia y Aragón usan `prussian_constitutionalism`, que hace de monarquía con estamentos.
- **1836 frente al juego base:** 864 provincias con otro dueño. La mayoría son decisiones del UPM: China unida como `QIN`, Japón repartido entre el shogunato y 4 dominios, Egipto y Persia con otra etiqueta. Población del UPM frente al base: Estados Unidos +68 %, Brasil +35 %, Prusia +32 %. El base da a Estados Unidos 16 M de personas, cerca de los 15 M reales de 1836; el UPM le da 27 M.
- **Errores sueltos:** el dominio de Chōshū (`CHO`) tiene de cultura principal `dummy`. Las provincias 1396 y 1397 tienen dos archivos en el juego base, uno en `asia` y otro en `indonesia`.
