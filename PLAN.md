# Plan de la expansión del UPM (nombre provisional)

Expansión del **Universal Project Mod (UPM)** para Victoria 2, con permiso de su autor (su última versión es del 24-10-2025). Funciona sobre **Project Alice**, el motor abierto de 64 bits que lee los archivos de Victoria 2, y sobre nuestra propia versión de ese motor.

*Versión 3 del plan: se pasa a Alice, se añade el espacio y la economía pasa a ser muy realista.*

## 1. Visión

Victoria 2 actualizado: **fiel a la historia real hasta hoy**, con un **futuro ampliado y abierto** que llega al **sistema solar**. Debe verse bien, sentirse nuevo y no colgarse en el late game.

## 2. Decisiones tomadas

| Tema | Decisión |
|---|---|
| Motor | **Project Alice** (64 bits, código abierto GPL-3.0), con nuestra versión propia para subir topes y añadir funciones. `v2game.exe` queda solo como referencia. |
| Identidad | Historia real de 1836 a 2026 y futuro ampliado con libertad. Realista pero jugable: la historia no se fuerza. |
| Público | Se desarrolla en abierto (repo público). La versión jugable se comparte cuando esté madura. Español primero y luego inglés. |
| Modo | Un jugador primero; después, multijugador al mismo nivel. |
| Sistemas | Los cuatro: economía, política, diplomacia y guerra, tecnología y eventos. |
| Economía | **Muy realista**, reprogramada en nuestra versión de Alice: dinero y finanzas, mercados y comercio, trabajo y sectores, energía y recursos. |
| Moneda | **Una sola moneda mundial, española**. Se llama **real de a ocho** (o dólar español) hasta 1868 y **peseta** desde 1868. Solo cambia el nombre: por debajo es la misma moneda. No hay divisas por país. |
| Datos de partida | **Datos históricos reales** (PIB, población, producción) en 1492, 1836 y 2026. |
| Manejo de la economía | **Compleja pero explicada**: toda la profundidad, con ventanas que expliquen por qué pasa cada cosa. |
| Realismo frente a velocidad | **Primero el realismo**: se acepta que el late game vaya algo más lento. |
| Temas | Siglo XX, mundo actual, carrera espacial y futuro, sociedad y cultura. |
| Interfaz | Claridad, rediseño visual y **ventanas nuevas de verdad**, que con Alice sí se pueden programar. |
| Vista del mapa | Cada jugador elige entre **plano** (como el Victoria 2 original) o **globo** (como Alice). |
| Fondo | **Estrellado**, con el Sol y los planetas visibles al estilo de un sistema solar. |
| Espacio | Primero **bases y recursos**, luego **colonias con población**. Otros sistemas estelares, más adelante. |
| Carrera espacial | **Programa espacial completo**: presupuesto, investigación, cohetes y misiones que pueden fallar. |
| Cuándo llega el espacio | **Configurable en cada partida**: "histórico" (cohetes en los 40–50, la Luna hacia 1969, colonias desde 2030–2050) o "por tecnología" (sin fechas). |
| Fechas prioritarias | **1836**, **1492** y **actualidad (2026)**. |
| 1492 | **Historia real de 1492**: el mundo tal como era (Reyes Católicos y Granada, imperios precolombinos, otomanos, Ming…), con datos históricos. La era de los descubrimientos, jugable. |
| Gráficos | Los genera Claude por código o IA. |
| Equipo | El dueño diseña y prueba; Claude escribe y prueba. |
| Código | El mod va en **`KH4IN/UPM-MOD`** (público). Nuestra versión de Alice va en **`KH4IN/upm-alice`** (privado), que conserva su licencia GPL-3.0. Las licencias de cada parte están en `LICENCIAS.md`. |
| Nombre | Se decide más adelante. |

## 3. Lo que permite Alice

