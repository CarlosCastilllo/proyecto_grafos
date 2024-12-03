import tkinter as tk
from tkinter import ttk, messagebox
from typing import Tuple

class PipesPanel(ttk.LabelFrame):
    def __init__(self, parent, network):
        super().__init__(parent, text="Gestión de Tuberías", padding=10)
        self.network = network
        self.create_widgets()

    def create_widgets(self):
        """Crea todos los widgets del panel"""
        # Frame principal
        frame = ttk.Frame(self)
        frame.pack(fill=tk.BOTH, expand=True)

        # Frame para agregar tuberías
        add_frame = ttk.LabelFrame(frame, text="Agregar Tubería", padding=5)
        add_frame.pack(fill=tk.X, padx=5, pady=5)

        # Frame interno para elementos de agregar
        frame_interno = ttk.Frame(add_frame)
        frame_interno.pack(fill=tk.X, padx=5, pady=5)

        # Campos para origen y destino
        ttk.Label(frame_interno, text="Origen:").grid(row=0, column=0, padx=5, pady=5)
        self.source_entry = ttk.Entry(frame_interno)
        self.source_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(frame_interno, text="Destino:").grid(row=1, column=0, padx=5, pady=5)
        self.target_entry = ttk.Entry(frame_interno)
        self.target_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Campo para capacidad
        ttk.Label(frame_interno, text="Capacidad:").grid(row=2, column=0, padx=5, pady=5)
        self.capacity_entry = ttk.Entry(frame_interno)
        self.capacity_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        self.capacity_entry.insert(0, "100")

        # Configurar el grid
        frame_interno.columnconfigure(1, weight=1)

        # Botón de agregar
        ttk.Button(frame_interno, 
                  text="➕ Agregar Tubería",
                  command=self.add_pipe).grid(
                      row=3, 
                      column=0, 
                      columnspan=2, 
                      pady=10, 
                      sticky="ew"
        )

        # Frame para eliminar tuberías
        delete_frame = ttk.LabelFrame(frame, text="Eliminar Tubería", padding=5)
        delete_frame.pack(fill=tk.X, padx=5, pady=5)

        # Frame interno para elementos de eliminación
        delete_frame_internal = ttk.Frame(delete_frame)
        delete_frame_internal.pack(fill=tk.X, padx=5, pady=5)

        # Etiqueta y combobox para selección
        ttk.Label(delete_frame_internal, 
                 text="Seleccionar tubería:").pack(fill=tk.X, pady=2)
        
        self.pipe_to_delete = ttk.Combobox(delete_frame_internal, state='readonly')
        self.pipe_to_delete.pack(fill=tk.X, pady=2)
        ttk.Button(delete_frame_internal, text=" ", command=self.delete_pipe).pack(fill=tk.X, pady=5)

        # Actualizar lista de tuberías
        self.update_pipe_list()

    def add_pipe(self):
        """Agrega una nueva tubería"""
        try:
            # Obtener valores
            source = self.source_entry.get()
            target = self.target_entry.get()
            capacity = float(self.capacity_entry.get())

            # Validar campos
            if not all([source, target]):
                raise ValueError("Origen y destino son requeridos")
            if capacity <= 0:
                raise ValueError("La capacidad debe ser mayor que 0")

            # Agregar tubería
            if self.network:
                if self.network.add_pipe(source, target, capacity):
                    messagebox.showinfo("Éxito", "Tubería agregada correctamente")
                    self.clear_fields()
                    self.update_pipe_list()
                else:
                    messagebox.showerror("Error", "No se pudo agregar la tubería")
            else:
                # Modo simulación
                messagebox.showinfo("Simulación", 
                                  f"Tubería agregada (simulado):\n"
                                  f"Origen: {source}\n"
                                  f"Destino: {target}\n"
                                  f"Capacidad: {capacity}")
                self.clear_fields()

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def update_pipe_list(self):
        """Actualiza la lista de tuberías en el combobox para eliminar"""
        # Datos de ejemplo para modo simulación
        pipes = ['A-B', 'B-C', 'C-D']
        
        # Actualizar el combobox
        if hasattr(self, 'pipe_to_delete'):
            self.pipe_to_delete['values'] = pipes
            if pipes:
                self.pipe_to_delete.set(pipes[0])
        else:
            self.pipe_to_delete.set('')

    def delete_pipe(self):
        """Elimina una tubería de la red"""
        pipe = self.pipe_to_delete.get()
        if not pipe:
            messagebox.showerror("Error", "Por favor seleccione una tubería para eliminar")
            return
    
        # Separar los nodos de la tubería seleccionada
        source, target = pipe.split('-')
        
        # Verificar si es seguro eliminar la tuberí
        
        try:
        # Remove pipe and its references
            self.network.G.remove_edge(source, target)
            del self.network.capacities[(source, target)]
            del self.network.capacities[(target, source)]
            del self.network.obstructions[(source, target)]
            del self.network.obstructions[(target, source)]
            del self.network.flows[(source, target)]
            del self.network.flows[(target, source)]
    
            self.network.update_visualization()
            self.update_pipe_list()  # Update available pipes list
            messagebox.showinfo("Success", f"Pipe between {source} and {target} successfully removed")
            self.network.log_change("Remove Pipe", f"Pipe between {source} and {target} successfully removed")
    
        except Exception as e:
            messagebox.showerror("Error", f"Error removing pipe: {str(e)}")

    def verify_safe_pipe_deletion(self, source: str, target: str) -> bool:
        """Verifica si es seguro eliminar una tubería sin afectar la conectividad crítica"""
        if not self.network:
            return True  # En modo simulación, permitir todo
        
        try:
            # Verificar con el network manager
            return self.network.verify_safe_pipe_deletion(source, target)
        except Exception as e:
            messagebox.showerror("Error", f"Error al verificar seguridad de eliminación: {str(e)}")
            return False

    def clear_fields(self):
        """Limpia los campos del formulario"""
        self.source_entry.delete(0, tk.END)
        self.target_entry.delete(0, tk.END)
        self.capacity_entry.delete(0, tk.END)
        self.capacity_entry.insert(0, "100")

    @staticmethod
    def parse_pipe_string(pipe_str: str) -> Tuple[str, str]:
        """Convierte un string de tubería en origen y destino"""
        return tuple(pipe_str.split('-'))