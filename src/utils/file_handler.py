import json
from typing import Dict, Any
from models.network import WaterNetwork

class NetworkFileHandler:
    @staticmethod
    def load_network(filename: str, network: WaterNetwork) -> bool:
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            if not NetworkFileHandler.validate_data(data):
                return False
                
            network.clear()
            
            # Cargar nodos
            for node in data['nodos']:
                network.add_node(
                    node['id'],
                    node['tipo'],
                    node.get('num_casas')
                )
                
            # Cargar conexiones
            for conn in data['conexiones']:
                network.add_pipe(
                    conn['origen'],
                    conn['destino'],
                    float(conn['capacidad'])
                )
                
            return True
            
        except Exception as e:
            return False
            
    @staticmethod
    def validate_data(data: Dict[str, Any]) -> bool:
        return all(key in data for key in ['nodos', 'conexiones'])