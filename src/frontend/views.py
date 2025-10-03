"""
Vistas de la aplicación.
Cada vista representa una "pantalla" o sección de la interfaz.
Las vistas NO contienen lógica de negocio, solo presentan datos.
"""

import tkinter as tk
from tkinter import ttk
from typing import Protocol, List
from .components import EntradaTexto, BotonPrimario, PanelMensaje


class VistaProtocol(Protocol):
    """
    Protocolo que define qué debe implementar una vista.
    Esto ayuda a mantener consistencia entre todas las vistas.
    """
    
    def mostrar(self):
        """Muestra la vista"""
        pass
    
    def ocultar(self):
        """Oculta la vista"""
        pass


class VentanaPrincipal:
    """
    Ventana principal de la aplicación.
    Es una ventana en blanco que sirve como contenedor de otras vistas.
    """
    
    def __init__(self, titulo: str = "Orbita-CodeCaster", ancho: int = 800, alto: int = 600):
        """
        Inicializa la ventana principal.
        
        Args:
            titulo: Título de la ventana
            ancho: Ancho de la ventana en píxeles
            alto: Alto de la ventana en píxeles
        """
        # Crear la ventana raíz
        self.root = tk.Tk()
        self.root.title(titulo)
        
        # Configurar tamaño
        self.root.geometry(f"{ancho}x{alto}")
        
        # Centrar la ventana en la pantalla
        self._centrar_ventana(ancho, alto)
        
        # Frame principal que contendrá todas las vistas
        self.frame_principal = ttk.Frame(self.root, padding=10)
        self.frame_principal.pack(fill=tk.BOTH, expand=True)
        
        # Diccionario para almacenar vistas
        self._vistas = {}
        self._vista_actual = None
    
    def _centrar_ventana(self, ancho: int, alto: int):
        """
        Centra la ventana en la pantalla.
        
        Args:
            ancho: Ancho de la ventana
            alto: Alto de la ventana
        """
        # Obtener dimensiones de la pantalla
        ancho_pantalla = self.root.winfo_screenwidth()
        alto_pantalla = self.root.winfo_screenheight()
        
        # Calcular posición
        x = (ancho_pantalla - ancho) // 2
        y = (alto_pantalla - alto) // 2
        
        # Establecer posición
        self.root.geometry(f"{ancho}x{alto}+{x}+{y}")
    
    def agregar_vista(self, nombre: str, vista):
        """
        Agrega una vista al contenedor.
        
        Args:
            nombre: Nombre identificador de la vista
            vista: Instancia de la vista
        """
        self._vistas[nombre] = vista
    
    def mostrar_vista(self, nombre: str):
        """
        Muestra una vista específica y oculta la actual.
        
        Args:
            nombre: Nombre de la vista a mostrar
        """
        # Ocultar vista actual si existe
        if self._vista_actual:
            self._vista_actual.ocultar()
        
        # Mostrar nueva vista
        if nombre in self._vistas:
            self._vista_actual = self._vistas[nombre]
            self._vista_actual.mostrar()
    
    def ejecutar(self):
        """Inicia el loop principal de la aplicación"""
        self.root.mainloop()


class VistaEjemplo:
    """
    Vista de ejemplo para demostrar cómo crear vistas.
    Esta vista muestra un formulario simple.
    """
    
    def __init__(self, parent):
        """
        Inicializa la vista de ejemplo.
        
        Args:
            parent: Frame padre donde se mostrará la vista
        """
        # Frame principal de la vista
        self.frame = ttk.Frame(parent)
        
        # Título
        titulo = ttk.Label(
            self.frame,
            text="Vista de Ejemplo",
            font=("Arial", 16, "bold")
        )
        titulo.pack(pady=20)
        
        # Descripción
        descripcion = ttk.Label(
            self.frame,
            text="Esta es una ventana en blanco de ejemplo.\n"
                 "Puedes agregar tus propios componentes aquí.",
            justify=tk.CENTER
        )
        descripcion.pack(pady=10)
        
        # Separador visual
        ttk.Separator(self.frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=20)
        
        # Ejemplo de componente personalizado
        self.entrada_nombre = EntradaTexto(self.frame, "Nombre:")
        self.entrada_nombre.pack(pady=10, padx=50, fill=tk.X)
        
        # Panel de mensajes
        self.panel_mensaje = PanelMensaje(self.frame)
        
        # Botón de ejemplo
        boton = BotonPrimario(
            self.frame,
            text="Saludar",
            command=self._manejar_click
        )
        boton.pack(pady=20)
    
    def _manejar_click(self):
        """
        Maneja el evento de click del botón.
        En una aplicación real, esto llamaría al presenter/controlador.
        """
        nombre = self.entrada_nombre.get()
        if nombre:
            self.panel_mensaje.mostrar(f"¡Hola {nombre}!", "success")
        else:
            self.panel_mensaje.mostrar("Por favor ingresa un nombre", "error")
    
    def mostrar(self):
        """Muestra la vista"""
        self.frame.pack(fill=tk.BOTH, expand=True)
    
    def ocultar(self):
        """Oculta la vista"""
        self.frame.pack_forget()
