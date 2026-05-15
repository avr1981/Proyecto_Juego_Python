from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List
import random

from estados import Estado


@dataclass
class Personaje:
    """Clase base de todos los personajes del juego."""

    nombre: str
    tipo: str
    max_vida: int
    ataque: int
    defensa: int
    vida: int | None = None
    cooldown_habilidad: int = 0
    estados: List[Estado] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.vida is None:
            self.vida = self.max_vida
        self.vida = max(0, min(self.vida, self.max_vida))

    def esta_vivo(self) -> bool:
        return self.vida > 0

    def ataque_actual(self) -> int:
        bonus = sum(estado.modificador_ataque for estado in self.estados)
        return max(1, self.ataque + bonus)

    def defensa_actual(self) -> int:
        bonus = sum(estado.modificador_defensa for estado in self.estados)
        return max(0, self.defensa + bonus)

    def curar(self, cantidad: int) -> int:
        vida_anterior = self.vida
        self.vida = min(self.max_vida, self.vida + cantidad)
        return self.vida - vida_anterior

    def recibir_danio(self, danio: int, ignora_defensa: bool = False) -> int:
        if ignora_defensa:
            danio_real = max(0, danio)
        else:
            danio_real = max(1, danio - self.defensa_actual())
        self.vida = max(0, self.vida - danio_real)
        return danio_real

    def atacar(self, objetivo: "Personaje") -> str:
        variacion = random.randint(-2, 3)
        es_critico = random.random() < 0.15
        multiplicador = 2 if es_critico else 1
        danio_base = max(1, self.ataque_actual() + variacion) * multiplicador
        danio_real = objetivo.recibir_danio(danio_base)

        texto_critico = " CRÍTICO" if es_critico else ""
        return f"{self.nombre} ataca a {objetivo.nombre} y causa {danio_real} de daño.{texto_critico}"

    def usar_habilidad(self, objetivo: "Personaje") -> str:
        return f"{self.nombre} no tiene una habilidad especial definida."

    def aplicar_estado(self, nuevo_estado: Estado) -> str:
        """Añade un estado o refresca su duración si ya existe."""

        for estado in self.estados:
            if estado.nombre == nuevo_estado.nombre:
                estado.turnos = max(estado.turnos, nuevo_estado.turnos)
                return f"{self.nombre} ya tenía {estado.nombre}; se refresca a {estado.turnos} turno(s)."

        self.estados.append(nuevo_estado)
        return f"{self.nombre} recibe el estado {nuevo_estado.nombre} durante {nuevo_estado.turnos} turno(s)."

    def procesar_inicio_turno(self) -> tuple[list[str], bool]:
        """Aplica daño/curación de estados y devuelve si puede actuar."""

        mensajes: list[str] = []
        puede_actuar = True

        for estado in self.estados:
            if estado.danio_por_turno > 0:
                self.recibir_danio(estado.danio_por_turno, ignora_defensa=True)
                mensajes.append(
                    f"{self.nombre} sufre {estado.danio_por_turno} de daño por {estado.nombre}."
                )

            if estado.cura_por_turno > 0 and self.esta_vivo():
                curado = self.curar(estado.cura_por_turno)
                mensajes.append(
                    f"{self.nombre} recupera {curado} de vida por {estado.nombre}."
                )

            if estado.impide_actuar:
                puede_actuar = False
                mensajes.append(f"{self.nombre} está {estado.nombre} y pierde la acción.")

        return mensajes, puede_actuar

    def finalizar_turno(self) -> list[str]:
        """Reduce la duración de los estados al terminar el turno del personaje."""

        mensajes: list[str] = []
        estados_activos: list[Estado] = []

        for estado in self.estados:
            estado.turnos -= 1
            if estado.turnos > 0:
                estados_activos.append(estado)
            else:
                mensajes.append(f"El estado {estado.nombre} de {self.nombre} ha terminado.")

        self.estados = estados_activos
        return mensajes

    def bajar_cooldown(self) -> None:
        if self.cooldown_habilidad > 0:
            self.cooldown_habilidad -= 1

    def resumen(self) -> str:
        estados = self.texto_estados()
        return (
            f"{self.tipo} {self.nombre} | vida {self.vida}/{self.max_vida} | "
            f"atk {self.ataque_actual()} | def {self.defensa_actual()} | estados: {estados}"
        )

    def texto_estados(self) -> str:
        if not self.estados:
            return "ninguno"
        return ", ".join(f"{estado.nombre}({estado.turnos})" for estado in self.estados)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "nombre": self.nombre,
            "tipo": self.tipo,
            "max_vida": self.max_vida,
            "ataque": self.ataque,
            "defensa": self.defensa,
            "vida": self.vida,
            "cooldown_habilidad": self.cooldown_habilidad,
            "estados": [estado.to_dict() for estado in self.estados],
        }
