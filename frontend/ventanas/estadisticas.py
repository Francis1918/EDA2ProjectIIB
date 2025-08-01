from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QComboBox, QGroupBox, QSplitter)
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
from collections import defaultdict
from datetime import datetime, timedelta


class MatplotlibCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        super(MatplotlibCanvas, self).__init__(self.fig)



class EstadisticasWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.historial_resultados = []
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

    def agregar_resultados(self, resultados):
        """Agrega nuevos resultados al historial con timestamp"""
        timestamp = datetime.now()
        self.historial_resultados.append((timestamp, resultados))
        self.actualizar_estadisticas()

    def filtrar_resultados_por_periodo(self):
        """Filtra resultados según el período seleccionado"""
        periodo = self.period_combo.currentText()
        ahora = datetime.now()
        
        if periodo == "Última semana":
            fecha_inicio = ahora - timedelta(days=7)
        elif periodo == "Último mes":
            fecha_inicio = ahora - timedelta(days=30)
        elif periodo == "Último trimestre":
            fecha_inicio = ahora - timedelta(days=90)
        else:  # Último año
            fecha_inicio = ahora - timedelta(days=365)

        return [(t, r) for t, r in self.historial_resultados if t >= fecha_inicio]

    def actualizar_estadisticas(self):
        """Actualiza los gráficos con datos reales"""
        resultados_filtrados = self.filtrar_resultados_por_periodo()
        
        # Contadores para las estadísticas
        tipos_count = defaultdict(int)
        severidad_count = defaultdict(int)
        dias_count = defaultdict(int)
        algoritmos_tiempo = defaultdict(list)

        # Procesar resultados
        for _, resultados in resultados_filtrados:
            for resultado in resultados:
                # Conteo por tipo
                tipos_count[resultado['tipo']] += 1
                
                # Conteo por severidad
                severidad_count[resultado['nivel']] += 1
                
                # Conteo por día
                dia = _.strftime('%a')
                dias_count[dia] += 1
                
                # Tiempo por algoritmo
                if 'tiempo_ejecucion' in resultado:
                    algoritmos_tiempo[resultado['algoritmo']].append(resultado['tiempo_ejecucion'])
                else:
                    algoritmos_tiempo[resultado['algoritmo']].append(1)

        # Gráfico 1: Distribución por tipo
        self.chart1.fig.clear()
        ax1 = self.chart1.fig.add_subplot(111)

        categories = list(tipos_count.keys()) if tipos_count else ['Sin datos']
        values = list(tipos_count.values()) if tipos_count else [0]
        colors = ['#ff9800', '#f44336', '#2196f3', '#9c27b0'][:len(categories)]

        ax1.bar(categories, values, color=colors, alpha=0.7)
        ax1.set_ylabel('Número de alertas')
        ax1.tick_params(axis='x', rotation=45)
        ax1.grid(axis='y', linestyle='--', alpha=0.7)

        self.chart1.fig.tight_layout()
        self.chart1.draw()

        # Gráfico 2: Distribución por severidad
        self.chart2.fig.clear()
        ax2 = self.chart2.fig.add_subplot(111)

        severities = list(severidad_count.keys()) if severidad_count else ['Sin datos']
        sev_values = list(severidad_count.values()) if severidad_count else [1]
        sev_colors = {'Alto': '#f44336', 'Moderado': '#ff9800', 'Bajo': '#4caf50'}
        colors = [sev_colors.get(sev, '#808080') for sev in severities]

        if sum(sev_values) > 0:
            ax2.pie(sev_values, labels=severities, colors=colors, autopct='%1.1f%%',
                    startangle=90, shadow=False)
        else:
            ax2.text(0.5, 0.5, 'Sin datos', horizontalalignment='center', verticalalignment='center')
        ax2.axis('equal')

        self.chart2.fig.tight_layout()
        self.chart2.draw()

        # Gráfico 3: Tendencia temporal
        self.chart3.fig.clear()
        ax3 = self.chart3.fig.add_subplot(111)

        dias_semana = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']
        trends = [dias_count.get(dia, 0) for dia in dias_semana]

        ax3.plot(dias_semana, trends, marker='o', linestyle='-', color='#3f51b5', linewidth=2)
        ax3.set_xlabel('Día de la semana')
        ax3.set_ylabel('Alertas detectadas')
        ax3.grid(linestyle='--', alpha=0.7)

        self.chart3.fig.tight_layout()
        self.chart3.draw()

        # Gráfico 4: Rendimiento de algoritmos
        self.chart4.fig.clear()
        ax4 = self.chart4.fig.add_subplot(111)

        algorithms = list(algoritmos_tiempo.keys())
        times = [np.mean(tiempos) for tiempos in algoritmos_tiempo.values()] if algoritmos_tiempo else []

        if algorithms:
            ax4.barh(algorithms, times, color=['#cddc39', '#00bcd4'], alpha=0.7)
            ax4.set_xlabel('Tiempo promedio (ms)')
        else:
            ax4.text(0.5, 0.5, 'Sin datos', horizontalalignment='center', verticalalignment='center')
        ax4.grid(axis='x', linestyle='--', alpha=0.7)

        self.chart4.fig.tight_layout()
        self.chart4.draw()