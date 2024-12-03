from typing import Dict, List, Tuple, Optional
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, PathPatch
import matplotlib.path as mpath
import matplotlib.colors as mcolors
import numpy as np

class NetworkGraph:
    """Clase para manejar la visualización y operaciones del grafo de la red"""
    
    def __init__(self, ax):
        self.ax = ax
        self.node_positions: Dict[str, Tuple[float, float]] = {}
        
    def calculate_layout(self, G: nx.Graph) -> Dict[str, Tuple[float, float]]:
        """Calcula las posiciones óptimas de los nodos"""
        positions = {}
        
        # Separar nodos por tipo
        tanks = [n for n, attr in G.nodes(data=True) if attr['tipo'] == 'tanque']
        neighborhoods = [n for n, attr in G.nodes(data=True) if attr['tipo'] == 'barrio']
        intersections = [n for n, attr in G.nodes(data=True) if attr['tipo'] == 'interseccion']
        
        # Posicionar tanques en la parte superior
        for i, tank in enumerate(tanks):
            x = -4 + (8 * i/(len(tanks) if len(tanks) > 1 else 1))
            positions[tank] = (x, 6)
        
        # Posicionar intersecciones en el medio
        for i, intersection in enumerate(intersections):
            x = -4 + (8 * i/(len(intersections) if len(intersections) > 1 else 1))
            positions[intersection] = (x, 0)
        
        # Posicionar barrios en la parte inferior
        for i, neighborhood in enumerate(neighborhoods):
            x = -4 + (8 * i/(len(neighborhoods) if len(neighborhoods) > 1 else 1))
            positions[neighborhood] = (x, -6)
            
        return positions
    
    def draw_pipe(self, x1: float, y1: float, x2: float, y2: float, 
                  flow: float = 0, obstruction: float = 0, is_route: bool = False) -> None:
        """Dibuja una tubería con efectos visuales"""
        # Calcular vectores de dirección y normales
        dx = x2 - x1
        dy = y2 - y1
        length = np.sqrt(dx*dx + dy*dy)
        nx = -dy/length * 0.05
        ny = dx/length * 0.05
        
        # Crear el path para la tubería
        path_data = [
            (mpath.Path.MOVETO, (x1+nx, y1+ny)),
            (mpath.Path.LINETO, (x2+nx, y2+ny)),
            (mpath.Path.LINETO, (x2-nx, y2-ny)),
            (mpath.Path.LINETO, (x1-nx, y1-ny)),
            (mpath.Path.CLOSEPOLY, (x1+nx, y1+ny)),
        ]
        codes, verts = zip(*path_data)
        path = mpath.Path(verts, codes)
        
        # Determinar color y estilo
        color = self._get_pipe_color(flow, obstruction, is_route)
        patch = PathPatch(path, facecolor=color['fill'], 
                         edgecolor=color['edge'],
                         alpha=color['alpha'],
                         linewidth=color['width'])
        self.ax.add_patch(patch)
        
        # Dibujar indicadores de flujo si es necesario
        if flow != 0:
            self._draw_flow_indicators(x1, y1, x2, y2, flow)
    
    def _get_pipe_color(self, flow: float, obstruction: float, 
                       is_route: bool) -> Dict[str, any]:
        """Determina los colores y estilos de la tubería"""
        if is_route:
            return {
                'fill': 'lightgreen',
                'edge': 'green',
                'alpha': 0.8,
                'width': 2.5
            }
        elif obstruction > 0:
            return {
                'fill': '#ffcccc',
                'edge': 'darkred',
                'alpha': 0.7,
                'width': 2
            }
        else:
            intensity = min(1.0, abs(flow) / 100) if flow != 0 else 0
            return {
                'fill': mcolors.to_rgba('royalblue', 0.6 + 0.4 * intensity),
                'edge': 'navy' if flow != 0 else '#808080',
                'alpha': 0.8,
                'width': 2
            }
    
    def _draw_flow_indicators(self, x1: float, y1: float, 
                            x2: float, y2: float, flow: float) -> None:
        """Dibuja indicadores de dirección y magnitud del flujo"""
        # Punto medio y vectores de dirección
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        dx, dy = x2 - x1, y2 - y1
        length = np.sqrt(dx*dx + dy*dy)
        dx_norm, dy_norm = dx/length, dy/length
        
        # Tamaño y color de la flecha
        arrow_scale = min(0.15, 0.05 + abs(flow) / 200)
        arrow_color = 'blue'
        arrow_alpha = min(1.0, 0.5 + abs(flow) / 100)
        
        # Dibujar flecha
        if flow > 0:
            self.ax.arrow(mx-dx_norm*0.2, my-dy_norm*0.2,
                         dx_norm*0.4, dy_norm*0.4,
                         head_width=arrow_scale,
                         head_length=arrow_scale*1.5,
                         fc=arrow_color, ec=arrow_color,
                         alpha=arrow_alpha,
                         length_includes_head=True)