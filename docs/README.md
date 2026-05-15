
# Juego de Combate por Turnos con Personajes y Habilidades

Este proyecto es un juego de combate por turnos desarrollado en Python aplicando Programación Orientada a Objetos.  
El usuario puede crear personajes, elegir un tipo predefinido, consultar sus estadísticas y enfrentarlos en combates estratégicos.

## Descripción del proyecto

El juego permite crear diferentes tipos de personajes, cada uno con estadísticas, habilidades especiales y comportamientos propios.  
Durante el combate, los personajes pueden realizar ataques normales o utilizar habilidades especiales, siempre que la recarga de la habilidad lo permita.

El sistema incluye elementos de azar, como ataques críticos, fallos, variación de daño y efectos de estado. Además, los personajes pueden subir de nivel y ganar experiencia tras los combates.

## Funcionalidades principales

- Creación de personajes desde el menú.
- Selección de tipo de personaje.
- Combate por turnos entre dos personajes.
- Ataques normales y habilidades especiales.
- Sistema de recarga de habilidades.
- Efectos de estado como veneno, quemadura, congelación, parálisis, sangrado, escudo y regeneración.
- Sistema de experiencia y niveles.
- Guardado y carga de personajes en archivos JSON.
- Guardado del historial de combates.
- Interfaz gráfica básica con Tkinter.
- Menú principal ampliable y organizado por funciones.

## Tipos de personajes incluidos

El proyecto incluye cinco tipos de personajes por defecto:

- Guerrero
- Mago
- Arquero
- Pícaro
- Clérigo

Cada tipo hereda de la clase principal `Personaje` y redefine sus estadísticas y habilidades, aplicando herencia y polimorfismo.

## Conceptos de POO aplicados

En este proyecto se utilizan los siguientes conceptos de Programación Orientada a Objetos:

- Clases y objetos.
- Herencia.
- Polimorfismo.
- Encapsulación.
- Constructores `__init__`.
- Método especial `__str__`.
- Getters y setters.
- Validaciones y manejo básico de excepciones.
- Separación de responsabilidades mediante módulos.

## Estructura del proyecto

```text
proyecto_combate_mejorado/
│
├── main.py
├── abrir_gui.py
├── personaje.py
├── guerrero.py
├── mago.py
├── arquero.py
├── picaro.py
├── clerigo.py
├── combate.py
├── estados.py
├── storage.py
├── gui.py
├── personajes.json
├── combates.json
├── documentacion.txt
├── requirements.txt
├── arrancar_consola.bat
└── arrancar_gui.bat
