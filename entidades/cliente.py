class Cliente:
    def __init__(self, id, tiempo_llegada):
        self.id = id
        self.tiempo_llegada = tiempo_llegada
        self.estado = None
        self.hora_refrigerio = None