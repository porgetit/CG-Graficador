# Graficador con Algoritmos Básicos

## Descripción del Proyecto

Este proyecto es una aplicación de dibujo interactiva desarrollada con **PyGame**, diseñada para permitir a los usuarios crear figuras geométricas básicas utilizando algoritmos de rasterización implementados manualmente. Aunque durante la etapa de desarrollo se incluyó la posibilidad de comparar los algoritmos básicos con los métodos nativos de PyGame, esta funcionalidad ha sido deshabilitada en la versión final. Por lo tanto, el sistema utiliza exclusivamente los algoritmos básicos para el trazado de figuras.

## Funcionalidades Principales

### 1. Dibujo de Figuras Básicas
El sistema permite al usuario dibujar las siguientes figuras geométricas:
- **Líneas**: Utilizando el algoritmo **DDA (Digital Differential Analyzer)**.
- **Círculos**: Implementados con el **Midpoint Circle Algorithm**.
- **Rectángulos**: Construidos mediante la conexión de cuatro líneas trazadas con **DDA**.
- **Polígonos**: Trazados mediante la conexión de puntos consecutivos utilizando **DDA**.
- **Curvas**: Implementadas como curvas cuadráticas de Bézier.

### 2. Herramientas de Dibujo
El sistema incluye herramientas adicionales para mejorar la experiencia del usuario:
- **Selección de herramientas**: Área dedicada para elegir entre las diferentes figuras geométricas.
- **Cambio de color**: Posibilidad de cambiar el color del pincel y del lienzo.
- **Borrado**: Herramientas para borrar figuras.

### 3. Guardado y Exportación
- **Guardado del lienzo**: Permite almacenar el lienzo en disco en un formato JSON.
- **Exportación**: Posibilidad de exportar el lienzo como una imagen en formato JPG.

### 4. Interfaz Gráfica
- **Diseño adaptable**: La interfaz gráfica se ajusta automáticamente a los cambios en el tamaño de la ventana.
- **Botones personalizados**: Los botones de la barra de herramientas están diseñados para ser intuitivos y visualmente representativos de su función.

## Vídeo de demostración

https://youtu.be/aSBfI1AK_7Q

## Detalles Técnicos

### Algoritmos Básicos
Los algoritmos básicos han sido implementados manualmente para garantizar un control completo sobre el proceso de rasterización. Estos algoritmos incluyen:
- **DDA (Digital Differential Analyzer)** para líneas.
- **Midpoint Circle Algorithm** para círculos.
- **Curvas de Bézier** para curvas cuadráticas.

### Comparación con PyGame
Durante el desarrollo, se incluyó la posibilidad de comparar los algoritmos básicos con los métodos nativos de PyGame. Sin embargo, esta funcionalidad ha sido deshabilitada en la versión final, y el sistema utiliza exclusivamente los algoritmos básicos.

## Requisitos del Sistema
- **Python 3.8 o superior**.
- **PyGame 2.0 o superior**.
- **Numpy** (para manipulación de matrices de píxeles).

## Contribuciones
Las contribuciones son bienvenidas.

## Autores
Kevin Esguerra Cardona y Juan Pablo Sánchez Zapata.
