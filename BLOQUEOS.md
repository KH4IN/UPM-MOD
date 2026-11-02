# Bloqueos

Tareas que no salen tras varios intentos, con lo probado, los errores y lo que haría falta.

Ahora mismo no hay ninguna tarea bloqueada.

## Resueltos

### Compilador (2026-11-02)

- **Qué bloqueaba:** compilar Alice y todo lo que dependa de ello.
- **Probado:** el script `portable-msvc`, bloqueado por el control de permisos por ser de un tercero, y Microsoft Build Tools con `winget`, que acabó con el código 1602 porque no se aceptó el aviso de administrador.
- **Solución:** Ricardo instaló Build Tools 17.14 en el PC.
