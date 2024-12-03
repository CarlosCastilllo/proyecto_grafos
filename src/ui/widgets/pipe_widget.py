import numpy as np
from matplotlib.patches import PathPatch
import matplotlib.path as mpath
from matplotlib.collections import PatchCollection
import matplotlib.colors as mcolors
from typing import Tuple, Dict, Optional

class PipeWidget:
    """Widget para representar tuberías en la visualización"""
    
    def __init__(self, ax):
        self.ax = ax
        self.flow_animations = {}
        self.patches = {}
        
    def draw(self, start: Tuple[float, float], end: Tuple[float, float],
            flow: float = 0, capacity: float = 100, 
            obstruction: float = 0, highlighted: bool = False) -> None:
        """
        Dibuja una tubería con efectos visuales
        
        Args:
            start: Coordenadas de inicio (x, y)
            end: Coordenadas de fin (x, y)
            flow: Flujo actual
            capacity: Capacidad máxima
            obstruction: Porcentaje de obstrucción
            highlighted: Si la tubería está resaltada
        """
        x1, y1 = start
        x2, y2 = end
        
        # Crear geometría de la tubería
        pipe_path = self._create_pipe_path(x1, y1, x2, y2)
        
        # Determinar estilo visual
        style = self._get_pipe_style(flow, capacity, obstruction, highlighted)
        
        # Crear y agregar el patch
        pipe_patch = PathPatch(
            pipe_path,
            facecolor=style['fill_color'],
            edgecolor=style['edge_color'],
            linewidth=style['line_width'],
            alpha=style['alpha']
        )
        self.ax.add_patch(pipe_patch)
        
        # Agregar indicadores de flujo si es necesario
        if flow != 0:
            self._add_flow_indicators(x1, y1, x2, y2, flow, capacity)
            
        # Agregar indicadores de obstrucción si es necesario
        if obstruction > 0:
            self._add_obstruction_indicators(x1, y1, x2, y2, obstruction)
    
    def _create_pipe_path(self, x1: float, y1: float, 
                         x2: float, y2: float) -> mpath.Path:
        """Crea el path geométrico de la tubería"""
        # Calcular vectores de dirección y normales
        dx = x2 - x1
        dy = y2 - y1
        length = np.sqrt(dx*dx + dy*dy)
        nx = -dy/length * 0.1  # Grosor de la tubería
        ny = dx/length * 0.1
        
        # Crear el path
        path_data = [
            (mpath.Path.MOVETO, (x1+nx, y1+ny)),
            (mpath.Path.LINETO, (x2+nx, y2+ny)),
            (mpath.Path.LINETO, (x2-nx, y2-ny)),
            (mpath.Path.LINETO, (x1-nx, y1-ny)),
            (mpath.Path.CLOSEPOLY, (x1+nx, y1+ny)),
        ]
        codes, verts = zip(*path_data)
        return mpath.Path(verts, codes)
    
    def _get_pipe_style(self, flow: float, capacity: float,
                       obstruction: float, highlighted: bool) -> Dict:
        """Determina el estilo visual de la tubería"""
        # Calcular utilización
        utilization = abs(flow) / capacity if capacity > 0 else 0
        
        if highlighted:
            return {
                'fill_color': 'yellow',
                'edge_color': 'gold',
                'line_width': 2.5,
                'alpha': 0.8
            }
        elif obstruction > 0:
            return {
                'fill_color': self._get_obstruction_color(obstruction),
                'edge_color': 'darkred',
                'line_width': 2.0,
                'alpha': 0.7
            }
        else:
            return {
                'fill_color': self._get_flow_color(utilization),
                'edge_color': 'navy',
                'line_width': 2.0,
                'alpha': 0.6 + 0.4 * utilization
            }
    
    def _get_flow_color(self, utilization: float) -> str:
        """Determina el color basado en la utilización"""
        if utilization > 0.9:
            return 'red'
        elif utilization > 0.7:
            return 'orange'
        elif utilization > 0.4:
            return 'royalblue'
        else:
            return 'lightblue'
    
    def _get_obstruction_color(self, obstruction: float) -> str:
        """Determina el color basado en la obstrucción"""
        if obstruction > 75:
            return 'darkred'
        elif obstruction > 50:
            return 'red'
        elif obstruction > 25:
            return 'orange'
        else:
            return 'yellow'
    
    def _add_flow_indicators(self, x1: float, y1: float,
                           x2: float, y2: float,
                           flow: float, capacity: float) -> None:
        """Agrega indicadores de dirección y magnitud del flujo"""
        # Calcular puntos para las flechas
        dx = x2 - x1
        dy = y2 - y1
        length = np.sqrt(dx*dx + dy*dy)
        
        # Determinar número de flechas basado en la longitud
        num_arrows = max(1, int(length / 0.5))
        
        # Crear flechas
        for i in range(num_arrows):
            t = (i + 1) / (num_arrows + 1)
            x = x1 + t * dx
            y = y1 + t * dy
            
            # Tamaño y color de la flecha
            arrow_size = 0.1 * min(1.0, abs(flow) / capacity)
            arrow_color = self._get_flow_color(abs(flow) / capacity)
            
            # Dibujar flecha
            if flow > 0:
                self.ax.arrow(x, y, dx/length*0.2, dy/length*0.2,
                            head_width=arrow_size,
                            head_length=arrow_size*1.5,
                            fc=arrow_color, ec=arrow_color,
                            alpha=0.8)
            else:
                self.ax.arrow(x, y, -dx/length*0.2, -dy/length*0.2,
                            head_width=arrow_size,
                            head_length=arrow_size*1.5,
                            fc=arrow_color, ec=arrow_color,
                            alpha=0.8)
    
    def _add_obstruction_indicators(self, x1: float, y1: float,
                                  x2: float, y2: float,
                                  obstruction: float) -> None:
        """Agrega indicadores visuales de obstrucción"""
        # Punto medio de la tubería
        mx = (x1 + x2) / 2
        my = (y1 + y2) / 2
        
        # Tamaño del indicador basado en la obstrucción
        size = 0.15 * (obstruction / 100)
        
        # Crear símbolo de advertencia
        warning_color = self._get_obstruction_color(obstruction)
        
        # Dibujar triángulo de advertencia
        triangle = mpath.Path([
            (mx, my + size),
            (mx - size*0.866, my - size*0.5),
            (mx + size*0.866, my - size*0.5),
            (mx, my + size)
        ])
        
        warning_patch = PathPatch(
            triangle,
            facecolor=warning_color,
            edgecolor='black',
            alpha=0.8
        )
        self.ax.add_patch(warning_patch)
        
        # Agregar texto de porcentaje
        self.ax.text(mx, my, f"{int(obstruction)}%",
                    ha='center', va='center',
                    color='white',
                    fontsize=8,
                    fontweight='bold')