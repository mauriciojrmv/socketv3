import socket  # Importa la biblioteca de sockets de Python
from hilo_conexiones import HiloConexiones  # Importa la clase HiloConexiones
from conexion import Conexion  # Importa la clase Conexion

# Clase 2: Servidor - Configura el socket y maneja las conexiones
class Servidor:
    def __init__(self, host, port):
        # Almacenamos el host y puerto proporcionado dinámicamente
        self.host = host
        self.port = port
        # Crear el socket TCP
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Lista única para almacenar todas las conexiones activas
        self.lista_conexiones = []

    def iniciar_servidor(self):
        # Vincula el socket a la dirección y puerto
        self.server_socket.bind((self.host, self.port))
        # Configura el servidor para escuchar hasta 5 conexiones simultáneas
        self.server_socket.listen(5)
        print(f"Servidor escuchando en {self.host}:{self.port}")

        # Crear el hilo encargado de aceptar conexiones
        hilo_conexion = HiloConexiones(self.server_socket, self)
        hilo_conexion.start()  # Iniciar el hilo para gestionar conexiones

    def get_lista_conexiones(self):
        """Devuelve la lista de conexiones activas."""
        return self.lista_conexiones
