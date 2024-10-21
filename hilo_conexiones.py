import threading  # Importa threading para crear hilos
from hilo_comunicacion import HiloComunicacion  # Importa la clase HiloComunicacion
from conexion import Conexion  # Importa la clase Conexion
import uuid  # Para generar IDs únicos

# Clase 3: HiloConexiones - Administra las conexiones de los clientes en hilos separados
class HiloConexiones(threading.Thread):
    def __init__(self, server_socket, servidor):
        super().__init__()
        self.server_socket = server_socket  # Socket del servidor
        self.servidor = servidor  # Referencia al servidor que maneja las conexiones
        self.activo = True  # Variable de control para gestionar el ciclo de vida del hilo

    def run(self):
        # Bucle controlado por la variable 'activo'
        while self.activo:
            try:
                cliente_socket, direccion = self.server_socket.accept()  # Espera una conexión entrante
                cliente_ip = direccion[0]  # Obtener la IP del cliente

                # Verificar si la IP ya está conectada
                if any(conexion.direccion[0] == cliente_ip for conexion in self.servidor.get_lista_conexiones()):
                    # Enviar un mensaje de rechazo antes de cerrar la conexión
                    mensaje_rechazo = "Conexión rechazada: Ya existe una sesión activa desde esta IP."
                    cliente_socket.send(mensaje_rechazo.encode())
                    print(f"Conexión rechazada para el cliente {cliente_ip}.")
                    cliente_socket.close()  # Rechazar la conexión
                else:
                    print(f"Conexión aceptada desde {direccion}")
                    
                    # Crear un hilo para manejar la comunicación con este cliente
                    hilo_comunicacion = HiloComunicacion(cliente_socket, self.servidor, direccion)
                    hilo_comunicacion.start()  # Iniciar el hilo para gestionar los mensajes del cliente
                    
                    # Crear un objeto Conexion y agregarlo a la lista
                    nueva_conexion = Conexion(
                        id_sesion=str(uuid.uuid4()),  # Generar un ID único para la sesión
                        socket=cliente_socket,
                        direccion=direccion,
                        hilo=hilo_comunicacion
                    )
                    self.servidor.get_lista_conexiones().append(nueva_conexion)
                    print(f"Conexiones activas: {len(self.servidor.get_lista_conexiones())}")

            except Exception as e:
                print(f"Error en la aceptación de conexiones: {e}")
                self.activo = False  # Si hay un error grave, detenemos el hilo

    def detener(self):
        """Método para detener el hilo de conexiones de manera controlada."""
        self.activo = False
        self.server_socket.close()  # Cerramos el socket del servidor para detener las conexiones
