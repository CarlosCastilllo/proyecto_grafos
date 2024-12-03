import tkinter as tk
from tkinter import ttk, messagebox

class ObstructionsPanel(ttk.LabelFrame):
    def __init__(self, parent, network):
        super().__init__(parent, text="Gestión de Obstrucciones", padding=10)
        self.network = network
        self.create_widgets()

    def create_widgets(self):
        """Crea los widgets del panel"""
        frame = ttk.Frame(self)
        frame.pack(fill=tk.BOTH, expand=True)

        # Frame para agregar obstrucción
        add_frame = ttk.LabelFrame(frame, text="Agregar Obstrucción", padding=5)
        add_frame.pack(fill=tk.X, padx=5, pady=5)

        # Selector de tubería
        ttk.Label(add_frame, text="Tubería:").pack(fill=tk.X, pady=2)
        self.pipe_combo = ttk.Combobox(add_frame, state='readonly')
        self.pipe_combo.pack(fill=tk.X, pady=2)

        # Nivel de obstrucción
        ttk.Label(add_frame, text="Nivel (0-100%):").pack(fill=tk.X, pady=2)
        self.level_entry = ttk.Entry(add_frame)
        self.level_entry.pack(fill=tk.X, pady=2)
        self.level_entry.insert(0, "50")

        # Botón de agregar
        ttk.Button(add_frame,
                  text=" ",
                  command=self.add_obstruction).pack(fill=tk.X, pady=5)

        # Frame para lista de obstrucciones
        list_frame = ttk.LabelFrame(frame, text="Obstrucciones Actuales", padding=5)
        list_frame.pack(fill=tk.X, padx=5, pady=5)

        # Lista de obstrucciones
        self.obstruction_list = ttk.Treeview(list_frame, 
                                           columns=("Tubería", "Nivel"),
                                           show="headings",
                                           height=5)
        self.obstruction_list.heading("Tubería", text="Tubería")
        self.obstruction_list.heading("Nivel", text="Nivel")
        self.obstruction_list.pack(fill=tk.X, pady=5)

        # Botón de eliminar
        ttk.Button(list_frame,
                  text=" ",
                  command=self.remove_obstruction).pack(fill=tk.X, pady=5)

        # Actualizar listas
        self.update_lists()

    def add_obstruction(self):
        """Agrega una nueva obstrucción"""
        try:
            pipe = self.pipe_combo.get()
            level = float(self.level_entry.get())

            if not pipe:
                raise ValueError("Seleccione una tubería")
            if not 0 <= level <= 100:
                raise ValueError("El nivel debe estar entre 0 y 100")

            if self.network:
                source, target = self.parse_pipe_string(pipe)
                self.network.add_obstruction(source, target, level)
                messagebox.showinfo("Éxito", "Obstrucción agregada correctamente")
                self.update_lists()
            else:
                messagebox.showinfo("Simulación", 
                                  f"Obstrucción agregada (simulado):\n"
                                  f"Tubería: {pipe}\n"
                                  f"Nivel: {level}%")
                self.update_lists()

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def remove_obstruction(self):
        """Elimina la obstrucción seleccionada"""
        selection = self.obstruction_list.selection()
        if not selection:
            messagebox.showerror("Error", "Seleccione una obstrucción")
            return

        item = self.obstruction_list.item(selection[0])
        pipe = item['values'][0]

        if messagebox.askyesno("Confirmar", f"¿Eliminar obstrucción en {pipe}?"):
            if self.network:
                source, target = self.parse_pipe_string(pipe)
                self.network.remove_obstruction(source, target)
                messagebox.showinfo("Éxito", "Obstrucción eliminada correctamente")
                self.update_lists()
            else:
                messagebox.showinfo("Simulación", 
                                  f"Obstrucción eliminada (simulado)")
                self.update_lists()

    def update_lists(self):
        """Actualiza las listas de tuberías y obstrucciones"""
        # Actualizar lista de tuberías
        if self.network:
            pipes = [f"{u}-{v}" for u, v in self.network.graph.edges()]
        else:
            pipes = ['A-B', 'B-C', 'C-D']  # Simulación
        self.pipe_combo['values'] = pipes

        # Limpiar y actualizar lista de obstrucciones
        for item in self.obstruction_list.get_children():
            self.obstruction_list.delete(item)

        if self.network:
            for (u, v), level in self.network.obstructions.items():
                self.obstruction_list.insert('', 'end', values=(f"{u}-{v}", f"{level}%"))
        else:
            # Datos de ejemplo para simulación
            self.obstruction_list.insert('', 'end', values=("A-B", "30%"))
            self.obstruction_list.insert('', 'end', values=("B-C", "50%"))

    @staticmethod
    def parse_pipe_string(pipe_str):
        """Convierte un string de tubería en origen y destino"""
        return tuple(pipe_str.split('-'))