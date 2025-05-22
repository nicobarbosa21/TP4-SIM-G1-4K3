class Servidor:
    def __init__(self, nombre, tiempo_servicio_min, tiempo_servicio_max):
        self.nombre = nombre
        self.estado = "Libre"
        self.cliente_actual = None
        self.cola = []
        self.tiempo_servicio = (tiempo_servicio_min, tiempo_servicio_max)
    
    def esta_libre(self) -> bool:
        return self.estado == "Libre"
    
    def asignar_cliente(self, cliente: object):
        self.estado = "Ocupado"
        self.cliente_actual = cliente
    
    def liberar(self):
        self.estado = "Libre"
        self.cliente_actual = None