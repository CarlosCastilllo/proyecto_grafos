import tkinter as tk
from tkinter import ttk, messagebox

class RoutesPanel(ttk.LabelFrame):
    def __init__(self, parent, network):
        super().__init__(parent, text="Análisis de Rutas", padding=10)
        self.network = network
        self.create_widgets()

    def create_widgets(self):
        """Crea los widgets del panel"""
        frame = ttk.Frame(self)
        frame.pack(fill=tk.BOTH, expand=True)

        # Frame para selección de nodos
        select_frame = ttk.LabelFrame(frame, text="Selección de Nodos", padding=5)
        select_frame.pack(fill=tk.X, padx=5, pady=5)

        # Origen
        ttk.Label(select_frame, text="Origen:").pack(fill=tk.X, pady=2)
        self.source_combo = ttk.Combobox(select_frame, state='readonly')
        self.source_combo.pack(fill=tk.X, pady=2)

        # Destino
        ttk.Label(select_frame, text="Destino:").pack(fill=tk.X, pady=2)
        self.target_combo = ttk.Combobox(select_frame, state='readonly')
        self.target_combo.pack(fill=tk.X, pady=2)

        # Botones de análisis
        buttons_frame = ttk.Frame(frame)
        buttons_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(buttons_frame,
                  text=" ",
                  command=self.find_shortest_path).pack(fill=tk.X, pady=2)

        ttk.Button(buttons_frame,
                  text=" ",
                  command=self.analyze_capacity).pack(fill=tk.X, pady=2)

        # Frame para resultados
        results_frame = ttk.LabelFrame(frame, text="Resultados", padding=5)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Área de texto para resultados
        self.results_text = tk.Text(results_frame, height=6, wrap=tk.WORD)
        self.results_text.pack(fill=tk.BOTH, expand=True, pady=5)

        # Actualizar listas de nodos
        self.update_node_lists()

    def find_shortest_path(self):
        """Busca la ruta más corta entre origen y destino"""
        try:
            source = self.source_combo.get()
            target = self.target_combo.get()

            if not all([source, target]):
                raise ValueError("Seleccione origen y destino")

            if self.network:
                path = self.network.find_shortest_path(source, target)
                if path:
                    self.show_results(
                        "Ruta más corta encontrada:\n" +
                        " → ".join(path)
                    )
                else:
                    self.show_results("No se encontró una ruta")
            else:
                # Simulación
                self.show_results(
                    "Ruta simulada:\n"
                    f"{source} → B → C → {target}"
                )

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def analyze_capacity(self):
        """Analiza la capacidad de flujo entre origen y destino"""
        try:
            source = self.source_combo.get()
            target = self.target_combo.get()

            if not all([source, target]):
                raise ValueError("Seleccione origen y destino")

            if self.network:
                capacity = self.network.analyze_flow_capacity(source, target)
                self.show_results(
                    f"Capacidad máxima de flujo: {capacity} unidades\n"
                    f"Estado: {'Óptimo' if capacity > 0 else 'Limitado'}"
                )
            else:
                # Simulación
                self.show_results(
                    "Análisis simulado:\n"
                    f"Capacidad máxima: 100 unidades\n"
                    "Estado: Óptimo"
                )

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def update_node_lists(self):
        """Actualiza las listas de nodos en los combobox"""
        if self.network:
            nodes = list(self.network.graph.nodes())
        else:
            nodes = ['A', 'B', 'C', 'D']  # Simulación

        self.source_combo['values'] = nodes
        self.target_combo['values'] = nodes

    def show_results(self, text):
        """Muestra resultados en el área de texto"""
        self.results_text.delete('1.0', tk.END)
        self.results_text.insert('1.0', text)