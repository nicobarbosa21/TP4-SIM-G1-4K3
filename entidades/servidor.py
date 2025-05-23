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
    
    def liberar(self):
        self.estado = "Libre"
        self.cliente_actual = None