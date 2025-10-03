"""
Componentes de UI reutilizables.
Widgets personalizados que se pueden usar en múltiples vistas.
"""

import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional


class BotonPrimario(ttk.Button):
    """
    Botón con estilo primario.
    Ejemplo de componente reutilizable para mantener consistencia visual.
    """
    
    def __init__(self, parent, text: str, command: Optional[Callable] = None, **kwargs):
        """
        Inicializa un botón primario.
        
        Args:
            parent: Widget padre
            text: Texto del botón
            command: Función a ejecutar al hacer clic
            **kwargs: Argumentos adicionales para el botón
        """
        super().__init__(parent, text=text, command=command, **kwargs)
        # Aquí se pueden aplicar estilos personalizados


class EntradaTexto(ttk.Frame):
    """
    Campo de entrada de texto con etiqueta.
    Componente que agrupa una etiqueta y un campo de entrada.
    """
    
    def __init__(self, parent, label: str, **kwargs):
        """
        Inicializa un campo de entrada con etiqueta.
        
        Args:
            parent: Widget padre
            label: Texto de la etiqueta
            **kwargs: Argumentos adicionales
        """
        super().__init__(parent)
        
        # Etiqueta
        self.label = ttk.Label(self, text=label)
        self.label.pack(side=tk.TOP, anchor=tk.W, pady=(0, 5))
        
        # Campo de entrada
        self.entry = ttk.Entry(self, **kwargs)
        self.entry.pack(side=tk.TOP, fill=tk.X)
    
    def get(self) -> str:
        """
        Obtiene el valor del campo.
        
        Returns:
            Texto ingresado
        """
        return self.entry.get()
    
    def set(self, value: str):
        """
        Establece el valor del campo.
        
        Args:
            value: Valor a establecer
        """
        self.entry.delete(0, tk.END)
        self.entry.insert(0, value)
    
    def clear(self):
        """Limpia el campo de entrada"""
        self.entry.delete(0, tk.END)


class PanelMensaje(ttk.Frame):
    """
    Panel para mostrar mensajes informativos.
    Componente que muestra mensajes de éxito, error, etc.
    """
    
    def __init__(self, parent):
        """
        Inicializa el panel de mensajes.
        
        Args:
            parent: Widget padre
        """
        super().__init__(parent)
        
        # Label para mostrar mensajes
        self.label = ttk.Label(self, text="", wraplength=400)
        self.label.pack(pady=10)
        
        # Ocultar por defecto
        self.pack_forget()
    
    def mostrar(self, mensaje: str, tipo: str = "info"):
        """
        Muestra un mensaje.
        
        Args:
            mensaje: Texto del mensaje
            tipo: Tipo de mensaje (info, error, success)
        """
        self.label.config(text=mensaje)
        
        # Aplicar colores según el tipo (simplificado)
        if tipo == "error":
            self.label.config(foreground="red")
        elif tipo == "success":
            self.label.config(foreground="green")
        else:
            self.label.config(foreground="black")
        
        # Mostrar el panel
        self.pack(pady=10)
    
    def ocultar(self):
        """Oculta el panel de mensajes"""
        self.pack_forget()
