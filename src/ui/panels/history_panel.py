import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from typing import List, Dict
import json
from datetime import datetime

class HistoryPanel(ttk.LabelFrame):
    """Panel para visualización y gestión del historial"""
    
    def __init__(self, parent, network):
        super().__init__(parent, text="Historial de Flujo", padding=10)
        self.network = network
        self.history_window = None
        self.create_widgets()
        
    def create_widgets(self):
        """Crea los widgets del panel"""
        frame = ttk.Frame(self)
        frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Botones principales
        ttk.Button(frame, 
                  text="Ver Historial",
                  style='Action.TButton',
                  command=self.show_history).pack(fill=tk.X, pady=2)
        
        ttk.Button(frame,
                  text="Exportar Datos",
                  style='Action.TButton',
                  command=self.export_history).pack(fill=tk.X, pady=2)
        
        # Tabla de eventos
        self.create_history_table()
    
    def create_history_table(self):
        """Crea la tabla para mostrar el historial"""
        frame = ttk.Frame(self)
        frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Crear Treeview
        self.history_tree = ttk.Treeview(
            frame,
            columns=('Tiempo', 'Evento', 'Detalles'),
            show='headings',
            height=6
        )
        
        # Configurar columnas
        self.history_tree.heading('Tiempo', text='Tiempo')
        self.history_tree.heading('Evento', text='Evento')
        self.history_tree.heading('Detalles', text='Detalles')
        
        # Scrollbars
        vsb = ttk.Scrollbar(frame, orient="vertical", 
                           command=self.history_tree.yview)
        hsb = ttk.Scrollbar(frame, orient="horizontal",
                           command=self.history_tree.xview)
        self.history_tree.configure(yscrollcommand=vsb.set,
                                  xscrollcommand=hsb.set)
        
        # Layout
        self.history_tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)
    
    def show_history(self):
        """Muestra la ventana de historial con gráficos"""
        if self.history_window is None or not tk.Toplevel.winfo_exists(self.history_window):
            self.history_window = tk.Toplevel(self)
            self.history_window.title("Historial de Flujo")
            self.history_window.geometry("800x600")
            
            # Crear figura y canvas
            fig = Figure(figsize=(8, 6))
            ax = fig.add_subplot(111)
            canvas = FigureCanvasTkAgg(fig, master=self.history_window)
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            # Graficar datos históricos
            self.plot_history_data(ax)
            canvas.draw()
    
    def plot_history_data(self, ax):
        """Grafica los datos históricos"""
        history = self.network.get_flow_history()
        times = [entry['time'] for entry in history]
        
        # Graficar flujos para cada tubería
        for edge in self.network.graph.edges():
            flows = [entry['flows'].get(edge, 0) for entry in history]
            ax.plot(times, flows, label=f'{edge[0]}-{edge[1]}')
        
        ax.set_xlabel('Tiempo')
        ax.set_ylabel('Flujo')
        ax.legend()
        ax.grid(True)
    
    def export_history(self):
        """Exporta el historial a un archivo"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[
                ("JSON files", "*.json"),
                ("CSV files", "*.csv"),
                ("All files", "*.*")
            ]
        )
        
        if filename:
            try:
                if filename.endswith('.json'):
                    self.export_as_json(filename)
                elif filename.endswith('.csv'):
                    self.export_as_csv(filename)
                messagebox.showinfo("Éxito", "Historial exportado correctamente")
            except Exception as e:
                messagebox.showerror("Error", f"Error al exportar: {str(e)}")