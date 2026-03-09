
from PySide6.QtWidgets import QApplication, QPushButton, QWidget, QLabel, QMessageBox
from About import InfoWindow
from Sim import SimulationWindow
import os
import sys


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("My Simulation")
        self.setGeometry(600, 200, 300, 400)
        
        with open("stylesheet.css", "r", encoding="utf-8") as fp:
            self.setStyleSheet(fp.read())
        
        self.name = QLabel("Welcome to my\nHeat Transfer Simulation",self)
        self.name.setGeometry(60, 40, 250, 40)
        self.name.setStyleSheet("font-size: 18px; font-weight: bold; color: #333;")

        self.button_simulation = QPushButton("Start Simulation", self)
        self.button_simulation.setGeometry(60, 100, 150, 40)
        self.button_simulation.clicked.connect(self.open_simulation)

        self.button_video = QPushButton("Show Video", self)
        self.button_video.setGeometry(60,150, 150, 40)
        self.button_video.clicked.connect(self.open_video)

        self.button_document = QPushButton("Open Document", self)
        self.button_document.setGeometry(60, 200, 150, 40)
        self.button_document.clicked.connect(self.open_document)
        
        self.button_about = QPushButton("About", self)
        self.button_about.setGeometry(60, 250, 150, 40)
        self.button_about.clicked.connect(self.open_about)
    
    def open_simulation(self):
            self.main_simulation = SimulationWindow()
            self.main_simulation.show()
    
    def open_video(self):
        video_path = os.path.abspath("video.mp4")
        if os.path.exists(video_path):
            os.startfile(video_path)
        else:
            QMessageBox.warning(self, "Video Not Found", f"Cannot find the video:\n{video_path}")
    
    def open_document(self):
        path = "doc.docx" 

        if not os.path.exists(path):
            path = "doc.docx"
            if not os.path.exists(path):
                QMessageBox.warning(self, "File Not Found", f"Cannot find the file:\n{path}")
                return

        if sys.platform == "win32":
            os.startfile(os.path.abspath(path))
        elif sys.platform == "darwin":  
            os.system(f'open "{os.path.abspath(path)}"')
        else:  
            os.system(f'xdg-open "{os.path.abspath(path)}"')


    def open_about(self):
         self.about = InfoWindow()
         self.about.show()



            
if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()