- **Sin techo de 4 GB.** Ahora el límite práctico es la **velocidad**: cuánto tarda en calcularse cada día de partida.
- **Topes ampliables.** Están en `src/gamestate/dcon_generated.txt` (líneas `size{ N }`).
  - **Fáciles** (basta con cambiar el número): países (2.000), partidos (15.000), provincias (17.000), tecnologías (400), inventos (900), culturas (2.800), decisiones, eventos.
  - **Con más programación:** mercancías (126), religiones (126), ideologías (125), tipos de gobierno (100), tipos de rebelde (127), grupos culturales (255) y tipos de pop (20). Su identificador probablemente ocupa un solo byte.
- **Vistas de mapa.** Ya trae 4: plano, globo ortográfico, globo en perspectiva y estereográfico.
- **Fondo.** Hoy es un color liso detrás del globo. Cambiarlo por estrellas es una modificación pequeña del código de dibujo.
- **Reglas de partida (`gamerule`).** Sirven para hacer configurable lo del espacio.
- **Licencia GPL.** Si compartís vuestra versión compilada, aunque sea con amigos, hay que darles también el código. No hace falta publicarlo para todo el mundo.

## 4. Fases

Cada fase deja el mod jugable, y no se empieza la siguiente sin pasar sus pruebas.

### Fase 0: preparación
- [x] Repo del mod creado: `KH4IN/UPM-MOD`, público.
- [ ] Subir a `UPM-MOD` los archivos de texto del UPM, con los créditos de su autor. Ni el juego base ni ningún binario.
- [x] Repo de nuestra versión de Alice creado: `KH4IN/upm-alice`, privado y con licencia GPL-3.0.
- [ ] Subir a `upm-alice` el código de Project Alice (fork o espejo del original) con sus cambios. Solo código fuente, sin binarios.
- [x] Hacer nuestra versión de Alice (fork) y dejar listo su compilado en el PC de pruebas.
- [x] Traer las herramientas de prueba de la sesión local: arranque automático, partida a máxima velocidad, capturas y medición. Están en `herramientas/pruebas/`.
- [ ] Flujo de trabajo: rama → cambio → compilado y prueba automática en el PC → fusionar.

### Fase 1: el UPM en Alice
- [x] Ejecutar el UPM corregido en Alice 1.3.0, en una tercera copia (`Victoria II + Alice`). Arranca desde 1492 y desde 2000, en español y con su lanzador.
- [x] Primera medición: en Alice avanzó **11 años en 3 minutos** con 0,9 GB de RAM. En `v2game.exe` fueron 4 años en 12 minutos con 2,3 GB. No es una comparación exacta.
- [x] **Quitar el tope de fechas.** Alice guardaba la fecha en un número de 16 bits: como mucho 65.535 días, unos 179 años, y la campaña de 1492 terminaba en 1671. Ahora son 32 bits (rama `upm/fecha-32-bits`). Probado sin ventana desde 1492 hasta 1698, con guardar y cargar. Falta probarlo en multijugador.
- [x] Adaptar **76 eventos** que tienen más opciones de las que admite Alice y **93 condiciones** que usan una palabra que no reconoce. Los 76 avisos eran un solo evento de 84 opciones: el límite sube a 96 y se comprobó en partida eligiendo la opción 82.
- [x] Revisar los **2.842 avisos** al cargar el UPM. Quedan 1.797: 1.626 quitan reclamaciones que no existen, 130 usan `FROM` donde no hay país de origen y 41 son casos sueltos, entre ellos 6 garantías y 3 relaciones de vasallaje que no se cargan. Las reglas están en `herramientas/`.
- [x] Iconos de la lista de ejércitos que desaparecen al cambiar el idioma con la partida abierta. No era el cambio de idioma: la traducción española de Alice tenía 753 textos vacíos que borraban el inglés.
- [x] Probar guardar y cargar, el multijugador y más de 15 años seguidos desde 2000. Partida automática de 2000 a 2250 sin cierres, guardando y cargando en cada tramo. Multijugador en este PC, seis meses sin desincronización. La partida de 2250 se abre y se termina con ventana.
- [ ] Probar una partida larga **en automático** (la hace la sesión local, no Ricardo): un país controlado por la IA, con guerras forzadas, guardando y cargando partidas y con capturas.
- [ ] Comprobar el equilibrio, porque la economía de Alice es distinta. Medido en Alice de 1836 a 1936: la población crece de forma razonable, pero los precios no tienen tope y el PIB da saltos imposibles. La comparación con `v2game.exe` y el arreglo de fondo pasan a la fase 4a.

