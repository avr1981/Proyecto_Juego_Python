from __future__ import annotations

from typing import List
import random

from personaje_base import Personaje


def combate(p1: Personaje, p2: Personaje, max_turnos: int = 100) -> List[str]:
    """Ejecuta un combate por turnos y devuelve el registro completo."""

    log: List[str] = []
    turno = 1
    atacante, defensor = p1, p2

    log.append("INICIO DEL COMBATE")
    log.append(p1.resumen())
    log.append(p2.resumen())
    log.append("-" * 60)

    while p1.esta_vivo() and p2.esta_vivo() and turno <= max_turnos:
        log.append(f"\nTurno {turno}: actúa {atacante.nombre} ({atacante.tipo})")

        mensajes_estado, puede_actuar = atacante.procesar_inicio_turno()
        log.extend(mensajes_estado)

        if not atacante.esta_vivo():
            log.append(f"{atacante.nombre} cae derrotado por los estados alterados.")
            break

        atacante.bajar_cooldown()

        if puede_actuar:
            usa_habilidad = atacante.cooldown_habilidad == 0 and random.random() < 0.35
            if usa_habilidad:
                log.append(atacante.usar_habilidad(defensor))
            else:
                log.append(atacante.atacar(defensor))
        else:
            log.append(f"{atacante.nombre} no puede atacar este turno.")

        log.extend(atacante.finalizar_turno())

        log.append(
            f"Vida: {p1.nombre} {p1.vida}/{p1.max_vida} [{p1.texto_estados()}] | "
            f"{p2.nombre} {p2.vida}/{p2.max_vida} [{p2.texto_estados()}]"
        )

        atacante, defensor = defensor, atacante
        turno += 1

    log.append("\n" + "-" * 60)

    if p1.esta_vivo() and not p2.esta_vivo():
        log.append(f"Ganador: {p1.nombre} ({p1.tipo})")
    elif p2.esta_vivo() and not p1.esta_vivo():
        log.append(f"Ganador: {p2.nombre} ({p2.tipo})")
    elif p1.vida > p2.vida:
        log.append(f"Combate terminado por límite de turnos. Gana {p1.nombre} por tener más vida.")
    elif p2.vida > p1.vida:
        log.append(f"Combate terminado por límite de turnos. Gana {p2.nombre} por tener más vida.")
    else:
        log.append("Combate terminado en empate.")

    return log
