"""
Ejemplo de cómo agregar una nueva funcionalidad completa.
Este archivo muestra paso a paso cómo implementar "Gestión de Tareas".
NO es necesario ejecutar este archivo, es solo una guía de referencia.
"""

# ============================================================================
# PASO 1: BACKEND - Definir el modelo de datos
# ============================================================================
# Archivo: src/backend/models.py

from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Tarea:
    """
    Modelo de datos para una Tarea.
    Representa una tarea que el usuario puede crear.
    """
    id: Optional[int] = None
    titulo: str = ""
    descripcion: str = ""
    completada: bool = False
    fecha_creacion: Optional[str] = None
    
    def es_valida(self) -> bool:
        """Valida que la tarea tenga los datos mínimos"""
        return bool(self.titulo and len(self.titulo) >= 3)
    
    def marcar_completada(self):
        """Marca la tarea como completada"""
        self.completada = True
    
    def marcar_pendiente(self):
        """Marca la tarea como pendiente"""
        self.completada = False


# ============================================================================
# PASO 2: BACKEND - Implementar el servicio
# ============================================================================
# Archivo: src/backend/services.py

from typing import List, Optional
from .models import Tarea

class TareaService:
    """
    Servicio para gestionar tareas.
    Contiene toda la lógica de negocio relacionada con tareas.
    """
    
    def __init__(self):
        """Inicializa el servicio con almacenamiento en memoria"""
        self._tareas: List[Tarea] = []
        self._siguiente_id: int = 1
    
    def crear_tarea(self, titulo: str, descripcion: str = "") -> Optional[Tarea]:
        """
        Crea una nueva tarea.
        
        Args:
            titulo: Título de la tarea
            descripcion: Descripción opcional de la tarea
            
        Returns:
            Tarea creada o None si los datos no son válidos
        """
        # Crear tarea
        tarea = Tarea(titulo=titulo, descripcion=descripcion)
        
        # Validar
        if not tarea.es_valida():
            return None
        
        # Asignar ID y guardar
        tarea.id = self._siguiente_id
        self._siguiente_id += 1
        self._tareas.append(tarea)
        
        return tarea
    
    def obtener_todas(self) -> List[Tarea]:
        """Obtiene todas las tareas"""
        return self._tareas.copy()
    
    def obtener_por_id(self, id: int) -> Optional[Tarea]:
        """Busca una tarea por su ID"""
        for tarea in self._tareas:
            if tarea.id == id:
                return tarea
        return None
    
    def completar_tarea(self, id: int) -> bool:
        """Marca una tarea como completada"""
        tarea = self.obtener_por_id(id)
        if tarea:
            tarea.marcar_completada()
            return True
        return False
    
    def eliminar_tarea(self, id: int) -> bool:
        """Elimina una tarea"""
        for i, tarea in enumerate(self._tareas):
            if tarea.id == id:
                del self._tareas[i]
                return True
        return False
    
    def contar_tareas(self) -> dict:
        """Cuenta las tareas por estado"""
        total = len(self._tareas)
        completadas = sum(1 for t in self._tareas if t.completada)
        pendientes = total - completadas
        
        return {
            "total": total,
            "completadas": completadas,
            "pendientes": pendientes
        }


# ============================================================================
# PASO 3: BACKEND - Crear caso de uso (opcional si es complejo)
# ============================================================================
# Archivo: src/backend/use_cases.py

from typing import Tuple, Optional
from .services import TareaService
from .models import Tarea

class CrearTareaUseCase:
    """
    Caso de uso para crear una nueva tarea.
    Valida y orquesta la creación.
    """
    
    def __init__(self, tarea_service: TareaService):
        self.tarea_service = tarea_service
    
    def ejecutar(self, titulo: str, descripcion: str = "") -> Tuple[bool, str, Optional[Tarea]]:
        """
        Ejecuta la creación de una tarea.
        
        Returns:
            Tupla (éxito, mensaje, tarea_creada)
        """
        # Validaciones
        if not titulo or len(titulo.strip()) < 3:
            return False, "El título debe tener al menos 3 caracteres", None
        
        # Crear tarea
        tarea = self.tarea_service.crear_tarea(titulo.strip(), descripcion.strip())
        
        if not tarea:
            return False, "Error al crear la tarea", None
        
        return True, f"Tarea '{titulo}' creada exitosamente", tarea


