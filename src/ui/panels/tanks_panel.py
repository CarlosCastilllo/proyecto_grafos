import tkinter as tk
from tkinter import ttk, messagebox

class TanksPanel(ttk.LabelFrame):
    def __init__(self, parent, network):
        super().__init__(parent, text="Gestión de Tanques", padding=10)
        self.network = network
        self.create_widgets()

    def create_widgets(self):
        """Crea los widgets del panel"""
        frame = ttk.Frame(self)
        frame.pack(fill=tk.BOTH, expand=True)

        # Frame para agregar tanque
        add_frame = ttk.LabelFrame(frame, text="Agregar Tanque", padding=5)
        add_frame.pack(fill=tk.X, padx=5, pady=5)

        # ID del tanque
        ttk.Label(add_frame, text="ID:").pack(fill=tk.X, pady=2)
        self.tank_id = ttk.Entry(add_frame)
        self.tank_id.pack(fill=tk.X, pady=2)

        # Capacidad
        ttk.Label(add_frame, text="Capacidad (m³):").pack(fill=tk.X, pady=2)
        self.capacity_entry = ttk.Entry(add_frame)
        self.capacity_entry.pack(fill=tk.X, pady=2)
        self.capacity_entry.insert(0, "1000")

        # Nivel actual
        ttk.Label(add_frame, text="Nivel Actual (%):").pack(fill=tk.X, pady=2)
        self.level_entry = ttk.Entry(add_frame)
        self.level_entry.pack(fill=tk.X, pady=2)
        self.level_entry.insert(0, "50")

        # Botón de agregar
        ttk.Button(add_frame,
                  text=" ",
                  command=self.add_tank).pack(fill=tk.X, pady=5)

        # Frame para lista de tanques
        list_frame = ttk.LabelFrame(frame, text="Tanques Actuales", padding=5)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Lista de tanques
        self.tanks_list = ttk.Treeview(list_frame,
                                     columns=("ID", "Capacidad", "Nivel"),
                                     show="headings",
                                     height=5)
        
        self.tanks_list.heading("ID", text="ID")
        self.tanks_list.heading("Capacidad", text="Capacidad (m³)")
        self.tanks_list.heading("Nivel", text="Nivel (%)")
        
        self.tanks_list.column("ID", width=100)
        self.tanks_list.column("Capacidad", width=100)
        self.tanks_list.column("Nivel", width=100)
        
        self.tanks_list.pack(fill=tk.BOTH, expand=True, pady=5)

        # Frame de acciones
        actions_frame = ttk.Frame(list_frame)
        actions_frame.pack(fill=tk.X, pady=5)

        # Botón de eliminar
        ttk.Button(actions_frame,
                  text=" ",
                  command=self.remove_tank).pack(side=tk.LEFT, padx=5)

        # Botón de actualizar nivel
        ttk.Button(actions_frame,
                  text=" ",
                  command=self.update_tank_level).pack(side=tk.LEFT, padx=5)

        # Actualizar lista
        self.update_tanks_list()

    def add_tank(self):
        """Agrega un nuevo tanque"""
        try:
            tank_id = self.tank_id.get()
            capacity = float(self.capacity_entry.get())
            level = float(self.level_entry.get())

            if not tank_id:
                raise ValueError("El ID del tanque es requerido")
            if capacity <= 0:
                raise ValueError("La capacidad debe ser mayor a 0")
            if not 0 <= level <= 100:
                raise ValueError("El nivel debe estar entre 0 y 100")

            if self.network:
                self.network.add_tank(tank_id, capacity, level)
                messagebox.showinfo("Éxito", "Tanque agregado correctamente")
                self.clear_fields()
                self.update_tanks_list()
            else:
                # Simulación
                messagebox.showinfo("Simulación",
                                  f"Tanque agregado (simulado):\n"
                                  f"ID: {tank_id}\n"
                                  f"Capacidad: {capacity} m³\n"
                                  f"Nivel: {level}%")
                self.clear_fields()
                self.update_tanks_list()

        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Error al agregar tanque: {str(e)}")

    def remove_tank(self):
        """Elimina el tanque seleccionado"""
        selection = self.tanks_list.selection()
        if not selection:
            messagebox.showerror("Error", "Seleccione un tanque")
            return

        tank_id = self.tanks_list.item(selection[0])['values'][0]

        if messagebox.askyesno("Confirmar", f"¿Eliminar tanque {tank_id}?"):
            if self.network:
                self.network.remove_tank(tank_id)
                messagebox.showinfo("Éxito", "Tanque eliminado correctamente")
                self.update_tanks_list()
            else:
                messagebox.showinfo("Simulación",
                                  f"Tanque {tank_id} eliminado (simulado)")
                self.update_tanks_list()

    def update_tank_level(self):
        """Actualiza el nivel del tanque seleccionado"""
        selection = self.tanks_list.selection()
        if not selection:
            messagebox.showerror("Error", "Seleccione un tanque")
            return

        tank_id = self.tanks_list.item(selection[0])['values'][0]
        
        # Crear diálogo para nuevo nivel
        dialog = tk.Toplevel(self)
        dialog.title("Actualizar Nivel")
        dialog.geometry("300x150")
        dialog.resizable(False, False)

        ttk.Label(dialog, text="Nuevo nivel (%):").pack(pady=10)
        level_var = tk.StringVar(value="50")
        level_entry = ttk.Entry(dialog, textvariable=level_var)
        level_entry.pack(pady=5)

        def apply_update():
            try:
                new_level = float(level_var.get())
                if not 0 <= new_level <= 100:
                    raise ValueError("El nivel debe estar entre 0 y 100")

                if self.network:
                    self.network.update_tank_level(tank_id, new_level)
                    messagebox.showinfo("Éxito", "Nivel actualizado correctamente")
                else:
                    messagebox.showinfo("Simulación",
                                      f"Nivel actualizado (simulado):\n"
                                      f"Tanque: {tank_id}\n"
                                      f"Nuevo nivel: {new_level}%")
                dialog.destroy()
                self.update_tanks_list()

            except ValueError as e:
                messagebox.showerror("Error", str(e))
            except Exception as e:
                messagebox.showerror("Error", f"Error al actualizar nivel: {str(e)}")

        ttk.Button(dialog,
                  text=" ",
                  command=apply_update).pack(pady=10)

    def update_tanks_list(self):
        """Actualiza la lista de tanques"""
        # Limpiar lista actual
        for item in self.tanks_list.get_children():
            self.tanks_list.delete(item)

        if self.network:
            # Obtener datos reales de la red
            for tank in self.network.get_tanks():
                self.tanks_list.insert('', 'end', values=(
                    tank['id'],
                    f"{tank['capacity']}",
                    f"{tank['level']}%"
                ))
        else:
            # Datos de ejemplo para simulación
            sample_data = [
                ("T1", "1000", "80%"),
                ("T2", "1500", "60%"),
                ("T3", "2000", "45%")
            ]
            for tank in sample_data:
                self.tanks_list.insert('', 'end', values=tank)

    def clear_fields(self):
        """Limpia los campos del formulario"""
        self.tank_id.delete(0, tk.END)
        self.capacity_entry.delete(0, tk.END)
        self.capacity_entry.insert(0, "1000")
        self.level_entry.delete(0, tk.END)
        self.level_entry.insert(0, "50")