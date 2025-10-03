"""
Servicios (Business Logic).
Contiene la lógica de negocio de la aplicación.
Los servicios NO conocen nada sobre Tkinter o la UI.
"""

from typing import List, Optional
from .models import Usuario, Mensaje


class UsuarioService:
    """
    Servicio para gestionar usuarios.
    Ejemplo de cómo implementar lógica de negocio separada de la UI.
    """
    
    def __init__(self):
        """Inicializa el servicio con una lista de usuarios en memoria"""
        self._usuarios: List[Usuario] = []
        self._siguiente_id: int = 1
    
    def crear_usuario(self, nombre: str, email: str) -> Optional[Usuario]:
        """
        Crea un nuevo usuario si los datos son válidos.
        
        Args:
            nombre: Nombre del usuario
            email: Email del usuario
            
        Returns:
            Usuario creado o None si los datos no son válidos
        """
        # Crear el usuario temporal para validación
        usuario = Usuario(nombre=nombre, email=email)
        
        # Validar datos
        if not usuario.es_valido():
            return None
        
        # Asignar ID y guardar
        usuario.id = self._siguiente_id
        self._siguiente_id += 1
        self._usuarios.append(usuario)
        
        return usuario
    
    def obtener_usuarios(self) -> List[Usuario]:
        """
        Obtiene todos los usuarios.
        
        Returns:
            Lista de todos los usuarios
        """
        return self._usuarios.copy()
    
    def buscar_usuario(self, id: int) -> Optional[Usuario]:
        """
        Busca un usuario por su ID.
        
        Args:
            id: ID del usuario a buscar
            
        Returns:
            Usuario encontrado o None
        """
        for usuario in self._usuarios:
            if usuario.id == id:
                return usuario
        return None


class MensajeService:
    """
    Servicio para gestionar mensajes.
    Otro ejemplo de servicio de lógica de negocio.
    """
    
    def __init__(self):
        """Inicializa el servicio con una lista de mensajes en memoria"""
        self._mensajes: List[Mensaje] = []
        self._siguiente_id: int = 1
    
    def crear_mensaje(self, contenido: str, autor: str) -> Mensaje:
        """
        Crea un nuevo mensaje.
        
        Args:
            contenido: Contenido del mensaje
            autor: Autor del mensaje
            
        Returns:
            Mensaje creado
        """
        mensaje = Mensaje(
            id=self._siguiente_id,
            contenido=contenido,
            autor=autor
        )
        self._siguiente_id += 1
        self._mensajes.append(mensaje)
        
        return mensaje
    
    def obtener_mensajes(self) -> List[Mensaje]:
        """
        Obtiene todos los mensajes.
        
        Returns:
            Lista de todos los mensajes
        """
        return self._mensajes.copy()
    
    def contar_mensajes(self) -> int:
        """
        Cuenta el total de mensajes.
        
        Returns:
            Número total de mensajes
        """
        return len(self._mensajes)
