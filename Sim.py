
from PySide6.QtCore import QTimer
import pandas as pd
import os
from fpdf import FPDF
import numpy as np
from PySide6.QtWidgets import (
    QApplication,
    QPushButton,
    QWidget,
    QComboBox,
    QDoubleSpinBox,
    QMessageBox,
    QLabel,
    QFileDialog,
    QCheckBox)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.colors import ListedColormap
from Calculations import CalculationWindow
from Graph import GraphWindow

class SimulationWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.model = None  
        self.adding_hot_spot = False
        self.adding_cold_spot = False
        self.running_simulation = False
        self.controls = []
        self.point1_temp_list = []
        self.point_time_list = []   
        self.clicked_point1 = None
        self.colormap_drawn = False
        self.point_choisen = False 
        self.boundry_temp_list = []
        self.point1_dt_list = []
        self.custom_color_map = False
        self.saved_colormap_path = None
        self.saved_graph_temp_path = None
        self.saved_graph_dTdt_path = None
        self.time_step = 0.001  
        self.init_ui()
        self.init_timer()
        self.max_temp = 200
        self.sim_steps_since_draw = 0
        self.N_draw = 2 
        self.elapsed_time = 0.0
        self.hot_spot_selected = None
        self.cold_spot_selected = None
        self.hot_spot = False
        self.cold_spot = False
        self.custom_color_map = False
        self.spot_markers = []

    def init_ui(self):
        self.setWindowTitle("2D Heat Transfer")
        self.setGeometry(100, 200, 1200, 590)
        with open("stylesheet.css", "r", encoding="utf-8") as fp:
            self.setStyleSheet(fp.read())
        
        lbl_ic = QLabel("Initial Temp (°C):", self)
        lbl_ic.setGeometry(30, 90, 130, 30)
        self.initial_condition = QDoubleSpinBox(self)
        self.initial_condition.setGeometry(30, 120, 30, 30)
        self.initial_condition.setRange(-1000,1000)
        self.initial_condition.setValue(200)
        self.controls.append(self.initial_condition)

        lbl_bottom = QLabel("Bottom temp (°C):", self)
        lbl_bottom.setGeometry(30, 150, 135, 30)
        self.bottom_temp = QDoubleSpinBox(self)
        self.bottom_temp.setGeometry(30, 180, 30, 30)
        self.bottom_temp.setRange(-1000,1000)
        self.bottom_temp.setValue(0.0)
        self.controls.append(self.bottom_temp)
        
        lbl_right = QLabel("Right temp (°C):", self)
        lbl_right.setGeometry(30, 210, 130, 30)
        self.right_temp = QDoubleSpinBox(self)
        self.right_temp.setGeometry(30, 240, 100, 30)
        self.right_temp.setRange(-1000,1000)
        self.right_temp.setValue(0.0)
        self.controls.append(self.right_temp)
        
        lbl_top = QLabel("Top temp (°C):", self)
        lbl_top.setGeometry(30, 270, 130, 30)
        self.top_temp = QDoubleSpinBox(self)
        self.top_temp.setGeometry(30, 300, 100, 30)
        self.top_temp.setRange(-1000,1000)
        self.top_temp.setValue(0.0)
        self.controls.append(self.top_temp)
   
        lbl_left = QLabel("Left temp (°C):", self)
        lbl_left.setGeometry(30, 330, 130, 30)
        self.left_temp = QDoubleSpinBox(self)
        self.left_temp.setGeometry(30, 360, 100, 30)
        self.left_temp.setRange(-1000,1000)
        self.left_temp.setValue(0.0)
        self.controls.append(self.left_temp)

        lbl_mass = QLabel("Mass of cell (kg):", self)
        lbl_mass.setGeometry(30, 30, 150, 30)
        self.mass = QDoubleSpinBox(self)
        self.mass.setGeometry(30, 60, 100, 30)
        self.mass.setRange(-1000,1000)
        self.mass.setValue(10)
        self.controls.append(self.mass)

        lbl_cp = QLabel("Specific heat (J/kg·°C):", self)
        lbl_cp.setGeometry(190, 30, 180, 30)
        self.h_capacity = QDoubleSpinBox(self)
        self.h_capacity.setGeometry(190, 60, 100, 30)
        self.h_capacity.setRange(-1000,1000)
        self.h_capacity.setValue(5)
        self.controls.append(self.h_capacity)

        self.lbl_keep_point = QLabel("Keep Point", self)
        self.lbl_keep_point.setGeometry(190, 340, 180, 30)
        self.keep_point_checkbox = QCheckBox(self)
        self.keep_point_checkbox.setChecked(False)  
        self.keep_point_checkbox.setGeometry(290, 340, 30, 30)
        self.controls.append(self.keep_point_checkbox)
        
        self.colors = {
            "Blue": (0,0,1),
            "Green": (0,1,0),
            "Red": (1,0,0),
            "Yellow": (1,1,0),
            "Purple": (0.5,0,0.5),
            "White": (1,1,1),
            "Black": (0,0,0),
            "Gray": (0.5, 0.5, 0.5),
            "Orange": (1,0.5,0)}

        self.lbl_max_color = QLabel("Max color:", self)
        self.lbl_max_color.setGeometry(190, 90, 100, 30)
        self.combo_max = QComboBox(self)
        self.combo_max.setGeometry(190, 120, 100 ,30)
        self.combo_max.addItems(self.colors.keys())
        self.controls.append(self.combo_max)

        self.lbl_mid_color = QLabel("Mid Color:", self)
        self.lbl_mid_color.setGeometry(190, 150, 100, 30)
        self.combo_mid = QComboBox(self)
        self.combo_mid.setGeometry(190, 180, 100 ,30)
        self.combo_mid.addItems(self.colors.keys())
        self.controls.append(self.combo_mid)

        self.lbl_min_color = QLabel("Min Color:", self)
        self.lbl_min_color.setGeometry(190, 210, 100, 30)
        self.combo_min = QComboBox(self)
        self.combo_min.setGeometry(190, 240, 100 ,30)
        self.combo_min.addItems(self.colors.keys())
        self.controls.append(self.combo_min)

        self.colors_apply_button = QPushButton("Apply colors", self)
        self.colors_apply_button.setGeometry(190, 290, 120, 30)
        self.colors_apply_button.clicked.connect(self.build_colormap)
        self.controls.append(self.colors_apply_button)

        self.button_simulation = QPushButton("Start", self)
        self.button_simulation.setGeometry(30, 450, 120, 50)
        self.button_simulation.setCheckable(True)
        self.button_simulation.clicked.connect(self.toggle_simulation)

        self.button_clear = QPushButton("Clear", self)
        self.button_clear.setGeometry(180, 450, 120, 50)
        self.button_clear.clicked.connect(self.clear_colormap)
        self.controls.append(self.button_clear)

        self.button_graph = QPushButton("Graph", self)
        self.button_graph.setGeometry(330, 450, 120, 50)
        self.button_graph.clicked.connect(self.open_graph)
        self.controls.append(self.button_graph)

        self.save_state_button = QPushButton("Save State", self)
        self.save_state_button.setGeometry(30, 520, 120, 50)
        self.save_state_button.clicked.connect(self.save_simulation_state)
        self.controls.append(self.save_state_button)

        self.load_button = QPushButton("Load State", self)
        self.load_button.setGeometry(180, 520, 120, 50)
        self.load_button.clicked.connect(self.load_simulation_state)
        self.controls.append(self.load_button)

        self.export_button = QPushButton("Export EXL", self)
        self.export_button.setGeometry(330, 520, 120, 50)
        self.export_button.clicked.connect(self.export_to_exl)
        self.controls.append(self.export_button)

        self.export_pdf_button = QPushButton("Export PDF", self)
        self.export_pdf_button.setGeometry(330, 380, 120, 50)
        self.export_pdf_button.clicked.connect(self.export_pdf_report)
        self.controls.append(self.export_pdf_button)

        self.add_cold_button = QPushButton("Add Cold Spots", self)
        self.add_cold_button.setGeometry(330, 320, 140, 40)
        self.add_cold_button.clicked.connect(self.enable_cold_spot_mode)
        self.controls.append(self.add_cold_button)

        self.add_hot_button = QPushButton("Add Hot Spots", self)
        self.add_hot_button.setGeometry(330, 270, 140, 40) 
        self.add_hot_button.clicked.connect(self.enable_hot_spot_mode)
        self.controls.append(self.add_hot_button)
        
        self.fig = Figure(figsize=(8, 8))
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self)
        self.canvas.setGeometry(500, 20, 680, 550)
        self.ax = self.fig.add_subplot(111)
        self.ax.axis('off')

        nx = CalculationWindow.nx
        ny = CalculationWindow.ny
        zeros = np.zeros((nx, ny))

        self.im = self.ax.imshow(
            zeros,
            cmap= "jet",
            interpolation='bicubic',
            vmin=0,
            vmax=200,
            origin='lower')
        self.cbar = self.fig.colorbar(self.im, ax=self.ax, label='Temperature (°C)', pad=0.13)
        self.ax.set_title("2D Heat Transfer Plate", size=16, y=1.08)
        self.canvas.mpl_connect("button_press_event", self.on_click)

        self.canvas.draw()
    
    def select_color(self):
        max_color = self.colors[self.combo_max.currentText()]
        min_color = self.colors[self.combo_min.currentText()]
        mid_color = self.colors[self.combo_mid.currentText()]
        return max_color, min_color, mid_color
    
    def build_colormap(self):
        self.custom_color_map = True
        self.cbar.remove()
        self.im.remove()

        max_color, min_color, mid_color = self.select_color() 
        gradient1 = np.linspace(min_color, mid_color, 128)
        gradient2 = np.linspace(mid_color, max_color, 128)
        full_gradient = np.concatenate([gradient1, gradient2])
        custom_map = ListedColormap(full_gradient)
        
        nx = CalculationWindow.nx
        ny = CalculationWindow.ny
        zeros = np.zeros((nx, ny))

        self.im = self.ax.imshow(
            zeros,
            cmap= custom_map,
            interpolation='bicubic',
            vmin=0,
            vmax=200,
            origin='lower')
        self.cbar = self.fig.colorbar(self.im, ax=self.ax, label='Temperature (°C)', pad=0.13)

        self.canvas.draw()

    def enable_hot_spot_mode(self):

        if self.elapsed_time > 0.0:
            QMessageBox.warning(self, "Too Late",
                "You can only place hot spots before the simulation begins (t = 0).")
            return
    
        if self.running_simulation:
            QMessageBox.warning(self,"You can only place hot spots before the simulation starts.")
            return
        
        if self.hot_spot_selected is not None:
            QMessageBox.information(self, "Limit Reached", "Maximum 1 hot spot allowed.")
            return

        self.adding_hot_spot = True
        self.adding_cold_spot = False
        
        QMessageBox.information(self, "Place Hot Spot", 
            "Click anywhere on the plate to place your hot spot.")

    def enable_cold_spot_mode(self):

        if self.elapsed_time > 0.0:
            QMessageBox.warning(self, "Too Late",
                "You can only place cold spots before the simulation begins (t = 0).")
            return

        if self.running_simulation:
            QMessageBox.warning(self,"You can only place cold spots before the simulation starts.")
            return
        
        if self.cold_spot_selected is not None:
            QMessageBox.information(self, "Limit Reached", "Maximum 1 cold spot allowed.")
            return
        self.adding_cold_spot = True
        self.adding_hot_spot = False
        
        QMessageBox.information(self, "Place Cold Spot", 
            "Click anywhere on the plate to place your cold spot.")

    def init_timer(self):
        self.timer = QTimer(self)
        self.timer.setInterval(int(self.time_step * 100)) 
        self.timer.timeout.connect(self.timer_method)
    
    def on_click(self, event):

        if self.running_simulation:
            return
        
        
        if event.inaxes is None:
            return
        
        x_data = event.xdata
        y_data = event.ydata
        
        i = int(round(y_data))
        j = int(round(x_data))

        i = max(0, min(CalculationWindow.nx - 1, i))
        j = max(0, min(CalculationWindow.ny - 1, j))

        if self.adding_hot_spot:
            self.hot_spot_selected = (i, j)
            self.ax.plot(j, i, marker='o', markersize=6, color='red', linestyle='')
            self.canvas.draw()
            self.adding_hot_spot = False
            self.hot_spot = True

            if self.model is not None:
                self.model.hot_spot_coords.append(self.hot_spot_selected)

            return

        if self.adding_cold_spot:
            self.cold_spot_selected = (i, j)
            self.ax.plot(j, i, marker='o', markersize=6, color='blue', linestyle='')
            self.canvas.draw()
            self.adding_cold_spot = False
            self.cold_spot = True

            if self.model is not None:
                self.model.cold_spot_coords.append(self.cold_spot_selected)

            return
    
        if self.point_choisen:
            return
        
        self.clicked_point1 = (i, j)
        self.point_choisen = True
        self.point_time_list.clear()
        self.point1_temp_list.clear()

        self.ax.plot(j, i, marker='o', color="#050005", linestyle='' , markersize=8)           
        self.canvas.draw()

    def calculate_point_dt(self):
        if self.clicked_point1 is None:
            return

        i, j = self.clicked_point1
        T = self.model.T
        T0 = T[i, j]
        neighbors = []

        if i > 0: neighbors.append(T[i - 1, j]) 
        if i < self.model.nx - 1: neighbors.append(T[i + 1, j])
        if j > 0: neighbors.append(T[i, j - 1]) 
        if j < self.model.ny - 1: neighbors.append(T[i, j + 1]) 

        dTsum = sum(Tn - T0 for Tn in neighbors)
        alpha = self.model.alpha
        dx2 = self.model.dx ** 2

        dTdt = (alpha * dTsum) / dx2
        self.point1_dt_list.append(dTdt)
    
    def validate_inputs(self, mass, c, T_ic, T_top, T_bottom, T_left, T_right):

        if mass <= 0:
            return "Mass must be greater than zero."
        if c <= 0:
            return "Specific heat must be greater than zero."
        for name, T in [
            ("Initial", T_ic),
            ("Top", T_top),
            ("Bottom", T_bottom),
            ("Left", T_left),
            ("Right", T_right)]:
            if T < 0:
                return f"{name} temperature must be non-negative."
            if T > self.max_temp:
                return f"{name} temperature must be lower than {self.max_temp} °C."
        return None
    
    def toggle_simulation(self):
            if self.button_simulation.isChecked():
             
                if self.model is None:
                    T_ic         = self.initial_condition.value()
                    T_top_val    = self.top_temp.value()
                    T_bottom_val = self.bottom_temp.value()
                    T_left_val   = self.left_temp.value()
                    T_right_val  = self.right_temp.value()
                    mass_val     = self.mass.value()
                    cp_val       = self.h_capacity.value()

                    error = self.validate_inputs(
                        mass_val, cp_val,
                        T_ic, T_top_val, T_bottom_val, T_left_val, T_right_val
                    )
                    if error:
                        QMessageBox.warning(self, "Input Error", error)
                        self.button_simulation.setChecked(False)
                        return
                        

                    self.model = CalculationWindow(
                        T_ic, T_top_val, T_bottom_val,
                        T_left_val, T_right_val,
                        mass_val, cp_val
                    )

                    if self.hot_spot_selected is not None:
                    # this list is what calculations() uses to re‑apply hot temps
                        self.model.hot_spot_coords.append(self.hot_spot_selected)

                    if self.cold_spot_selected is not None:
                        self.model.cold_spot_coords.append(self.cold_spot_selected)

                for w in self.controls:
                    w.setEnabled(False)

                self.elapsed_time = 0.0
                self.sim_steps_since_draw = 0
                self.adding_hot_spot = False
                self.adding_cold_spot = False
                self.running_simulation = True
                self.button_simulation.setText("Stop")
                self.timer.start(int(self.time_step * 1000))
            else:
                self.timer.stop()
                self.button_simulation.setText("Start")

                for w in self.controls:
                    w.setEnabled(True)

                self.running_simulation = False

    def timer_method(self):

        """
        Called every self.time_step seconds by QTimer.
        We do one vectorized step each tick but redraw only every N_draw steps.
        """
        if self.model is None:
            return

        T_old = self.model.T.copy()
        T_new = self.model.calculations()
        self.calculate_point_dt()
        self.elapsed_time += self.time_step
       
        self.sim_steps_since_draw += 1

        if self.clicked_point1 is not None:
            i, j = self.clicked_point1
            self.point_time_list.append(self.elapsed_time)
            self.point1_temp_list.append(self.model.T[i, j])
            
        if self.sim_steps_since_draw >= self.N_draw:
            diff = np.abs(T_new - T_old).max()
            if diff < 1e-3:
          
                self.timer.stop()
                self.button_simulation.setText("Start")
                for w in self.controls:
                    w.setEnabled(True)
                self.running_simulation = False
                self.update_colormap()
                return

            self.update_colormap()
            self.sim_steps_since_draw = 0

    def update_colormap(self):
        
        self.colormap_drawn = True
        self.im.set_data(self.model.T)
        self.ax.set_title(f"2D Heat Transfer (t = {self.elapsed_time:.3f} s)", size=16, y=1.15)

        for txt in self.boundry_temp_list:
            txt.remove()
        self.boundry_temp_list.clear()

        label_top = (f'{self.model.T_top:.2f} °C')
        label_bottom = (f'{self.model.T_bottom:.2f} °C')
        label_left = (f'{self.model.T_left:.2f} °C')
        label_right = (f'{self.model.T_right:.2f} °C')
        
        T = self.model.T
        nx, ny = self.model.nx, self.model.ny
        mid_col = (ny - 1) // 2
        mid_row = (nx - 1) // 2

        txt_bottom = self.ax.text(mid_col, -3.2, label_bottom, ha='center', va='bottom', fontsize=10, color='black')
        self.boundry_temp_list.append(txt_bottom)
        txt_top = self.ax.text(mid_col, (ny-1) + 3.2, label_top, ha='center', va='top', fontsize=10, color='black')
        self.boundry_temp_list.append(txt_top)
        txt_left = self.ax.text(-3, mid_row, label_left, ha='right', va='center', fontsize=10, color='black', rotation=90)
        self.boundry_temp_list.append(txt_left)
        txt_right = self.ax.text((nx-1) + 3, mid_row, label_right, ha='left', va='center', fontsize=10, color='black', rotation=270)
        self.boundry_temp_list.append(txt_right)

        txt_bottom_left = self.ax.text(0, - 1,
                                        f"{T[0, 0]:.2f} °C",
                                        ha='center', va='center',
                                        fontsize=8, color='black')
        self.boundry_temp_list.append(txt_bottom_left)

        txt_bottom_right = self.ax.text((ny - 1) + 1,- 1,
                                        f"{T[0, ny - 1]:.2f} °C",
                                        ha='center', va='center',
                                        fontsize=8, color='black')
        self.boundry_temp_list.append(txt_bottom_right)

        txt_top_left = self.ax.text(0, (nx-1) + 1,
                                    f"{T[nx - 1, 0]:.2f} °C",
                                    ha='center', va='center',
                                    fontsize=8, color='black')
        self.boundry_temp_list.append(txt_top_left)

        txt_top_right = self.ax.text((ny - 1) +1,
                                    (nx - 1) + 1,
                                    f"{T[nx - 1, ny - 1]:.2f} °C",
                                    ha='center', va='center',
                                    fontsize=8, color='black')  
        self.boundry_temp_list.append(txt_top_right)

        txt_middle_bottom = self.ax.text(
                                        mid_col,        
                                        0 -1,        
                                        f"{T[0, mid_col]:.2f} °C",
                                        ha='center', va='center',
                                        fontsize=8, color='black')
        self.boundry_temp_list.append(txt_middle_bottom)

        txt_middle_top = self.ax.text(mid_col, (nx - 1) + 1,
                                     f"{T[nx - 1, mid_col]:.2f} °C",
                                     ha='center', va='center',
                                     fontsize=8, color='black')
        self.boundry_temp_list.append(txt_middle_top) 
       
        txt_middle_right = self.ax.text((ny-1) + 1,mid_row,
                                        f"{T[mid_row, ny-1]:.2f} °C",
                                        ha='center', va='center',
                                        rotation=270,
                                        fontsize=8, color='black')
        self.boundry_temp_list.append(txt_middle_right)
      
        txt_middle_left = self.ax.text(-1, mid_row,
                                        f"{T[mid_row, 0]:.2f} °C",
                                        ha='center', va='center',
                                        rotation=90,
                                        fontsize=8, color='black')
        self.boundry_temp_list.append(txt_middle_left) 
        
        power = self.model.heat_rate
       
        txt_rate_top_left = self.ax.text(-1, (nx-1) + 2,
                                        f"{power['corner_top_left']:.2e} J/s",
                                        ha='left',  va='top',
                                        fontsize=8, color='black')
        self.boundry_temp_list.append(txt_rate_top_left)
      
        txt_rate_top_right = self.ax.text((nx-1) + 2, (nx-1) + 2, 
                                  f"{power['corner_top_right']:.2e} J/s",
                                  ha='right', va='top',
                                  fontsize=8, color='black')
        self.boundry_temp_list.append(txt_rate_top_right)
       
        txt_rate_bottom_left = self.ax.text(-1, -2, 
                                    f"{power['corner_bottom_left']:.2e} J/s",
                                    ha='left', va='bottom',
                                    fontsize=8, color='black')
        self.boundry_temp_list.append(txt_rate_bottom_left)
        
        txt_rate_bottom_right = self.ax.text((nx-1) + 2, -2, 
                                            f"{power['corner_bottom_right']:.2e} J/s",
                                            ha='right', va='bottom', 
                                            fontsize=8, color='black')
        self.boundry_temp_list.append(txt_rate_bottom_right)
       
        txt_rate_middle_top = self.ax.text(mid_col, (ny-1) +2, 
                                            f"{power['middle_top']:.2e} J/s",
                                            ha='center', va='top',
                                            fontsize=8, color='black')
        self.boundry_temp_list.append(txt_rate_middle_top)
     
        txt_rate_middle_bottom = self.ax.text(mid_col, -2, 
                                                f"{power['middle_bottom']:.2e} J/s",
                                                ha='center', va='bottom',
                                                fontsize=8, color='black')
        self.boundry_temp_list.append(txt_rate_middle_bottom)

        txt_rate_middle_left = self.ax.text(-2, mid_row, 
                                            f"{power['middle_left']:.2e} J/s",
                                            ha='left',  va='center',
                                            rotation=90, fontsize=8, 
                                            color='black')
        self.boundry_temp_list.append(txt_rate_middle_left)

        txt_rate_middle_right = self.ax.text((nx-1) + 2, mid_row, 
                                    f"{power['middle_right']:.2e} J/s",
                                    ha='right', va='center',
                                    rotation=270, fontsize=8, 
                                    color='black')
        self.boundry_temp_list.append(txt_rate_middle_right)

        self.canvas.draw()

        self.saved_colormap_path = "colormap_temp_plot.png"
        self.fig.savefig(self.saved_colormap_path)


    def clear_colormap(self):
        self.colormap_drawn = False
        self.model = None
        self.point1_dt_list.clear()
        self.elapsed_time = 0.0
        self.point_time_list.clear()
        self.point1_temp_list.clear()
        self.hot_spot_selected = None
        self.cold_spot_selected = None
        self.adding_hot_spot = False
        self.adding_cold_spot = False
        self.custom_color_map = False

        for line in list(self.ax.lines):
            if line.get_marker() == 'o' and line.get_color() in ('red', 'blue'):
                line.remove()
                # clear their flags
        self.hot_spot_selected = None
        self.cold_spot_selected = None

        if not self.keep_point_checkbox.isChecked():
            self.clicked_point1 = None
            self.point_choisen = False
            for point in list(self.ax.lines):
                point.remove()

        for txt in self.boundry_temp_list:
            txt.remove()
        
        self.boundry_temp_list =  []

        self.canvas.draw()
        self.cbar.remove()
        self.im.remove()
        zeros = np.zeros((CalculationWindow.nx, CalculationWindow.ny))
        self.im = self.ax.imshow(
            zeros,
            cmap= "jet",
            interpolation='bicubic',
            vmin=0,
            vmax=200,
            origin='lower')
        self.cbar = self.fig.colorbar(self.im, ax=self.ax, label='Temperature (°C)', pad=0.13)
        self.ax.set_title("2D Heat Transfer Plate", size=16, y =1.08)
        self.canvas.draw()

    def open_graph(self):
            if not self.point_choisen:
                QMessageBox.warning(self, "No Data", "Please click on the plate to have a point to record data before running the simulation.")
                return

            self.graph_window = GraphWindow(self)
            self.graph_window.show()

    def save_simulation_state(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Simulation State As…",
            os.path.expanduser("~") + "/my_simulation.pkl",
            "Pickle Files (*.pkl)"
        )
        if not file_path:
            return
        if not file_path.lower().endswith(".pkl"):
            file_path += ".pkl"

        state = {
            "settings": pd.DataFrame({
                "Setting": [
                    "Initial Temp", "Top", "Bottom", "Left", "Right",
                    "Mass", "Heat Capacity", "Color Min", "Color Mid", "Color Max",
                    "Elapsed Time", "Clicked Point", "Hot Spot", "Cold Spot", "Custom Color Map"
                ],
                "Value": [
                    self.initial_condition.value(),
                    self.top_temp.value(),
                    self.bottom_temp.value(),
                    self.left_temp.value(),
                    self.right_temp.value(),
                    self.mass.value(),
                    self.h_capacity.value(),
                    self.combo_min.currentText(),
                    self.combo_mid.currentText(),
                    self.combo_max.currentText(),
                    self.elapsed_time,
                    self.clicked_point1,
                    self.hot_spot_selected,
                    self.cold_spot_selected,
                    self.custom_color_map
                ]
            }),
            "corner_heat_history": self.model.corner_heat_history.copy(),
            "middle_heat_history": self.model.middle_heat_history.copy(),
            
            "point_data": pd.DataFrame({
                "Time [s]": self.point_time_list,
                "Temp [°C]": self.point1_temp_list,
                "dT/dt [°C/s]": self.point1_dt_list
            }),
            "temperature_matrix": pd.DataFrame(self.model.T),
            "heat_rate": pd.DataFrame({
                "Point":           list(self.model.heat_rate.keys()),
                "Heat Rate [J/s]": list(self.model.heat_rate.values())
            })
        }
            
        pd.to_pickle(state, file_path)
        QMessageBox.information(self, "Saved", f"State saved to:\n{file_path}")


    def load_simulation_state(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Simulation State…",
            os.path.expanduser("~"),
            "Pickle Files (*.pkl)"
        )
        if not file_path or not os.path.exists(file_path):
            return

        state = pd.read_pickle(file_path)

        df_settings = state.get("settings")
        if df_settings is not None:
            vals = df_settings["Value"].tolist()
            if len(vals) >= 15:
                self.initial_condition.setValue(float(vals[0]))
                self.top_temp.setValue(float(vals[1]))
                self.bottom_temp.setValue(float(vals[2]))
                self.left_temp.setValue(float(vals[3]))
                self.right_temp.setValue(float(vals[4]))
                self.mass.setValue(float(vals[5]))
                self.h_capacity.setValue(float(vals[6]))
                self.combo_min.setCurrentText(vals[7])
                self.combo_mid.setCurrentText(vals[8])
                self.combo_max.setCurrentText(vals[9])
                self.elapsed_time = float(vals[10])
                self.clicked_point1 = vals[11]
                self.hot_spot_selected = vals[12]  
                self.cold_spot_selected = vals[13]
                self.custom_color_map = bool(vals[14])

        df_point = state.get("point_data")
        if df_point is not None:
            self.point_time_list  = df_point["Time [s]"].tolist()
            self.point1_temp_list = df_point["Temp [°C]"].tolist()
            self.point1_dt_list   = df_point["dT/dt [°C/s]"].tolist()
            self.point_choisen    = bool(self.point_time_list)
        else:
            self.point_time_list = []
            self.point1_temp_list = []
            self.point1_dt_list = []
            self.point_choisen = False

        if self.custom_color_map:
            self.build_colormap()
        else:
            self.im.set_cmap("jet")
            self.im.set_clim(0, self.max_temp)
            self.cbar.remove()
            self.cbar = self.fig.colorbar(self.im, ax=self.ax,
                                        label='Temperature (°C)', pad=0.13)


        df_temp = state.get("temperature_matrix")
        if df_temp is None:
            QMessageBox.warning(self, "Missing Data", "No temperature matrix saved.")
            return

        self.model = CalculationWindow(
            self.initial_condition.value(),
            self.top_temp.value(),
            self.bottom_temp.value(),
            self.left_temp.value(),
            self.right_temp.value(),
            self.mass.value(),
            self.h_capacity.value()
        )
        self.model.T = df_temp.values

        self.model.corner_heat_history = state.get("corner_heat_history", {})
        self.model.middle_heat_history = state.get("middle_heat_history", {})
        


        df_htr = state.get("heat_rate")
        if df_htr is not None:
            for _, row in df_htr.iterrows():
                pt, q = row["Point"], float(row["Heat Rate [J/s]"])
                if pt in self.model.heat_rate:
                    self.model.heat_rate[pt] = q
        else:
            QMessageBox.warning(self, "Missing Data", "No heat‐rate saved.")
            return

        self.update_colormap()
        self.canvas.draw()
        
        for ln in list(self.ax.lines):
            ln.remove()
        
        if self.point_choisen and self.clicked_point1:
            x, y = self.clicked_point1
            self.ax.plot(x, y, marker='o', color='purple', markersize=6)
        self.canvas.draw()

        if self.hot_spot_selected:
            x, y = self.hot_spot_selected
            self.model.T[x, y] = self.model.hot_temp
            self.hot_spot = True
            self.ax.plot(y, x, marker='o', color='red', markersize=8)
        self.canvas.draw()
        
        if self.cold_spot_selected:
            x, y = self.cold_spot_selected
            self.model.T[x, y] = self.model.cold_temp
            self.cold_spot = True
            self.ax.plot(y, x, marker='o', color='blue', markersize=8)
        self.canvas.draw()

        self.saved_graph_temp_path = None
        self.saved_graph_dTdt_path = None
        
        QMessageBox.information(self, "Loaded", f"Loaded state from:\n{file_path}")

    def export_to_exl(self):
            path, _ = QFileDialog.getSaveFileName(
                self,
                "Export to CSV",
                "heat_transfer.csv",
                "CSV Files (*.csv)")

            if path == "":
                return

            with open(path, "w", encoding="utf-8") as fp:
                fp.write("Selected Point Data:\n")
                fp.write("Time [s], Temperature [C], dT/dt [C/s]\n")
                for i in range(len(self.point_time_list)):
                    t = self.point_time_list[i]
                    temp = self.point1_temp_list[i]
                    dtdt = self.point1_dt_list[i]
                    fp.write(f"{t}, {temp}, {dtdt}\n")

                for name, q_list in self.model.corner_heat_history.items():
                    fp.write(f"Corner Heat Rate - {name}\n")
                    fp.write("Step, q̇ [W]\n")
                    for i in range(len(q_list)):
                        q = q_list[i]
                        fp.write(f"{i}, {q}\n")
                    fp.write("\n")

                for name, q_list in self.model.middle_heat_history.items():
                    fp.write(f"Middle Heat Rate - {name}\n")
                    fp.write("Step, q̇ [W]\n")
                    for i in range(len(q_list)):
                        q = q_list[i]
                        fp.write(f"{i}, {q}\n")
                    fp.write("\n")

                fp.write(f"Initial Temperature [C], {self.initial_condition.value()}\n")
                fp.write("Boundary Conditions:\n")
                fp.write(f"Top    [°C], {self.model.T_top}\n")
                fp.write(f"Bottom [°C], {self.model.T_bottom}\n")
                fp.write(f"Left   [°C], {self.model.T_left}\n")
                fp.write(f"Right  [°C], {self.model.T_right}\n")
                fp.write("\n")

                fp.write("Corner Temperatures (Fixed Average):\n")
                for name in self.model.points:
                    if "corner" in name:
                        i, j = self.model.points[name]
                        temp = self.model.T[i, j]
                        fp.write(f"{name}, {temp:.3f} C\n")
                fp.write("\n")

                fp.write("Middle Boundary Temperatures:\n")
                for name in self.model.points:
                    if "middle" in name:
                        i, j = self.model.points[name]
                        temp = self.model.T[i, j]
                        fp.write(f"{name}, {temp:.3f} C\n")
                fp.write("\n")


                fp.write("Hot Spot:\n")
                if self.hot_spot_selected is not None:
                    i, j = self.hot_spot_selected
                    temp = self.model.T[i, j]
                    fp.write(f"  ({i}, {j}): {temp:.3f} C\n")
                else:
                    fp.write("  None\n")
                fp.write("\n")

                fp.write("Cold Spots:\n")
                if self.cold_spot_selected is not None:
                    i, j = self.cold_spot_selected
                    temp = self.model.T[i, j]
                    fp.write(f"  ({i}, {j}): {temp:.3f} C\n")
                else:
                    fp.write("  None\n")
                fp.write("\n")
                

            os.startfile(path)

    def export_pdf_report(self):

            if (self.saved_graph_temp_path is None or
                self.saved_graph_dTdt_path is None or
                self.saved_colormap_path is None or
                not os.path.exists(self.saved_graph_temp_path) or
                not os.path.exists(self.saved_graph_dTdt_path) or
                not os.path.exists(self.saved_colormap_path)):

                QMessageBox.warning(self, "Missing Images",
                    "Please make sure you have:\n"
                    "1. Opened the Graph Window\n"
                    "2. Drawn and saved BOTH graphs (Temp and dT/dt)\n"
                    "3. You must save the graphs with different file names"
                    "\nOnly then can we create the PDF report.")
                return

            path, _ = QFileDialog.getSaveFileName(
                self,
                "Save PDF Report",
                "heat_transfer_report.pdf",
                "PDF Files (*.pdf)")
            if path == "":
                return

            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()

            pdf.set_font("Arial", 'B', 16)
            pdf.cell(0, 10, "2D Heat Transfer Simulation Report", ln=True, align='C')
            pdf.ln(10)

            pdf.set_font("Arial", "B", size=15)
            pdf.cell(0, 10, "Simulation Settings:", ln=True)
            pdf.ln(5)
            pdf.set_font("Arial","B", size=14)
            pdf.cell(0, 8, f"Initial Condition: {self.initial_condition.value()} °C", ln=True)
            pdf.cell(0, 8, f"Top Temperature:    {self.top_temp.value()} °C", ln=True)
            pdf.cell(0, 8, f"Bottom Temperature: {self.bottom_temp.value()} °C", ln=True)
            pdf.cell(0, 8, f"Left Temperature:   {self.left_temp.value()} °C", ln=True)
            pdf.cell(0, 8, f"Right Temperature:  {self.right_temp.value()} °C", ln=True)

            pdf.ln(5)

            pdf.cell(0, 8, f"Mass:               {self.mass.value()} kg", ln=True)
            pdf.cell(0, 8, f"Heat Capacity:      {self.h_capacity.value()} J/kg°C", ln=True)
            pdf.cell(0, 8, f"Elapsed Time:       {self.elapsed_time:.2f} seconds", ln=True)
            pdf.ln(5)

            if not self.custom_color_map:
                pdf.cell(0, 8, "Colormap: Default (jet)", ln=True)
            else:
                pdf.cell(0, 8, "Colormap Colors:", ln=True)
                pdf.cell(0, 8, f"Minimum Color: {self.combo_min.currentText()}", ln=True)
                pdf.cell(0, 8, f"Middle Color:  {self.combo_mid.currentText()}", ln=True)
                pdf.cell(0, 8, f"Maximum Color: {self.combo_max.currentText()}", ln=True)
            pdf.ln(5)

            if self.clicked_point1:
                x, y = self.clicked_point1
                pdf.cell(0, 8, f"Tracked Point: ({x}, {y})", ln=True)

            if self.hot_spot_selected:
                x_h, y_h = self.hot_spot_selected
                pdf.cell(0, 8, f"Hot Spot: ({x_h}, {y_h})", ln=True)

            if self.cold_spot_selected:
                x_c, y_c = self.cold_spot_selected
                pdf.cell(0, 8, f"Cold Spot: ({x_c}, {y_c})", ln=True)

            pdf.cell(0, 10, "Final Temperature Map:", ln=True)
            pdf.image(self.saved_colormap_path, x = 30, w=160)
            pdf.ln(5)

            pdf.cell(0, 10, "Graph: Temperature vs Time", ln=True)
            pdf.image(self.saved_graph_temp_path, x = 30, w=120)
            pdf.ln(5)

            pdf.cell(0, 10, "Graph: dT/dt vs Time", ln=True)
            pdf.image(self.saved_graph_dTdt_path, x= 30,w=120)

            pdf.output(path)
            os.startfile(path)

if __name__ == "__main__":
    app = QApplication([])
    window = SimulationWindow()
    window.show()
    app.exec()



