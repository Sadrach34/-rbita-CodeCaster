"""
Módulo para generar reportes HTML interactivos con visualizaciones embebidas.
"""
import base64
from io import BytesIO
from pathlib import Path
from datetime import datetime
import json


class GeneradorReporteHTML:
    """Genera reportes HTML interactivos con gráficos y mapas embebidos."""
    
    def __init__(self, titulo="Reporte de Predicción Temporal"):
        """
        Inicializa el generador de reportes HTML.
        
        Args:
            titulo: Título del reporte
        """
        self.titulo = titulo
        self.secciones = []
        self.graficos = []
        self.mapas = []
        self.metricas = {}
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def agregar_metrica(self, nombre, valor, descripcion="", icono="📊"):
        """
        Agrega una métrica al reporte.
        
        Args:
            nombre: Nombre de la métrica
            valor: Valor de la métrica
            descripcion: Descripción adicional
            icono: Icono emoji para la métrica
        """
        if nombre not in self.metricas:
            self.metricas[nombre] = []
        
        self.metricas[nombre].append({
            'valor': valor,
            'descripcion': descripcion,
            'icono': icono
        })
    
    def fig_a_base64(self, fig):
        """
        Convierte una figura de matplotlib a string base64.
        
        Args:
            fig: Figura de matplotlib
            
        Returns:
            String base64 de la imagen
        """
        buffer = BytesIO()
        fig.savefig(buffer, format='png', dpi=150, bbox_inches='tight', 
                   facecolor='white', edgecolor='none')
        buffer.seek(0)
        img_base64 = base64.b64encode(buffer.read()).decode()
        buffer.close()
        return img_base64
    
    def agregar_grafico(self, fig, titulo, descripcion=""):
        """
        Agrega un gráfico de matplotlib al reporte.
        
        Args:
            fig: Figura de matplotlib
            titulo: Título del gráfico
            descripcion: Descripción del gráfico
        """
        img_base64 = self.fig_a_base64(fig)
        self.graficos.append({
            'titulo': titulo,
            'descripcion': descripcion,
            'imagen': img_base64
        })
    
    def agregar_mapa_interactivo(self, ruta_mapa, titulo, descripcion=""):
        """
        Agrega un mapa HTML de folium al reporte.
        
        Args:
            ruta_mapa: Ruta al archivo HTML del mapa
            titulo: Título del mapa
            descripcion: Descripción del mapa
        """
        try:
            with open(ruta_mapa, 'r', encoding='utf-8') as f:
                contenido_mapa = f.read()
            
            self.mapas.append({
                'titulo': titulo,
                'descripcion': descripcion,
                'html': contenido_mapa
            })
        except Exception as e:
            print(f"⚠️  Error al cargar mapa {ruta_mapa}: {e}")
    
    def agregar_seccion(self, titulo, contenido, tipo="texto"):
        """
        Agrega una sección al reporte.
        
        Args:
            titulo: Título de la sección
            contenido: Contenido de la sección
            tipo: Tipo de contenido (texto, lista, tabla)
        """
        self.secciones.append({
            'titulo': titulo,
            'contenido': contenido,
            'tipo': tipo
        })
    
    def generar_css(self):
        """Genera el CSS del reporte."""
        return """
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: #333;
                line-height: 1.6;
                padding: 20px;
            }
            
            .container {
                max-width: 1400px;
                margin: 0 auto;
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                overflow: hidden;
            }
            
            .header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 40px;
                text-align: center;
            }
            
            .header h1 {
                font-size: 2.5em;
                margin-bottom: 10px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
            }
            
            .header .timestamp {
                font-size: 1em;
                opacity: 0.9;
            }
            
            .metricas-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                padding: 40px;
                background: #f8f9fa;
            }
            
            .metrica-card {
                background: white;
                padding: 25px;
                border-radius: 15px;
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
                transition: transform 0.3s ease, box-shadow 0.3s ease;
            }
            
            .metrica-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 10px 25px rgba(0,0,0,0.15);
            }
            
            .metrica-card .icono {
                font-size: 2.5em;
                margin-bottom: 10px;
            }
            
            .metrica-card .nombre {
                font-size: 0.9em;
                color: #666;
                text-transform: uppercase;
                letter-spacing: 1px;
                margin-bottom: 5px;
            }
            
            .metrica-card .valor {
                font-size: 2em;
                font-weight: bold;
                color: #667eea;
                margin-bottom: 10px;
            }
            
            .metrica-card .descripcion {
                font-size: 0.85em;
                color: #888;
            }
            
            .seccion {
                padding: 40px;
                border-bottom: 1px solid #eee;
            }
            
            .seccion:last-child {
                border-bottom: none;
            }
            
            .seccion h2 {
                color: #667eea;
                margin-bottom: 20px;
                font-size: 2em;
                display: flex;
                align-items: center;
                gap: 10px;
            }
            
            .seccion h2::before {
                content: '';
                width: 5px;
                height: 30px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 3px;
            }
            
            .grafico-container {
                background: white;
                padding: 25px;
                border-radius: 15px;
                margin-bottom: 30px;
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            }
            
            .grafico-container h3 {
                color: #333;
                margin-bottom: 10px;
                font-size: 1.5em;
            }
            
            .grafico-container .descripcion {
                color: #666;
                margin-bottom: 20px;
                font-size: 0.95em;
            }
            
            .grafico-container img {
                width: 100%;
                height: auto;
                border-radius: 10px;
            }
            
            .mapa-container {
                background: white;
                padding: 25px;
                border-radius: 15px;
                margin-bottom: 30px;
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            }
            
            .mapa-container h3 {
                color: #333;
                margin-bottom: 10px;
                font-size: 1.5em;
            }
            
            .mapa-container .descripcion {
                color: #666;
                margin-bottom: 20px;
                font-size: 0.95em;
            }
            
            .mapa-container iframe {
                width: 100%;
                height: 600px;
                border: none;
                border-radius: 10px;
            }
            
            .lista {
                list-style: none;
                padding-left: 0;
            }
            
            .lista li {
                padding: 12px 20px;
                margin-bottom: 8px;
                background: #f8f9fa;
                border-left: 4px solid #667eea;
                border-radius: 5px;
                transition: background 0.3s ease;
            }
            
            .lista li:hover {
                background: #e9ecef;
            }
            
            .tabla {
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
                border-radius: 10px;
                overflow: hidden;
            }
            
            .tabla th {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 15px;
                text-align: left;
                font-weight: 600;
            }
            
            .tabla td {
                padding: 12px 15px;
                border-bottom: 1px solid #eee;
            }
            
            .tabla tr:hover {
                background: #f8f9fa;
            }
            
            .footer {
                background: #2c3e50;
                color: white;
                text-align: center;
                padding: 30px;
                font-size: 0.9em;
            }
            
            .footer a {
                color: #667eea;
                text-decoration: none;
            }
            
            .alerta {
                padding: 15px 20px;
                border-radius: 10px;
                margin-bottom: 20px;
                display: flex;
                align-items: center;
                gap: 15px;
            }
            
            .alerta.info {
                background: #d1ecf1;
                color: #0c5460;
                border-left: 4px solid #17a2b8;
            }
            
            .alerta.success {
                background: #d4edda;
                color: #155724;
                border-left: 4px solid #28a745;
            }
            
            .alerta.warning {
                background: #fff3cd;
                color: #856404;
                border-left: 4px solid #ffc107;
            }
            
            @media (max-width: 768px) {
                .metricas-grid {
                    grid-template-columns: 1fr;
                }
                
                .header h1 {
                    font-size: 1.8em;
                }
                
                .seccion {
                    padding: 20px;
                }
            }
            
            @keyframes fadeIn {
                from {
                    opacity: 0;
                    transform: translateY(20px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            .container {
                animation: fadeIn 0.6s ease;
            }
        </style>
        """
    
    def generar_html(self, ruta_salida="data/output/reporte_completo.html"):
        """
        Genera el archivo HTML completo.
        
        Args:
            ruta_salida: Ruta donde guardar el archivo HTML
        """
        # Crear directorio si no existe
        Path(ruta_salida).parent.mkdir(parents=True, exist_ok=True)
        
        html = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.titulo}</title>
    {self.generar_css()}
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <h1>🛰️ {self.titulo}</h1>
            <p class="timestamp">Generado el: {self.timestamp}</p>
        </div>
        
        <!-- Métricas -->
        {self._generar_html_metricas()}
        
        <!-- Secciones -->
        {self._generar_html_secciones()}
        
        <!-- Gráficos -->
        {self._generar_html_graficos()}
        
        <!-- Mapas -->
        {self._generar_html_mapas()}
        
        <!-- Footer -->
        <div class="footer">
            <p>🌍 <strong>Orbita-CodeCaster</strong> - Análisis Satelital y Predicción Temporal</p>
            <p>Generado automáticamente con datos de Sentinel-2</p>
        </div>
    </div>