# ============================================================================
# PASO 4: PRESENTATION - Crear el Presenter
# ============================================================================
# Archivo: src/presentation/presenters.py

from ..backend.services import TareaService
from ..backend.use_cases import CrearTareaUseCase

class TareaPresenter:
    """
    Presenter para la gestión de tareas.
    Conecta la vista de tareas con el backend.
    """
    
    def __init__(self, tarea_service: TareaService):
        """Inicializa el presenter con sus dependencias"""
        self._vista = None
        self.tarea_service = tarea_service
        self.crear_tarea_uc = CrearTareaUseCase(tarea_service)
    
    def vincular_vista(self, vista):
        """Vincula la vista con este presenter"""
        self._vista = vista
    
    def manejar_crear_tarea(self, titulo: str, descripcion: str = ""):
        """
        Maneja el evento de crear tarea desde la vista.
        
        Args:
            titulo: Título de la tarea
            descripcion: Descripción de la tarea
        """
        # Llamar al caso de uso
        exito, mensaje, tarea = self.crear_tarea_uc.ejecutar(titulo, descripcion)
        
        # Actualizar la vista
        if self._vista:
            if exito:
                self._vista.mostrar_mensaje(mensaje, "success")
                self._vista.agregar_tarea_a_lista(tarea)
                self._vista.limpiar_formulario()
                self._vista.actualizar_contadores()
            else:
                self._vista.mostrar_mensaje(mensaje, "error")
    
    def manejar_completar_tarea(self, tarea_id: int):
        """Maneja el evento de completar una tarea"""
        exito = self.tarea_service.completar_tarea(tarea_id)
        
        if self._vista:
            if exito:
                self._vista.actualizar_lista_tareas()
                self._vista.actualizar_contadores()
            else:
                self._vista.mostrar_mensaje("Error al completar tarea", "error")
    
    def manejar_eliminar_tarea(self, tarea_id: int):
        """Maneja el evento de eliminar una tarea"""
        exito = self.tarea_service.eliminar_tarea(tarea_id)
        
        if self._vista:
            if exito:
                self._vista.actualizar_lista_tareas()
                self._vista.actualizar_contadores()
                self._vista.mostrar_mensaje("Tarea eliminada", "success")
            else:
                self._vista.mostrar_mensaje("Error al eliminar tarea", "error")
    
    def manejar_cargar_tareas(self):
        """Carga todas las tareas para mostrar en la vista"""
        tareas = self.tarea_service.obtener_todas()
        contadores = self.tarea_service.contar_tareas()
        
        if self._vista:
            self._vista.mostrar_tareas(tareas)
            self._vista.mostrar_contadores(contadores)


# ============================================================================
# PASO 5: FRONTEND - Crear componentes específicos (si son necesarios)
# ============================================================================
# Archivo: src/frontend/components.py

import tkinter as tk
from tkinter import ttk

