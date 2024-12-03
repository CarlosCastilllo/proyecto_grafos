import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional
import matplotlib.animation as animation

class SimulationPanel(ttk.LabelFrame):
    """Panel para control de simulación"""
    
    def __init__(self, parent, network):
        super().__init__(parent, text="Control de Simulación", padding=10)
        self.network = network
        self.animation: Optional[animation.FuncAnimation] = None
        self.simulation_time = 0
        self.is_running = False
        self.create_widgets()
        
    def create_widgets(self):
        """Crea los widgets del panel"""
        # Frame de control principal
        control_frame = ttk.Frame(self)
        control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Controles de simulación
        self.create_simulation_controls(control_frame)
        
        # Frame de parámetros
        params_frame = ttk.LabelFrame(self, text="Parámetros", padding=5)
        params_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.create_parameter_controls(params_frame)
        
        # Frame de estado
        status_frame = ttk.LabelFrame(self, text="Estado", padding=5)
        status_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.create_status_display(status_frame)
        
    def create_simulation_controls(self, parent):
        """Crea los controles de simulación"""
        # Botones de control
        self.start_button = ttk.Button(
            parent,
            text="▶ Iniciar",
            style='Action.TButton',
            command=self.start_simulation
        )
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.pause_button = ttk.Button(
            parent,
            text="⏸ Pausar",
            style='Action.TButton',
            command=self.pause_simulation,
            state=tk.DISABLED
        )
        self.pause_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = ttk.Button(
            parent,
            text="⏹ Detener",
            style='Action.TButton',
            command=self.stop_simulation,
            state=tk.DISABLED
        )
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        self.reset_button = ttk.Button(
            parent,
            text="↺ Reiniciar",
            style='Action.TButton',
            command=self.reset_simulation
        )
        self.reset_button.pack(side=tk.LEFT, padx=5)
        
    def create_parameter_controls(self, parent):
        """Crea los controles de parámetros"""
        # Velocidad de simulación
        ttk.Label(parent, text="Velocidad:").pack(fill=tk.X, pady=2)
        self.speed_scale = ttk.Scale(
            parent,
            from_=0.1,
            to=2.0,
            orient=tk.HORIZONTAL
        )
        self.speed_scale.set(1.0)
        self.speed_scale.pack(fill=tk.X, pady=2)
        
        # Factor de consumo
        ttk.Label(parent, text="Factor de consumo:").pack(fill=tk.X, pady=2)
        self.consumption_scale = ttk.Scale(
            parent,
            from_=0.5,
            to=1.5,
            orient=tk.HORIZONTAL
        )
        self.consumption_scale.set(1.0)
        self.consumption_scale.pack(fill=tk.X, pady=2)
        
    def create_status_display(self, parent):
        """Crea la visualización de estado"""
        # Tiempo de simulación
        self.time_label = ttk.Label(
            parent,
            text="Tiempo: 0s"
        )
        self.time_label.pack(fill=tk.X, pady=2)
        
        # Estado del sistema
        self.status_text = tk.Text(
            parent,
            height=4,
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.status_text.pack(fill=tk.X, pady=2)
        
    def start_simulation(self):
        """Inicia la simulación"""
        if not self.is_running:
            self.is_running = True
            self.update_button_states()
            
            # Configurar la animación
            self.animation = animation.FuncAnimation(
                self.network.fig,
                self.update_simulation,
                interval=50,
                blit=False
            )
            
            self.network.canvas.draw()
            
    def pause_simulation(self):
        """Pausa la simulación"""
        if self.is_running:
            self.is_running = False
            if self.animation:
                self.animation.event_source.stop()
            self.update_button_states()
            
    def stop_simulation(self):
        """Detiene la simulación"""
        self.is_running = False
        if self.animation:
            self.animation.event_source.stop()
            self.animation = None
        self.simulation_time = 0
        self.update_time_display()
        self.update_button_states()
        
    def reset_simulation(self):
        """Reinicia la simulación"""
        self.stop_simulation()
        self.network.reset_simulation()
        self.update_status()
        messagebox.showinfo("Reinicio", "Simulación reiniciada")
        
    def update_simulation(self, frame):
        """Actualiza el estado de la simulación"""
        if self.is_running:
            self.simulation_time += 1
            
            # Actualizar la red
            speed = self.speed_scale.get()
            consumption = self.consumption_scale.get()
            self.network.update_simulation(speed, consumption)
            
            # Actualizar visualización
            self.update_time_display()
            self.update_status()
            
    def update_time_display(self):
        """Actualiza el display de tiempo"""
        self.time_label.config(
            text=f"Tiempo: {self.simulation_time}s"
        )
        
    def update_status(self):
        """Actualiza el estado del sistema"""
        status = self.network.get_system_status()
        
        self.status_text.config(state=tk.NORMAL)
        self.status_text.delete(1.0, tk.END)
        self.status_text.insert(tk.END, status)
        self.status_text.config(state=tk.DISABLED)
        
    def update_button_states(self):
        """Actualiza el estado de los botones"""
        if self.is_running:
            self.start_button.config(state=tk.DISABLED)
            self.pause_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.NORMAL)
            self.reset_button.config(state=tk.DISABLED)
        else:
            self.start_button.config(state=tk.NORMAL)
            self.pause_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.DISABLED)
            self.reset_button.config(state=tk.NORMAL)