# 📖 GUÍA DE DESARROLLO - Orbita-CodeCaster

Esta guía te ayudará a entender cómo trabajar en cada parte de la aplicación.

## 🎯 Flujo de Trabajo por Rol

### 🎨 Desarrollador Frontend

**Tu espacio de trabajo:** `src/frontend/`

#### ¿Qué haces?

- Crear y modificar componentes visuales en `components.py`
- Diseñar vistas/pantallas en `views.py`
- Manejar eventos de UI (clicks, inputs, etc.)

#### ¿Qué NO haces?

- ❌ NO escribes lógica de negocio
- ❌ NO accedes directamente a servicios del backend
- ✅ Solo te comunicas con Presenters

#### Ejemplo: Crear un nuevo botón

```python
# src/frontend/components.py

class BotonEliminar(ttk.Button):
    """Botón para eliminar elementos"""

    def __init__(self, parent, command=None):
        super().__init__(
            parent,
            text="🗑️ Eliminar",
            command=command
        )
        # Aquí puedes agregar estilos
```

#### Ejemplo: Crear una nueva vista

```python
# src/frontend/views.py

class VistaPerfil:
    """Vista para mostrar el perfil del usuario"""

    def __init__(self, parent):
        self.frame = ttk.Frame(parent)

        # Crear componentes
        self.titulo = ttk.Label(self.frame, text="Mi Perfil")
        self.titulo.pack()

        # Panel de información
        self.info_panel = ttk.Frame(self.frame)
        self.info_panel.pack()

    def actualizar_datos(self, usuario):
        """Actualiza la vista con datos del usuario"""
        # Este método será llamado por el Presenter
        pass

    def mostrar(self):
        self.frame.pack(fill=tk.BOTH, expand=True)

    def ocultar(self):
        self.frame.pack_forget()
```

---

### 🔧 Desarrollador Backend

**Tu espacio de trabajo:** `src/backend/`

#### ¿Qué haces?

- Definir modelos de datos en `models.py`
- Implementar lógica de negocio en `services.py`
- Crear casos de uso complejos en `use_cases.py`

#### ¿Qué NO haces?

- ❌ NO importas nada de Tkinter
- ❌ NO conoces nada sobre vistas o UI
- ✅ Solo expones métodos que pueden ser llamados desde Presentation

#### Ejemplo: Crear un nuevo modelo

```python
# src/backend/models.py

@dataclass
class Proyecto:
    """Modelo de datos para un proyecto"""
    id: Optional[int] = None
    nombre: str = ""
    descripcion: str = ""
    fecha_creacion: Optional[str] = None

    def es_valido(self) -> bool:
        """Valida que el proyecto tenga datos válidos"""
        return bool(self.nombre and len(self.nombre) >= 3)
```

#### Ejemplo: Crear un nuevo servicio

```python
# src/backend/services.py

class ProyectoService:
    """Servicio para gestionar proyectos"""

    def __init__(self):
        self._proyectos: List[Proyecto] = []
        self._siguiente_id: int = 1

    def crear_proyecto(self, nombre: str, descripcion: str) -> Optional[Proyecto]:
        """Crea un nuevo proyecto"""
        proyecto = Proyecto(nombre=nombre, descripcion=descripcion)

        if not proyecto.es_valido():
            return None

        proyecto.id = self._siguiente_id
        self._siguiente_id += 1
        self._proyectos.append(proyecto)

        return proyecto

    def listar_proyectos(self) -> List[Proyecto]:
        """Lista todos los proyectos"""
        return self._proyectos.copy()
```

#### Ejemplo: Crear un caso de uso

```python
# src/backend/use_cases.py

class CrearProyectoUseCase:
    """Caso de uso: Crear un nuevo proyecto"""

    def __init__(self, proyecto_service: ProyectoService):
        self.proyecto_service = proyecto_service

    def ejecutar(self, nombre: str, descripcion: str) -> Tuple[bool, str, Optional[Proyecto]]:
        """Ejecuta el caso de uso"""
        # Validaciones
        if not nombre:
            return False, "El nombre es obligatorio", None

        # Crear proyecto
        proyecto = self.proyecto_service.crear_proyecto(nombre, descripcion)

        if not proyecto:
            return False, "Error al crear proyecto", None

        return True, "Proyecto creado exitosamente", proyecto
```

---

### 🔗 Desarrollador Fullstack (Presentation)

**Tu espacio de trabajo:** `src/presentation/`

#### ¿Qué haces?

- Crear Presenters que conecten Frontend y Backend
- Recibir eventos de la UI
- Llamar a servicios del Backend
- Actualizar las vistas con los resultados

#### ¿Qué NO haces?

- ❌ NO escribes código de Tkinter aquí
- ❌ NO implementas lógica de negocio aquí
- ✅ Solo orquestas la comunicación entre capas

#### Ejemplo: Crear un nuevo Presenter