class TarjetaTarea(ttk.Frame):
    """
    Componente que muestra una tarea individual.
    Ejemplo de componente reutilizable y específico.
    """
    
    def __init__(self, parent, tarea, on_completar=None, on_eliminar=None):
        """
        Inicializa la tarjeta de tarea.
        
        Args:
            parent: Widget padre
            tarea: Objeto Tarea a mostrar
            on_completar: Callback cuando se completa la tarea
            on_eliminar: Callback cuando se elimina la tarea
        """
        super().__init__(parent, relief=tk.RAISED, borderwidth=1)
        self.tarea = tarea
        
        # Frame para contenido
        contenido = ttk.Frame(self)
        contenido.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Checkbox para completar
        self.var_completada = tk.BooleanVar(value=tarea.completada)
        check = ttk.Checkbutton(
            contenido,
            variable=self.var_completada,
            command=lambda: on_completar(tarea.id) if on_completar else None
        )
        check.pack(side=tk.LEFT)
        
        # Información de la tarea
        info_frame = ttk.Frame(contenido)
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        
        # Título
        titulo_label = ttk.Label(
            info_frame,
            text=tarea.titulo,
            font=("Arial", 12, "bold")
        )
        titulo_label.pack(anchor=tk.W)
        
        # Descripción si existe
        if tarea.descripcion:
            desc_label = ttk.Label(
                info_frame,
                text=tarea.descripcion,
                wraplength=300
            )
            desc_label.pack(anchor=tk.W)
        
        # Botón eliminar
        btn_eliminar = ttk.Button(
            contenido,
            text="🗑️",
            width=3,
            command=lambda: on_eliminar(tarea.id) if on_eliminar else None
        )
        btn_eliminar.pack(side=tk.RIGHT)


# ============================================================================
# PASO 6: FRONTEND - Crear la vista
# ============================================================================
# Archivo: src/frontend/views.py

import tkinter as tk
from tkinter import ttk
from .components import EntradaTexto, PanelMensaje, TarjetaTarea

