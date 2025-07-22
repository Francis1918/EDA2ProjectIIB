from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QTableWidget, QTableWidgetItem, QTextEdit, QHeaderView,
                             QGroupBox, QSplitter)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor


class ResultadosWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.resultados = []
        self.init_ui()

    def init_ui(self):
        # Layout principal
        main_layout = QVBoxLayout()

        # Título
        title_label = QLabel("Resultados del Análisis")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        main_layout.addWidget(title_label)

        # Resumen
        self.resumen_group = QGroupBox("Resumen")
        resumen_layout = QVBoxLayout()

        self.resumen_text = QTextEdit()
        self.resumen_text.setReadOnly(True)
        resumen_layout.addWidget(self.resumen_text)

        self.resumen_group.setLayout(resumen_layout)

        # Tabla de alertas
        self.alertas_group = QGroupBox("Alertas Detectadas")
        alertas_layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(5)  # Patrón, Tipo, Nivel, Posición, Algoritmo
        self.table.setHorizontalHeaderLabels(["Patrón", "Tipo", "Severidad", "Posición", "Algoritmo"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.table.itemClicked.connect(self.mostrar_contexto)

        alertas_layout.addWidget(self.table)
        self.alertas_group.setLayout(alertas_layout)

        # Contexto
        self.contexto_group = QGroupBox("Contexto")
        contexto_layout = QVBoxLayout()

        self.contexto_text = QTextEdit()
        self.contexto_text.setReadOnly(True)
        contexto_layout.addWidget(self.contexto_text)

        self.contexto_group.setLayout(contexto_layout)

        # Crear un splitter para dividir la pantalla
        splitter = QSplitter(Qt.Vertical)
        splitter.addWidget(self.resumen_group)

        alertas_contexto_splitter = QSplitter(Qt.Horizontal)
        alertas_contexto_splitter.addWidget(self.alertas_group)
        alertas_contexto_splitter.addWidget(self.contexto_group)

        splitter.addWidget(alertas_contexto_splitter)

        # Botones de acción
        buttons_layout = QHBoxLayout()

        self.export_button = QPushButton("Exportar Resultados")
        self.export_button.clicked.connect(self.exportar_resultados)

        buttons_layout.addWidget(self.export_button)
        buttons_layout.addStretch()

        # Añadir todo al layout principal
        main_layout.addWidget(splitter)
        main_layout.addLayout(buttons_layout)

        self.setLayout(main_layout)

    def actualizar_resultados(self, resultados):
        """Actualiza la vista con los nuevos resultados"""
        self.resultados = resultados

        # Actualizar resumen
        self.actualizar_resumen()

        # Actualizar tabla
        self.actualizar_tabla()

    def actualizar_resumen(self):
        """Actualiza el resumen con estadísticas de los resultados"""
        if not self.resultados:
            self.resumen_text.setText("No se encontraron patrones de ciberacoso.")
            return

        # Contar por tipo
        tipos = {}
        niveles = {}

        for resultado in self.resultados:
            tipo = resultado['tipo']
            nivel = resultado['nivel']

            tipos[tipo] = tipos.get(tipo, 0) + 1
            niveles[nivel] = niveles.get(nivel, 0) + 1

        # Crear texto de resumen
        resumen = f"<h3>Análisis Completado</h3>"
        resumen += f"<p>Se encontraron <b>{len(self.resultados)}</b> posibles indicadores de ciberacoso.</p>"

        resumen += "<h4>Distribución por tipo:</h4>"
        resumen += "<ul>"
        for tipo, count in tipos.items():
            resumen += f"<li><b>{tipo}:</b> {count}</li>"
        resumen += "</ul>"

        resumen += "<h4>Distribución por severidad:</h4>"
        resumen += "<ul>"
        for nivel, count in niveles.items():
            resumen += f"<li><b>{nivel}:</b> {count}</li>"
        resumen += "</ul>"

        # Recomendaciones basadas en la severidad
        if niveles.get("Alto", 0) > 0:
            resumen += "<p><b>Recomendación:</b> Se detectaron patrones de alta severidad. Se recomienda intervención inmediata.</p>"
        elif niveles.get("Moderado", 0) > 0:
            resumen += "<p><b>Recomendación:</b> Se detectaron patrones de severidad moderada. Se recomienda monitoreo continuo.</p>"
        else:
            resumen += "<p><b>Recomendación:</b> Se detectaron patrones de baja severidad. Se recomienda observación periódica.</p>"

        self.resumen_text.setHtml(resumen)

    def actualizar_tabla(self):
        """Actualiza la tabla con los resultados"""
        self.table.setRowCount(0)  # Limpiar tabla

        for i, resultado in enumerate(self.resultados):
            self.table.insertRow(i)

            # Añadir datos a la tabla
            self.table.setItem(i, 0, QTableWidgetItem(resultado['patron']))
            self.table.setItem(i, 1, QTableWidgetItem(resultado['tipo']))
            self.table.setItem(i, 2, QTableWidgetItem(resultado['nivel']))
            self.table.setItem(i, 3, QTableWidgetItem(str(resultado['posicion'])))
            self.table.setItem(i, 4, QTableWidgetItem(resultado['algoritmo']))

            # Colorear según severidad
            color = QColor(255, 255, 255)  # Blanco por defecto
            if resultado['nivel'] == "Alto":
                color = QColor(255, 200, 200)  # Rojo claro
            elif resultado['nivel'] == "Moderado":
                color = QColor(255, 230, 200)  # Naranja claro
            elif resultado['nivel'] == "Bajo":
                color = QColor(230, 255, 230)  # Verde claro

            for j in range(5):
                self.table.item(i, j).setBackground(color)

    def mostrar_contexto(self, item):
        """Muestra el contexto de la alerta seleccionada"""
        row = item.row()
        if row < len(self.resultados):
            resultado = self.resultados[row]

            # Obtener contexto y resaltar el patrón
            contexto = resultado['contexto']
            patron = resultado['patron']

            # Crear HTML con el patrón resaltado
            html_contexto = contexto.replace(patron,
                                             f"<span style='background-color: yellow; font-weight: bold;'>{patron}</span>")

            # Mostrar información adicional
            html = f"<h4>Contexto de la alerta:</h4>"
            html += f"<p>{html_contexto}</p>"
            html += f"<p><b>Tipo:</b> {resultado['tipo']}</p>"
            html += f"<p><b>Severidad:</b> {resultado['nivel']}</p>"
            html += f"<p><b>Algoritmo utilizado:</b> {resultado['algoritmo']}</p>"

            self.contexto_text.setHtml(html)

    def exportar_resultados(self):
        """Exporta los resultados a un archivo"""
        # Esta función se implementaría para exportar a PDF, CSV, etc.
        pass