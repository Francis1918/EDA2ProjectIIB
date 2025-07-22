from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QComboBox, QGroupBox, QSplitter)
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np


class MatplotlibCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        super(MatplotlibCanvas, self).__init__(self.fig)


class EstadisticasWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Layout principal
        main_layout = QVBoxLayout()

        # Título
        title_label = QLabel("Estadísticas del Sistema")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        main_layout.addWidget(title_label)

        # Controles
        controls_layout = QHBoxLayout()

        self.period_combo = QComboBox()
        self.period_combo.addItems(["Última semana", "Último mes", "Último trimestre", "Último año"])
        self.period_combo.currentIndexChanged.connect(self.actualizar_estadisticas)

        self.refresh_button = QPushButton("Actualizar")
        self.refresh_button.clicked.connect(self.actualizar_estadisticas)

        controls_layout.addWidget(QLabel("Período:"))
        controls_layout.addWidget(self.period_combo)
        controls_layout.addWidget(self.refresh_button)
        controls_layout.addStretch()

        main_layout.addLayout(controls_layout)

        # Gráficos
        charts_layout = QHBoxLayout()

        # Gráfico 1: Distribución por tipo
        self.chart1 = MatplotlibCanvas(self, width=5, height=4, dpi=100)
        chart1_group = QGroupBox("Distribución por Tipo")
        chart1_layout = QVBoxLayout()
        chart1_layout.addWidget(self.chart1)
        chart1_group.setLayout(chart1_layout)

        # Gráfico 2: Distribución por severidad
        self.chart2 = MatplotlibCanvas(self, width=5, height=4, dpi=100)
        chart2_group = QGroupBox("Distribución por Severidad")
        chart2_layout = QVBoxLayout()
        chart2_layout.addWidget(self.chart2)
        chart2_group.setLayout(chart2_layout)

        charts_layout.addWidget(chart1_group)
        charts_layout.addWidget(chart2_group)

        main_layout.addLayout(charts_layout)

        # Gráficos inferiores
        charts2_layout = QHBoxLayout()

        # Gráfico 3: Tendencia temporal
        self.chart3 = MatplotlibCanvas(self, width=5, height=4, dpi=100)
        chart3_group = QGroupBox("Tendencia Temporal")
        chart3_layout = QVBoxLayout()
        chart3_layout.addWidget(self.chart3)
        chart3_group.setLayout(chart3_layout)

        # Gráfico 4: Rendimiento de algoritmos
        self.chart4 = MatplotlibCanvas(self, width=5, height=4, dpi=100)
        chart4_group = QGroupBox("Rendimiento de Algoritmos")
        chart4_layout = QVBoxLayout()
        chart4_layout.addWidget(self.chart4)
        chart4_group.setLayout(chart4_layout)

        charts2_layout.addWidget(chart3_group)
        charts2_layout.addWidget(chart4_group)

        main_layout.addLayout(charts2_layout)

        self.setLayout(main_layout)

        # Inicializar gráficos
        self.actualizar_estadisticas()

    def actualizar_estadisticas(self):
        """Actualiza los gráficos con datos de ejemplo"""
        # Gráfico 1: Distribución por tipo
        self.chart1.fig.clear()
        ax1 = self.chart1.fig.add_subplot(111)

        categories = ['Insultos', 'Amenazas', 'Exclusión', 'Burlas']
        values = [42, 15, 28, 35]
        colors = ['#ff9800', '#f44336', '#2196f3', '#9c27b0']

        ax1.bar(categories, values, color=colors, alpha=0.7)
        ax1.set_ylabel('Número de alertas')
        ax1.tick_params(axis='x', rotation=45)
        ax1.grid(axis='y', linestyle='--', alpha=0.7)

        self.chart1.fig.tight_layout()
        self.chart1.draw()

        # Gráfico 2: Distribución por severidad
        self.chart2.fig.clear()
        ax2 = self.chart2.fig.add_subplot(111)

        severities = ['Alto', 'Moderado', 'Bajo']
        sev_values = [15, 65, 40]
        sev_colors = ['#f44336', '#ff9800', '#4caf50']

        ax2.pie(sev_values, labels=severities, colors=sev_colors, autopct='%1.1f%%',
                startangle=90, shadow=False)
        ax2.axis('equal')

        self.chart2.fig.tight_layout()
        self.chart2.draw()

        # Gráfico 3: Tendencia temporal
        self.chart3.fig.clear()
        ax3 = self.chart3.fig.add_subplot(111)

        days = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']
        trends = [10, 8, 15, 12, 20, 7, 5]

        ax3.plot(days, trends, marker='o', linestyle='-', color='#3f51b5', linewidth=2)
        ax3.set_xlabel('Día de la semana')
        ax3.set_ylabel('Alertas detectadas')
        ax3.grid(linestyle='--', alpha=0.7)

        self.chart3.fig.tight_layout()
        self.chart3.draw()

        # Gráfico 4: Rendimiento de algoritmos
        self.chart4.fig.clear()
        ax4 = self.chart4.fig.add_subplot(111)

        algorithms = ['KMP', 'Boyer-Moore']
        times = [15, 8]

        ax4.barh(algorithms, times, color=['#cddc39', '#00bcd4'], alpha=0.7)
        ax4.set_xlabel('Tiempo promedio (ms)')
        ax4.grid(axis='x', linestyle='--', alpha=0.7)

        self.chart4.fig.tight_layout()
        self.chart4.draw()