### Fase 2: estabilidad y topes
- [ ] Terminar las correcciones del UPM: partidos que caducan en 2000, prefijos `n_` y claves perdidas.
- [ ] Subir los topes que necesite la expansión. Primero los fáciles; los de un byte, cuando haga falta. Hechos: regimientos, barcos, ejércitos, fábricas, rutas y construcciones de tierra. Los de un byte siguen sin tocar.
- [ ] Pruebas de estrés hasta 2250 con mucha población. Hecha desde 2000, con 252.000 M de personas al final. Falta desde 1492.

### Fase 3: fechas prioritarias
- [ ] **1836**: repaso de la historia y del equilibrio.
- [ ] **1492**: rehacer la fecha con la historia real de 1492 (países, fronteras, gobernantes, religiones, culturas, población y economía de la época), con fuentes. Partir de lo que tiene el UPM.
- [ ] **2026**: fronteras, gobiernos, partidos, economía, ejércitos y alianzas actuales.

### Fase 4: sistemas

#### 4a. Economía realista (la pieza más grande de esta fase)
Se reprograma la economía en el código C++ de nuestra versión de Alice, por partes y comprobando cada una:

1. **Datos reales de partida.** PIB, población y producción de cada país en 1492, 1836 y 2026, a partir de fuentes históricas (Proyecto Maddison, series de población y de producción). Cada dato lleva su fuente.
2. **Trabajo y sectores.** Agricultura, industria y servicios; salarios, paro, emigración por trabajo, sindicatos y automatización.
3. **Mercados y comercio.** Mercados regionales con costes de transporte en lugar de un único mercado mundial, aranceles, tratados comerciales y bloqueos.
4. **Dinero y finanzas.** **Una sola moneda para todo el mundo, de origen español:** se muestra como **real de a ocho** desde 1492 y como **peseta** a partir de 1868, el año en que se creó. Solo cambia el nombre en la interfaz (texto y símbolo según la fecha); los cálculos son siempre los mismos. Sobre ella: inflación, bancos centrales, tipos de interés, deuda pública, bolsa y crisis financieras que salen de la propia simulación, no solo de eventos.
5. **Energía y recursos.** Carbón, petróleo, gas, nuclear y renovables, yacimientos que se agotan y crisis energéticas. Bienes modernos como electrónica, chips y servicios. Hará falta subir el tope de mercancías (126).
6. **Herramientas económicas para el jugador:**
   - **Sanciones y presión:** embargos a un país o a un bien concreto, sanciones, congelación de activos y bloqueos comerciales.
   - **Comercio:** aranceles y cuotas por país y por bien, uniones aduaneras y tratados de libre comercio.
   - **Industria:** subvenciones, nacionalizaciones y privatizaciones, y controles de precios.
   - **Ayuda entre países:** préstamos y ayuda exterior. Con una moneda única no hay devaluación ni controles de capital.

   La IA también las usará, y los demás países reaccionarán a ellas.
7. **Explicación al jugador.** Ventanas y ayudas que desglosan cada cifra: por qué sube la inflación, de dónde sale el paro o qué encarece un bien.

**Prueba de realismo:** una partida automática de 1836 a 2026 sin jugador, cuya evolución del PIB y de la población se compara con la historia real. Los parámetros se ajustan hasta que la curva se parezca.

#### 4b. Resto de sistemas
- **Política:** ideologías modernas, reformas actuales, elecciones y movimientos sociales. Revisar el tope de ideologías.
- **Diplomacia y guerra:** bloques tipo OTAN, UE, ONU o Pacto de Varsovia, Guerra Fría, armas nucleares y ejércitos modernos.
- **Tecnología:** árbol actualizado hasta hoy y más allá, enlazado con los eventos y con el programa espacial.

