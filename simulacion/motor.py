import heapq
from entidades.cliente import Cliente
from entidades.evento import Evento
from entidades.servidor import Servidor
import config as cfg
from . import aleatorios as ale

def simular_dia(i, j, x):
    
    #Inicializaciones básicas para la simulación
    reloj = 0.0
    eventos = []  # heapq para eventos ordenados
    iteraciones = 0
    gastos_refrigerios = 0
    recaudacion_total = 0

    #Variables estadisticas
    personas_esperando_max = 0
    supera_x = 0

    #Vector estado
    vector_estado = []
    nro_fila = 0
    ultima_fila = None

    #PRIMERA LLEGADA
    id_cliente = 1
    clientes = []

    #Creación del primer cliente
    cliente = Cliente(id_cliente, reloj)
    clientes.append(cliente)

    #Creación del evento de llegada del primer cliente
    evento_llegada = Evento(tiempo=reloj, tipo="llegada", cliente=cliente)
    heapq.heappush(eventos, evento_llegada)

    #Inicialización de los servidores
    colorista = Servidor("Colorista", "colorista", *cfg.TIEMPOS_COLORISTA, cfg.PRECIO_COLORISTA)
    peluquero_a = Servidor("Peluquero A", "peluquero", *cfg.TIEMPOS_PELUQUERO_A, cfg.PRECIO_PELUQUERO)
    peluquero_b = Servidor("Peluquero B", "peluquero", *cfg.TIEMPOS_PELUQUERO_B, cfg.PRECIO_PELUQUERO)

    #Inicio del ciclo (programa principal)
    while eventos and iteraciones < cfg.MAX_ITERACIONES:
        evento = heapq.heappop(eventos)
        reloj = evento.tiempo
        iteraciones += 1

        #Al final de cada evento verificamos la cantidad de personas en cola    
        personas_esperando = len(colorista.cola) + len(peluquero_a.cola) + len(peluquero_b.cola)

        # Actualizar máximo si corresponde
        if personas_esperando > personas_esperando_max:
            personas_esperando_max = personas_esperando

        # Verificar si se supera x (el umbral maximo que ingresó el usuario)
        if personas_esperando > x:
            supera_x = 1
        #Cadena principal de ifs según el tipo de evento que ocurra
        if evento.tipo == "llegada":
            cliente = evento.cliente
            print(f"[{reloj:.2f}] Llega cliente {cliente.id}")

            #Si está libre le asignamos un servidor al cual ir
            servidor = ale.elegir_servidor(colorista, peluquero_a, peluquero_b)

            if servidor.esta_libre():
                servidor.asignar_cliente(cliente)
                print(f"    → Asignado directamente a {servidor.nombre}")

                duracion, rnd_duracion = ale.generar_uniforme(*servidor.tiempo_servicio)
                fin_servicio = reloj + duracion
                evento_fin = Evento(tiempo=fin_servicio, tipo="fin_servicio", cliente=cliente)
                heapq.heappush(eventos, evento_fin)
                print(f"    → Servicio durará {duracion:.2f} min, terminará a {fin_servicio:.2f}")
            
            #Si tiene que esperar entra al else
            else:
                cliente.estado = f"E{servidor.nombre.upper().replace(' ', '')}"
                cliente.hora_refrigerio = reloj + cfg.TIEMPO_MAX_ESPERA_REFRIGERIO
                servidor.cola.append(cliente)

                evento_refrigerio = Evento(tiempo=cliente.hora_refrigerio, tipo="paga_refrigerio", cliente=cliente)
                heapq.heappush(eventos, evento_refrigerio)
                print(f"    → Se agenda pago de refrigerio para {cliente.hora_refrigerio:.2f}")

            if reloj <= cfg.TIEMPO_RECEPCION_CLIENTES:
                #Crea el tiempo entre llegadas y a que hora efectivamente llegará
                tiempo_entre_llegadas, rnd_llegada = ale.generar_uniforme(*cfg.TIEMPOS_LLEGADA)
                nueva_llegada = reloj + tiempo_entre_llegadas

                if nueva_llegada <= cfg.TIEMPO_RECEPCION_CLIENTES:
                    id_cliente += 1

                    nuevo_cliente = Cliente(id_cliente, nueva_llegada)
                    clientes.append(nuevo_cliente)

                    nuevo_evento = Evento(tiempo=nueva_llegada, tipo="llegada", cliente=nuevo_cliente)
                    heapq.heappush(eventos, nuevo_evento)

        elif evento.tipo == "paga_refrigerio":
            cliente = evento.cliente
            
            #Una solución rapida para ver si esta en estado de espera, ya sea EAPA, EAPB o EAC
            if cliente.estado and cliente.estado.startswith("E"):
                print(f"[{reloj:.2f}] Cliente {cliente.id} sigue esperando → se cobra refrigerio")
                gastos_refrigerios += cfg.COSTO_REFRIGERIO
            else:
                print(f"[{reloj:.2f}] Cliente {cliente.id} ya fue atendido → no se cobra refrigerio")
        
        elif evento.tipo == "fin_servicio":
            cliente = evento.cliente

            #Tenemos que ver que servidor tiene asignado así lo liberamos
            servidores = [colorista, peluquero_a, peluquero_b]

            #Los objetos servidores tienen asignado un cliente actual, la iteracion con el next se hará como máximo 3 veces
            servidor = next(s for s in servidores if s.cliente_actual == cliente)
            servidor.liberar()
            recaudacion_total += servidor.precio

            #El len de la cola es literalmente el contador de cantidad de clientes en cola, no es necesario usar otra variable
            if len(servidor.cola) > 0:
                siguiente_cliente = servidor.cola.pop(0)
                servidor.asignar_cliente(siguiente_cliente)

                print(f"    → Ahora atiende a Cliente {siguiente_cliente.id}")

                duracion, rnd_duracion = ale.generar_uniforme(*servidor.tiempo_servicio)
                fin_servicio = reloj + duracion
                evento_fin = Evento(tiempo=fin_servicio, tipo="fin_servicio", cliente=siguiente_cliente)
                heapq.heappush(eventos, evento_fin)

                print(f"    → Servicio durará {duracion:.2f} min, terminará a {fin_servicio:.2f}")

        #Consigna de "Se mostrará en el vector de estado i iteraciones a partir de una hora j"
        if reloj >= j and len(vector_estado) < i:
            fila = {
                "nro_fila": nro_fila,
                "reloj": reloj,
                "evento": evento.tipo,
                "cliente_id": evento.cliente.id if evento.cliente else None,
                "colorista_estado": colorista.estado,
                "cola_colorista": len(colorista.cola),
                "peluquero_a_estado": peluquero_a.estado,
                "cola_a": len(peluquero_a.cola),
                "peluquero_b_estado": peluquero_b.estado,
                "cola_b": len(peluquero_b.cola),
                "recaudacion": recaudacion_total,
                "costos": gastos_refrigerios,
                "ganancia": recaudacion_total - gastos_refrigerios,
                "clientes_activos": [
                    {
                        "id": c.id,
                        "estado": c.estado,
                        "hora_refrigerio": c.hora_refrigerio if c.estado and c.estado.startswith("E") else None
                    }
                    for c in clientes
                    if c.estado in ["EAPA", "EAPB", "EAC", "SAPA", "SAPB", "SAC"]
                ]
            }
            vector_estado.append(fila)
            nro_fila += 1
        
        #Guardo la última fila porque la consigna dice "También se mostrará en el vector de estado la última fila de 
        # simulación, es decir la fila correspondiente al instante X. En esta fila no es necesario mostrar los objetos temporales"
        ultima_fila = {
            "nro_fila": "FINAL",
            "reloj": reloj,
            "evento": evento.tipo,
            "cliente_id": evento.cliente.id if evento.cliente else None,
            "colorista_estado": colorista.estado,
            "cola_colorista": len(colorista.cola),
            "peluquero_a_estado": peluquero_a.estado,
            "cola_a": len(peluquero_a.cola),
            "peluquero_b_estado": peluquero_b.estado,
            "cola_b": len(peluquero_b.cola),
            "recaudacion": recaudacion_total,
            "costos": gastos_refrigerios,
            "ganancia": recaudacion_total - gastos_refrigerios
        }
    
    #Afuera del ciclo while agregamos la ultima fila de la iteración si no fue incluida antes
    if not vector_estado or vector_estado[-1]["reloj"] != ultima_fila["reloj"]:
        vector_estado.append(ultima_fila)
    
    return vector_estado, recaudacion_total, gastos_refrigerios, supera_x

