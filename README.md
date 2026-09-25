# Laboratorio de expresiones faciales

Aplicación educativa de Python que usa la cámara, OpenCV y MediaPipe Face Landmarker para dibujar puntos faciales y detectar movimientos visibles: apertura de boca, cierre de ojos, sonrisa y conteo de parpadeos.

El programa analiza movimientos observables; no determina emociones, intenciones ni el estado mental de una persona.

## Instalación

Necesitas Python compatible con [requirements.txt](requirements.txt), una webcam y un entorno gráfico.

```bash
git clone https://github.com/Lenin-Miranda/Python-face-expression-scanner.git
cd Python-face-expression-scanner
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python src/main.py
```

En Windows PowerShell, activa el entorno con `.venv\Scripts\Activate.ps1`. Las dependencias tienen versiones fijadas; si no hay un paquete binario compatible con tu Python/sistema, revisa esa compatibilidad antes de cambiar las versiones.

## Uso

1. Concede permiso de cámara a la terminal o editor.
2. Coloca un rostro frente a la cámara.
3. Observa los puntos, indicadores de movimiento y contador.
4. Pulsa **q** con la ventana activa para cerrar.

La implementación procesa un rostro por fotograma. La cámara predeterminada es la de índice `0`.

## Estructura

| Archivo | Responsabilidad |
| --- | --- |
| [src/main.py](src/main.py) | Captura, detección y cierre de recursos |
| [src/config.py](src/config.py) | Ruta del modelo, cámara y umbrales |
| [src/geometry.py](src/geometry.py) | Distancias y proporciones |
| [src/expressions.py](src/expressions.py) | Estado, suavizado y conteo |
| [src/drawing.py](src/drawing.py) | Superposición de indicadores |
| [models/README.md](models/README.md) | Modelo utilizado |

El modelo `models/face_landmarker.task` está incluido en el repositorio; no forma parte del entorno virtual.

## Ajustes y problemas habituales

- **No se abre la cámara:** revisa permisos, otras aplicaciones que la estén usando y `CAMERA_INDEX`.
- **Modelo no encontrado:** confirma la ruta configurada y que el archivo exista.
- **Detección inestable:** mejora la iluminación y ajusta umbrales/suavizado en `src/config.py`.
- **La ventana no aparece:** ejecuta en un escritorio, no en una sesión sin interfaz gráfica.

## Desarrollo y privacidad

No hay una suite automatizada incluida. Comprueba apertura/cierre de cámara, pérdida/recuperación del rostro y varios parpadeos al modificar el análisis.

Practica con consentimiento y no publiques imágenes ni grabaciones personales. El bucle actual procesa fotogramas en memoria y no incluye grabación. Para salir del entorno virtual usa `deactivate`.
