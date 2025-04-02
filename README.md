# Documento de Requisitos para el Graficador

## I. Introducción

Este documento define los requisitos funcionales y no funcionales para el desarrollo de una aplicación de dibujo (graficador) utilizando PyGame. La herramienta permitirá al usuario crear figuras básicas mediante interacciones con el ratón, ofreciendo la opción de elegir entre algoritmos de trazado implementados manualmente (básicos) y métodos propios de PyGame.

## II. Requisitos Funcionales

### 1. Dibujo de Líneas
- **RF1.1**: El sistema debe permitir dibujar líneas utilizando dos puntos de referencia.
- **RF1.2**: Los puntos de referencia se obtendrán a partir de la posición del ratón y el clic derecho.
- **RF1.3**: El usuario podrá configurar el algoritmo de trazado para las líneas, pudiendo elegir entre:
  - **Algoritmo básico**: **DDA (Digital Differential Analyzer)**.
  - **Método propio de PyGame**.

### 2. Dibujo de Círculos
- **RF2.1**: El sistema debe permitir dibujar círculos utilizando dos puntos de referencia: uno para definir el centro y otro para definir el radio.
- **RF2.2**: Los puntos de referencia se registrarán a partir de la posición del ratón y el clic derecho.
- **RF2.3**: Se deberá configurar el algoritmo de trazado para los círculos, pudiendo elegir entre:
  - **Algoritmo básico**: **Midpoint Circle Algorithm** o **Bresenham Circle Algorithm** (se recomienda el primero por su simplicidad y eficiencia en enteros).
  - **Método propio de PyGame**.

### 3. Dibujo de Rectángulos
- **RF3.1**: El sistema debe permitir dibujar rectángulos utilizando dos puntos de referencia que correspondan a dos vértices opuestos.
- **RF3.2**: Los puntos de referencia se obtendrán a partir de la posición del ratón y el clic derecho.
- **RF3.3**: Se deberá configurar el algoritmo de trazado para los rectángulos, pudiendo elegir entre:
  - **Algoritmo básico**: Implementación mediante la conexión de cuatro líneas, cada una trazada con **DDA** o **Bresenham**.
  - **Método propio de PyGame**.

### 4. Dibujo de Polígonos
- **RF4.1**: El sistema debe permitir dibujar polígonos a partir de una secuencia de puntos de referencia.
- **RF4.2**: La interacción para registrar los puntos será la siguiente:
  - Cada punto se marca con un clic izquierdo.
  - El último punto se define mediante un clic derecho.
  - Si el último punto no coincide con el primero, el sistema trazará una línea que cierre la figura.
- **RF4.3**: Se deberá configurar el algoritmo de trazado para los polígonos, pudiendo elegir entre:
  - **Algoritmo básico**: Trazado de cada segmento entre puntos consecutivos utilizando un algoritmo de línea básico (DDA o Bresenham), conectando el último punto con el primero en caso necesario.
  - **Método propio de PyGame**.

### 5. Dibujo de Curvas
- **RF5.1**: El sistema debe permitir dibujar curvas utilizando tres puntos de referencia.
- **RF5.2**: Los puntos de referencia se registrarán mediante la posición del ratón:
  - Los dos primeros puntos se marcarán con clic izquierdo.
  - El tercer punto se confirmará con clic derecho.
- **RF5.3**: Se deberá configurar el algoritmo de trazado para las curvas, pudiendo elegir entre:
  - **Algoritmo básico**: Implementación de una curva **cuadrática de Bézier**, la cual permite emular un comportamiento vectorial mediante tres puntos de control.  
  - **Método propio de PyGame**.

### 6. Menús y Configuraciones
- **RF6.1**: Todas las configuraciones se agruparán en un menú desplegable ubicado en la parte superior de la ventana principal.
- **RF6.2**: Cada tipo de figura (línea, círculo, rectángulo, polígono y curva) dispondrá de un submenú de configuración para seleccionar el algoritmo de trazado.

### 7. Área de Selección de Herramientas
- **RF7.1**: Se implementará un área de selección de herramientas en la parte superior de la ventana, donde cada herramienta se representará mediante un ícono o figura que refleje su función.
- **RF7.2**: El área de herramientas deberá permitir la selección de:
  - Las figuras mencionadas en los puntos 1 a 5.
  - Funciones adicionales: borrado por área, borrado por píxel, deshacer, rehacer y cambio del color de fondo del lienzo.
- **RF7.3**: Se recomienda construir los botones de manera personalizada, aunque es admisible el uso de botones propios de PyGame si fuera necesario.

### 8. Interfaz Gráfica
- **RF8.1**: La interfaz gráfica deberá ser *responsive*, adaptándose de forma adecuada a cambios en la altura y anchura de la ventana.

### 9. Guardado de Lienzo
- **RF9.1**: El sistema debe permitir guardar el lienzo en disco.
- **RF9.2**: Se recomienda el uso de Numpy para manipular y almacenar la matriz de píxeles del lienzo.

### 10. Exportación del Lienzo
- **RF10.1**: El sistema debe permitir exportar el lienzo en formato JPG.
- **RF10.2**: Se recomienda utilizar MatPlotLib para realizar la exportación.

### 11. Implementación de Funciones Básicas
- **RF11.1**: Las funciones básicas de dibujo (los algoritmos básicos) deben implementarse manualmente, sin recurrir a funcionalidades preexistentes en PyGame. Esto asegura que la opción de "algoritmo básico" sea una implementación propia.

---

## III. Requisitos No Funcionales

