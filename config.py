# Acá definimos constantes

TIEMPO_RECEPCION_CLIENTES = 480  # en minutos (8 horas)
MAX_ITERACIONES = 100_000

PRECIO_COLORISTA = 35_000
PRECIO_PELUQUERO = 18_000
COSTO_REFRIGERIO = 6_500

TIEMPO_MAX_ESPERA_REFRIGERIO = 30

ESTADOS_SERVIDOR = {
    "Colorista": ("EAC", "SAC"),
    "Peluquero A": ("EAPA", "SAPA"),
    "Peluquero B": ("EAPB", "SAPB")
}