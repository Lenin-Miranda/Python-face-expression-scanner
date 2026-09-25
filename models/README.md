# Modelo facial

El detector utiliza el archivo incluido `face_landmarker.task`, cargado desde [src/config.py](../src/config.py) y abierto por [src/main.py](../src/main.py).

## Contenido y uso

Es el modelo de MediaPipe Face Landmarker utilizado para puntos faciales y coeficientes de movimiento (*blendshapes*). La aplicación habilita `output_face_blendshapes` y procesa un rostro por fotograma.

## Comprobar la instalación

Desde la raíz:

```bash
python -c "from pathlib import Path; p = Path('models/face_landmarker.task'); print(p.is_file(), p.stat().st_size if p.exists() else 0)"
```

El archivo debe existir y tener contenido. El programa lanza un error explícito si falta; no lo descarga automáticamente. Conserva el nombre/ruta o actualiza `MODEL_PATH` al usar otro archivo compatible.

## Alcance

Los resultados describen geometría y movimientos visibles, no identidad ni emociones. Si sustituyes el modelo, revisa su compatibilidad con la versión fijada de MediaPipe y sus condiciones de uso.

[Instalación y ejecución](../README.md).
