"""
DIAGRAMA DE ARQUITECTURA - Orbita-CodeCaster

Este archivo explica visualmente cómo fluyen los datos en la aplicación.
"""

# =============================================================================
# FLUJO DE DATOS: Usuario -> Vista -> Presenter -> Backend -> Presenter -> Vista
# =============================================================================

"""
┌─────────────────────────────────────────────────────────────────────────┐
│                              USUARIO                                    │
│                         (Interactúa con la UI)                          │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
                                 │ 1. Hace click en botón
                                 │    Ingresa datos
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         CAPA FRONTEND                                   │
│                     (src/frontend/views.py)                             │
│                                                                         │
│  • Captura evento de UI                                                 │
│  • Obtiene datos de los campos                                          │
│  • NO valida lógica de negocio                                          │
│  • Llama al Presenter                                                   │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
                                 │ 2. presenter.manejar_evento(datos)
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      CAPA PRESENTATION                                  │
│                  (src/presentation/presenters.py)                       │
│                                                                         │
│  • Recibe evento y datos del frontend                                   │
│  • Decide qué hacer (qué servicio/caso de uso llamar)                   │
│  • NO tiene lógica de negocio                                           │
│  • NO tiene código de Tkinter                                           │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
                                 │ 3. service.operacion(datos)
                                 │    use_case.ejecutar(datos)
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         CAPA BACKEND                                    │
│                    (src/backend/services.py)                            │
│                    (src/backend/use_cases.py)                           │
│                                                                         │
│  • Ejecuta la lógica de negocio                                         │
│  • Valida datos según reglas del negocio                                │
│  • Manipula modelos (entities)                                          │
│  • Realiza cálculos, transformaciones                                   │
│  • NO conoce nada de Tkinter o UI                                       │
│  • Retorna resultados                                                   │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
                                 │ 4. Retorna: (éxito, mensaje, datos)
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      CAPA PRESENTATION                                  │
│                  (src/presentation/presenters.py)                       │
│                                                                         │
│  • Recibe resultado del backend                                         │
│  • Decide cómo actualizar la vista                                      │
│  • Llama a métodos de la vista para actualizar UI                       │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
                                 │ 5. vista.mostrar_resultado(datos)
                                 │    vista.actualizar_lista(datos)
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         CAPA FRONTEND                                   │
│                     (src/frontend/views.py)                             │
│                                                                         │
│  • Actualiza widgets de Tkinter                                         │
│  • Muestra mensajes al usuario                                          │
│  • Actualiza listas, campos, etc.                                       │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
                                 │ 6. Actualiza la interfaz visual
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                              USUARIO                                    │
│                        (Ve el resultado)                                │
└─────────────────────────────────────────────────────────────────────────┘
"""

# =============================================================================
# EJEMPLO CONCRETO: Usuario crea una nueva tarea
# =============================================================================

"""
PASO A PASO DEL FLUJO:

1. USUARIO: Hace click en botón "Crear Tarea"
   ↓
   
2. FRONTEND (VistaTareas._al_crear_tarea):
   ```python
   def _al_crear_tarea(self):
       titulo = self.entrada_titulo.get()
       descripcion = self.entrada_descripcion.get()
       # Delegar al Presenter
       self.presenter.manejar_crear_tarea(titulo, descripcion)
   ```
   ↓
   
3. PRESENTER (TareaPresenter.manejar_crear_tarea):
   ```python
   def manejar_crear_tarea(self, titulo, descripcion):
       # Llamar al caso de uso
       exito, mensaje, tarea = self.crear_tarea_uc.ejecutar(titulo, descripcion)
       
       # Actualizar vista según resultado
       if exito:
           self._vista.mostrar_mensaje(mensaje, "success")
           self._vista.agregar_tarea_a_lista(tarea)
       else:
           self._vista.mostrar_mensaje(mensaje, "error")
   ```
   ↓
   
4. BACKEND (CrearTareaUseCase.ejecutar):
   ```python
   def ejecutar(self, titulo, descripcion):
       # Validar
       if not titulo or len(titulo) < 3:
           return False, "Título muy corto", None
       
       # Crear tarea
       tarea = self.tarea_service.crear_tarea(titulo, descripcion)
       
       if not tarea:
           return False, "Error al crear", None
       
       return True, "Tarea creada", tarea
   ```
   ↓
   
5. PRESENTER: Recibe (True, "Tarea creada", tarea_obj)
   ↓
   
6. FRONTEND: Recibe llamada a mostrar_mensaje() y agregar_tarea_a_lista()
   ```python
   def mostrar_mensaje(self, mensaje, tipo):
       self.panel_mensaje.mostrar(mensaje, tipo)
   
   def agregar_tarea_a_lista(self, tarea):
       tarjeta = TarjetaTarea(self.frame_tareas, tarea)
       tarjeta.pack()
   ```
   ↓
   
7. USUARIO: Ve la tarea agregada en la lista + mensaje de éxito
"""

