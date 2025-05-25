from math import floor

def truncar_decimales(valor, decimales=2):
    factor = 10 ** decimales
    return floor(valor * factor) / factor

def construir_fila(nro_fila, reloj, evento, colorista, peluquero_a, peluquero_b, recaudacion, costos, clientes):
    return {
        "nro_fila": nro_fila,
        "reloj": truncar_decimales(reloj),
        "evento": evento.tipo,
        "cliente_id": evento.cliente.id if evento.cliente else None,
        "colorista_estado": colorista.estado,
        "cola_colorista": len(colorista.cola),
        "peluquero_a_estado": peluquero_a.estado,
        "cola_a": len(peluquero_a.cola),
        "peluquero_b_estado": peluquero_b.estado,
        "cola_b": len(peluquero_b.cola),
        "recaudacion": recaudacion,
        "costos": costos,
        "ganancia": recaudacion - costos,
        "clientes_activos": [
            {
                "id": c.id,
                "estado": c.estado,
                "hora_refrigerio": truncar_decimales(c.hora_refrigerio) if c.estado and c.estado.startswith("E") else None
            }
            for c in clientes
            if c.estado in ["EAPA", "EAPB", "EAC", "SAPA", "SAPB", "SAC"]
        ]
    }

def construir_ultima_fila(reloj, evento, colorista, peluquero_a, peluquero_b, recaudacion, costos):
    return {
        "nro_fila": "FINAL",
        "reloj": truncar_decimales(reloj),
        "evento": evento.tipo,
        "cliente_id": evento.cliente.id if evento.cliente else None,
        "colorista_estado": colorista.estado,
        "cola_colorista": len(colorista.cola),
        "peluquero_a_estado": peluquero_a.estado,
        "cola_a": len(peluquero_a.cola),
        "peluquero_b_estado": peluquero_b.estado,
        "cola_b": len(peluquero_b.cola),
        "recaudacion": recaudacion,
        "costos": costos,
        "ganancia": recaudacion - costos
        # no mostramos clientes_activos en la última fila
    }