import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Any
import numpy as np

class FlowPanel(ttk.LabelFrame):
    """Panel para control y visualización de flujos"""
    
    def __init__(self, parent, network):
        super().__init__(parent, text="Gestión de Flujos", padding=10)
        self.network = network
        self.create_widgets()
        
    def create_widgets(self):
        """Crea los widgets del panel"""
        # Frame para información de flujo
        info_frame = ttk.LabelFrame(self, text="Información de Flujo", padding=5)
        info_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Área de texto para mostrar información
        self.flow_text = tk.Text(info_frame, height=4, width=30)
        self.flow_text.pack(fill=tk.X, padx=5, pady=5)
        
        # Frame para selección de tubería
        pipe_frame = ttk.LabelFrame(self, text="Seleccionar Tubería", padding=5)
        pipe_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(pipe_frame, text="Tubería:").pack(fill=tk.X, pady=2)
        self.pipe_select = ttk.Combobox(pipe_frame, state='readonly')
        self.pipe_select.pack(fill=tk.X, pady=2)
        
        # Frame para bloquear/desbloquear tubería
        block_frame = ttk.LabelFrame(self, text="Bloquear/Desbloquear Tubería", padding=5)
        block_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(block_frame, text="Tubería:").pack(fill=tk.X, pady=2)
        self.pipe_to_block = ttk.Combobox(block_frame, state='readonly')
        self.pipe_to_block.pack(fill=tk.X, pady=2)
        
        # Botones de acción
        button_frame = ttk.Frame(block_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(button_frame, 
                  text="🔒 Bloquear",
                  command=self.block_pipe).pack(side=tk.LEFT, expand=True, padx=2)
        
        ttk.Button(button_frame, 
                  text="🔓 Desbloquear",
                  command=self.unblock_pipe).pack(side=tk.RIGHT, expand=True, padx=2)
        
        # Actualizar listas e información
        self.update_pipe_list()
        self.update_flow_info()
        
    def update_flow_info(self):
        """Actualiza la información de flujo mostrada"""
        if self.network is None:
            # Si no hay red, mostrar valores por defecto o limpiar la información
            self.flow_text.delete(1.0, tk.END)
            self.flow_text.insert(tk.END, "No hay red disponible")
            return

        try:
            flow_info = self.network.get_flow_info()
            self.flow_text.delete(1.0, tk.END)
            self.flow_text.insert(tk.END, flow_info)
        except Exception as e:
            self.flow_text.delete(1.0, tk.END)
            self.flow_text.insert(tk.END, f"Error al obtener información de flujo: {str(e)}")
        
    def block_pipe(self):
        """Bloquea una tubería seleccionada"""
        if self.network is None:
            messagebox.showerror("Error", "No hay red disponible")
            return
            
        pipe = self.pipe_to_block.get()
        if not pipe:
            messagebox.showerror("Error", "Por favor seleccione una tubería")
            return
            
        try:
            origen, destino = pipe.split('-')
            self.network.block_pipe(origen, destino)
            self.update_flow_info()
            messagebox.showinfo("Éxito", f"Tubería {pipe} bloqueada correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"Error al bloquear tubería: {str(e)}")

    def unblock_pipe(self):
        """Desbloquea una tubería seleccionada"""
        if self.network is None:
            messagebox.showerror("Error", "No hay red disponible")
            return
            
        pipe = self.pipe_to_block.get()
        if not pipe:
            messagebox.showerror("Error", "Por favor seleccione una tubería")
            return
            
        try:
            origen, destino = pipe.split('-')
            self.network.unblock_pipe(origen, destino)
            self.update_flow_info()
            messagebox.showinfo("Éxito", f"Tubería {pipe} desbloqueada correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"Error al desbloquear tubería: {str(e)}")
        
    def update_pipe_list(self):
        """Actualiza la lista de tuberías en los comboboxes"""
        if self.network is None:
            # Si no hay red, establecer listas vacías
            pipes = []
        else:
            try:
                pipes = [f"{u}-{v}" for u, v in self.network.get_pipes()]
            except:
                pipes = []
        
        # Actualizar los comboboxes
        for combo in [self.pipe_select]:
            combo['values'] = pipes
            if pipes:
                combo.set(pipes[0])
            else:
                combo.set('')