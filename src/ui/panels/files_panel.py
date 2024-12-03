import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class FilesPanel(ttk.LabelFrame):
    def __init__(self, parent, network):
        super().__init__(parent, text="Gestión de Archivos", padding=10)
        self.network = network
        self.create_widgets()

    def create_widgets(self):
        """Crea los widgets del panel"""
        frame = ttk.Frame(self)
        frame.pack(fill=tk.BOTH, expand=True)

        # Botones de carga y guardado
        buttons_frame = ttk.Frame(frame)
        buttons_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(buttons_frame,
                  text=" ",
                  command=self.load_network).pack(fill=tk.X, pady=2)

        ttk.Button(buttons_frame,
                  text=" ",
                  command=self.save_network).pack(fill=tk.X, pady=2)

    def load_network(self):
        """Carga una red desde un archivo"""
        try:
            filename = filedialog.askopenfilename(
                title="Cargar Red",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            if filename and self.network:
                self.network.load_from_file(filename)
                messagebox.showinfo("Éxito", "Red cargada correctamente")
            elif filename:
                messagebox.showinfo("Simulación", f"Red cargada desde {filename} (simulado)")
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar la red: {str(e)}")

    def save_network(self):
        """Guarda la red en un archivo"""
        try:
            filename = filedialog.asksaveasfilename(
                title="Guardar Red",
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            if filename and self.network:
                self.network.save_to_file(filename)
                messagebox.showinfo("Éxito", "Red guardada correctamente")
            elif filename:
                messagebox.showinfo("Simulación", f"Red guardada en {filename} (simulado)")
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar la red: {str(e)}")