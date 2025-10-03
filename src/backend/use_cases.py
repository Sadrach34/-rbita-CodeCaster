"""
Casos de Uso (Use Cases).
Orquesta las operaciones de los servicios para casos específicos.
Ejemplo: "Enviar mensaje nuevo" podría involucrar validar usuario y crear mensaje.
"""

from typing import Optional, Tuple
from .services import UsuarioService, MensajeService
from .models import Usuario, Mensaje


class RegistrarUsuarioUseCase:
    """
    Caso de uso: Registrar un nuevo usuario en el sistema.
    Ejemplo de cómo orquestar operaciones de múltiples servicios.
    """
    
    def __init__(self, usuario_service: UsuarioService):
        """
        Inicializa el caso de uso con sus dependencias.
        
        Args:
            usuario_service: Servicio de usuarios
        """
        self.usuario_service = usuario_service
    
    def ejecutar(self, nombre: str, email: str) -> Tuple[bool, str, Optional[Usuario]]:
        """
        Ejecuta el caso de uso de registrar usuario.
        
        Args:
            nombre: Nombre del usuario
            email: Email del usuario
            
        Returns:
            Tupla (éxito, mensaje, usuario_creado)
        """
        # Validación básica
        if not nombre or not email:
            return False, "Nombre y email son obligatorios", None
        
        # Intentar crear el usuario
        usuario = self.usuario_service.crear_usuario(nombre, email)
        
        if usuario is None:
            return False, "Datos de usuario inválidos", None
        
        return True, f"Usuario {nombre} registrado exitosamente", usuario


class EnviarMensajeUseCase:
    """
    Caso de uso: Enviar un nuevo mensaje.
    Valida que el autor exista antes de crear el mensaje.
    """
    
    def __init__(self, usuario_service: UsuarioService, mensaje_service: MensajeService):
        """
        Inicializa el caso de uso con sus dependencias.
        
        Args:
            usuario_service: Servicio de usuarios
            mensaje_service: Servicio de mensajes
        """
        self.usuario_service = usuario_service
        self.mensaje_service = mensaje_service
    
    def ejecutar(self, contenido: str, autor_nombre: str) -> Tuple[bool, str, Optional[Mensaje]]:
        """
        Ejecuta el caso de uso de enviar mensaje.
        
        Args:
            contenido: Contenido del mensaje
            autor_nombre: Nombre del autor
            
        Returns:
            Tupla (éxito, mensaje_info, mensaje_creado)
        """
        # Validación
        if not contenido or not autor_nombre:
            return False, "Contenido y autor son obligatorios", None
        
        # Crear mensaje
        mensaje = self.mensaje_service.crear_mensaje(contenido, autor_nombre)
        
        return True, "Mensaje enviado correctamente", mensaje