</body>
</html>
        """
        
        with open(ruta_salida, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"✅ Reporte HTML generado: {ruta_salida}")
        return ruta_salida
    
    def _generar_html_metricas(self):
        """Genera el HTML de las métricas."""
        if not self.metricas:
            return ""
        
        html = '<div class="metricas-grid">\n'
        
        for nombre, valores in self.metricas.items():
            for item in valores:
                html += f"""
                <div class="metrica-card">
                    <div class="icono">{item['icono']}</div>
                    <div class="nombre">{nombre}</div>
                    <div class="valor">{item['valor']}</div>
                    <div class="descripcion">{item['descripcion']}</div>
                </div>
                """
        
        html += '</div>\n'
        return html
    
    def _generar_html_secciones(self):
        """Genera el HTML de las secciones."""
        if not self.secciones:
            return ""
        
        html = ""
        for seccion in self.secciones:
            html += f'<div class="seccion">\n'
            html += f'<h2>{seccion["titulo"]}</h2>\n'
            
            if seccion['tipo'] == 'texto':
                html += f'<p>{seccion["contenido"]}</p>\n'
            elif seccion['tipo'] == 'lista':
                html += '<ul class="lista">\n'
                for item in seccion['contenido']:
                    html += f'<li>{item}</li>\n'
                html += '</ul>\n'
            elif seccion['tipo'] == 'tabla':
                html += self._generar_tabla(seccion['contenido'])
            
            html += '</div>\n'
        
        return html
    
    def _generar_html_graficos(self):
        """Genera el HTML de los gráficos."""
        if not self.graficos:
            return ""
        
        html = '<div class="seccion">\n'
        html += '<h2>📊 Visualizaciones</h2>\n'
        
        for grafico in self.graficos:
            html += f"""
            <div class="grafico-container">
                <h3>{grafico['titulo']}</h3>
                <p class="descripcion">{grafico['descripcion']}</p>
                <img src="data:image/png;base64,{grafico['imagen']}" alt="{grafico['titulo']}">
            </div>
            """
        
        html += '</div>\n'
        return html
    
    def _generar_html_mapas(self):
        """Genera el HTML de los mapas interactivos."""
        if not self.mapas:
            return ""
        
        html = '<div class="seccion">\n'
        html += '<h2>🗺️ Mapas Interactivos</h2>\n'
        
        for i, mapa in enumerate(self.mapas):
            # Crear archivo temporal para el mapa
            map_id = f"mapa_{i}"
            html += f"""
            <div class="mapa-container">
                <h3>{mapa['titulo']}</h3>
                <p class="descripcion">{mapa['descripcion']}</p>
                <div id="{map_id}" style="width: 100%; height: 600px; border-radius: 10px;">
                    {mapa['html']}
                </div>
            </div>
            """
        
        html += '</div>\n'
        return html
    
    def _generar_tabla(self, datos):
        """Genera HTML para una tabla."""
        if not datos or len(datos) == 0:
            return ""
        
        html = '<table class="tabla">\n'
        
        # Encabezados (primera fila)
        html += '<thead><tr>\n'
        for header in datos[0].keys():
            html += f'<th>{header}</th>\n'
        html += '</tr></thead>\n'
        
        # Datos
        html += '<tbody>\n'
        for fila in datos:
            html += '<tr>\n'
            for valor in fila.values():
                html += f'<td>{valor}</td>\n'
            html += '</tr>\n'
        html += '</tbody>\n'
        
        html += '</table>\n'
        return html


if __name__ == "__main__":
    # Ejemplo de uso
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
    
    reporte = GeneradorReporteHTML("Reporte de Ejemplo")
    
    # Agregar métricas
    reporte.agregar_metrica("Archivos Procesados", "33", "Imágenes Sentinel-2", "📁")
    reporte.agregar_metrica("Periodo Analizado", "6 meses", "Jul-Oct 2025", "📅")
    reporte.agregar_metrica("Precisión", "92.5%", "Modelo predictivo", "🎯")
    
    # Agregar sección
    reporte.agregar_seccion(
        "Resumen Ejecutivo",
        "Este reporte presenta el análisis de predicción temporal para la zona de Sonora.",
        "texto"
    )
    
    # Crear un gráfico de ejemplo
    fig, ax = plt.subplots(figsize=(10, 6))
    x = np.linspace(0, 10, 100)
    ax.plot(x, np.sin(x), label='NDVI')
    ax.set_xlabel('Tiempo')
    ax.set_ylabel('Valor')
    ax.set_title('Serie Temporal NDVI')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    reporte.agregar_grafico(fig, "Evolución NDVI", "Análisis temporal del índice de vegetación")
    plt.close()
    
    # Generar HTML
    reporte.generar_html()
