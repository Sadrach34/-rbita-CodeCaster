"""
Modelos de datos (Entities).
Define las estructuras de datos que usa la aplicación.
Son clases simples que representan los objetos del dominio.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Usuario:
    """
    Modelo de datos para un Usuario.
    Ejemplo de cómo crear entidades en el backend.
    """
    id: Optional[int] = None
    nombre: str = ""
    email: str = ""
    
    def es_valido(self) -> bool:
        """
        Valida si el usuario tiene datos válidos.
        
        Returns:
            bool: True si el usuario es válido, False en caso contrario
        """
        return bool(self.nombre and self.email and "@" in self.email)


@dataclass
class Mensaje:
    """
    Modelo de datos para un Mensaje.
    Otro ejemplo de entidad del dominio.
    """
    id: Optional[int] = None
    contenido: str = ""
    autor: str = ""
    fecha: Optional[str] = None
    
    def __str__(self) -> str:
        """Representación en string del mensaje"""
        return f"[{self.autor}]: {self.contenido}"
