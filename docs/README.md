# Ejercicio de POO - Juego de Combate por Turnos

Este proyecto corresponde al penúltimo ejercicio de Programación Orientada a Objetos en Python.  
Consiste en un juego de combate por turnos donde el usuario puede crear personajes, elegir su tipo y enfrentarlos entre sí utilizando ataques normales y habilidades especiales.

El proyecto trabaja los principales conceptos de la POO, como clases, objetos, herencia, polimorfismo, encapsulación, constructores y métodos especiales como `__str__`.

## Funcionalidades principales

- Crear personajes desde el menú principal.
- Elegir entre distintos tipos de personaje.
- Ver los personajes creados y sus estadísticas.
- Iniciar combates por turnos.
- Usar ataques normales y habilidades especiales.
- Gestionar recargas de habilidades.
- Aplicar efectos de estado durante el combate.
- Guardar y cargar personajes mediante archivos JSON.
- Guardar historial de combates.
- Utilizar una interfaz gráfica básica con Tkinter.

## Tipos de personajes

El juego incluye diferentes clases de personajes, cada una con sus propias estadísticas y habilidades:

- Guerrero
- Mago
- Arquero
- Pícaro
- Clérigo

Cada clase hereda de la clase principal `Personaje` y redefine parte de su comportamiento, aplicando polimorfismo.

## Ampliaciones incluidas

Además de los requisitos básicos del ejercicio, se han añadido varias ampliaciones:

- Interfaz gráfica con Tkinter.
- Sistema de experiencia y niveles.
- Estados alterados avanzados.
- Historial de combates.
- Código separado en varios archivos para facilitar futuras ampliaciones.

## Ejecución

Para ejecutar el proyecto en consola:

```bash
py main.py
