import heapq
from entidades.cliente import Cliente
from entidades.evento import Evento
from entidades.servidor import Servidor
import config as cfg
from . import aleatorios as ale
from simulacion.vector_estado import construir_fila, construir_ultima_fila

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
        evento_relevante = False

        # Esto se setea para que se actualice segun el evento que toque, entonces solo se modificaran ciertos valores por 
        # iteración y el resto quedarán en None para que se muestren vacios en el vector
        tipo_evento = evento.tipo
        rnd_llegada = None
        tiempo_entre_llegadas = None
        nueva_llegada = None
        rnd_atencion = None
        servidor = None
        duracion = None
        rnd_duracion = None
        fin_servicio = None

        #Cadena principal de ifs según el tipo de evento que ocurra
        if evento.tipo == "llegada":
            evento_relevante = True
            cliente = evento.cliente
            # Elegir servidor
            servidor_asignado, rnd_atencion = ale.elegir_servidor(colorista, peluquero_a, peluquero_b)
            servidor = servidor_asignado  # para mantener compatibilidad con el resto del código


            if servidor.esta_libre():
                servidor.asignar_cliente(cliente)

                duracion, rnd_duracion = ale.generar_uniforme(*servidor.tiempo_servicio)
                fin_servicio = reloj + duracion
                evento_fin = Evento(tiempo=fin_servicio, tipo="fin_servicio", cliente=cliente)
                heapq.heappush(eventos, evento_fin)

            else:
                cliente.estado = cfg.ESTADOS_SERVIDOR[servidor.nombre][0]
                cliente.hora_refrigerio = reloj + cfg.TIEMPO_MAX_ESPERA_REFRIGERIO
                servidor.cola.append(cliente)

                evento_refrigerio = Evento(tiempo=cliente.hora_refrigerio, tipo="paga_refrigerio", cliente=cliente)
                heapq.heappush(eventos, evento_refrigerio)

            if reloj <= cfg.TIEMPO_RECEPCION_CLIENTES:
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
            
            #Una solución rapida para ver si esta en estado de espera, ya sea EAPA, EAPB o EAC, el and cliente.hora_refrigerio basicamente verifica que no sea None, ya que None es falsy en pytho
            if cliente.estado and cliente.estado.startswith("E") and cliente.hora_refrigerio and cliente.hora_refrigerio <= reloj:
                evento_relevante = True
                gastos_refrigerios += cfg.COSTO_REFRIGERIO
                
        elif evento.tipo == "fin_servicio":
            evento_relevante = True
            cliente = evento.cliente

            #Tenemos que ver que servidor tiene asignado así lo liberamos
            servidores = [colorista, peluquero_a, peluquero_b]

            #Los objetos servidores tienen asignado un cliente actual, la iteracion con el next se hará como máximo 3 veces
            servidor = next(s for s in servidores if s.cliente_actual == cliente)
            servidor.liberar()
            cliente.estado = None
            recaudacion_total += servidor.precio

            #El len de la cola es literalmente el contador de cantidad de clientes en cola, no es necesario usar otra variable
            if len(servidor.cola) > 0:
                siguiente_cliente = servidor.cola.pop(0)
                servidor.asignar_cliente(siguiente_cliente)
                siguiente_cliente.hora_refrigerio = None
                duracion, rnd_duracion = ale.generar_uniforme(*servidor.tiempo_servicio)
                fin_servicio = reloj + duracion
                evento_fin = Evento(tiempo=fin_servicio, tipo="fin_servicio", cliente=siguiente_cliente)
                heapq.heappush(eventos, evento_fin)
        
        
        #Al final de cada evento verificamos la cantidad de personas en cola    
        personas_esperando = len(colorista.cola) + len(peluquero_a.cola) + len(peluquero_b.cola)

        # Actualizar máximo si corresponde
        if personas_esperando > personas_esperando_max:
            personas_esperando_max = personas_esperando

        # Verificar si se supera x (el umbral maximo que ingresó el usuario)
        if personas_esperando > x:
            supera_x = 1
        
        #Trae todos los datos necesarios por fila para contruir el vector estado
        datos_evento = {
            "rnd_llegada": rnd_llegada if tipo_evento == "llegada" else None,
            "tiempo_entre_llegadas": tiempo_entre_llegadas if tipo_evento == "llegada" else None,
            "proxima_llegada": nueva_llegada if tipo_evento == "llegada" else None,
            "rnd_atencion": rnd_atencion if tipo_evento == "llegada" else None,
            "servidor_a_atender": servidor_asignado.nombre if tipo_evento == "llegada" else None,
            "se_puede_recibir_clientes": reloj <= cfg.TIEMPO_RECEPCION_CLIENTES,
            "termino_dia": len(eventos) == 0,
            "rnd_peluquero_a": rnd_duracion if servidor and servidor.nombre == "Peluquero A" else None,
            "tiempo_atencion_a": duracion if servidor and servidor.nombre == "Peluquero A" else None,
            "fin_atencion_a": fin_servicio if servidor and servidor.nombre == "Peluquero A" else None,
            "rnd_peluquero_b": rnd_duracion if servidor and servidor.nombre == "Peluquero B" else None,
            "tiempo_atencion_b": duracion if servidor and servidor.nombre == "Peluquero B" else None,
            "fin_atencion_b": fin_servicio if servidor and servidor.nombre == "Peluquero B" else None,
            "rnd_colorista": rnd_duracion if servidor and servidor.nombre == "Colorista" else None,
            "tiempo_atencion_c": duracion if servidor and servidor.nombre == "Colorista" else None,
            "fin_atencion_c": fin_servicio if servidor and servidor.nombre == "Colorista" else None,
            "numero_dia": 1,
            "personas_esperando": len(colorista.cola) + len(peluquero_a.cola) + len(peluquero_b.cola),
            "maximo_cola": personas_esperando_max,
            "supero_umbral_x": supera_x
        }

        #Consigna de "Se mostrará en el vector de estado i iteraciones a partir de una hora j"
        if reloj >= j and len(vector_estado) < i and evento_relevante:
            fila = construir_fila(nro_fila, reloj, evento, datos_evento, colorista, peluquero_a, peluquero_b, recaudacion_total, gastos_refrigerios, clientes)
            vector_estado.append(fila)
            nro_fila += 1
        
        #Guardo la última fila porque la consigna dice "También se mostrará en el vector de estado la última fila de 
        # simulación, es decir la fila correspondiente al instante X. En esta fila no es necesario mostrar los objetos temporales"
        ultima_fila = construir_ultima_fila(reloj, evento, colorista, peluquero_a, peluquero_b, recaudacion_total, gastos_refrigerios, datos_evento)
    
    #Afuera del ciclo while agregamos la ultima fila de la iteración si no fue incluida antes
    if not vector_estado or vector_estado[-1]["reloj"] != ultima_fila["reloj"]:
        vector_estado.append(ultima_fila)
    
    return vector_estado, recaudacion_total, gastos_refrigerios, supera_x

