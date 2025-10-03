"""
Punto de entrada principal de la aplicación Orbita-CodeCaster.

Este archivo inicializa todas las capas de la aplicación:
1. Backend (servicios y lógica de negocio)
2. Presentación (presenters que conectan backend y frontend)
3. Frontend (interfaz gráfica con Tkinter)

Arquitectura:
┌─────────────────────────────────────────────┐
│            FRONTEND (Tkinter)               │
│  - views.py: Vistas/Pantallas               │
│  - components.py: Componentes reutilizables │
└──────────────────┬──────────────────────────┘
                   │ Eventos de UI
                   ▼
┌─────────────────────────────────────────────┐
│         PRESENTATION (Presenters)           │
│  - presenters.py: Conecta Vista y Backend   │
└──────────────────┬──────────────────────────┘
                   │ Llamadas a lógica
                   ▼
┌─────────────────────────────────────────────┐
│           BACKEND (Lógica)                  │
│  - services.py: Servicios de negocio        │
│  - use_cases.py: Casos de uso               │
│  - models.py: Modelos de datos              │
└─────────────────────────────────────────────┘

Esta separación permite:
- Desarrolladores de frontend pueden trabajar en la UI sin tocar lógica
- Desarrolladores de backend pueden trabajar en servicios sin tocar UI
- Fácil testing de cada capa por separado
- Escalabilidad y mantenibilidad
"""

from src.config.settings import active_config
from src.backend.services import UsuarioService, MensajeService
from src.presentation.presenters import EjemploPresenter
from src.frontend.views import VentanaPrincipal, VistaEjemplo


def inicializar_backend():
    """
    Inicializa la capa de backend.
    Crea todos los servicios necesarios.
    
    Returns:
        Tupla con los servicios inicializados
    """
    print("⚙️  Inicializando Backend...")
    
    # Crear servicios
    usuario_service = UsuarioService()
    mensaje_service = MensajeService()
    
    print("✓ Backend inicializado correctamente")
    
    return usuario_service, mensaje_service


def inicializar_presentacion(usuario_service, mensaje_service):
    """
    Inicializa la capa de presentación.
    Crea los presenters que conectan frontend con backend.
    
    Args:
        usuario_service: Servicio de usuarios
        mensaje_service: Servicio de mensajes
        
    Returns:
        Tupla con los presenters inicializados
    """
    print("⚙️  Inicializando Capa de Presentación...")
    
    # Crear presenters
    ejemplo_presenter = EjemploPresenter(usuario_service, mensaje_service)
    
    print("✓ Capa de Presentación inicializada correctamente")
    
    return ejemplo_presenter,


def inicializar_frontend(presenters):
    """
    Inicializa la capa de frontend.
    Crea la ventana principal y las vistas.
    
    Args:
        presenters: Tupla con los presenters
        
    Returns:
        Ventana principal de la aplicación
    """
    print("⚙️  Inicializando Frontend...")
    
    ejemplo_presenter = presenters[0]
    
    # Crear ventana principal
    ventana = VentanaPrincipal(
        titulo=active_config.APP_NAME,
        ancho=active_config.WINDOW_WIDTH,
        alto=active_config.WINDOW_HEIGHT
    )
    
    # Crear vistas
    vista_ejemplo = VistaEjemplo(ventana.frame_principal)
    
    # Vincular vistas con presenters
    ejemplo_presenter.vincular_vista(vista_ejemplo)
    
    # Agregar vistas a la ventana
    ventana.agregar_vista("ejemplo", vista_ejemplo)
    
    # Mostrar vista inicial
    ventana.mostrar_vista("ejemplo")
    
    print("✓ Frontend inicializado correctamente")
    
    return ventana


def main():
    """
    Función principal que arranca la aplicación.
    Sigue el patrón de inicialización en capas.
    """
    print("=" * 50)
    print(f"🚀 Iniciando {active_config.APP_NAME} v{active_config.VERSION}")
    print("=" * 50)
    
    try:
        # 1. Inicializar Backend
        usuario_service, mensaje_service = inicializar_backend()
        
        # 2. Inicializar Presentación
        presenters = inicializar_presentacion(usuario_service, mensaje_service)
        
        # 3. Inicializar Frontend
        ventana = inicializar_frontend(presenters)
        
        print("=" * 50)
        print("✓ Aplicación iniciada correctamente")
        print("=" * 50)
        print()
        
        # 4. Ejecutar la aplicación (loop principal)
        ventana.ejecutar()
        
    except Exception as e:
        print(f"❌ Error al iniciar la aplicación: {e}")
        raise


if __name__ == "__main__":
    main()
