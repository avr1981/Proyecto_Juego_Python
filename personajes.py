"""Archivo puente para poder importar todos los tipos desde un único sitio."""

from personaje_base import Personaje
from guerrero import Guerrero
from mago import Mago
from arquero import Arquero
from picaro import Picaro
from clerigo import Clerigo
from factory import crear_personaje, personaje_desde_dict, TIPOS_DISPONIBLES, VALORES_DEFECTO

__all__ = [
    "Personaje",
    "Guerrero",
    "Mago",
    "Arquero",
    "Picaro",
    "Clerigo",
    "crear_personaje",
    "personaje_desde_dict",
    "TIPOS_DISPONIBLES",
    "VALORES_DEFECTO",
]