### Fase 5: contenido temático
- **Siglo XX:** guerras mundiales, Guerra Fría, descolonización, caída de la URSS y UE.
- **Mundo actual:** globalización, internet, crisis de 2008, pandemias, clima, energía y China.
- **Sociedad y cultura:** derechos civiles, migraciones, religión, medios y nivel de vida.

### Fase 6: interfaz y aspecto visual
1. **Claridad:** que nada salga cortado, ayudas útiles y fuentes legibles.
2. **Selector de vista** plano / globo, accesible desde las opciones.
3. **Fondo estrellado** detrás del globo, con el Sol y los planetas de decoración.
4. **Rediseño visual** con un estilo moderno y coherente.
5. **Ventanas nuevas** programadas en Alice: "Naciones Unidas", "Resumen del país" y la ventana del programa espacial.

### Fase 7: espacio
- **7a. Programa espacial completo:** presupuesto, ramas de investigación, cohetes, misiones con probabilidad de fallo y hitos con prestigio (primer satélite, primer humano en órbita, la Luna…). Regla de partida: modo "histórico" o "por tecnología".
- **7b. Prueba técnica de varios cuerpos:** que el motor tenga Tierra, Luna y Marte, cada uno con su mapa y sus provincias, y una **vista de sistema solar** para pasar de uno a otro. Es el cambio más grande del motor; antes, una prueba de concepto.
- **7c. Bases:** bases científicas y mineras en la Luna y Marte que dan recursos y prestigio.
- **7d. Colonias con población:** ciudades en otros cuerpos, con economía, cultura, política e independencia. En multijugador, cada amigo podría llevar un planeta.
- **7e. Otros sistemas estelares:** a decidir más adelante.

### Fase 8: multijugador
- La misma versión de Alice y del mod para todos, pruebas de desincronización y partidas largas con varias personas.

### Fase 9: publicación
- Textos en inglés, créditos al autor del UPM y a Project Alice, publicación del código de nuestra versión de Alice (GPL) y guía de instalación.

## 5. Cómo trabajamos

- **Diseño:** el dueño decide y valida en partida.
- **Sesión en la nube:** scripts, textos y gráficos en `UPM-MOD`, y código C++ en `upm-alice`.
- **Sesión local (PC con Windows):** compila Alice, ejecuta el juego, lanza las pruebas automáticas y da el visto bueno.
- **Reglas:** siempre sobre copias, con copia de seguridad. Nunca se mezclan el juego base, el UPM original y la expansión.

## 6. Riesgos

| Riesgo | Cómo lo controlamos |
|---|---|
| El UPM no funciona bien en Alice | La fase 1 lo comprueba antes de invertir más |
| Velocidad del late game con mucho contenido | Medir en cada fase y optimizar el motor |
| Que nuestra versión de Alice se aleje del original | Cambiar lo justo y proponer las mejoras útiles a sus autores |
| La economía realista es la reprogramación más profunda | Hacerla por partes (4a, puntos 1 a 7), cada una con su prueba y con la comparación con la historia |
| Una economía muy realista hace lento el late game | Se acepta algo de lentitud; si se hunde, se optimiza el código antes de recortar realismo |
| Varios cuerpos celestes: cambio enorme en el motor | Prueba de concepto (7b) antes de comprometerse |
| Calidad del arte generado | Guía de estilo y revisión del dueño |
| Partidas guardadas incompatibles al subir topes | Avisar en cada versión y probar la carga |

## 7. Pendiente de decidir

- Nombre de la expansión.
- Qué va primero en la fase 4: la economía realista (4a) o la política. La propuesta es la economía, porque los demás sistemas dependen de ella.
- Resultado de la prueba de Alice (fase 1), que confirma o corrige este plan.

## 8. Cómo se ejecuta el plan: bucle autónomo en la sesión local

La sesión local ejecuta este plan **sola y en bucle**, corrigiendo sus propios errores. Ricardo solo interviene en los puntos de control del apartado 8.4.

