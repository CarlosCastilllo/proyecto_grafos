from matplotlib.patches import Rectangle, Circle
import matplotlib.colors as mcolors
from typing import Tuple, Dict, Optional
import numpy as np

class NeighborhoodWidget:
    """Widget para representar barrios en la visualización"""
    
    def __init__(self, ax):
        self.ax = ax
        self.houses = {}  # Almacena las casas por barrio
        self.consumption_indicators = {}  # Almacena indicadores de consumo
        
    def draw(self, position: Tuple[float, float], name: str,
            num_houses: int = 6, consumption: float = 0,
            pressure: float = 100, highlighted: bool = False) -> None:
        """
        Dibuja un barrio con sus casas y consumo
        
        Args:
            position: Coordenadas (x, y) del centro del barrio
            name: Nombre del barrio
            num_houses: Número de casas en el barrio
            consumption: Consumo actual de agua
            pressure: Presión actual en el barrio
            highlighted: Si el barrio está resaltado
        """
        x, y = position
        
        # Dibujar área del barrio
        self._draw_neighborhood_area(x, y, highlighted)
        
        # Dibujar casas
        self._draw_houses(x, y, num_houses)
        
        # Dibujar indicadores
        self._draw_consumption_indicator(x, y, consumption)
        self._draw_pressure_indicator(x, y, pressure)
        
        # Agregar etiqueta
        self._add_label(x, y, name, num_houses, consumption, pressure)
    
    def _draw_neighborhood_area(self, x: float, y: float, 
                              highlighted: bool) -> None:
        """Dibuja el área base del barrio"""
        # Tamaño base del barrio
        width = 1.0
        height = 0.8
        
        # Estilo basado en si está resaltado
        style = {
            'facecolor': 'yellow' if highlighted else 'lightgreen',
            'edgecolor': 'gold' if highlighted else 'darkgreen',
            'alpha': 0.8 if highlighted else 0.6,
            'linewidth': 2 if highlighted else 1
        }
        
        # Crear y agregar el rectángulo base
        rect = Rectangle(
            (x - width/2, y - height/2),
            width, height,
            **style
        )
        self.ax.add_patch(rect)
        
        # Agregar borde decorativo
        self._add_decorative_border(x, y, width, height)
    
    def _draw_houses(self, x: float, y: float, num_houses: int) -> None:
        """Dibuja las casas en el barrio"""
        # Calcular disposición de las casas
        rows = 2
        cols = (num_houses + 1) // 2
        house_size = 0.15
        
        for i in range(num_houses):
            row = i % rows
            col = i // rows
            
            # Calcular posición de la casa
            hx = x - (cols-1)*house_size + col*2*house_size
            hy = y - house_size/2 + row*house_size
            
            self._draw_house(hx, hy, house_size)
    
    def _draw_house(self, x: float, y: float, size: float) -> None:
        """Dibuja una casa individual"""
        # Base de la casa
        rect = Rectangle(
            (x - size/2, y - size/2),
            size, size,
            facecolor='white',
            edgecolor='gray',
            alpha=0.8
        )
        self.ax.add_patch(rect)
        
        # Techo
        roof_height = size * 0.4
        self.ax.plot(
            [x - size/2, x, x + size/2],
            [y + size/2, y + size/2 + roof_height, y + size/2],
            color='brown',
            linewidth=2
        )
    
    def _draw_consumption_indicator(self, x: float, y: float,
                                 consumption: float) -> None:
        """Dibuja el indicador de consumo de agua"""
        indicator_x = x + 0.6
        max_height = 0.3
        height = max_height * (consumption / 100)
        
        # Barra de fondo
        rect_bg = Rectangle(
            (indicator_x - 0.05, y - max_height/2),
            0.1, max_height,
            facecolor='lightgray',
            edgecolor='gray',
            alpha=0.5
        )
        self.ax.add_patch(rect_bg)
        
        # Barra de consumo
        rect_consumption = Rectangle(
            (indicator_x - 0.05, y - max_height/2),
            0.1, height,
            facecolor=self._get_consumption_color(consumption),
            edgecolor='none',
            alpha=0.8
        )
        self.ax.add_patch(rect_consumption)
    
    def _draw_pressure_indicator(self, x: float, y: float,
                              pressure: float) -> None:
        """Dibuja el indicador de presión"""
        circle = Circle(
            (x - 0.6, y),
            0.15,
            facecolor=self._get_pressure_color(pressure),
            edgecolor='gray',
            alpha=0.8
        )
        self.ax.add_patch(circle)
        
        # Agregar valor numérico
        self.ax.text(
            x - 0.6, y,
            f"{int(pressure)}",
            ha='center',
            va='center',
            color='white',
            fontweight='bold',
            fontsize=8
        )
    
    def _add_label(self, x: float, y: float, name: str,
                  num_houses: int, consumption: float,
                  pressure: float) -> None:
        """Agrega la etiqueta con información del barrio"""
        label_text = (
            f"{name}\n"
            f"{num_houses} casas\n"
            f"Consumo: {consumption:.1f}%\n"
            f"Presión: {pressure:.1f}"
        )
        
        self.ax.text(
            x, y + 0.5,
            label_text,
            ha='center',
            va='bottom',
            fontsize=9,
            bbox=dict(
                facecolor='white',
                edgecolor='none',
                alpha=0.7,
                pad=2
            )
        )
    
    def _add_decorative_border(self, x: float, y: float,
                             width: float, height: float) -> None:
        """Agrega un borde decorativo al barrio"""
        # Puntos para el borde decorativo
        border_points = np.array([
            [x - width/2, y - height/2],  # Esquina inferior izquierda
            [x + width/2, y - height/2],  # Esquina inferior derecha
            [x + width/2, y + height/2],  # Esquina superior derecha
            [x - width/2, y + height/2],  # Esquina superior izquierda
            [x - width/2, y - height/2]   # Cerrar el path
        ])
        
        # Dibujar borde con línea punteada
        self.ax.plot(
            border_points[:, 0],
            border_points[:, 1],
            'k--',
            linewidth=1,
            alpha=0.5
        )
    
    @staticmethod
    def _get_consumption_color(consumption: float) -> str:
        """Determina el color basado en el consumo"""
        if consumption > 90:
            return 'red'
        elif consumption > 70:
            return 'orange'
        elif consumption > 40:
            return 'yellow'
        else:
            return 'green'
    
    @staticmethod
    def _get_pressure_color(pressure: float) -> str:
        """Determina el color basado en la presión"""
        if pressure < 30:
            return 'red'
        elif pressure < 50:
            return 'orange'
        elif pressure < 70:
            return 'yellow'
        else:
            return 'green'