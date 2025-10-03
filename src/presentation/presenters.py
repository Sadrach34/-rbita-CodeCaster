"""
Presentadores (Presenters/Controllers).
Capa intermedia entre Frontend y Backend.
Recibe eventos del frontend, llama al backend, y actualiza la vista.

RESPONSABILIDADES:
- Capturar eventos de la vista (clicks, inputs, etc.)
- Llamar a los casos de uso del backend
- Actualizar la vista con los resultados
- NO contiene lógica de negocio (eso es del backend)
- NO contiene código de UI (eso es del frontend)
"""

from typing import Optional
from ..backend.services import UsuarioService, MensajeService
from ..backend.use_cases import RegistrarUsuarioUseCase, EnviarMensajeUseCase


class PresenterBase:
    """
    Clase base para todos los presenters.
    Define la estructura común de los presenters.
    """
    
    def __init__(self):
        """Inicializa el presenter"""
        self._vista = None
    
    def vincular_vista(self, vista):
        """
        Vincula una vista con este presenter.
        
        Args:
            vista: Instancia de la vista a vincular
        """
        self._vista = vista


class EjemploPresenter(PresenterBase):
    """
    Presenter de ejemplo que conecta la vista de ejemplo con el backend.
    Demuestra cómo separar la lógica de presentación de la UI y el backend.
    """
    
    def __init__(self, usuario_service: UsuarioService, mensaje_service: MensajeService):
        """
        Inicializa el presenter con sus dependencias del backend.
        
        Args:
            usuario_service: Servicio de usuarios del backend
            mensaje_service: Servicio de mensajes del backend
        """
        super().__init__()
        
        # Servicios del backend
        self.usuario_service = usuario_service
        self.mensaje_service = mensaje_service
        
        # Casos de uso
        self.registrar_usuario_uc = RegistrarUsuarioUseCase(usuario_service)
        self.enviar_mensaje_uc = EnviarMensajeUseCase(usuario_service, mensaje_service)
    
    def manejar_registro_usuario(self, nombre: str, email: str):
        """
        Maneja el evento de registro de usuario desde la vista.
        
        Args:
            nombre: Nombre del usuario
            email: Email del usuario
        """
        # Llamar al caso de uso del backend
        exito, mensaje, usuario = self.registrar_usuario_uc.ejecutar(nombre, email)
        
        # Actualizar la vista con el resultado
        # (En la vista real, necesitarías métodos para esto)
        if self._vista:
            if exito:
                print(f"✓ {mensaje}")
                print(f"  Usuario creado: {usuario}")
            else:
                print(f"✗ {mensaje}")
    
    def manejar_envio_mensaje(self, contenido: str, autor: str):
        """
        Maneja el evento de envío de mensaje desde la vista.
        
        Args:
            contenido: Contenido del mensaje
            autor: Autor del mensaje
        """
        # Llamar al caso de uso del backend
        exito, mensaje, mensaje_obj = self.enviar_mensaje_uc.ejecutar(contenido, autor)
        
        # Actualizar la vista con el resultado
        if self._vista:
            if exito:
                print(f"✓ {mensaje}")
                print(f"  Mensaje: {mensaje_obj}")
            else:
                print(f"✗ {mensaje}")
    
    def obtener_resumen_datos(self) -> dict:
        """
        Obtiene un resumen de los datos del backend para mostrar en la vista.
        
        Returns:
            Diccionario con el resumen de datos
        """
        usuarios = self.usuario_service.obtener_usuarios()
        mensajes = self.mensaje_service.obtener_mensajes()
        
        return {
            "total_usuarios": len(usuarios),
            "total_mensajes": len(mensajes),
            "usuarios": usuarios,
            "mensajes": mensajes
        }
