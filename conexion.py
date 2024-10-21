class Conexion:
    def __init__(self, id_sesion, socket, direccion, hilo):
        self.id_sesion = id_sesion  # ID único de la sesión
        self.socket = socket        # Socket del cliente
        self.direccion = direccion  # Dirección del cliente (IP, puerto)
        self.hilo = hilo            # Hilo asociado a la conexión (HiloComunicacion)
