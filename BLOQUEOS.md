# Bloqueos

Tareas que no salen tras varios intentos, con lo probado, los errores y lo que haría falta.

## Compilador (2026-11-02)

- **Qué bloquea:** compilar Alice y todo lo que dependa de ello.
- **Probado:** el script `portable-msvc`, bloqueado por el control de permisos por ser de un tercero, y Microsoft Build Tools con `winget`, que acabó con el código 1602 porque no se aceptó el aviso de administrador.
- **Hace falta:** que Ricardo acepte ese aviso de Windows en el PC.