class VistaTareas:
    """
    Vista para gestionar tareas.
    Muestra la lista de tareas y permite crear nuevas.
    """
    
    def __init__(self, parent):
        """Inicializa la vista de tareas"""
        self.presenter = None  # Se asignará después
        
        # Frame principal
        self.frame = ttk.Frame(parent, padding=10)
        
        # Título
        titulo = ttk.Label(
            self.frame,
            text="Gestión de Tareas",
            font=("Arial", 16, "bold")
        )
        titulo.pack(pady=(0, 20))
        
        # Panel de contadores
        self._crear_panel_contadores()
        
        # Panel de mensajes
        self.panel_mensaje = PanelMensaje(self.frame)
        
        # Formulario para nueva tarea
        self._crear_formulario()
        
        # Lista de tareas
        self._crear_lista_tareas()
    
    def _crear_panel_contadores(self):
        """Crea el panel de contadores"""
        panel = ttk.Frame(self.frame)
        panel.pack(fill=tk.X, pady=(0, 20))
        
        # Contadores
        self.label_total = ttk.Label(panel, text="Total: 0")
        self.label_total.pack(side=tk.LEFT, padx=10)
        
        self.label_pendientes = ttk.Label(panel, text="Pendientes: 0")
        self.label_pendientes.pack(side=tk.LEFT, padx=10)
        
        self.label_completadas = ttk.Label(panel, text="Completadas: 0")
        self.label_completadas.pack(side=tk.LEFT, padx=10)
    
    def _crear_formulario(self):
        """Crea el formulario para agregar tareas"""
        form_frame = ttk.LabelFrame(self.frame, text="Nueva Tarea", padding=10)
        form_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Campo título
        self.entrada_titulo = EntradaTexto(form_frame, "Título:")
        self.entrada_titulo.pack(fill=tk.X, pady=5)
        
        # Campo descripción
        self.entrada_descripcion = EntradaTexto(form_frame, "Descripción (opcional):")
        self.entrada_descripcion.pack(fill=tk.X, pady=5)
        
        # Botón crear
        btn_crear = ttk.Button(
            form_frame,
            text="➕ Crear Tarea",
            command=self._al_crear_tarea
        )
        btn_crear.pack(pady=10)
    
    def _crear_lista_tareas(self):
        """Crea el área de lista de tareas"""
        # Frame con scrollbar
        lista_frame = ttk.LabelFrame(self.frame, text="Mis Tareas", padding=10)
        lista_frame.pack(fill=tk.BOTH, expand=True)
        
        # Canvas y scrollbar
        self.canvas = tk.Canvas(lista_frame)
        scrollbar = ttk.Scrollbar(lista_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.frame_tareas = ttk.Frame(self.canvas)
        
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.canvas.create_window((0, 0), window=self.frame_tareas, anchor=tk.NW)
        self.frame_tareas.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
    
    # Métodos que serán llamados por el Presenter
    
    def _al_crear_tarea(self):
        """Maneja el evento de crear tarea"""
        if self.presenter:
            titulo = self.entrada_titulo.get()
            descripcion = self.entrada_descripcion.get()
            self.presenter.manejar_crear_tarea(titulo, descripcion)
    
    def mostrar_mensaje(self, mensaje: str, tipo: str):
        """Muestra un mensaje al usuario"""
        self.panel_mensaje.mostrar(mensaje, tipo)
    
    def agregar_tarea_a_lista(self, tarea):
        """Agrega una tarea a la lista visual"""
        tarjeta = TarjetaTarea(
            self.frame_tareas,
            tarea,
            on_completar=self._al_completar_tarea,
            on_eliminar=self._al_eliminar_tarea
        )
        tarjeta.pack(fill=tk.X, pady=5)
    
    def limpiar_formulario(self):
        """Limpia los campos del formulario"""
        self.entrada_titulo.clear()
        self.entrada_descripcion.clear()
    
    def actualizar_lista_tareas(self):
        """Recarga toda la lista de tareas"""
        if self.presenter:
            self.presenter.manejar_cargar_tareas()
    
    def actualizar_contadores(self):
        """Solicita al presenter actualizar los contadores"""
        if self.presenter:
            self.presenter.manejar_cargar_tareas()
    
    def mostrar_tareas(self, tareas):
        """Muestra una lista de tareas"""
        # Limpiar lista actual
        for widget in self.frame_tareas.winfo_children():
            widget.destroy()
        
        # Agregar tareas
        for tarea in tareas:
            self.agregar_tarea_a_lista(tarea)
    
    def mostrar_contadores(self, contadores: dict):
        """Actualiza los contadores"""
        self.label_total.config(text=f"Total: {contadores['total']}")
        self.label_pendientes.config(text=f"Pendientes: {contadores['pendientes']}")
        self.label_completadas.config(text=f"Completadas: {contadores['completadas']}")
    
    def _al_completar_tarea(self, tarea_id: int):
        """Maneja el evento de completar tarea"""
        if self.presenter:
            self.presenter.manejar_completar_tarea(tarea_id)
    
    def _al_eliminar_tarea(self, tarea_id: int):
        """Maneja el evento de eliminar tarea"""
        if self.presenter:
            self.presenter.manejar_eliminar_tarea(tarea_id)
    
    def mostrar(self):
        """Muestra la vista"""
        self.frame.pack(fill=tk.BOTH, expand=True)
        # Cargar tareas al mostrar
        if self.presenter:
            self.presenter.manejar_cargar_tareas()
    
    def ocultar(self):
        """Oculta la vista"""
        self.frame.pack_forget()


# ============================================================================
# PASO 7: INTEGRACIÓN - Conectar todo en main.py
# ============================================================================
# Archivo: main.py

"""
# Agregar en la función inicializar_backend():
tarea_service = TareaService()

# Agregar en la función inicializar_presentacion():
tarea_presenter = TareaPresenter(tarea_service)

# Agregar en la función inicializar_frontend():
vista_tareas = VistaTareas(ventana.frame_principal)
tarea_presenter.vincular_vista(vista_tareas)
ventana.agregar_vista("tareas", vista_tareas)

# Para mostrar la vista de tareas:
ventana.mostrar_vista("tareas")
"""

print("""
Este archivo es solo una GUÍA DE REFERENCIA.
Muestra cómo implementar una funcionalidad completa paso a paso.

Para usarlo:
1. Copia el código de cada sección al archivo correspondiente
2. Adapta según tus necesidades
3. Conecta todo en main.py

¡Buena suerte! 🚀
""")
