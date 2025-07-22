from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QTextEdit, QFileDialog, QGroupBox)
from PyQt5.QtCore import pyqtSignal
from backend.utils.procesador_texto import detect_patterns


class CargaMensajesWidget(QWidget):
    # Señal para comunicar que el análisis ha terminado
    analisis_completado = pyqtSignal(list)

    def __init__(self, patrones_manager):
        super().__init__()
        self.patrones_manager = patrones_manager
        self.init_ui()

    def init_ui(self):
        # Layout principal
        main_layout = QVBoxLayout()

        # Sección de carga de archivos
        file_group = QGroupBox("Cargar archivo de chat")
        file_layout = QVBoxLayout()

        self.file_label = QLabel("Ningún archivo seleccionado")
        self.file_button = QPushButton("Seleccionar archivo")
        self.file_button.clicked.connect(self.seleccionar_archivo)

        file_layout.addWidget(self.file_label)
        file_layout.addWidget(self.file_button)
        file_group.setLayout(file_layout)

        # Sección de ingreso manual
        text_group = QGroupBox("Ingreso manual de texto")
        text_layout = QVBoxLayout()

        self.text_edit = QTextEdit()
        text_layout.addWidget(self.text_edit)
        text_group.setLayout(text_layout)

        # Botón de análisis
        self.analyze_button = QPushButton("ANALIZAR")
        self.analyze_button.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 10px;")
        self.analyze_button.clicked.connect(self.analizar_texto)

        # Añadir todo al layout principal
        main_layout.addWidget(file_group)
        main_layout.addWidget(text_group)
        main_layout.addWidget(self.analyze_button)

        self.setLayout(main_layout)

    def seleccionar_archivo(self):
        """Abre un diálogo para seleccionar un archivo de texto"""
        file_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo de chat", "",
                                                   "Archivos de texto (*.txt);;Todos los archivos (*)")

        if file_path:
            self.file_label.setText(file_path)
            # Cargar contenido del archivo en el editor de texto
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    self.text_edit.setText(file.read())
            except Exception as e:
                self.file_label.setText(f"Error al abrir archivo: {e}")

    def analizar_texto(self):
        """Analiza el texto ingresado buscando patrones de ciberacoso"""
        texto = self.text_edit.toPlainText()
        if not texto:
            return

        # Obtener patrones del gestor
        patrones = self.patrones_manager.obtener_patrones()

        # Detectar patrones en el texto
        resultados = detect_patterns(texto, patrones)

        # Emitir señal con los resultados
        self.analisis_completado.emit(resultados)