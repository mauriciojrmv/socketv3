import threading  # Importa threading para crear hilos

# Clase 4: HiloComunicacion - Maneja la comunicación entre el servidor y el cliente
class HiloComunicacion(threading.Thread):
    def __init__(self, cliente_socket, servidor, direccion):
        super().__init__()
        self.cliente_socket = cliente_socket  # Socket del cliente conectado
        self.servidor = servidor  # Referencia al servidor para modificar la lista de conexiones
        self.direccion = direccion  # Dirección IP del cliente
        self.activo = True  # Variable de control para gestionar la comunicación

    def run(self):
        while self.activo:  # Bucle controlado por 'self.activo'
            try:
                # Recibe el mensaje del cliente
                mensaje = self.cliente_socket.recv(1024).decode()

                if mensaje:  # Si hay un mensaje
                    print(f"Mensaje recibido de {self.direccion}: {mensaje}")
                    # Envía una respuesta de vuelta al cliente
                    self.cliente_socket.send(f"Tu mensaje fue: {mensaje}".encode())
                else:  # Si no hay mensaje, significa que el cliente cerró la conexión
                    self.activo = False

            except ConnectionResetError:
                print(f"Error de conexión con el cliente {self.direccion}.")
                self.activo = False  # Cambia el estado de conexión para salir del bucle

        # Cerrar el socket cuando termine la comunicación
        self.cliente_socket.close()
        
        # Eliminar la conexión (socket) de la lista de conexiones activas
        for conexion in self.servidor.get_lista_conexiones():
            if conexion.socket == self.cliente_socket:
                self.servidor.get_lista_conexiones().remove(conexion)
                print(f"Cliente {self.direccion} se ha desconectado.")
                break
        
        # Mostrar la cantidad de conexiones activas
        print(f"Conexiones activas: {len(self.servidor.get_lista_conexiones())}")

    def detener(self):
        """Método para detener la comunicación de manera controlada."""
        self.activo = False
        self.cliente_socket.close()  # Cerramos el socket del cliente cuando detenemos la comunicación
