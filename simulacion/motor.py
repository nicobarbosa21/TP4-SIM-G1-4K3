import heapq
from entidades.cliente import Cliente
from entidades.evento import Evento
from entidades.servidor import Servidor
import config as cfg
from . import aleatorios as ale
from simulacion.vector_estado import construir_fila, construir_ultima_fila

def simular_dia(numero_dia, i, j, x, llegada, colorista_tiempo, peluquero_a_tiempo, peluquero_b_tiempo, prob_colorista, prob_a):
    reloj = 0.0
    eventos = []
    iteraciones = 0
    gastos_refrigerios = 0
    recaudacion_total = 0
    personas_esperando_max = 0
    supera_x = False
    vector_estado = []
    nro_fila = 1
    ultima_fila = None
    id_cliente = 1
    clientes = []

    colorista = Servidor("Colorista", "colorista", *colorista_tiempo, cfg.PRECIO_COLORISTA)
    peluquero_a = Servidor("Peluquero A", "peluquero", *peluquero_a_tiempo, cfg.PRECIO_PELUQUERO)
    peluquero_b = Servidor("Peluquero B", "peluquero", *peluquero_b_tiempo, cfg.PRECIO_PELUQUERO)

    # --- INICIALIZACIÓN ---
    tiempo_entre_llegadas, rnd_llegada = ale.generar_uniforme(*llegada)
    proxima_llegada = tiempo_entre_llegadas
    proxima_llegada_actual = proxima_llegada
    fin_a_actual = fin_b_actual = fin_c_actual = None

    datos_evento_inicial = {
        "rnd_llegada": rnd_llegada,
        "tiempo_entre_llegadas": tiempo_entre_llegadas,
        "proxima_llegada": proxima_llegada,
        "rnd_atencion": None,
        "servidor_a_atender": None,
        "se_puede_recibir_clientes": True,
        "termino_dia": False,
        "rnd_peluquero_a": None,
        "tiempo_atencion_a": None,
        "fin_atencion_a": None,
        "rnd_peluquero_b": None,
        "tiempo_atencion_b": None,
        "fin_atencion_b": None,
        "rnd_colorista": None,
        "tiempo_atencion_c": None,
        "fin_atencion_c": None,
        "numero_dia": numero_dia,
        "personas_esperando": 0,
        "maximo_cola": 0,
        "supero_umbral_x": False
    }

    if j <= 0 and i > 0:
        fila_inicial = construir_fila(
            nro_fila, 0.0, Evento(tiempo=0.0, tipo="Inicialización"), None,
            datos_evento_inicial, colorista, peluquero_a, peluquero_b, 0, 0, clientes
        )
        vector_estado.append(fila_inicial)
        nro_fila += 1

    cliente = Cliente(id_cliente, proxima_llegada)
    clientes.append(cliente)
    evento_llegada = Evento(tiempo=proxima_llegada, tipo="llegada", cliente=cliente)
    evento_llegada.rnd_llegada = rnd_llegada
    evento_llegada.tiempo_entre_llegadas = tiempo_entre_llegadas
    heapq.heappush(eventos, evento_llegada)

    while eventos and iteraciones < cfg.MAX_ITERACIONES:
        evento = heapq.heappop(eventos)
        reloj = evento.tiempo
        iteraciones += 1
        evento_relevante = False

        tipo_evento = evento.tipo
        rnd_llegada = tiempo_entre_llegadas = nueva_llegada = None
        rnd_atencion = rnd_duracion = duracion = fin_servicio = None
        servidor = None
        servidor_asignado = None

        if tipo_evento == "llegada":
            evento_relevante = True
            cliente = evento.cliente
            rnd_llegada = getattr(evento, "rnd_llegada", None)
            tiempo_entre_llegadas = getattr(evento, "tiempo_entre_llegadas", None)

            servidor_asignado, rnd_atencion = ale.elegir_servidor(
                colorista, peluquero_a, peluquero_b, prob_colorista, prob_a
            )
            servidor = servidor_asignado

            if servidor.esta_libre():
                servidor.asignar_cliente(cliente)
                duracion, rnd_duracion = ale.generar_uniforme(*servidor.tiempo_servicio)
                fin_servicio = reloj + duracion
                if servidor.nombre == "Peluquero A": fin_a_actual = fin_servicio
                elif servidor.nombre == "Peluquero B": fin_b_actual = fin_servicio
                elif servidor.nombre == "Colorista": fin_c_actual = fin_servicio
                heapq.heappush(eventos, Evento(tiempo=fin_servicio, tipo="fin_servicio", cliente=cliente))
            else:
                cliente.estado = cfg.ESTADOS_SERVIDOR[servidor.nombre][0]
                cliente.hora_refrigerio = reloj + cfg.TIEMPO_MAX_ESPERA_REFRIGERIO
                servidor.cola.append(cliente)
                heapq.heappush(eventos, Evento(tiempo=cliente.hora_refrigerio, tipo="paga_refrigerio", cliente=cliente))

            if reloj <= cfg.TIEMPO_RECEPCION_CLIENTES:
                tiempo_entre_llegadas, rnd_llegada = ale.generar_uniforme(*llegada)
                nueva_llegada = reloj + tiempo_entre_llegadas
                proxima_llegada_actual = nueva_llegada
                if nueva_llegada <= cfg.TIEMPO_RECEPCION_CLIENTES:
                    id_cliente += 1
                    nuevo_cliente = Cliente(id_cliente, nueva_llegada)
                    clientes.append(nuevo_cliente)
                    nuevo_evento = Evento(tiempo=nueva_llegada, tipo="llegada", cliente=nuevo_cliente)
                    nuevo_evento.rnd_llegada = rnd_llegada
                    nuevo_evento.tiempo_entre_llegadas = tiempo_entre_llegadas
                    heapq.heappush(eventos, nuevo_evento)

        elif tipo_evento == "paga_refrigerio":
            cliente = evento.cliente
            if cliente.estado and cliente.estado.startswith("E") and cliente.hora_refrigerio and cliente.hora_refrigerio <= reloj:
                evento_relevante = True
                gastos_refrigerios += cfg.COSTO_REFRIGERIO

        elif tipo_evento == "fin_servicio":
            evento_relevante = True
            cliente = evento.cliente
            servidores = [colorista, peluquero_a, peluquero_b]
            servidor = next(s for s in servidores if s.cliente_actual == cliente)
            servidor.liberar()
            cliente.estado = None
            recaudacion_total += servidor.precio

            if servidor.cola:
                siguiente_cliente = servidor.cola.pop(0)
                servidor.asignar_cliente(siguiente_cliente)
                siguiente_cliente.hora_refrigerio = None
                duracion, rnd_duracion = ale.generar_uniforme(*servidor.tiempo_servicio)
                fin_servicio = reloj + duracion
                if servidor.nombre == "Peluquero A": fin_a_actual = fin_servicio
                elif servidor.nombre == "Peluquero B": fin_b_actual = fin_servicio
                elif servidor.nombre == "Colorista": fin_c_actual = fin_servicio
                heapq.heappush(eventos, Evento(tiempo=fin_servicio, tipo="fin_servicio", cliente=siguiente_cliente))
            else:
                if servidor.nombre == "Peluquero A": fin_a_actual = None
                elif servidor.nombre == "Peluquero B": fin_b_actual = None
                elif servidor.nombre == "Colorista": fin_c_actual = None

        personas_esperando = len(colorista.cola) + len(peluquero_a.cola) + len(peluquero_b.cola)
        if personas_esperando > personas_esperando_max:
            personas_esperando_max = personas_esperando
        if personas_esperando > x:
            supera_x = True

        if reloj > cfg.TIEMPO_RECEPCION_CLIENTES:
            proxima_llegada_actual = None
        if fin_a_actual is not None and reloj > fin_a_actual:
            fin_a_actual = None
        if fin_b_actual is not None and reloj > fin_b_actual:
            fin_b_actual = None
        if fin_c_actual is not None and reloj > fin_c_actual:
            fin_c_actual = None

        datos_evento = {
            "rnd_llegada": rnd_llegada if tipo_evento == "llegada" else None,
            "tiempo_entre_llegadas": tiempo_entre_llegadas if tipo_evento == "llegada" else None,
            "proxima_llegada": proxima_llegada_actual,
            "rnd_atencion": rnd_atencion if tipo_evento == "llegada" else None,
            "servidor_a_atender": servidor_asignado.nombre if tipo_evento == "llegada" and servidor_asignado else None,
            "se_puede_recibir_clientes": reloj <= cfg.TIEMPO_RECEPCION_CLIENTES,
            "termino_dia": len(eventos) == 0,
            "rnd_peluquero_a": rnd_duracion if servidor and servidor.nombre == "Peluquero A" else None,
            "tiempo_atencion_a": duracion if servidor and servidor.nombre == "Peluquero A" else None,
            "fin_atencion_a": fin_a_actual,
            "rnd_peluquero_b": rnd_duracion if servidor and servidor.nombre == "Peluquero B" else None,
            "tiempo_atencion_b": duracion if servidor and servidor.nombre == "Peluquero B" else None,
            "fin_atencion_b": fin_b_actual,
            "rnd_colorista": rnd_duracion if servidor and servidor.nombre == "Colorista" else None,
            "tiempo_atencion_c": duracion if servidor and servidor.nombre == "Colorista" else None,
            "fin_atencion_c": fin_c_actual,
            "numero_dia": numero_dia,
            "personas_esperando": personas_esperando,
            "maximo_cola": personas_esperando_max,
            "supero_umbral_x": supera_x
        }

        if reloj >= j and len(vector_estado) < i and evento_relevante:
            servidor_del_evento = servidor if tipo_evento == "fin_servicio" else None
            fila = construir_fila(
                nro_fila, reloj, evento, servidor_del_evento, datos_evento,
                colorista, peluquero_a, peluquero_b, recaudacion_total, gastos_refrigerios, clientes
            )
            vector_estado.append(fila)
            nro_fila += 1

        servidor_final = servidor if tipo_evento == "fin_servicio" else None

        datos_evento["proxima_llegada"] = proxima_llegada_actual
        datos_evento["fin_atencion_a"] = fin_a_actual
        datos_evento["fin_atencion_b"] = fin_b_actual
        datos_evento["fin_atencion_c"] = fin_c_actual

        ultima_fila = construir_ultima_fila(
            reloj, evento, servidor_final, colorista, peluquero_a, peluquero_b,
            recaudacion_total, gastos_refrigerios, datos_evento
        )

    if not vector_estado or vector_estado[-1]["reloj"] != ultima_fila["reloj"]:
        vector_estado.append(ultima_fila)

    return vector_estado, recaudacion_total, gastos_refrigerios, supera_x