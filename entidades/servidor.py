import config as cfg

class Servidor:
    def __init__(self, nombre, tipo, tiempo_servicio_min, tiempo_servicio_max, precio):
        self.nombre = nombre
        self.tipo = tipo
        self.estado = "Libre"
        self.cliente_actual = None
        self.cola = []
        self.tiempo_servicio = (tiempo_servicio_min, tiempo_servicio_max)
        self.precio = precio
    
    def esta_libre(self) -> bool:
        return self.estado == "Libre"
    
    def asignar_cliente(self, cliente: object):
        self.estado = "Ocupado"
        self.cliente_actual = cliente
        cliente.hora_refrigerio = None
        cliente.estado = cfg.ESTADOS_SERVIDOR[self.nombre][1]
    
    def liberar(self):
        self.estado = "Libre"
        self.cliente_actual = None