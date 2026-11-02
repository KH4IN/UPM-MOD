# Herramientas de prueba

Pruebas automáticas de nuestra versión de Alice sobre la copia `Victoria II + Alice dev` del escritorio. Solo tocan esa copia y las partidas de `Documentos\Project Alice`.

## Compilar y crear el escenario

| Herramienta | Qué hace |
|---|---|
| `alice_make.bat Alice launch_alice` | Compila los objetivos indicados del repo `upm-alice`. |
| `alice_build.ps1 -Salida upm.bin` | Crea el escenario del mod y sus marcadores de fecha. |
| `alice_err3.py <scenario_errors.txt>` | Agrupa los avisos por tipo. |

## Partidas sin ventana

| Herramienta | Qué hace |
|---|---|
| `alice_head.ps1` | Juega a baja prioridad y mide memoria y fecha. |
| `alice_ciclo.ps1` | Carga, juega, guarda, vuelve a cargar y sigue. |
| `alice_tramos.ps1` | Juega hasta varios años y guarda cada tramo para volver cerca de un cierre. Si el motor se cierra, muestra `crash_stack.txt`. |
| `alice_arranque.ps1` | Repite muchos arranques seguidos y cuenta los que fallan. |
| `savedate.py` | Lee la versión y la fecha de las partidas guardadas. |

## Datos de una partida

Con la opción `-stats`, el juego añade una tanda de datos cada 1 de enero a cuatro archivos de su carpeta. El cuarto, `province_stats.csv`, lista las 15 provincias más pobladas con su crecimiento y sus modificadores, y se lee a simple vista.

| Herramienta | Lee | Qué hace |
|---|---|---|
| `alice_stats.py` | `nation_stats.csv` | Resume población, PIB y países. |
| `alice_serie.py` | `nation_stats.csv` | Saca la evolución año a año. |
| `alice_precios.py` | `commodity_stats.csv` | Saca la evolución de los precios. |
| `alice_topes.py` | `limit_stats.csv` | Ordena las tablas del motor por lo llenas que están y calcula cuándo se llenarían. |

## Partidas con ventana

`ctl.ps1 -Proc Alice` enfoca el juego, pulsa, teclea, mueve la rueda y captura. Nunca envía ratón ni teclado si la ventana del juego no está delante.

## Traducciones

`loc_es.py <assets\localisation>` compara el inglés y el español de `alice.csv`: textos vacíos, ausentes y con variables distintas.
