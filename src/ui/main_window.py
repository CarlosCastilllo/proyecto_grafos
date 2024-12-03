from tkinter import ttk, filedialog, messagebox
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from .panels import PipesPanel, NodesPanel, MaintenancePanel, HistoryPanel, FlowPanel, SimulationPanel, ObstructionsPanel, FilesPanel, RoutesPanel, OptimizationPanel, TanksPanel

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.create_interface()

    def create_interface(self):
        """Crea la interfaz principal con estilo moderno"""
        # Configurar el estilo general
        self.setup_styles()
        
        # Panel principal que divide la pantalla
        self.main_panel = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.main_panel.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Crear panel izquierdo (control)
        self.create_left_panel()
        
        # Crear panel derecho (visualización)
        self.create_right_panel()

    def setup_styles(self):
        """Configura los estilos de la interfaz"""
        style = ttk.Style()
        style.theme_use('clam')  # Usar un tema moderno
        
        # Configurar estilos personalizados
        style.configure('Panel.TLabelframe', 
                       background='#f0f0f0',
                       padding=10)
        style.configure('Action.TButton',
                       padding=10,
                       font=('Segoe UI', 9, 'bold'))
        style.configure('Title.TLabel',
                       font=('Segoe UI', 11, 'bold'),
                       foreground='#2c3e50')
        style.configure('Info.TLabel',
                       font=('Segoe UI', 9),
                       foreground='#34495e')

    def create_left_panel(self):
        """Crea el panel de control izquierdo"""
        # Contenedor para el panel de control con scrollbar
        control_container = ttk.Frame(self.main_panel)
        self.main_panel.add(control_container, weight=2)
        
        # Título principal
        title_frame = ttk.Frame(control_container)
        title_frame.pack(fill=tk.X, padx=5, pady=(5,15))
        ttk.Label(title_frame, 
                 text="Control de Red de Tuberías",
                 style='Title.TLabel').pack(side=tk.LEFT, padx=5)
        
        # Crear canvas y scrollbar
        canvas = tk.Canvas(control_container, 
                         background='#ffffff',
                         highlightthickness=0)
        scrollbar = ttk.Scrollbar(control_container, 
                                orient="vertical", 
                                command=canvas.yview)
        
        # Panel de control principal
        self.left_panel = ttk.Frame(canvas)
        
        # Configurar el scroll
        self.left_panel.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        # Crear ventana en el canvas
        canvas.create_window((5, 5), 
                           window=self.left_panel, 
                           anchor="nw", 
                           width=canvas.winfo_reqwidth()-10)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Empaquetar scrollbar y canvas
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        
        # Configurar el scroll con la rueda del mouse
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Crear los paneles de control
        self.create_panels()

    def create_right_panel(self):
        """Crea el panel de visualización derecho"""
        # Contenedor del panel de visualización
        viz_container = ttk.LabelFrame(self.main_panel, 
                                 text="Visualización de la Red",
                                 style='Panel.TLabelframe')
        self.main_panel.add(viz_container, weight=3)
        
        # Toolbar
        toolbar = ttk.Frame(viz_container)
        toolbar.pack(fill=tk.X, padx=5, pady=5)
    
        ttk.Button(toolbar, 
              text="⟲ Reset Zoom",
              style='Action.TButton',
              command=self.reset_view).pack(side=tk.LEFT, padx=5)
    
        ttk.Button(toolbar,
              text=" ",  # Texto vacío aquí
              style='Action.TButton',
              command=self.capture_view).pack(side=tk.LEFT, padx=5)
    
        # Panel de visualización
        self.viz_panel = ttk.Frame(viz_container)
        self.viz_panel.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
        # Configurar la figura de matplotlib
        self.setup_matplotlib()
        
    def setup_matplotlib(self):
        """Configura la visualización con matplotlib"""
        #self.viz_panel = ttk.Frame(self.viz_container)
        #self.viz_panel.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Configurar la figura con estilo moderno
        self.fig = Figure(figsize=(8, 6), facecolor='#ffffff')
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor('#f8f9fa')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.viz_panel)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def create_panels(self):
        """Crea los paneles de control con separadores"""
        # Paneles principales
        self.nodes_panel = NodesPanel(self.left_panel, None)
        self.nodes_panel.pack(fill=tk.X, pady=5)
        
        self.pipes_panel = PipesPanel(self.left_panel, None)
        self.pipes_panel.pack(fill=tk.X, pady=5)
        
        # Separador
        ttk.Separator(self.left_panel, orient='horizontal').pack(fill=tk.X, pady=10)
        
        # Panel de flujo
        self.flow_panel = FlowPanel(self.left_panel, None)
        self.flow_panel.pack(fill=tk.X, pady=5)
        
        # Separador
        ttk.Separator(self.left_panel, orient='horizontal').pack(fill=tk.X, pady=10)
        
        # Panel de tanques
        self.tanks_panel = TanksPanel(self.left_panel, None)
        self.tanks_panel.pack(fill=tk.X, pady=5)
        
        # Separador
        ttk.Separator(self.left_panel, orient='horizontal').pack(fill=tk.X, pady=10)
        
        # Panel de optimización
        self.optimization_panel = OptimizationPanel(self.left_panel, None)
        self.optimization_panel.pack(fill=tk.X, pady=5)
        
        # Separador
        ttk.Separator(self.left_panel, orient='horizontal').pack(fill=tk.X, pady=10)
        
        # Panel de archivos
        self.files_panel = FilesPanel(self.left_panel, None)
        self.files_panel.pack(fill=tk.X, pady=5)
        
        # Separador
        ttk.Separator(self.left_panel, orient='horizontal').pack(fill=tk.X, pady=10)
        
        # Panel de obstrucciones
        self.obstructions_panel = ObstructionsPanel(self.left_panel, None)
        self.obstructions_panel.pack(fill=tk.X, pady=5)
        
        # Separador
        ttk.Separator(self.left_panel, orient='horizontal').pack(fill=tk.X, pady=10)
        
        # Panel de rutas
        self.routes_panel = RoutesPanel(self.left_panel, None)
        self.routes_panel.pack(fill=tk.X, pady=5)
        
        # Separador
        ttk.Separator(self.left_panel, orient='horizontal').pack(fill=tk.X, pady=10)
        
        # Panel de simulación
        self.simulation_panel = SimulationPanel(self.left_panel, None)
        self.simulation_panel.pack(fill=tk.X, pady=5)
        
        # Separador
        ttk.Separator(self.left_panel, orient='horizontal').pack(fill=tk.X, pady=10)
        
        # Panel de historial
        self.history_panel = HistoryPanel(self.left_panel, None)
        self.history_panel.pack(fill=tk.X, pady=5)
        
        # Separador
        ttk.Separator(self.left_panel, orient='horizontal').pack(fill=tk.X, pady=10)
        
        # Panel de mantenimiento
        self.maintenance_panel = MaintenancePanel(self.left_panel, None)
        self.maintenance_panel.pack(fill=tk.X, pady=5)
        
    def reset_view(self):
        """Resetea la vista del gráfico a su estado inicial"""
        try:
            self.ax.clear()
            if self.network:
                # Redibujar el grafo con la configuración inicial
                self.network.draw(self.ax)
            else:
                # Dibujar un grafo de ejemplo
                self.ax.text(0.5, 0.5, 'Red no cargada', 
                            horizontalalignment='center',
                            verticalalignment='center')
            self.canvas.draw()
        except Exception as e:
            messagebox.showerror("Error", f"Error al resetear vista: {str(e)}")

    def capture_view(self):
        """Captura la vista actual del gráfico"""
        try:
            filename = filedialog.asksaveasfilename(
                title="Guardar Captura",
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), 
                        ("All files", "*.*")]
            )
            if filename:
                self.fig.savefig(filename, 
                                bbox_inches='tight', 
                                dpi=300)
                messagebox.showinfo("Éxito", 
                                "Captura guardada correctamente")
        except Exception as e:
            messagebox.showerror("Error", 
                                f"Error al guardar captura: {str(e)}")