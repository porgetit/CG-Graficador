# Graficador ✏️🖼️

> Un editor 2D académico escrito en **Python 3 + PyGame** que demuestra — de forma interactiva — los algoritmos clásicos de rasterizado (DDA, midpoint circle, Bézier discreta…) frente a las primitivas nativas de PyGame.
>   
> **Autor:** Kevin Esguerra Cardona — `Porgetit`

---

## Índice

1. [Objetivos](#objetivos)  
2. [Características](#características)  
3. [Instalación](#instalación)  
4. [Puesta en marcha](#puesta-en-marcha)  
5. [Guía de usuario](#guía-de-usuario)  
   - 5.1&nbsp;[Interfaz general](#51-interfaz-general)  
   - 5.2&nbsp;[Barra de herramientas](#52-barra-de-herramientas)  
   - 5.3&nbsp;[Flujo de dibujo](#53-flujo-de-dibujo)  
   - 5.4&nbsp;[Atajos de teclado](#54-atajos-de-teclado)  
6. [Estructura del código](#estructura-del-código)  
7. [Hoja de ruta](#hoja-de-ruta)  
8. [Créditos](#créditos)  

---

## Objetivos

* Comparar visualmente **algoritmos manuales** de rasterizado con el motor interno de PyGame.  
* Practicar el patrón de diseño **Modelo–Vista–Controlador (MVC)**.  
* Servir de base para futuras extensiones (herramientas de transformación, capas, etc.).

## Características

| ✔ Función                                   | Detalle                                                                                |
| ------------------------------------------- | -------------------------------------------------------------------------------------- |
| Herramientas de dibujo                      | Línea, Rectángulo, Círculo, Polígono, Curva Bézier (cuadrática)                        |
| Algoritmos duales                           | **BASIC** (DDA, midpoint, etc.) / **PYGAME** (nativo)                                  |
| Colores y grosor                            | Selector *Tkinter* para pincel y color de lienzo                                       |
| Borrado                                     | Área rectangular (con soporte listo para borrado libre)                                |
| Guardar / Abrir                             | Formato **JSON** propio — conserva color, grosor y algoritmo de cada figura            |
| Exportar                                    | PNG / JPG usando NumPy + Matplotlib                                                    |
| Ventana redimensionable                     | El lienzo se adapta manteniendo el dibujo                                              |
| Arquitectura limpia                         | Capas desacopladas, fácil de testear/extender                                          |

## Instalación

# 1. Clona el repositorio
git clone https://github.com/tu-usuario/graficador.git
cd graficador

# 2. (Opcional) crea entorno virtual
python -m venv venv && source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Instala dependencias
pip install pygame numpy matplotlib

> **Tkinter** viene incluido en las distribuciones oficiales de Python.  
> Si usas una instalación «slim» de Linux, instala el paquete `python3-tk`.

## Puesta en marcha

```bash
python main.py
```

La ventana principal aparece con un lienzo blanco y una barra de herramientas vertical de 60 px.

---

## Guía de usuario

### 5.1 Interfaz general
![UI](docs/img/ui_overview.png)

1. **Barra de herramientas** — selección de herramienta, algoritmo, colores y archivo.  
2. **Lienzo** — área donde se dibuja; su fondo puede cambiar de color.  
3. **Estado** — la herramienta seleccionada se marca con un borde rojo.

### 5.2 Barra de herramientas

| Icono               | Acción        | Descripción                                               |
| -------------------- | ------------ | --------------------------------------------------------- |
| 🗲 (línea)           | `LINE`       | Clic-inicio ➜ clic-fin                                    |
| ⭕ (círculo)         | `CIRCLE`     | Clic en centro ➜ clic en borde                            |
| ▢ (rectángulo)      | `RECTANGLE`  | Esquinas opuestas                                         |
| 🔺 (polígono)       | `POLYGON`    | Clics sucesivos, botón derecho para cerrar                |
| ~ (curva)           | `CURVE`      | Inicio, punto de control, fin                             |
| ⬜ (goma)            | `ERASE_AREA` | Arrastra área a borrar                                    |
| **B**               | `BASIC`      | Dibujo con algoritmos manuales                            |
| **P**               | `PYGAME`     | Dibujo con PyGame (no disponible en borrado)              |
| 🎨 (brocha)         | Color pincel | Abre selector RGB + grosor                                |
| 🖼️ (lienzo)         | Color fondo  | Cambia fondo (afecta borrador)                            |
| 💾                  | Guardar      | JSON                                                      |
| 📂                  | Abrir        | JSON                                                      |
| 📤                  | Exportar     | PNG/JPG                                                   |

### 5.3 Flujo de dibujo

1. Selecciona **herramienta**.  
2. (Opcional) selecciona **algoritmo**.  
3. Define **puntos** con el mouse:  
   *Línea* → inicio y fin; *Curva* → inicio, control, fin; *Polígono* → clics sucesivos, botón derecho para cerrar.  
4. El trazo aparece inmediatamente.  
5. Guarda (`💾` o **S**) o exporta (`📤` o **E**) cuando lo necesites.

### 5.4 Atajos de teclado

| Tecla           | Acción                                  |
| --------------- | ---------------------------------------- |
| **S**           | Guardar JSON                            |
| **E**           | Exportar imagen                         |
| Mouse izquierdo | Añadir punto / definir origen           |
| Mouse derecho   | Cerrar figura / procesar forma          |

---

## Estructura del código

```text
controllers/  # SuperController, DrawingController, EventHandler
models/       # Canvas, Shape* + algorithms (BASIC / PYGAME)
views/        # CanvasView, ToolbarView, Tk color picker
main.py       # loop principal, inyección MVC
icons/        # PNGs 24×24
docs/         # Diagramas, screenshots, PDF técnico
```

*El documento técnico completo con UML y flujo de control se encuentra en*  
`./documento técnico.pdf` (fuente `.tex` en `./`).

---

## Hoja de ruta

- [ ] Undo / Redo con pila de snapshots  
- [ ] Borrador libre (`EraseFree`) en la GUI  
- [ ] Selección y transformación (mover, escalar, rotar)  
- [ ] Test unitarios (algoritmos BASIC, serialización JSON)

---

## Créditos

* **PyGame** — motor de renderizado.  
* **NumPy + Matplotlib** — exportación de imagen.

¡Disfruta dibujando y experimentando con algoritmos gráficos!  
Cualquier *pull request*, sugerencia o reporte de *bug* es bienvenido. ✨