# =============================================================================
# ESTRUCTURA DE CARPETAS Y RESPONSABILIDADES
# =============================================================================

"""
src/
│
├── backend/              ← LÓGICA PURA, SIN UI
│   ├── models.py        ← Define ESTRUCTURAS de datos (Usuario, Tarea, etc.)
│   ├── services.py      ← Implementa LÓGICA de negocio (crear, editar, etc.)
│   └── use_cases.py     ← ORQUESTA servicios para casos complejos
│
├── presentation/         ← PUENTE entre Frontend y Backend
│   └── presenters.py    ← CONECTA eventos de UI con lógica de negocio
│
├── frontend/             ← INTERFAZ VISUAL, SIN LÓGICA
│   ├── components.py    ← Widgets REUTILIZABLES (botones, inputs, etc.)
│   └── views.py         ← PANTALLAS completas (ventanas, vistas)
│
└── config/               ← CONFIGURACIÓN
    └── settings.py      ← Constantes, parámetros globales
"""

# =============================================================================
# REGLAS DE ORO
# =============================================================================

"""
✅ LO QUE DEBES HACER:

1. Backend:
   ✓ Toda la lógica de negocio va aquí
   ✓ Validaciones de datos
   ✓ Cálculos y transformaciones
   ✓ Operaciones con datos
   ✓ Retornar resultados simples (bool, string, objetos)

2. Presentation:
   ✓ Capturar eventos de la vista
   ✓ Llamar servicios del backend
   ✓ Decidir qué vista actualizar y cómo
   ✓ Formatear datos del backend para la vista (si es necesario)

3. Frontend:
   ✓ Crear la interfaz visual
   ✓ Capturar interacciones del usuario
   ✓ Mostrar datos en widgets
   ✓ Notificar al Presenter de eventos
   ✓ Actualizar la UI cuando el Presenter lo indique

❌ LO QUE NO DEBES HACER:

1. Backend:
   ✗ NO importar tkinter
   ✗ NO conocer nada de la UI
   ✗ NO llamar directamente a vistas

2. Presentation:
   ✗ NO escribir código de Tkinter
   ✗ NO implementar lógica de negocio
   ✗ NO hacer validaciones complejas (eso es del backend)

3. Frontend:
   ✗ NO implementar lógica de negocio
   ✗ NO llamar directamente a servicios del backend
   ✗ NO hacer validaciones complejas
   ✗ NO hacer cálculos de negocio
"""

# =============================================================================
# BENEFICIOS DE ESTA ARQUITECTURA
# =============================================================================

"""
🎯 SEPARACIÓN DE RESPONSABILIDADES
   - Cada capa tiene un propósito único y claro
   - Fácil entender dónde va cada código

🔧 MANTENIBILIDAD
   - Cambiar la UI no afecta la lógica
   - Cambiar la lógica no afecta la UI

🤝 TRABAJO EN EQUIPO
   - Frontend dev trabaja en frontend/
   - Backend dev trabaja en backend/
   - Fullstack dev trabaja en presentation/
   - ¡Sin conflictos!

🧪 TESTING
   - Puedes testear el backend sin UI
   - Puedes testear la UI con mocks

📈 ESCALABILIDAD
   - Fácil agregar nuevas funcionalidades
   - Patrón consistente para todo

🔄 REUTILIZACIÓN
   - Componentes reutilizables
   - Servicios reutilizables
   - Lógica centralizada
"""

# =============================================================================
# ¿DÓNDE VA MI CÓDIGO?
# =============================================================================

"""
PREGÚNTATE:

"¿Este código tiene lógica de negocio?"
└─ SÍ  → backend/services.py o backend/use_cases.py
└─ NO  → Sigue preguntando...

"¿Este código es código de Tkinter/UI?"
└─ SÍ  → frontend/views.py o frontend/components.py
└─ NO  → Sigue preguntando...

"¿Este código conecta la UI con la lógica?"
└─ SÍ  → presentation/presenters.py

"¿Este código es un dato/estructura?"
└─ SÍ  → backend/models.py

"¿Este código es una configuración?"
└─ SÍ  → config/settings.py
"""

print(__doc__)
