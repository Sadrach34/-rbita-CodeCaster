# Orbita-CodeCaster

Aplicación de escritorio desarrollada con Tkinter siguiendo principios de arquitectura limpia.

ÓRBITA (Codecasters) es un visualizador de escritorio (Python/Tkinter) para el desafío NASA Bloomwatch. Monitorea y predice la floración global. Usamos Datos de Observación Terrestre (EO) de la NASA en un mapa dinámico para detectar cambios fenológicos, ofreciendo información vital sobre ciclos de vida vegetal, salud de cultivos y fuentes de polen.

## 📁 Estructura del Proyecto

```
Orbita-CodeCaster/
├── main.py                      # Punto de entrada de la aplicación
├── requirements.txt             # Dependencias del proyecto
├── README.md                    # Este archivo
└── src/                         # Código fuente
    ├── __init__.py
    ├── backend/                 # 🔧 BACKEND: Lógica de negocio
    │   ├── __init__.py
    │   ├── models.py           # Modelos de datos (Entities)
    │   ├── services.py         # Servicios (Business Logic)
    │   └── use_cases.py        # Casos de uso (Use Cases)
    ├── presentation/            # 🔗 PRESENTACIÓN: Conecta Frontend y Backend
    │   ├── __init__.py
    │   └── presenters.py       # Presenters/Controllers
    ├── frontend/                # 🎨 FRONTEND: Interfaz de usuario
    │   ├── __init__.py
    │   ├── views.py            # Vistas/Pantallas
    │   └── components.py       # Componentes reutilizables
    └── config/                  # ⚙️ CONFIGURACIÓN
        ├── __init__.py
        └── settings.py         # Configuraciones de la app
```

## 🏗️ Arquitectura

La aplicación sigue el patrón de **Arquitectura Limpia** con separación clara de responsabilidades:

### 1. **Backend** (Lógica de Negocio)

- **NO conoce nada de Tkinter o UI**
- Contiene toda la lógica de negocio
- Componentes:
  - `models.py`: Define las entidades del dominio
  - `services.py`: Implementa la lógica de negocio
  - `use_cases.py`: Orquesta operaciones complejas

### 2. **Presentation** (Capa Intermedia)

- Conecta Frontend con Backend
- Recibe eventos de la UI
- Llama a los servicios del backend
- Actualiza las vistas
- **NO contiene lógica de negocio ni código de UI**

### 3. **Frontend** (Interfaz de Usuario)

- **SOLO** maneja la presentación visual con Tkinter
- **NO contiene lógica de negocio**
- Componentes:
  - `views.py`: Define las pantallas/vistas
  - `components.py`: Widgets reutilizables

## 🚀 Cómo Ejecutar

```bash
# Ejecutar la aplicación
python main.py
```

## ➕ Cómo Agregar Nuevas Funcionalidades

### Ejemplo: Agregar un nuevo módulo "Tareas"

#### 1. **Backend** (Desarrollador de Backend)

```python
# src/backend/models.py
@dataclass
class Tarea:
    id: Optional[int] = None
    titulo: str = ""
    completada: bool = False

# src/backend/services.py
class TareaService:
    def crear_tarea(self, titulo: str) -> Tarea:
        # Lógica para crear tarea
        pass

    def completar_tarea(self, id: int) -> bool:
        # Lógica para completar tarea
        pass

# src/backend/use_cases.py
class CrearTareaUseCase:
    def ejecutar(self, titulo: str):
        # Orquestar creación de tarea
        pass
```

#### 2. **Presentation** (Desarrollador Fullstack o Backend)

```python
# src/presentation/presenters.py
class TareaPresenter:
    def __init__(self, tarea_service):
        self.tarea_service = tarea_service

    def manejar_crear_tarea(self, titulo: str):
        # Llamar al backend
        tarea = self.tarea_service.crear_tarea(titulo)
        # Actualizar vista
        self._vista.actualizar_lista(tarea)
```

#### 3. **Frontend** (Desarrollador de Frontend)

```python
# src/frontend/views.py
class VistaTareas:
    def __init__(self, parent):
        # Crear interfaz
        self.lista_tareas = tk.Listbox(parent)
        self.boton_nueva = ttk.Button(
            parent,
            text="Nueva Tarea",
            command=self._al_crear_tarea
        )

    def _al_crear_tarea(self):
        # Notificar al presenter
        self.presenter.manejar_crear_tarea(titulo)

    def actualizar_lista(self, tarea):
        # Actualizar UI con nueva tarea
        pass
```

## 👥 Trabajo en Equipo

### Frontend Developer

- Trabaja en: `src/frontend/`
- Crea vistas y componentes visuales
- Solo se comunica con Presenters, nunca con Backend directamente

### Backend Developer

- Trabaja en: `src/backend/`
- Implementa lógica de negocio
- No necesita saber nada de Tkinter

### Fullstack Developer

- Trabaja en: `src/presentation/`
- Conecta Frontend y Backend
- Define la interfaz entre ambas capas

## 📝 Principios KISS Aplicados

1. **Separación clara**: Cada capa tiene una responsabilidad única
2. **Sin dependencias cruzadas**: Backend no conoce Frontend y viceversa
3. **Código comentado**: Todo está explicado en español
4. **Componentes pequeños**: Cada archivo tiene un propósito específico
5. **Escalable**: Fácil agregar nuevas funcionalidades

## 🔧 Tecnologías

- **Python 3.8+**
- **Tkinter** (incluido en Python)
- Sin dependencias externas adicionales (por ahora)

## 📚 Conceptos Importantes

### Modelo de Datos (Entity)

Representa un objeto del dominio (Usuario, Tarea, Mensaje, etc.)

### Servicio (Service)

Contiene la lógica de negocio para operar con las entidades

### Caso de Uso (Use Case)

Orquesta múltiples servicios para realizar una operación compleja

### Presenter

Captura eventos de UI, llama al backend, actualiza la vista

### Vista (View)

Presenta datos al usuario y captura sus interacciones

### Componente (Component)

Widget reutilizable de UI

---

**¡Happy Coding! 🚀**
