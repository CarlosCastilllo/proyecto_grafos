import networkx as nx
from typing import Dict, List, Tuple

class WaterNetwork:
    def __init__(self):
        self.graph = nx.Graph()
        self.capacities = {}
        self.obstructions = {}
        self.neighborhoods = {}
        self.flows = {}
        self.tank_levels = {}
        
    def add_node(self, node_id: str, node_type: str, houses: int = None) -> bool:
        try:
            self.graph.add_node(node_id, type=node_type)
            if node_type == 'barrio':
                self.neighborhoods[node_id] = houses or 6
            return True
        except Exception as e:
            return False
            
    def add_pipe(self, source: str, target: str, capacity: float) -> bool:
        try:
            self.graph.add_edge(source, target)
            self.capacities[(source, target)] = capacity
            self.capacities[(target, source)] = capacity
            self.obstructions[(source, target)] = 0
            self.obstructions[(target, source)] = 0
            return True
        except Exception as e:
            return False