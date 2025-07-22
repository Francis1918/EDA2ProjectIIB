import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget
from frontend.ventanas.carga_mensajes import CargaMensajesWidget
from frontend.ventanas.config_patrones import ConfigPatronesWidget
from frontend.ventanas.resultados import ResultadosWidget
from frontend.ventanas.animacion import AnimacionWidget
from frontend.ventanas.estadisticas import EstadisticasWidget
from backend.modelos.patrones import PatronesManager


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configuración de la ventana principal
        self.setWindowTitle("Sistema de Detección Temprana de Ciberacoso")
        self.setGeometry(100, 100, 1000, 600)

        # Inicializar el gestor de patrones
        self.patrones_manager = PatronesManager("data/patrones_ciberacoso.csv")

        # Crear pestañas
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Inicializar widgets de cada pestaña
        self.carga_mensajes = CargaMensajesWidget(self.patrones_manager)
        self.config_patrones = ConfigPatronesWidget(self.patrones_manager)
        self.resultados = ResultadosWidget()
        self.animacion = AnimacionWidget()
        self.estadisticas = EstadisticasWidget()

        # Añadir pestañas
        self.tabs.addTab(self.carga_mensajes, "Carga de Mensajes")
        self.tabs.addTab(self.config_patrones, "Configuración de Patrones")
        self.tabs.addTab(self.resultados, "Resultados")
        self.tabs.addTab(self.animacion, "Animación de Algoritmos")
        self.tabs.addTab(self.estadisticas, "Estadísticas")

        # Conectar señales
        self.carga_mensajes.analisis_completado.connect(self.mostrar_resultados)

    def mostrar_resultados(self, resultados):
        """Muestra los resultados del análisis en la pestaña correspondiente"""
        self.resultados.actualizar_resultados(resultados)
        self.tabs.setCurrentIndex(2)  # Cambiar a la pestaña de resultados


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())