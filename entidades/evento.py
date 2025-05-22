class Evento:
    def __init__(self, tiempo, tipo, cliente=None):
        self.tiempo = tiempo
        self.tipo = tipo  # EL TIPO SE DEFINE AL DECLARAR TODOS LOS EVENTOS Y GUARDARLOS EN UN ARRAY
        self.cliente = cliente

    def __lt__(self, other):
        return self.tiempo < other.tiempo