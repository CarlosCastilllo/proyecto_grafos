from typing import Dict, Any, List, Tuple, Optional
import networkx as nx
import json
from pathlib import Path

class NetworkValidator:
    """Validador para la red de distribución de agua"""
    
    @staticmethod
    def validate_network(G: nx.Graph) -> Tuple[bool, List[str]]:
        """
        Valida la estructura completa de la red
        
        Returns:
            Tuple[bool, List[str]]: (es_válido, lista_de_errores)
        """
        errors = []
        
        # Validar conectividad
        if not NetworkValidator._validate_connectivity(G):
            errors.append("La red no está completamente conectada")
            
        # Validar tipos de nodos
        node_type_errors = NetworkValidator._validate_node_types(G)
        errors.extend(node_type_errors)
        
        # Validar estructura mínima
        structure_errors = NetworkValidator._validate_minimum_structure(G)
        errors.extend(structure_errors)
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_json_data(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Valida los datos JSON para importación
        
        Returns:
            Tuple[bool, List[str]]: (es_válido, lista_de_errores)
        """
        errors = []
        
        # Validar estructura básica
        if not all(key in data for key in ['nodos', 'conexiones']):
            errors.append("Faltan campos requeridos en el JSON (nodos, conexiones)")
            return False, errors
            
        # Validar nodos
        node_errors = NetworkValidator._validate_json_nodes(data['nodos'])
        errors.extend(node_errors)
        
        # Validar conexiones
        connection_errors = NetworkValidator._validate_json_connections(
            data['conexiones'],
            [node['id'] for node in data['nodos']]
        )
        errors.extend(connection_errors)
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_pipe_parameters(capacity: float, 
                               length: float) -> Tuple[bool, Optional[str]]:
        """
        Valida los parámetros de una tubería
        
        Returns:
            Tuple[bool, Optional[str]]: (es_válido, mensaje_error)
        """
        if capacity <= 0:
            return False, "La capacidad debe ser mayor que 0"
            
        if length <= 0:
            return False, "La longitud debe ser mayor que 0"
            
        if capacity > 1000:  # Valor máximo configurable
            return False, "La capacidad excede el límite máximo permitido"
            
        if length > 1000:  # Valor máximo configurable
            return False, "La longitud excede el límite máximo permitido"
            
        return True, None
    
    @staticmethod
    def _validate_connectivity(G: nx.Graph) -> bool:
        """Valida que la red esté completamente conectada"""
        return nx.is_connected(G)
    
    @staticmethod
    def _validate_node_types(G: nx.Graph) -> List[str]:
        """Valida los tipos de nodos en la red"""
        errors = []
        valid_types = {'tanque', 'barrio', 'interseccion'}
        
        for node, attrs in G.nodes(data=True):
            if 'tipo' not in attrs:
                errors.append(f"Nodo {node} no tiene tipo definido")
            elif attrs['tipo'] not in valid_types:
                errors.append(f"Nodo {node} tiene un tipo inválido: {attrs['tipo']}")
                
        return errors
    
    @staticmethod
    def _validate_minimum_structure(G: nx.Graph) -> List[str]:
        """Valida la estructura mínima requerida"""
        errors = []
        
        # Contar tipos de nodos
        node_types = {
            'tanque': 0,
            'barrio': 0,
            'interseccion': 0
        }
        
        for _, attrs in G.nodes(data=True):
            if 'tipo' in attrs and attrs['tipo'] in node_types:
                node_types[attrs['tipo']] += 1
        
        # Validar requisitos mínimos
        if node_types['tanque'] == 0:
            errors.append("La red debe tener al menos un tanque")
        if node_types['barrio'] == 0:
            errors.append("La red debe tener al menos un barrio")
            
        return errors
    
    @staticmethod
    def _validate_json_nodes(nodes: List[Dict[str, Any]]) -> List[str]:
        """Valida la estructura de los nodos en el JSON"""
        errors = []
        node_ids = set()
        
        for node in nodes:
            # Validar campos requeridos
            if not all(key in node for key in ['id', 'tipo']):
                errors.append("Nodo con campos requeridos faltantes")
                continue
                
            # Validar ID único
            if node['id'] in node_ids:
                errors.append(f"ID de nodo duplicado: {node['id']}")
            node_ids.add(node['id'])
            
            # Validar tipo
            if node['tipo'] not in {'tanque', 'barrio', 'interseccion'}:
                errors.append(f"Tipo de nodo inválido: {node['tipo']}")
                
            # Validar campos específicos por tipo
            if node['tipo'] == 'barrio' and 'num_casas' not in node:
                errors.append(f"Falta número de casas en barrio: {node['id']}")
                
        return errors
    
    @staticmethod
    def _validate_json_connections(connections: List[Dict[str, Any]], 
                                 valid_nodes: List[str]) -> List[str]:
        """Valida la estructura de las conexiones en el JSON"""
        errors = []
        
        for conn in connections:
            # Validar campos requeridos
            if not all(key in conn for key in ['origen', 'destino', 'capacidad']):
                errors.append("Conexión con campos requeridos faltantes")
                continue
                
            # Validar nodos existentes
            if conn['origen'] not in valid_nodes:
                errors.append(f"Nodo origen no existe: {conn['origen']}")
            if conn['destino'] not in valid_nodes:
                errors.append(f"Nodo destino no existe: {conn['destino']}")
                
            # Validar capacidad
            try:
                capacidad = float(conn['capacidad'])
                if capacidad <= 0:
                    errors.append(f"Capacidad inválida en conexión: {capacidad}")
            except ValueError:
                errors.append("Capacidad no es un número válido")
                
        return errors