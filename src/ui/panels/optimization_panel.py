import tkinter as tk
from tkinter import ttk, messagebox

class OptimizationPanel(ttk.LabelFrame):
    def __init__(self, parent, network):
        super().__init__(parent, text="Optimización de Red", padding=10)
        self.network = network
        self.create_widgets()

    def create_widgets(self):
        """Crea los widgets del panel"""
        frame = ttk.Frame(self)
        frame.pack(fill=tk.BOTH, expand=True)

        # Frame para parámetros
        params_frame = ttk.LabelFrame(frame, text="Parámetros", padding=5)
        params_frame.pack(fill=tk.X, padx=5, pady=5)

        # Prioridad de barrios
        ttk.Label(params_frame, text="Prioridad de Barrios:").pack(fill=tk.X, pady=2)
        self.priority_combo = ttk.Combobox(params_frame, 
                                         values=["Alta", "Media", "Baja"],
                                         state='readonly')
        self.priority_combo.pack(fill=tk.X, pady=2)
        self.priority_combo.set("Media")

        # Factor de costo
        ttk.Label(params_frame, text="Factor de Costo (1-10):").pack(fill=tk.X, pady=2)
        self.cost_scale = ttk.Scale(params_frame, 
                                  from_=1, 
                                  to=10, 
                                  orient=tk.HORIZONTAL)
        self.cost_scale.pack(fill=tk.X, pady=2)
        self.cost_scale.set(5)

        # Botones de optimización
        buttons_frame = ttk.Frame(frame)
        buttons_frame.pack(fill=tk.X, padx=5, pady=5)

        # Botón de optimización de flujo
        ttk.Button(buttons_frame,
                  text=" ",
                  command=self.optimize_flow).pack(fill=tk.X, pady=2)

        # Botón de optimización de conexiones
        ttk.Button(buttons_frame,
                  text=" ",
                  command=self.optimize_connections).pack(fill=tk.X, pady=2)

        # Botón de balance de carga
        ttk.Button(buttons_frame,
                  text=" ",
                  command=self.balance_load).pack(fill=tk.X, pady=2)

        # Frame para resultados
        results_frame = ttk.LabelFrame(frame, text="Resultados de Optimización", padding=5)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Área de texto para resultados
        self.results_text = tk.Text(results_frame, height=6, wrap=tk.WORD)
        self.results_text.pack(fill=tk.BOTH, expand=True, pady=5)

    def optimize_flow(self):
        """Optimiza el flujo en la red"""
        try:
            priority = self.priority_combo.get()
            cost_factor = self.cost_scale.get()

            if self.network:
                result = self.network.optimize_flow(priority, cost_factor)
                self.show_results(
                    "Optimización de flujo completada:\n"
                    f"Mejora de eficiencia: {result['efficiency']}%\n"
                    f"Costo estimado: {result['cost']}\n"
                    f"Estado: {result['status']}"
                )
            else:
                # Simulación
                self.show_results(
                    "Optimización simulada:\n"
                    "Mejora de eficiencia: 15%\n"
                    "Costo estimado: 1000\n"
                    "Estado: Completado"
                )

        except Exception as e:
            messagebox.showerror("Error", f"Error en optimización: {str(e)}")

    def optimize_connections(self):
        """Optimiza las conexiones de la red"""
        try:
            priority = self.priority_combo.get()
            cost_factor = self.cost_scale.get()

            if self.network:
                result = self.network.optimize_connections(priority, cost_factor)
                self.show_results(
                    "Optimización de conexiones completada:\n"
                    f"Nuevas conexiones: {result['new_connections']}\n"
                    f"Conexiones modificadas: {result['modified']}\n"
                    f"Costo total: {result['cost']}"
                )
            else:
                # Simulación
                self.show_results(
                    "Optimización simulada:\n"
                    "Nuevas conexiones: 2\n"
                    "Conexiones modificadas: 3\n"
                    "Costo total: 1500"
                )

        except Exception as e:
            messagebox.showerror("Error", f"Error en optimización: {str(e)}")

    def balance_load(self):
        """Balancea la carga en la red"""
        try:
            if self.network:
                result = self.network.balance_load()
                self.show_results(
                    "Balance de carga completado:\n"
                    f"Desviación antes: {result['before_deviation']}%\n"
                    f"Desviación después: {result['after_deviation']}%\n"
                    f"Mejora total: {result['improvement']}%"
                )
            else:
                # Simulación
                self.show_results(
                    "Balance simulado:\n"
                    "Desviación antes: 25%\n"
                    "Desviación después: 10%\n"
                    "Mejora total: 15%"
                )

        except Exception as e:
            messagebox.showerror("Error", f"Error en balance: {str(e)}")

    def show_results(self, text):
        """Muestra resultados en el área de texto"""
        self.results_text.delete('1.0', tk.END)
        self.results_text.insert('1.0', text)
