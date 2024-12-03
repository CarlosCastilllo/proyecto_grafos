import tkinter as tk
from tkinter import ttk, messagebox
from models.network import WaterNetwork

class NodesPanel(ttk.LabelFrame):
    def __init__(self, parent, network: WaterNetwork):
        super().__init__(parent, text="Gestión de Nodos", padding=10)
        self.network = network
        self.create_widgets()
        
    def create_widgets(self):
        # Crear widgets del panel...
        self.name_entry = ttk.Entry(self)
        self.type_combo = ttk.Combobox(
            self,
            values=['tanque', 'barrio', 'interseccion'],
            state='readonly'
        )
        # ... más widgets
        
    def add_node(self):
        name = self.name_entry.get()
        node_type = self.type_combo.get()
        houses = int(self.houses_entry.get()) if node_type == 'barrio' else None
        
        if self.network.add_node(name, node_type, houses):
            messagebox.showinfo("Éxito", "Nodo agregado correctamente")
            self.clear_fields()
        else:
            messagebox.showerror("Error", "No se pudo agregar el nodo")