```python
# src/presentation/presenters.py

class ProyectoPresenter(PresenterBase):
    """Presenter para la gestión de proyectos"""

    def __init__(self, proyecto_service: ProyectoService):
        super().__init__()
        self.proyecto_service = proyecto_service
        self.crear_proyecto_uc = CrearProyectoUseCase(proyecto_service)

    def manejar_crear_proyecto(self, nombre: str, descripcion: str):
        """Maneja la creación de un proyecto desde la vista"""
        # Llamar al caso de uso
        exito, mensaje, proyecto = self.crear_proyecto_uc.ejecutar(nombre, descripcion)

        # Actualizar la vista
        if self._vista:
            if exito:
                self._vista.mostrar_mensaje(mensaje, "success")
                self._vista.agregar_proyecto_a_lista(proyecto)
            else:
                self._vista.mostrar_mensaje(mensaje, "error")

    def manejar_listar_proyectos(self):
        """Obtiene la lista de proyectos para mostrar en la vista"""
        proyectos = self.proyecto_service.listar_proyectos()

        if self._vista:
            self._vista.actualizar_lista_proyectos(proyectos)
```

---

## 🔄 Flujo Completo de una Funcionalidad

### Ejemplo: Agregar funcionalidad "Guardar Configuración"

#### Paso 1: Backend (Lógica)

```python
# models.py
@dataclass
class Configuracion:
    tema: str = "claro"
    idioma: str = "es"

# services.py
class ConfiguracionService:
    def guardar(self, config: Configuracion) -> bool:
        # Lógica para guardar
        return True
```

#### Paso 2: Presentation (Conexión)

```python
# presenters.py
class ConfigPresenter:
    def manejar_guardar_config(self, tema, idioma):
        config = Configuracion(tema=tema, idioma=idioma)
        if self.config_service.guardar(config):
            self._vista.mostrar_exito()
```

#### Paso 3: Frontend (UI)

```python
# views.py
class VistaConfiguracion:
    def __init__(self, parent):
        self.boton_guardar = ttk.Button(
            parent,
            text="Guardar",
            command=self._al_guardar
        )

    def _al_guardar(self):
        # Obtener valores de la UI
        tema = self.combo_tema.get()
        idioma = self.combo_idioma.get()
        # Notificar al presenter
        self.presenter.manejar_guardar_config(tema, idioma)
```

---

## 🔌 Cómo Conectar Todo en main.py

```python
# main.py

def main():
    # 1. Crear servicios (Backend)
    proyecto_service = ProyectoService()
    config_service = ConfiguracionService()

    # 2. Crear presenters (Presentation)
    proyecto_presenter = ProyectoPresenter(proyecto_service)
    config_presenter = ConfigPresenter(config_service)

    # 3. Crear ventana y vistas (Frontend)
    ventana = VentanaPrincipal()

    vista_proyectos = VistaProyectos(ventana.frame_principal)
    vista_config = VistaConfiguracion(ventana.frame_principal)

    # 4. Vincular vistas con presenters
    proyecto_presenter.vincular_vista(vista_proyectos)
    config_presenter.vincular_vista(vista_config)

    # 5. Agregar vistas a la ventana
    ventana.agregar_vista("proyectos", vista_proyectos)
    ventana.agregar_vista("config", vista_config)

    # 6. Mostrar vista inicial
    ventana.mostrar_vista("proyectos")

    # 7. Ejecutar
    ventana.ejecutar()
```

---

## 📋 Checklist para Nuevas Funcionalidades

### ✅ Backend

- [ ] ¿Creaste el modelo en `models.py`?
- [ ] ¿Implementaste el servicio en `services.py`?
- [ ] ¿El servicio NO importa nada de Tkinter?
- [ ] ¿Creaste un caso de uso si es necesario?

### ✅ Presentation

- [ ] ¿Creaste el presenter en `presenters.py`?
- [ ] ¿El presenter recibe eventos de la vista?
- [ ] ¿El presenter llama a servicios del backend?
- [ ] ¿El presenter actualiza la vista con resultados?

### ✅ Frontend

- [ ] ¿Creaste los componentes necesarios en `components.py`?
- [ ] ¿Creaste la vista en `views.py`?
- [ ] ¿La vista NO contiene lógica de negocio?
- [ ] ¿La vista notifica al presenter de los eventos?
- [ ] ¿Agregaste la vista en `main.py`?

---

## 🚨 Errores Comunes

### ❌ Error 1: Lógica de negocio en la Vista

```python
# ❌ MAL
class MiVista:
    def guardar(self):
        # Validar email
        if "@" not in self.email.get():
            messagebox.showerror("Error")
```

```python
# ✅ BIEN
class MiVista:
    def guardar(self):
        email = self.email.get()
        # Delegar al presenter
        self.presenter.manejar_guardar(email)
```

### ❌ Error 2: Importar Tkinter en Backend

```python
# ❌ MAL - backend/services.py
import tkinter as tk
from tkinter import messagebox
```

```python
# ✅ BIEN - backend/services.py
# Sin imports de Tkinter
# Solo lógica pura de Python
```

### ❌ Error 3: Vista accediendo directamente al Backend

```python
# ❌ MAL
class MiVista:
    def __init__(self, service):
        self.service = service  # ¡NO!

    def cargar(self):
        datos = self.service.obtener_datos()  # ¡NO!
```

```python
# ✅ BIEN
class MiVista:
    def __init__(self, presenter):
        self.presenter = presenter  # SÍ

    def cargar(self):
        self.presenter.manejar_cargar_datos()  # SÍ
```

---

## 📚 Recursos Adicionales

- Documentación de Tkinter: https://docs.python.org/3/library/tkinter.html
- Arquitectura Limpia: https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html
- Dataclasses en Python: https://docs.python.org/3/library/dataclasses.html

---

**¿Tienes dudas? Revisa los ejemplos en el código o pregunta al equipo. 🚀**
