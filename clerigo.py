from __future__ import annotations

from personaje_base import Personaje
from estados import crear_estado


class Clerigo(Personaje):
    def __init__(
        self,
        nombre: str,
        tipo: str = "Clérigo",
        max_vida: int = 70,
        ataque: int = 9,
        defensa: int = 5,
        vida: int | None = None,
        cooldown_habilidad: int = 0,
        estados=None,
    ) -> None:
        super().__init__(nombre, tipo, max_vida, ataque, defensa, vida, cooldown_habilidad, estados or [])

    def usar_habilidad(self, objetivo: Personaje) -> str:
        if self.cooldown_habilidad > 0:
            return f"{self.nombre} no puede usar Luz Sagrada. Recarga: {self.cooldown_habilidad} turno(s)."

        self.cooldown_habilidad = 4
        curado = self.curar(10)
        mensaje_estado = self.aplicar_estado(crear_estado("regeneracion", 2))
        danio = objetivo.recibir_danio(self.ataque_actual() + 2)
        return (
            f"{self.nombre} usa Luz Sagrada: se cura {curado}, causa {danio} de daño a {objetivo.nombre} "
            f"y activa regeneración. {mensaje_estado}"
        )
