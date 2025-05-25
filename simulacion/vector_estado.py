from math import floor

def truncar_decimales(valor, decimales=2):
    if valor == None:
        return None
    factor = 10 ** decimales
    return floor(valor * factor) / factor

def descripcion_evento(evento, servidor=None):
    if evento.tipo == "llegada":
        return f"Llegada cliente {evento.cliente.id}"
    elif evento.tipo == "paga_refrigerio":
        return f"Paga refrigerio {evento.cliente.id}"
    elif evento.tipo == "fin_servicio" and servidor:
        return f"Fin servicio {servidor.nombre}"
    elif evento.tipo == "Inicialización":
        return "Inicialización"
    return evento.tipo

def construir_fila(nro_fila, reloj, evento, servidor_del_evento, datos_evento, colorista, peluquero_a, peluquero_b, recaudacion, costos, clientes):
    return {
        "nro_fila": nro_fila,
        "reloj": truncar_decimales(reloj),
        "evento": descripcion_evento(evento, servidor_del_evento),
        "cliente_id": evento.cliente.id if evento.cliente else None,
        "rnd_cliente": truncar_decimales(datos_evento["rnd_llegada"]),
        "tiempo_entre_llegadas": truncar_decimales(datos_evento["tiempo_entre_llegadas"]),
        "proxima_llegada": truncar_decimales(datos_evento["proxima_llegada"]),
        "rnd_atencion": truncar_decimales(datos_evento["rnd_atencion"]),
        "servidor_a_atender": datos_evento["servidor_a_atender"],
        "se_puede_recibir_clientes": datos_evento["se_puede_recibir_clientes"],
        "termino_dia": datos_evento["termino_dia"],
        "rnd_peluquero_a": truncar_decimales(datos_evento["rnd_peluquero_a"]),
        "tiempo_atencion_a": truncar_decimales(datos_evento["tiempo_atencion_a"]),
        "fin_atencion_a": truncar_decimales(datos_evento["fin_atencion_a"]),
        "peluquero_a_estado": peluquero_a.estado,
        "cola_a": len(peluquero_a.cola),
        "rnd_peluquero_b": truncar_decimales(datos_evento["rnd_peluquero_b"]),
        "tiempo_atencion_b": truncar_decimales(datos_evento["tiempo_atencion_b"]),
        "fin_atencion_b": truncar_decimales(datos_evento["fin_atencion_b"]),
        "peluquero_b_estado": peluquero_b.estado,
        "cola_b": len(peluquero_b.cola),
        "rnd_colorista": truncar_decimales(datos_evento["rnd_colorista"]),
        "tiempo_atencion_c": truncar_decimales(datos_evento["tiempo_atencion_c"]),
        "fin_atencion_c": truncar_decimales(datos_evento["fin_atencion_c"]),
        "colorista_estado": colorista.estado,
        "cola_colorista": len(colorista.cola),
        "recaudacion": recaudacion,
        "costos": costos,
        "ganancia": recaudacion - costos,
        "numero_dia": datos_evento["numero_dia"],
        "personas_esperando": datos_evento["personas_esperando"],
        "maximo_cola": datos_evento["maximo_cola"],
        "supero_umbral_x": datos_evento["supero_umbral_x"],
        "clientes_activos": [
            {
                "id": c.id,
                "estado": c.estado,
                "hora_refrigerio": truncar_decimales(c.hora_refrigerio)
                if c.estado and c.estado.startswith("E") else None
            }
            for c in clientes
            if c.estado in ["EAPA", "EAPB", "EAC", "SAPA", "SAPB", "SAC"]
        ]
    }

def construir_ultima_fila(reloj, evento, servidor_del_evento,colorista, peluquero_a, peluquero_b, recaudacion, costos, datos_evento):
    return {
        "nro_fila": "FINAL",
        "reloj": truncar_decimales(reloj),
        "evento": descripcion_evento(evento, servidor_del_evento),
        "cliente_id": evento.cliente.id if evento.cliente else None,
        "rnd_cliente": truncar_decimales(datos_evento["rnd_llegada"]),
        "tiempo_entre_llegadas": truncar_decimales(datos_evento["tiempo_entre_llegadas"]),
        "proxima_llegada": truncar_decimales(datos_evento["proxima_llegada"]),
        "rnd_atencion": truncar_decimales(datos_evento["rnd_atencion"]),
        "servidor_a_atender": datos_evento["servidor_a_atender"],
        "se_puede_recibir_clientes": datos_evento["se_puede_recibir_clientes"],
        "termino_dia": datos_evento["termino_dia"],
        "rnd_peluquero_a": truncar_decimales(datos_evento["rnd_peluquero_a"]),
        "tiempo_atencion_a": truncar_decimales(datos_evento["tiempo_atencion_a"]),
        "fin_atencion_a": truncar_decimales(datos_evento["fin_atencion_a"]),
        "peluquero_a_estado": peluquero_a.estado,
        "cola_a": len(peluquero_a.cola),
        "rnd_peluquero_b": truncar_decimales(datos_evento["rnd_peluquero_b"]),
        "tiempo_atencion_b": truncar_decimales(datos_evento["tiempo_atencion_b"]),
        "fin_atencion_b": truncar_decimales(datos_evento["fin_atencion_b"]),
        "peluquero_b_estado": peluquero_b.estado,
        "cola_b": len(peluquero_b.cola),
        "rnd_colorista": truncar_decimales(datos_evento["rnd_colorista"]),
        "tiempo_atencion_c": truncar_decimales(datos_evento["tiempo_atencion_c"]),
        "fin_atencion_c": truncar_decimales(datos_evento["fin_atencion_c"]),
        "colorista_estado": colorista.estado,
        "cola_colorista": len(colorista.cola),
        "recaudacion": recaudacion,
        "costos": costos,
        "ganancia": recaudacion - costos,
        "numero_dia": datos_evento["numero_dia"],
        "personas_esperando": datos_evento["personas_esperando"],
        "maximo_cola": datos_evento["maximo_cola"],
        "supero_umbral_x": datos_evento["supero_umbral_x"]
    }