- **RNF1**: La aplicación deberá ser intuitiva y responder de manera fluida a las interacciones del usuario.
- **RNF2**: La arquitectura del sistema debe ser modular, facilitando la incorporación o modificación de algoritmos de trazado sin afectar la funcionalidad global.
- **RNF3**: El código fuente deberá estar bien documentado y seguir las buenas prácticas de programación para garantizar su mantenibilidad.

---

## IV. Análisis y Comentarios

1. **Algoritmos de Trazado**  
   Se han definido explícitamente los algoritmos básicos para cada figura:  
   - **Líneas**: DDA.  
   - **Círculos**: Midpoint Circle Algorithm o Bresenham Circle Algorithm (se recomienda el primero).  
   - **Rectángulos**: Trazado de cuatro líneas utilizando DDA o Bresenham.  
   - **Polígonos**: Conexión de puntos consecutivos con DDA o Bresenham, cerrando la figura de ser necesario.  
   - **Curvas**: Curva cuadrática de Bézier, la cual es una solución sencilla y eficaz para tres puntos de control.

2. **Interacción del Ratón**  
   Se ha diferenciado el uso del clic derecho y clic izquierdo según la figura, lo que permite una clara distinción en la forma de registrar los puntos de referencia para cada tipo de dibujo.

3. **Modularidad y Configuración**  
   Se establece una estructura de menús globales y submenús específicos para cada figura, lo que facilita la configuración del algoritmo de trazado sin afectar la interfaz general.

4. **Uso de Funcionalidades de PyGame**  
   La implementación manual (algoritmo básico) es obligatoria para garantizar el aprendizaje y control sobre la función de trazado, mientras que se permite la opción de métodos propios de PyGame para comparación y eficiencia.

---

## V. Métodos de Dibujo con PyGame

### 1. Líneas
- **Método de PyGame**:  
  Se utiliza la función:  
  ```python
  pygame.draw.line(surface, color, start_pos, end_pos, width)
  ```  
  - **Parámetros**:
    - `surface`: Superficie donde se dibuja.
    - `color`: Color de la línea.
    - `start_pos`: Coordenada inicial (x, y).
    - `end_pos`: Coordenada final (x, y).
    - `width`: Grosor de la línea.

### 2. Círculos
- **Método de PyGame**:  
  Se utiliza la función:  
  ```python
  pygame.draw.circle(surface, color, center, radius, width)
  ```  
  - **Parámetros**:
    - `surface`: Superficie de dibujo.
    - `color`: Color del círculo.
    - `center`: Centro del círculo (x, y).
    - `radius`: Radio del círculo.
    - `width`: Ancho del borde (si se establece en 0, se dibuja un círculo lleno).

*Nota*: Para la opción básica se puede implementar manualmente el **Midpoint Circle Algorithm** o el **Bresenham Circle Algorithm**.

### 3. Rectángulos
- **Método de PyGame**:  
  Se utiliza la función:  
  ```python
  pygame.draw.rect(surface, color, rect, width)
  ```  
  - **Parámetros**:
    - `surface`: Superficie donde se dibuja.
    - `color`: Color del rectángulo.
    - `rect`: Una tupla o un objeto `pygame.Rect` que define la posición y dimensiones (x, y, ancho, alto).
    - `width`: Ancho del borde (0 para un rectángulo lleno).

*Nota*: La implementación manual se realiza trazando el rectángulo mediante la conexión de cuatro líneas (usando DDA o Bresenham) que definen sus lados.

### 4. Polígonos
- **Método de PyGame**:  
  Se utiliza la función:  
  ```python
  pygame.draw.polygon(surface, color, pointlist, width)
  ```  
  - **Parámetros**:
    - `surface`: Superficie de dibujo.
    - `color`: Color del polígono.
    - `pointlist`: Lista de puntos (tuplas) que definen los vértices del polígono.
    - `width`: Ancho del borde (0 para un polígono lleno).

*Nota*: En la opción básica se puede implementar trazando cada segmento entre puntos consecutivos (con DDA o Bresenham) y cerrando la figura si es necesario.

### 5. Curvas
- **Método de PyGame (Convencional)**:  
  PyGame no cuenta con una función nativa específica para curvas tipo Bézier. La solución convencional consiste en:
  1. **Cálculo de Puntos**:  
     Calcular los puntos intermedios de una curva cuadrática de Bézier a partir de tres puntos de control, utilizando la fórmula:  
     \[
     B(t) = (1-t)^2 \, P_0 + 2(1-t)t \, P_1 + t^2 \, P_2,\quad t \in [0,1]
     \]
  2. **Dibujo de la Curva**:  
     Una vez calculados los puntos, unirlos mediante la función:  
     ```python
     pygame.draw.lines(surface, color, False, point_list, width)
     ```  
     - **Parámetros**:
       - `surface`: Superficie de dibujo.
       - `color`: Color de la curva.
       - `False`: Indica que no se cierra el conjunto de líneas.
       - `point_list`: Lista de puntos calculados de la curva.
       - `width`: Ancho de la línea.

*Nota*: La cantidad de puntos calculados (variando el parámetro "t") determinará la suavidad de la curva.

---

## VI. Análisis Final

Este documento presenta una formalización completa de los requisitos del graficador, definiendo tanto las funcionalidades básicas como la configuración de la interfaz, y estableciendo de forma clara los algoritmos básicos y los métodos convencionales de PyGame para cada figura. Se garantiza que la implementación permita comparar el rendimiento y la precisión de las soluciones manuales frente a las funcionalidades nativas de PyGame, manteniendo la escala del proyecto y promoviendo la modularidad y extensibilidad.

