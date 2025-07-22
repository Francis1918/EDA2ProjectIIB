from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QTableWidget, QTableWidgetItem, QComboBox, QLineEdit,
                             QHeaderView, QMessageBox)
from PyQt5.QtCore import Qt


class ConfigPatronesWidget(QWidget):
    def __init__(self, patrones_manager):
        super().__init__()
        self.patrones_manager = patrones_manager
        self.init_ui()
        self.cargar_patrones()

    def init_ui(self):
        # Layout principal
        main_layout = QVBoxLayout()

        # Título
        title_label = QLabel("Configuración de Patrones de Ciberacoso")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        main_layout.addWidget(title_label)

        # Tabla de patrones
        self.table = QTableWidget()
        self.table.setColumnCount(4)  # Patrón, Tipo, Nivel, Acciones
        self.table.setHorizontalHeaderLabels(["Patrón", "Tipo", "Nivel de Severidad", "Acciones"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        main_layout.addWidget(self.table)

        # Formulario para agregar nuevo patrón
        form_layout = QHBoxLayout()

        self.patron_input = QLineEdit()
        self.patron_input.setPlaceholderText("Nuevo patrón...")

        self.tipo_combo = QComboBox()
        self.tipo_combo.addItems(["Insulto", "Amenaza", "Exclusión", "Burla"])

        self.nivel_combo = QComboBox()
        self.nivel_combo.addItems(["Alto", "Moderado", "Bajo"])

        self.add_button = QPushButton("Agregar")
        self.add_button.clicked.connect(self.agregar_patron)

        form_layout.addWidget(self.patron_input)
        form_layout.addWidget(self.tipo_combo)
        form_layout.addWidget(self.nivel_combo)
        form_layout.addWidget(self.add_button)

        main_layout.addLayout(form_layout)

        # Botones de guardar/cargar
        buttons_layout = QHBoxLayout()

        self.save_button = QPushButton("Guardar Cambios")
        self.save_button.clicked.connect(self.guardar_cambios)

        self.load_button = QPushButton("Recargar desde Archivo")
        self.load_button.clicked.connect(self.cargar_patrones)

        buttons_layout.addWidget(self.save_button)
        buttons_layout.addWidget(self.load_button)

        main_layout.addLayout(buttons_layout)

        self.setLayout(main_layout)

    def cargar_patrones(self):
        """Carga los patrones desde el gestor a la tabla"""
        patrones = self.patrones_manager.obtener_patrones()

        self.table.setRowCount(0)  # Limpiar tabla

        for i, (patron, tipo, nivel) in enumerate(patrones):
            self.table.insertRow(i)

            # Añadir datos a la tabla
            self.table.setItem(i, 0, QTableWidgetItem(patron))
            self.table.setItem(i, 1, QTableWidgetItem(tipo))
            self.table.setItem(i, 2, QTableWidgetItem(nivel))

            # Botón de eliminar
            delete_button = QPushButton("Eliminar")
            delete_button.clicked.connect(lambda checked, row=i: self.eliminar_patron(row))

            self.table.setCellWidget(i, 3, delete_button)

    def agregar_patron(self):
        """Agrega un nuevo patrón a la lista"""
        patron = self.patron_input.text().strip()
        tipo = self.tipo_combo.currentText()
        nivel = self.nivel_combo.currentText()

        if not patron:
            QMessageBox.warning(self, "Error", "El patrón no puede estar vacío")
            return

        # Agregar al gestor
        self.patrones_manager.agregar_patron(patron, tipo, nivel)

        # Actualizar tabla
        self.cargar_patrones()

        # Limpiar campo
        self.patron_input.clear()

    def eliminar_patron(self, row):
        """Elimina un patrón de la lista"""
        if self.patrones_manager.eliminar_patron(row):
            self.cargar_patrones()

    def guardar_cambios(self):
        """Guarda los cambios al archivo CSV"""
        if self.patrones_manager.guardar_a_csv("data/patrones_ciberacoso.csv"):
            QMessageBox.information(self, "Éxito", "Patrones guardados correctamente")
        else:
            QMessageBox.warning(self, "Error", "No se pudieron guardar los patrones")