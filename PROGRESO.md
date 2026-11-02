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