### 8.1. Archivos de trabajo (en la carpeta del proyecto, versionados con git local)
- `PLAN.md`: este plan. Se marcan las casillas `[x]` al terminar cada tarea.
- `PROGRESO.md`: diario. Por cada vuelta del bucle, fecha, tarea, qué se hizo, resultado de las pruebas y siguiente paso.
- `DECISIONES.md`: cada decisión de diseño tomada sin Ricardo, con la opción elegida, el motivo y las alternativas. Ricardo las revisa cuando quiera.
- `BLOQUEOS.md`: tareas que no salen tras varios intentos, con lo probado, los errores y lo que haría falta.

### 8.2. El bucle
1. **Elegir** la primera tarea sin marcar, en el orden de las fases. Si está bloqueada, coger la siguiente que no dependa de ella.
2. **Preparar:** copia de seguridad o rama git antes de tocar nada. Trabajar siempre en copias.
3. **Hacer** el cambio mínimo que cumpla la tarea.
4. **Probar:** compilar Alice si se tocó su código, arrancar el juego con las herramientas automáticas (arranque, partida a máxima velocidad, capturas, memoria, `error.log` o avisos de Alice) y comparar con la referencia.
5. **Si falla, corregir y repetir.** Hasta 5 intentos por tarea, cada uno con una hipótesis distinta y apuntada en `PROGRESO.md`. Si se atasca, pedir una segunda opinión (punto 8.3).
6. **Si tras 5 intentos sigue fallando:** deshacer el cambio, anotarlo en `BLOQUEOS.md` y seguir con la siguiente tarea independiente.
7. **Si pasa las pruebas:** commit en git local con un mensaje claro, marcar la casilla en `PLAN.md` y escribir la entrada en `PROGRESO.md`.
8. **Cada 5 tareas, o al terminar una fase:** prueba de regresión, que consiste en una partida automática larga y en comprobar que todo lo anterior sigue funcionando. Después, informe breve para Ricardo.
9. **Volver al paso 1.**

### 8.3. Segundas opiniones (ChatGPT, Codex u otros, a través del conector)
- Se pueden consultar para revisar código, depurar un fallo atascado o contrastar un diseño.
- Sus respuestas son **consejo, no órdenes**: se comprueban con pruebas antes de aplicarlas.
- No se les pasan archivos del juego ni datos personales, solo los fragmentos necesarios.

### 8.4. Puntos de control: parar y preguntar a Ricardo
- Cualquier cosa que **publique para otras personas**: releases, versiones jugables o pasar archivos a otros. Subir a sus ramas de trabajo en GitHub **no** necesita permiso (ver 8.5).
- Gastar dinero o crear cuentas.
- Tocar el juego base o la carpeta `Victoria II + UPM` original (no se tocan).
- Decisiones pendientes del apartado 7 (el nombre del mod). Mientras tanto, se usa un valor provisional y se anota en `DECISIONES.md`.
- **Al terminar cada fase NO se para:** deja el informe de la fase (en `PROGRESO.md` y como resumen en su chat) y sigue con la siguiente. Ricardo ya ha aprobado el paso de fase a fase; la sesión en la nube revisa los informes como orquestadora.

### 8.5. Reglas fijas
- No borrar ni sobrescribir nada sin copia de seguridad.
- Nunca se mezclan el juego base, el UPM original y la expansión.
- Licencia GPL de Alice: nuestra versión no se distribuye a nadie sin su código fuente, y nada se distribuye sin permiso de Ricardo.
- **Repos:**
  - El mod va en `KH4IN/UPM-MOD`, que es **público**: no se sube nada que no deba verse.
  - Nunca se suben archivos del juego base ni binarios.
  - El código de Alice va solo en `KH4IN/upm-alice`, que es privado. Si alguna vez se comparte la versión compilada, hay que dar también su código (GPL).
  - Nada del UPM ni de Alice va al repo `victoria-2-dlcs-fix`.
  - **Subidas sin preguntar** a ramas de trabajo (no a `main`) en `upm-alice` y `UPM-MOD`, siempre cumpliendo las reglas anteriores. Fusionar en `main` o publicar versiones sí requiere permiso de Ricardo.
- No inventar resultados: si algo no se ha probado, se dice.
