from matplotlib.patches import Circle
import numpy as np
from typing import Tuple

class TankWidget:
    """Widget para representar tanques de agua en la visualización"""
    
    def __init__(self, ax):
        self.ax = ax
    
    def draw(self, x: float, y: float, level: float, 
            name: str, radius: float = 0.3) -> None:
        """
        Dibuja un tanque de agua con nivel y etiqueta
        
        Args:
            x: Posición X del centro del tanque
            y: Posición Y del centro del tanque
            level: Nivel de agua (0-100)
            name: Nombre del tanque
            radius: Radio del tanque
        """
        # Dibujar el tanque base
        self._draw_tank_body(x, y, radius)
        
        # Dibujar el nivel de agua
        self._draw_water_level(x, y, level, radius)
        
        # Agregar etiqueta
        self._add_label(x, y, name, level, radius)
    
    def _draw_tank_body(self, x: float, y: float, radius: float) -> None:
        """Dibuja el cuerpo del tanque"""
        # Círculo principal
        circle = Circle((x, y), radius, 
                       facecolor='lightblue',
                       edgecolor='blue',
                       linewidth=2)
        self.ax.add_patch(circle)
        
        # Detalles decorativos
        self._draw_tank_details(x, y, radius)
    
    def _draw_water_level(self, x: float, y: float, 
                         level: float, radius: float) -> None:
        """Dibuja el nivel de agua con efecto de onda"""
        # Calcular altura del agua basada en el nivel
        water_height = (level/100) * (2 * radius) - radius
        
        # Crear efecto de onda
        wave_x = np.linspace(x-radius*0.8, x+radius*0.8, 100)
        amplitude = 0.05 * min(1.0, level/50)  # Amplitud variable según nivel
        wave_y = y + water_height + amplitude * np.sin(10*np.pi*(wave_x-x)/radius)
        
        # Dibujar onda
        self.ax.plot(wave_x, wave_y, color='blue', linewidth=1, alpha=0.6)
        
        # Rellenar área bajo la onda
        self.ax.fill_between(wave_x, y - radius, wave_y,
                           color='royalblue', alpha=0.3)
    
    def _draw_tank_details(self, x: float, y: float, radius: float) -> None:
        """Dibuja detalles decorativos del tanque"""
        # Borde superior reforzado
        self.ax.plot([x-radius, x+radius],
                    [y+radius, y+radius],
                    color='navy', linewidth=3)
        
        # Conectores/tuberías
        connector_width = radius * 0.3
        self.ax.plot([x-connector_width, x+connector_width],
                    [y-radius, y-radius],
                    color='navy', linewidth=4)
    
    def _add_label(self, x: float, y: float, name: str, 
                  level: float, radius: float) -> None:
        """Agrega etiqueta con nombre y nivel"""
        self.ax.text(x, y+radius*1.5,
                    f"{name}\n{level:.0f}%",
                    ha='center',
                    va='bottom',
                    fontsize=10,
                    fontweight='bold',
                    bbox=dict(
                        facecolor='white',
                        edgecolor='none',
                        alpha=0.7,
                        pad=1
                    ))