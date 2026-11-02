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
| `savedate.py` | Lee la versión y la fecha de las partidas guardadas. |

## Partidas con ventana

`ctl.ps1 -Proc Alice` enfoca el juego, pulsa, teclea, mueve la rueda y captura. Nunca envía ratón ni teclado si la ventana del juego no está delante.

## Traducciones

`loc_es.py <assets\localisation>` compara el inglés y el español de `alice.csv`: textos vacíos, ausentes y con variables distintas.
