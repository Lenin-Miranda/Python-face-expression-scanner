# Laboratorio de expresiones faciales

Proyecto educativo para aprender visión por computadora desde cero. Primero
capturaremos imágenes de la cámara; después detectaremos puntos faciales y,
finalmente, interpretaremos gestos visibles como parpadear o abrir la boca.

> El programa analizará movimientos visibles del rostro. No puede determinar
> con certeza las emociones, intenciones o estado mental de una persona.

## Qué está preparado

- Python aislado dentro de `.venv`.
- OpenCV para acceder a la webcam y dibujar imágenes.
- MediaPipe Face Landmarker para detectar el rostro y sus puntos.
- El modelo oficial en `models/face_landmarker.task`.
- Módulos separados para cámara, configuración, matemáticas, análisis y dibujo.
- Carpetas locales para imágenes y videos que Git no publicará.

## Abrir el entorno

Desde la raíz del proyecto:

```bash
source .venv/bin/activate
```

Al activarlo, la terminal mostrará normalmente `(.venv)`. Comprueba que estás
usando el Python correcto:

```bash
which python
python --version
```

`which python` debe terminar en `.venv/bin/python`.

Para salir del entorno:

```bash
deactivate
```

## Ejecutar tu programa

Cuando hayas escrito código en `src/main.py`:

```bash
python src/main.py
```

La primera vez que uses la cámara, macOS solicitará permiso para la aplicación
desde la que ejecutas Python (Terminal, iTerm o Visual Studio Code). Si lo
rechazas, puedes cambiarlo en **Ajustes del Sistema → Privacidad y seguridad →
Cámara**.

Para detener una ventana de OpenCV, usaremos la tecla `q`. Si el proceso no
responde, vuelve a la terminal y presiona `Control + C`.

## Ruta de las lecciones

1. Abrir y cerrar la webcam correctamente.
2. Leer fotogramas y mostrarlos en una ventana.
3. Entender BGR, RGB, resolución y coordenadas.
4. Enviar un fotograma a MediaPipe.
5. Dibujar los 478 puntos faciales.
6. Leer los 52 movimientos faciales (*blendshapes*).
7. Crear reglas para parpadeo, boca abierta y sonrisa visible.
8. Reducir el parpadeo de resultados usando varios fotogramas.
9. Organizar el programa en módulos y añadir pruebas.

No avanzaremos a reconocimiento de identidad hasta dominar estas partes y
revisar sus implicaciones de privacidad.

## Estructura

```text
.
├── data/
│   ├── images/            # Imágenes locales; no se versionan
│   └── videos/            # Videos locales; no se versionan
├── models/
│   └── face_landmarker.task
├── src/
│   ├── config.py          # Rutas, índices y umbrales
│   ├── drawing.py         # Elementos dibujados con OpenCV
│   ├── expressions.py     # Estado y análisis de expresiones visibles
│   ├── geometry.py        # Distancias y proporciones
│   └── main.py            # Cámara y flujo principal
├── requirements.txt
└── README.md
```

## Recrear el entorno en el futuro

No es necesario hacerlo ahora. Si borras `.venv`, puedes reconstruirlo con:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

El entorno virtual es desechable; tus archivos de código y datos están fuera
de él.

## Privacidad

- Practica inicialmente con tu propia cara y con consentimiento.
- No guardes fotogramas ni grabaciones sin una razón explícita.
- No publiques `data/` ni bases de rostros.
- Describe resultados como movimientos faciales observados, no como emociones
  o diagnósticos psicológicos.
