"""
Paneles de control y visualización
"""

from .nodes_panel import NodesPanel
from .pipes_panel import PipesPanel
from .flow_panel import FlowPanel
from .simulation_panel import SimulationPanel
from .history_panel import HistoryPanel
from .maintenance_panel import MaintenancePanel
from .obstructions_panel import ObstructionsPanel
from .files_panel import FilesPanel
from .routes_panel import RoutesPanel
from .optimization_panel import OptimizationPanel
from .tanks_panel import TanksPanel

__all__ = [
    'PipesPanel',
    'NodesPanel',
    'MaintenancePanel',
    'HistoryPanel',
    'FlowPanel',
    'SimulationPanel',
    'ObstructionsPanel',
    'FilesPanel',
    'RoutesPanel',
    'OptimizationPanel',
    'TanksPanel'
]
