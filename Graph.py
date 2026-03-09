from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QComboBox, QMessageBox,  QFileDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import os


class GraphWindow(QWidget):
    def __init__(self, main_window=None):
        super().__init__()
        self.main = main_window
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Graph Window")
        self.setGeometry(900, 200, 730, 570)
        self.setStyleSheet('''QWidget { font-size: 16px; }''')
        with open("stylesheet.css", "r", encoding="utf-8") as fp:
            self.setStyleSheet(fp.read())
         
        self.draw_button = QPushButton("Draw", self)
        self.draw_button.setGeometry(20, 80, 150, 40)
        self.draw_button.clicked.connect(self.draw_graph)

        self.csv_button = QPushButton("Export to CSV", self)
        self.csv_button.setGeometry(20, 200, 150, 40)
        self.csv_button.clicked.connect(self.export_to_csv)

        self.save_button = QPushButton("Save", self)
        self.save_button.setGeometry(20, 140, 150, 40)
        self.save_button.clicked.connect(self.save_graph)

        self.graph_type_combo = QComboBox(self)
        self.graph_type_combo.setGeometry(20, 20, 150, 30)
        self.graph_type_combo.addItems(["Choose Graph","Temp vs Time", "dT/dt vs Time"])

        self.graph = FigureCanvas(Figure())
        self.graph.setParent(self)
        self.graph.setGeometry(200, 20, 500, 500)

    def setup_graph(self):
        self.ax = self.graph.figure.subplots()
        self.graph.draw()

    def show(self):
        super().show()
        self.setup_graph()
    
    def draw_graph(self):
        self.ax.clear()
        choice = self.graph_type_combo.currentText()

        if choice == "Choose Graph":
            QMessageBox.warning(self, "Warning", "Please select a graph type before drawing.")
            return

        time_list = self.main.point_time_list
        temp_list = self.main.point1_temp_list
        dtemp_list = self.main.point1_dt_list

        if not time_list:
            QMessageBox.warning(self, "Warning", "No data available to draw.")
            return

        if choice == "Temp vs Time":
            self.ax.plot(time_list, temp_list, label='T(t)', color='blue')
            self.ax.set_title("Temperature vs Time", fontsize=18)
            self.ax.set_ylabel("Temperature (°C)", fontsize=14)

        elif choice == "dT/dt vs Time":
            n = min(len(time_list), len(dtemp_list))
            t = time_list[:n]
            dt = dtemp_list[:n]

            dt = [x if isinstance(x, (int, float)) else 0 for x in dt]

            self.ax.plot(t, dt, label='dT/dt', color='red')
            self.ax.set_title("dT/dt vs Time", fontsize=18)
            self.ax.set_ylabel("Rate of Change (°C/s)", fontsize=14)

        self.ax.set_xlabel("Time (seconds)", fontsize=14)
        self.ax.legend()
        self.ax.figure.tight_layout()
        self.ax.grid(True)
        self.graph.draw()

    # def draw_graph(self):
    #         self.ax.clear()
    #         choice = self.graph_type_combo.currentText()

    #         if choice == "Choose Graph":
    #             QMessageBox.warning(self, "Warning", "Please select a graph type before drawing.")
    #             return

    #         time_list = self.main.point_time_list
    #         temp_list = self.main.point1_temp_list
    #         dtemp_list = self.main.point1_dt_list

    #         if not time_list:
    #             QMessageBox.warning(self, "Warning", "No data available to draw.")
    #             return

    #         if choice == "Temp vs Time":
    #                 self.ax.plot(time_list, temp_list, label='T(t)', color='blue')
    #                 self.ax.set_title("Temperature vs Time", fontsize=18)
    #                 self.ax.set_ylabel("Temperature (°C)", fontsize=14)
    #         elif choice == "dT/dt vs Time":
    #             if len(dtemp_list) != len(time_list):
    #                 dtemp_list = dtemp_list[:len(time_list)]
    #             self.ax.plot(time_list, dtemp_list, label='dT/dt', color='red')
    #             self.ax.set_title("dT/dt vs Time", fontsize=18)
    #             self.ax.set_ylabel("Rate of Change (°C/s)", fontsize=14)

    #         self.ax.set_xlabel("Time (seconds)", fontsize=14)
    #         self.ax.legend()
    #         self.ax.figure.tight_layout()
    #         self.ax.grid(True)
    #         self.graph.draw()
    
    def clear_graph(self):
        self.ax.clear()

        self.ax.set_xlabel("Time (seconds)", fontsize=14)
        self.ax.set_ylabel("Temperature (°C)", fontsize=14)
        self.ax.set_title("Temperature vs Time", fontsize=18)
        self.setup_graph()

    def export_to_csv(self):
            time_list = self.main.point_time_list
            temp_list = self.main.point1_temp_list
            dtemp_list = self.main.point1_dt_list

            with open("heat_transfer.csv", "w") as fp:
                fp.write("Time[sec], Temp [°C], dT/dt [°C/s]\n")
                for i in range(len(time_list)):
                    t = time_list[i]
                    T = temp_list[i]
                    dTdt = dtemp_list[i] if i < len(dtemp_list) else ""
                    fp.write(f"{t}, {T}, {dTdt}\n")
            os.startfile("heat_transfer.csv")
   
    def save_graph(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save Image", "heat_transfer_plot.png", "PNG Files (*.png)")
        if not filename:
            return

        self.graph.figure.savefig(filename)

        if self.main:
            choice = self.graph_type_combo.currentText()
            if choice == "Temp vs Time":
                self.main.saved_graph_temp_path = filename
            elif choice == "dT/dt vs Time":
                self.main.saved_graph_dTdt_path = filename

        os.startfile(filename)
                        

if __name__ == "__main__":
    app = QApplication()
    graph_window = GraphWindow()
    graph_window.show()
    app.exec()