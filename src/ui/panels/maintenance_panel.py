import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class MaintenancePanel(ttk.LabelFrame):
    def __init__(self, parent, network):
        super().__init__(parent, text="Mantenimiento", padding=10)
        self.network = network
        self.create_widgets()

    def create_widgets(self):
        """Crea los widgets del panel"""
        # Frame principal
        frame = ttk.Frame(self)
        frame.pack(fill=tk.BOTH, expand=True)

        # Frame para registro de mantenimiento
        register_frame = ttk.LabelFrame(frame, text="Registrar Mantenimiento", padding=5)
        register_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.create_register_form(register_frame)

    def create_register_form(self, parent):
        """Crea el formulario de registro de mantenimiento"""
        # Frame para el formulario
        form_frame = ttk.Frame(parent)
        form_frame.pack(fill=tk.X, padx=5, pady=5)

        # Selector de componente
        ttk.Label(form_frame, text="Componente:").grid(row=0, column=0, padx=5, pady=5)
        self.component_combo = ttk.Combobox(form_frame, state='readonly')
        self.component_combo.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Tipo de mantenimiento
        ttk.Label(form_frame, text="Tipo:").grid(row=1, column=0, padx=5, pady=5)
        self.maintenance_type = ttk.Combobox(form_frame, values=[
            "Limpieza",
            "Reparación",
            "Inspección",
            "Reemplazo"
        ], state='readonly')
        self.maintenance_type.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.maintenance_type.set("Limpieza")

        # Descripción
        ttk.Label(form_frame, text="Descripción:").grid(row=2, column=0, padx=5, pady=5)
        self.description_entry = ttk.Entry(form_frame)
        self.description_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        # Configurar grid
        form_frame.columnconfigure(1, weight=1)

        # Botón de registro
        ttk.Button(form_frame,
                  text="✔️ Registrar Mantenimiento",
                  command=self.register_maintenance).grid(
                      row=3,
                      column=0,
                      columnspan=2,
                      pady=10,
                      sticky="ew"
        )

        # Actualizar lista de componentes
        self.update_component_list()

    def update_component_list(self):
        """Actualiza la lista de componentes en el combobox"""
        if self.network:
            # Obtener componentes de la red
            components = []
            # Agregar tuberías
            for u, v in self.network.graph.edges():
                components.append(f"Tubería {u}-{v}")
            # Agregar nodos
            for node, attr in self.network.graph.nodes(data=True):
                node_type = attr.get('type', 'Desconocido')
                components.append(f"{node_type} {node}")
        else:
            # Datos de ejemplo para simulación
            components = [
                "Tubería A-B",
                "Tubería B-C",
                "Tanque A",
                "Barrio B",
                "Intersección C"
            ]

        self.component_combo['values'] = components
        if components:
            self.component_combo.set(components[0])

    def register_maintenance(self):
        """Registra un nuevo mantenimiento"""
        try:
            component = self.component_combo.get()
            maint_type = self.maintenance_type.get()
            description = self.description_entry.get()

            if not all([component, maint_type, description]):
                raise ValueError("Todos los campos son requeridos")

            if self.network:
                # Registrar en la red
                self.network.register_maintenance(
                    component=component,
                    maintenance_type=maint_type,
                    description=description,
                    date=datetime.now()
                )
                messagebox.showinfo(
                    "Éxito",
                    "Mantenimiento registrado correctamente"
                )
                self.clear_fields()
            else:
                # Modo simulación
                messagebox.showinfo(
                    "Simulación",
                    f"Mantenimiento registrado (simulado):\n"
                    f"Componente: {component}\n"
                    f"Tipo: {maint_type}\n"
                    f"Descripción: {description}"
                )
                self.clear_fields()

        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar mantenimiento: {str(e)}")

    def clear_fields(self):
        """Limpia los campos del formulario"""
        self.component_combo.set('')
        self.maintenance_type.set('Limpieza')
        self.description_entry.delete(0, tk.END)