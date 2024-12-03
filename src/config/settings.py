"""
Configuraciones globales del sistema
"""

from typing import Dict, Any
from pathlib import Path

# Configuraciones de la aplicación
APP_SETTINGS: Dict[str, Any] = {
    'name': "Sistema de Distribución de Agua",
    'version': "1.0.0",
    'window_size': (1400, 900),
    'min_window_size': (1000, 700),
    'theme': 'clam',
    'language': 'es',
    'debug_mode': False
}

# Configuraciones de la red
NETWORK_SETTINGS: Dict[str, Any] = {
    'max_nodes': 100,
    'max_connections': 200,
    'default_tank_capacity': 1000,
    'default_pipe_capacity': 100,
    'min_pressure': 10,
    'max_pressure': 100,
    'default_houses': 6,
    'flow_update_interval': 100,  # ms
    'simulation_speed': 1.0,
    'max_history_length': 1000
}

# Configuraciones de visualización
VISUALIZATION_SETTINGS: Dict[str, Any] = {
    'colors': {
        'tank': {
            'fill': 'lightblue',
            'edge': 'blue',
            'highlight': 'yellow'
        },
        'neighborhood': {
            'fill': 'lightgreen',
            'edge': 'darkgreen',
            'highlight': 'yellow'
        },
        'intersection': {
            'fill': 'lightgray',
            'edge': 'gray',
            'highlight': 'yellow'
        },
        'pipe': {
            'normal': 'royalblue',
            'warning': 'orange',
            'critical': 'red',
            'blocked': 'gray'
        }
    },
    'sizes': {
        'tank': 0.3,
        'neighborhood': 0.8,
        'intersection': 0.2,
        'pipe_width': 0.1
    },
    'labels': {
        'font_size': 9,
        'font_family': 'sans-serif',
        'font_weight': 'normal'
    },
    'animation': {
        'flow_speed': 1.0,
        'transition_time': 500,
        'fps': 30
    }
}

# Configuraciones de simulación
SIMULATION_SETTINGS: Dict[str, Any] = {
    'time_step': 0.1,
    'max_simulation_time': 3600,  # segundos
    'consumption_patterns': {
        'morning': {
            'start': 6,
            'end': 9,
            'factor': 1.5
        },
        'evening': {
            'start': 18,
            'end': 21,
            'factor': 1.3
        },
        'night': {
            'start': 0,
            'end': 5,
            'factor': 0.5
        }
    },
    'pressure_limits': {
        'min_operational': 20,
        'max_operational': 80,
        'critical_low': 15,
        'critical_high': 90
    },
    'maintenance': {
        'inspection_interval': 30,  # días
        'maintenance_interval': 180,  # días
        'max_obstruction': 90,  # porcentaje
        'deterioration_rate': 0.1  # porcentaje por día
    }
}

# Configuraciones de archivos
FILE_SETTINGS: Dict[str, Any] = {
    'save_directory': Path.home() / 'water_distribution_system',
    'backup_directory': Path.home() / 'water_distribution_system' / 'backups',
    'log_directory': Path.home() / 'water_distribution_system' / 'logs',
    'max_backup_files': 5,
    'auto_save_interval': 300,  # segundos
    'file_extensions': {
        'network': '.wdn',
        'simulation': '.sim',
        'report': '.pdf'
    }
}

# Configuraciones de validación
VALIDATION_SETTINGS: Dict[str, Any] = {
    'max_pipe_length': 1000,
    'max_pipe_capacity': 1000,
    'min_pipe_capacity': 10,
    'max_houses_per_neighborhood': 20,
    'min_houses_per_neighborhood': 1,
    'required_node_types': ['tanque', 'barrio', 'interseccion'],
    'min_tanks': 1,
    'min_neighborhoods': 1,
    'max_network_size': 1000  # nodos + conexiones
}

# Configuraciones de reportes
REPORT_SETTINGS: Dict[str, Any] = {
    'company_name': "Empresa de Agua",
    'report_logo': Path(__file__).parent / 'assets' / 'logo.png',
    'default_font': 'Arial',
    'header_font_size': 14,
    'body_font_size': 11,
    'line_spacing': 1.15,
    'page_margins': (2.54, 2.54, 2.54, 2.54),  # cm
    'include_graphs': True,
    'include_statistics': True,
    'include_recommendations': True
}

# Asegurarse de que existan los directorios necesarios
for directory in [
    FILE_SETTINGS['save_directory'],
    FILE_SETTINGS['backup_directory'],
    FILE_SETTINGS['log_directory']
]:
    directory.mkdir(parents=True, exist_ok=True)