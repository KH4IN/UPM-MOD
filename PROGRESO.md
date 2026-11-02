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
- **Pendiente de resultado:** partida desde 2000 hasta 2250.
