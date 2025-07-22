from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QComboBox, QTextEdit, QGroupBox, QSplitter, QRadioButton,
                             QButtonGroup, QSlider)
from PyQt5.QtCore import Qt, QTimer
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.patches as patches
import matplotlib.animation as animation
import numpy as np


class MatplotlibCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        super(MatplotlibCanvas, self).__init__(self.fig)


class AnimacionWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.animation = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_animation)
        self.current_frame = 0
        self.max_frames = 20
        self.animation_speed = 1000  # ms

    def init_ui(self):
        # Layout principal
        main_layout = QVBoxLayout()

        # Título
        title_label = QLabel("Visualización de Algoritmos")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        main_layout.addWidget(title_label)

        # Controles superiores
        top_controls = QHBoxLayout()

        # Selección de algoritmo
        self.algorithm_group = QButtonGroup(self)

        algorithm_box = QGroupBox("Algoritmo")
        algorithm_layout = QHBoxLayout()

        self.kmp_radio = QRadioButton("KMP")
        self.boyer_moore_radio = QRadioButton("Boyer-Moore")
        self.greedy_radio = QRadioButton("Algoritmo Voraz")

        self.algorithm_group.addButton(self.kmp_radio, 1)
        self.algorithm_group.addButton(self.boyer_moore_radio, 2)
        self.algorithm_group.addButton(self.greedy_radio, 3)

        self.kmp_radio.setChecked(True)

        algorithm_layout.addWidget(self.kmp_radio)
        algorithm_layout.addWidget(self.boyer_moore_radio)
        algorithm_layout.addWidget(self.greedy_radio)

        algorithm_box.setLayout(algorithm_layout)

        # Controles de animación
        animation_box = QGroupBox("Control de Animación")
        animation_layout = QHBoxLayout()

        self.play_button = QPushButton("▶ Reproducir")
        self.play_button.clicked.connect(self.toggle_animation)

        self.reset_button = QPushButton("⟲ Reiniciar")
        self.reset_button.clicked.connect(self.reset_animation)

        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setMinimum(1)
        self.speed_slider.setMaximum(10)
        self.speed_slider.setValue(5)
        self.speed_slider.setTickPosition(QSlider.TicksBelow)
        self.speed_slider.setTickInterval(1)
        self.speed_slider.valueChanged.connect(self.change_speed)

        animation_layout.addWidget(self.play_button)
        animation_layout.addWidget(self.reset_button)
        animation_layout.addWidget(QLabel("Velocidad:"))
        animation_layout.addWidget(self.speed_slider)

        animation_box.setLayout(animation_layout)

        top_controls.addWidget(algorithm_box)
        top_controls.addWidget(animation_box)

        main_layout.addLayout(top_controls)

        # Área de entrada de texto
        input_layout = QHBoxLayout()

        # Texto
        text_group = QGroupBox("Texto a analizar")
        text_layout = QVBoxLayout()

        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText("Ingrese texto para analizar...")
        self.text_input.setText("Eres un perdedor, nadie te quiere aquí en el grupo.")

        text_layout.addWidget(self.text_input)
        text_group.setLayout(text_layout)

        # Patrón
        pattern_group = QGroupBox("Patrón a buscar")
        pattern_layout = QVBoxLayout()

        self.pattern_input = QTextEdit()
        self.pattern_input.setPlaceholderText("Ingrese patrón a buscar...")
        self.pattern_input.setText("nadie te quiere")
        self.pattern_input.setMaximumHeight(80)

        pattern_layout.addWidget(self.pattern_input)
        pattern_group.setLayout(pattern_layout)

        input_layout.addWidget(text_group, 2)
        input_layout.addWidget(pattern_group, 1)

        main_layout.addLayout(input_layout)

        # Botón de iniciar
        self.start_button = QPushButton("Iniciar Visualización")
        self.start_button.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 10px;")
        self.start_button.clicked.connect(self.iniciar_visualizacion)

        main_layout.addWidget(self.start_button)

        # Área de visualización
        self.canvas = MatplotlibCanvas(self, width=10, height=6, dpi=100)
        main_layout.addWidget(self.canvas)

        # Explicación
        self.explanation_text = QTextEdit()
        self.explanation_text.setReadOnly(True)
        self.explanation_text.setMaximumHeight(100)

        main_layout.addWidget(self.explanation_text)

        self.setLayout(main_layout)

        # Inicializar con explicación del KMP
        self.cambiar_algoritmo()
        self.algorithm_group.buttonClicked.connect(self.cambiar_algoritmo)

    def cambiar_algoritmo(self):
        """Cambia la explicación según el algoritmo seleccionado"""
        if self.kmp_radio.isChecked():
            self.explanation_text.setHtml("""
                <h3>Algoritmo Knuth-Morris-Pratt (KMP)</h3>
                <p>El algoritmo KMP es un algoritmo de búsqueda de patrones que utiliza la información de coincidencias parciales para evitar retrocesos innecesarios.</p>
                <p>Ventajas: Garantiza un tiempo de ejecución lineal O(n+m) y es eficiente para patrones con caracteres repetidos.</p>
            """)
        elif self.boyer_moore_radio.isChecked():
            self.explanation_text.setHtml("""
                <h3>Algoritmo Boyer-Moore</h3>
                <p>Boyer-Moore es uno de los algoritmos más eficientes para búsqueda de patrones, especialmente para alfabetos grandes.</p>
                <p>Ventajas: Compara de derecha a izquierda y puede saltar múltiples posiciones, logrando en el mejor caso complejidad sublineal O(n/m).</p>
            """)
        else:  # Algoritmo Voraz
            self.explanation_text.setHtml("""
                <h3>Algoritmo Voraz (Greedy) para Priorización</h3>
                <p>El algoritmo voraz de la mochila fraccionaria se utiliza para priorizar alertas según su importancia y el tiempo disponible.</p>
                <p>Ventajas: Garantiza la solución óptima para el problema de la mochila fraccionaria, maximizando el valor total obtenido.</p>
            """)

    def iniciar_visualizacion(self):
        """Inicia la visualización del algoritmo seleccionado"""
        # Detener animación anterior si existe
        self.stop_animation()

        # Limpiar canvas
        self.canvas.fig.clear()

        # Obtener texto y patrón
        text = self.text_input.toPlainText()
        pattern = self.pattern_input.toPlainText()

        if not text or not pattern:
            return

        # Configurar visualización según algoritmo
        if self.kmp_radio.isChecked():
            self.setup_kmp_visualization(text, pattern)
        elif self.boyer_moore_radio.isChecked():
            self.setup_boyer_moore_visualization(text, pattern)
        else:  # Algoritmo Voraz
            self.setup_greedy_visualization()

        # Reiniciar animación
        self.reset_animation()
        self.canvas.draw()

    def setup_kmp_visualization(self, text, pattern):
        """Configura la visualización del algoritmo KMP"""
        # Configuración
        self.canvas.fig.patch.set_facecolor('#f5f5f5')

        # Crear layout con GridSpec
        gs = plt.GridSpec(5, 1, height_ratios=[1, 1, 0.7, 0.7, 2], hspace=0.4, figure=self.canvas.fig)

        # Crear los ejes
        self.axes = []
        for i in range(5):
            ax = self.canvas.fig.add_subplot(gs[i])
            ax.set_facecolor('#f5f5f5')
            ax.axis('off')
            self.axes.append(ax)

        # Título
        self.canvas.fig.suptitle('Visualización del Algoritmo KMP', fontsize=14, weight='bold')

        # Preprocesamiento: computar la tabla LPS
        def compute_lps(pattern):
            m = len(pattern)
            lps = [0] * m

            length = 0
            i = 1

            while i < m:
                if pattern[i] == pattern[length]:
                    length += 1
                    lps[i] = length
                    i += 1
                else:
                    if length != 0:
                        length = lps[length - 1]
                    else:
                        lps[i] = 0
                        i += 1

            return lps

        self.lps = compute_lps(pattern)
        self.text = text
        self.pattern = pattern

        # Generar pasos de ejecución del algoritmo KMP
        self.steps = []

        # Simulación del algoritmo KMP
        i = 0  # índice para text
        j = 0  # índice para pattern

        while i < len(text):
            self.steps.append({
                'text_pos': i,
                'pattern_pos': j,
                'status': f'Comparando texto[{i}]="{text[i]}" con patrón[{j}]="{pattern[j] if j < len(pattern) else ""}"',
                'match': i < len(text) and j < len(pattern) and text[i] == pattern[j],
                'skip': 0,
                'explanation': ''
            })

            # Coincidencia de caracteres
            if j < len(pattern) and i < len(text) and pattern[j] == text[i]:
                i += 1
                j += 1

                # Si encontramos el patrón completo
                if j == len(pattern):
                    self.steps[-1]['status'] = f'¡Patrón encontrado en posición {i - j}!'
                    self.steps[-1]['explanation'] = f'Se ha encontrado el patrón completo "{pattern}" en el texto.'
                    j = self.lps[j - 1]
            # Si hay una no coincidencia
            elif i < len(text):
                if j != 0:
                    self.steps[-1]['skip'] = j - self.lps[j - 1]
                    self.steps[-1]['explanation'] = f'No coincide. Usando tabla LPS, saltamos a j={self.lps[j - 1]}.'
                    j = self.lps[j - 1]
                else:
                    self.steps[-1]['explanation'] = 'No coincide. Avanzamos al siguiente carácter en el texto.'
                    i += 1

        # Limitar número de pasos para la animación
        self.max_frames = min(20, len(self.steps))

        # Dibujar primer frame
        self.update_kmp_frame(0)

    def update_kmp_frame(self, frame):
        """Actualiza la visualización del algoritmo KMP para el frame actual"""
        # Limpiar todos los ejes
        for ax in self.axes:
            ax.clear()
            ax.set_facecolor('#f5f5f5')
            ax.axis('off')

        # Obtener el paso actual
        if frame < len(self.steps):
            step = self.steps[frame]
        else:
            step = self.steps[-1]

        # Paso 1: Texto original
        self.axes[0].text(0.05, 0.7, 'Texto:', ha='left', va='center', fontsize=12, weight='bold')
        for i, char in enumerate(self.text):
            color = 'black'
            background = 'none'

            # Colorear caracteres según comparación actual
            if i == step['text_pos']:
                if step['match']:
                    color = '#4CAF50'  # Verde para coincidencia
                    background = '#E8F5E9'
                else:
                    color = '#F44336'  # Rojo para no coincidencia
                    background = '#FFEBEE'

            # Dibujar fondo si es necesario
            if background != 'none':
                rect = patches.Rectangle((0.05 + i * 0.02 - 0.01, 0.45), 0.02, 0.3,
                                         facecolor=background, alpha=0.7)
                self.axes[0].add_patch(rect)

            # Dibujar carácter
            self.axes[0].text(0.05 + i * 0.02, 0.6, char, ha='center', va='center', fontsize=10, color=color)

        # Paso 2: Patrón
        self.axes[1].text(0.05, 0.7, 'Patrón:', ha='left', va='center', fontsize=12, weight='bold')
        for i, char in enumerate(self.pattern):
            color = 'black'
            background = 'none'

            # Colorear caracteres según comparación actual
            if i == step['pattern_pos']:
                if step['match']:
                    color = '#4CAF50'  # Verde para coincidencia
                    background = '#E8F5E9'
                else:
                    color = '#F44336'  # Rojo para no coincidencia
                    background = '#FFEBEE'

            # Dibujar fondo si es necesario
            if background != 'none':
                rect = patches.Rectangle((0.15 + i * 0.03 - 0.015, 0.45), 0.03, 0.3,
                                         facecolor=background, alpha=0.7)
                self.axes[1].add_patch(rect)

            # Dibujar carácter
            self.axes[1].text(0.15 + i * 0.03, 0.6, char, ha='center', va='center', fontsize=10, color=color)

        # Paso 3: Tabla LPS
        self.axes[2].text(0.05, 0.7, 'Tabla LPS:', ha='left', va='center', fontsize=12, weight='bold')
        for i, val in enumerate(self.lps):
            self.axes[2].text(0.15 + i * 0.03, 0.6, str(val), ha='center', va='center', fontsize=10)

            # Resaltar valor actual si estamos usando la tabla
            if step['skip'] > 0 and i == step['pattern_pos'] - 1:
                rect = patches.Rectangle((0.15 + i * 0.03 - 0.015, 0.45), 0.03, 0.3,
                                         facecolor='#E3F2FD', alpha=0.7)
                self.axes[2].add_patch(rect)

        # Paso 4: Estado actual
        self.axes[3].text(0.05, 0.7, 'Estado:', ha='left', va='center', fontsize=12, weight='bold')
        self.axes[3].text(0.15, 0.7, step['status'], ha='left', va='center', fontsize=11)
        self.axes[3].text(0.05, 0.3, 'Explicación:', ha='left', va='center', fontsize=12, weight='bold')
        self.axes[3].text(0.15, 0.3, step['explanation'], ha='left', va='center', fontsize=11)

        # Paso 5: Visualización de la comparación
        self.axes[4].text(0.05, 0.9, 'Ejecución:', ha='left', va='center', fontsize=12, weight='bold')

        # Mostrar texto
        for i, char in enumerate(self.text):
            color = 'black'
            background = 'none'

            # Colorear caracteres según comparación actual
            if i < step['text_pos']:
                # Caracteres ya procesados
                color = '#9E9E9E'  # Gris
            elif i == step['text_pos']:
                if step['match']:
                    color = '#4CAF50'  # Verde para coincidencia
                    background = '#E8F5E9'
                else:
                    color = '#F44336'  # Rojo para no coincidencia
                    background = '#FFEBEE'

            # Dibujar fondo si es necesario
            if background != 'none':
                rect = patches.Rectangle((0.05 + i * 0.02 - 0.01, 0.75), 0.02, 0.1,
                                         facecolor=background, alpha=0.7)
                self.axes[4].add_patch(rect)

            # Dibujar carácter
            self.axes[4].text(0.05 + i * 0.02, 0.8, char, ha='center', va='center', fontsize=10, color=color)

        # Mostrar patrón alineado con la posición actual
        pattern_start = step['text_pos'] - step['pattern_pos']
        if pattern_start >= 0:
            for i, char in enumerate(self.pattern):
                if pattern_start + i < len(self.text):
                    color = 'black'
                    background = 'none'

                    # Colorear caracteres según comparación actual
                    if i < step['pattern_pos']:
                        # Caracteres ya comparados
                        if self.text[pattern_start + i] == self.pattern[i]:
                            color = '#4CAF50'  # Verde para coincidencias
                            background = '#E8F5E9'
                        else:
                            color = '#F44336'  # Rojo para no coincidencias
                            background = '#FFEBEE'
                    elif i == step['pattern_pos']:
                        # Carácter actual en comparación
                        if step['match']:
                            color = '#4CAF50'  # Verde para coincidencia
                            background = '#E8F5E9'
                        else:
                            color = '#F44336'  # Rojo para no coincidencia
                            background = '#FFEBEE'

                    # Dibujar fondo si es necesario
                    if background != 'none':
                        rect = patches.Rectangle((0.05 + (pattern_start + i) * 0.02 - 0.01, 0.55), 0.02, 0.1,
                                                 facecolor=background, alpha=0.7)
                        self.axes[4].add_patch(rect)

                    # Dibujar carácter
                    self.axes[4].text(0.05 + (pattern_start + i) * 0.02, 0.6, char, ha='center', va='center',
                                      fontsize=10, color=color)

        # Línea conectora
        self.axes[4].plot([0.05 + step['text_pos'] * 0.02, 0.05 + step['text_pos'] * 0.02],
                          [0.72, 0.68], 'k-', alpha=0.5)

        # Explicación del salto
        if step['skip'] > 0:
            self.axes[4].text(0.05, 0.4, f"Salto: {step['skip']} posición(es) en el patrón", ha='left', va='center',
                              fontsize=11, color='#2196F3')

            # Flecha de salto
            arrow = patches.FancyArrowPatch((0.05 + step['text_pos'] * 0.02, 0.45),
                                            (0.05 + step['text_pos'] * 0.02, 0.45),
                                            mutation_scale=15, facecolor='#2196F3', edgecolor='#2196F3')
            self.axes[4].add_patch(arrow)

        # Información del paso
        self.axes[4].text(0.05, 0.3, f"Paso {frame + 1} de {len(self.steps)}", ha='left', va='center',
                          fontsize=10, color='#9E9E9E')

    def setup_boyer_moore_visualization(self, text, pattern):
        """Configura la visualización del algoritmo Boyer-Moore"""
        # Configuración
        self.canvas.fig.patch.set_facecolor('#f5f5f5')

        # Crear layout con GridSpec
        gs = plt.GridSpec(5, 1, height_ratios=[1, 1, 0.7, 0.7, 2], hspace=0.4, figure=self.canvas.fig)

        # Crear los ejes
        self.axes = []
        for i in range(5):
            ax = self.canvas.fig.add_subplot(gs[i])
            ax.set_facecolor('#f5f5f5')
            ax.axis('off')
            self.axes.append(ax)

        # Título
        self.canvas.fig.suptitle('Visualización del Algoritmo Boyer-Moore', fontsize=14, weight='bold')

        # Preprocesamiento para Boyer-Moore
        def bad_character_heuristic(pattern):
            m = len(pattern)
            # Valor por defecto: -1 (el carácter no está en el patrón)
            bad_char = {c: -1 for c in set(pattern)}

            # Actualizar con la última ocurrencia de cada carácter
            for i in range(m):
                bad_char[pattern[i]] = i

            return bad_char

        self.bad_char = bad_character_heuristic(pattern)
        self.text = text
        self.pattern = pattern

        # Generar pasos de ejecución del algoritmo Boyer-Moore
        self.steps = []

        # Simulación del algoritmo Boyer-Moore
        s = 0  # s es el desplazamiento del patrón con respecto al texto

        while s <= len(text) - len(pattern):
            j = len(pattern) - 1  # Empezamos desde el final del patrón

            self.steps.append({
                'text_pos': s,
                'pattern_pos': j,
                'status': f'Comparando texto[{s + j}]="{text[s + j]}" con patrón[{j}]="{pattern[j]}"',
                'match': False,
                'skip': 0,
                'explanation': 'Comenzando comparación desde el final del patrón'
            })

            # Coincidencia de caracteres de derecha a izquierda
            while j >= 0 and pattern[j] == text[s + j]:
                self.steps.append({
                    'text_pos': s,
                    'pattern_pos': j,
                    'status': f'Coincidencia: texto[{s + j}]="{text[s + j]}" con patrón[{j}]="{pattern[j]}"',
                    'match': True,
                    'skip': 0,
                    'explanation': 'Caracteres coinciden. Continuamos comparando hacia la izquierda.'
                })
                j -= 1

            # Si el patrón se encontró completamente
            if j < 0:
                self.steps.append({
                    'text_pos': s,
                    'pattern_pos': 0,
                    'status': f'¡Patrón encontrado en posición {s}!',
                    'match': True,
                    'skip': 1,
                    'explanation': f'Se ha encontrado el patrón completo "{pattern}" en el texto.'
                })
                s += 1
            else:
                # Aplicamos la regla del mal carácter
                char_in_text = text[s + j]
                if char_in_text in self.bad_char:
                    skip = max(1, j - self.bad_char[char_in_text])
                else:
                    skip = max(1, j + 1)

                self.steps.append({
                    'text_pos': s,
                    'pattern_pos': j,
                    'status': f'No coincide: texto[{s + j}]="{text[s + j]}" con patrón[{j}]="{pattern[j]}"',
                    'match': False,
                    'skip': skip,
                    'explanation': f'Usando regla del mal carácter, saltamos {skip} posición(es).'
                })

                s += skip

        # Limitar número de pasos para la animación
        self.max_frames = min(20, len(self.steps))

        # Dibujar primer frame
        self.update_boyer_moore_frame(0)

    def update_boyer_moore_frame(self, frame):
        """Actualiza la visualización del algoritmo Boyer-Moore para el frame actual"""
        # Limpiar todos los ejes
        for ax in self.axes:
            ax.clear()
            ax.set_facecolor('#f5f5f5')
            ax.axis('off')

        # Obtener el paso actual
        if frame < len(self.steps):
            step = self.steps[frame]
        else:
            step = self.steps[-1]

        # Paso 1: Texto original
        self.axes[0].text(0.05, 0.7, 'Texto:', ha='left', va='center', fontsize=12, weight='bold')
        for i, char in enumerate(self.text):
            color = 'black'
            background = 'none'

            # Colorear caracteres según comparación actual
            if i == step['text_pos'] + step['pattern_pos']:
                if step['match']:
                    color = '#4CAF50'  # Verde para coincidencia
                    background = '#E8F5E9'
                else:
                    color = '#F44336'  # Rojo para no coincidencia
                    background = '#FFEBEE'

            # Dibujar fondo si es necesario
            if background != 'none':
                rect = patches.Rectangle((0.05 + i * 0.02 - 0.01, 0.45), 0.02, 0.3,
                                         facecolor=background, alpha=0.7)
                self.axes[0].add_patch(rect)

            # Dibujar carácter
            self.axes[0].text(0.05 + i * 0.02, 0.6, char, ha='center', va='center', fontsize=10, color=color)

        # Paso 2: Patrón
        self.axes[1].text(0.05, 0.7, 'Patrón:', ha='left', va='center', fontsize=12, weight='bold')
        for i, char in enumerate(self.pattern):
            color = 'black'
            background = 'none'

            # Colorear caracteres según comparación actual
            if i == step['pattern_pos']:
                if step['match']:
                    color = '#4CAF50'  # Verde para coincidencia
                    background = '#E8F5E9'
                else:
                    color = '#F44336'  # Rojo para no coincidencia
                    background = '#FFEBEE'

            # Dibujar fondo si es necesario
            if background != 'none':
                rect = patches.Rectangle((0.15 + i * 0.03 - 0.015, 0.45), 0.03, 0.3,
                                         facecolor=background, alpha=0.7)
                self.axes[1].add_patch(rect)

            # Dibujar carácter
            self.axes[1].text(0.15 + i * 0.03, 0.6, char, ha='center', va='center', fontsize=10, color=color)

        # Paso 3: Tabla de mal carácter
        self.axes[2].text(0.05, 0.7, 'Tabla de mal carácter:', ha='left', va='center', fontsize=12, weight='bold')
        bad_char_str = ", ".join([f"'{c}': {self.bad_char[c]}" for c in sorted(self.bad_char.keys())])
        self.axes[2].text(0.28, 0.6, bad_char_str, ha='left', va='center', fontsize=10)

        # Paso 4: Estado actual
        self.axes[3].text(0.05, 0.7, 'Estado:', ha='left', va='center', fontsize=12, weight='bold')
        self.axes[3].text(0.15, 0.7, step['status'], ha='left', va='center', fontsize=11)
        self.axes[3].text(0.05, 0.3, 'Explicación:', ha='left', va='center', fontsize=12, weight='bold')
        self.axes[3].text(0.15, 0.3, step['explanation'], ha='left', va='center', fontsize=11)

        # Paso 5: Visualización de la comparación
        self.axes[4].text(0.05, 0.9, 'Ejecución:', ha='left', va='center', fontsize=12, weight='bold')

        # Mostrar texto
        for i, char in enumerate(self.text):
            color = 'black'
            background = 'none'

            # Colorear caracteres según comparación actual
            if i < step['text_pos']:
                # Caracteres ya procesados
                color = '#9E9E9E'  # Gris
            elif i == step['text_pos'] + step['pattern_pos']:
                if step['match']:
                    color = '#4CAF50'  # Verde para coincidencia
                    background = '#E8F5E9'
                else:
                    color = '#F44336'  # Rojo para no coincidencia
                    background = '#FFEBEE'

            # Dibujar fondo si es necesario
            if background != 'none':
                rect = patches.Rectangle((0.05 + i * 0.02 - 0.01, 0.75), 0.02, 0.1,
                                         facecolor=background, alpha=0.7)
                self.axes[4].add_patch(rect)

            # Dibujar carácter
            self.axes[4].text(0.05 + i * 0.02, 0.8, char, ha='center', va='center', fontsize=10, color=color)

        # Mostrar patrón alineado con la posición actual
        for i, char in enumerate(self.pattern):
            if step['text_pos'] + i < len(self.text):
                color = 'black'
                background = 'none'

                # Colorear caracteres según comparación actual
                if i > step['pattern_pos']:
                    # Caracteres aún no comparados
                    color = '#9E9E9E'  # Gris
                elif i == step['pattern_pos']:
                    # Carácter actual en comparación
                    if step['match']:
                        color = '#4CAF50'  # Verde para coincidencia
                        background = '#E8F5E9'
                    else:
                        color = '#F44336'  # Rojo para no coincidencia
                        background = '#FFEBEE'
                else:
                    # Caracteres ya comparados (desde el final)
                    if self.text[step['text_pos'] + i] == self.pattern[i]:
                        color = '#4CAF50'  # Verde para coincidencias
                        background = '#E8F5E9'
                    else:
                        color = '#F44336'  # Rojo para no coincidencias
                        background = '#FFEBEE'

                # Dibujar fondo si es necesario
                if background != 'none':
                    rect = patches.Rectangle((0.05 + (step['text_pos'] + i) * 0.02 - 0.01, 0.55), 0.02, 0.1,
                                             facecolor=background, alpha=0.7)
                    self.axes[4].add_patch(rect)

                # Dibujar carácter
                self.axes[4].text(0.05 + (step['text_pos'] + i) * 0.02, 0.6, char, ha='center', va='center',
                                  fontsize=10, color=color)

        # Línea conectora
        self.axes[4].plot([0.05 + (step['text_pos'] + step['pattern_pos']) * 0.02,
                           0.05 + (step['text_pos'] + step['pattern_pos']) * 0.02],
                          [0.72, 0.68], 'k-', alpha=0.5)

        # Flecha de dirección de comparación (de derecha a izquierda)
        if step['pattern_pos'] < len(self.pattern) - 1:
            self.axes[4].arrow(0.05 + (step['text_pos'] + step['pattern_pos']) * 0.02 + 0.03, 0.6,
                               -0.03, 0, head_width=0.02, head_length=0.01,
                               fc='#2196F3', ec='#2196F3', alpha=0.7)

        # Explicación del salto
        if step['skip'] > 0:
            self.axes[4].text(0.05, 0.4, f"Salto: {step['skip']} posición(es)", ha='left', va='center',
                              fontsize=11, color='#2196F3')

            # Flecha de salto
            arrow = patches.FancyArrowPatch((0.05 + step['text_pos'] * 0.02, 0.45),
                                            (0.05 + (step['text_pos'] + step['skip']) * 0.02, 0.45),
                                            mutation_scale=15, facecolor='#2196F3', edgecolor='#2196F3')
            self.axes[4].add_patch(arrow)

        # Información del paso
        self.axes[4].text(0.05, 0.3, f"Paso {frame + 1} de {len(self.steps)}", ha='left', va='center',
                          fontsize=10, color='#9E9E9E')

    def setup_greedy_visualization(self):
        """Configura la visualización del algoritmo voraz"""
        # Configuración
        self.canvas.fig.patch.set_facecolor('#f5f5f5')

        # Crear layout con GridSpec
        gs = plt.GridSpec(4, 1, height_ratios=[1, 1, 0.7, 2], hspace=0.4, figure=self.canvas.fig)

        # Crear los ejes
        self.axes = []
        for i in range(4):
            ax = self.canvas.fig.add_subplot(gs[i])
            ax.set_facecolor('#f5f5f5')
            ax.axis('off')
            self.axes.append(ax)

        # Título
        self.canvas.fig.suptitle('Visualización del Algoritmo Voraz para Priorización', fontsize=14, weight='bold')

        # Datos de alertas
        self.alerts = [
            (3, 1.7, "Te voy a encontrar y te arrepentirás", "Amenaza", "Alto"),
            (2, 1.5, "Eres un perdedor, nadie te quiere", "Insulto", "Moderado"),
            (2, 2.0, "No te incluimos porque nadie te soporta", "Exclusión", "Moderado"),
            (1, 0.8, "Eres tonto como tu hermano", "Insulto", "Bajo")
        ]

        # Capacidad máxima
        self.max_capacity = 3.0

        # Ordenar alertas por ratio valor/peso
        self.sorted_alerts = sorted(self.alerts, key=lambda x: x[0] / x[1], reverse=True)

        # Generar pasos de ejecución del algoritmo voraz
        self.steps = []

        # Paso 1: Mostrar alertas originales
        self.steps.append({
            'step': 1,
            'status': 'Alertas detectadas',
            'explanation': 'Estas son las alertas detectadas en el texto, con su valor (importancia) y peso (tiempo de procesamiento).',
            'current_capacity': 0,
            'current_value': 0,
            'selected_alerts': []
        })

        # Paso 2: Ordenar por ratio valor/peso
        self.steps.append({
            'step': 2,
            'status': 'Ordenando alertas por ratio valor/peso',
            'explanation': 'Ordenamos las alertas por su ratio valor/peso de forma descendente para maximizar el valor obtenido.',
            'current_capacity': 0,
            'current_value': 0,
            'selected_alerts': []
        })

        # Pasos 3+: Seleccionar alertas
        current_capacity = 0
        current_value = 0
        selected_alerts = []

        for i, (value, weight, pattern, tipo, nivel) in enumerate(self.sorted_alerts):
            if current_capacity + weight <= self.max_capacity:
                # Seleccionamos la alerta completa
                fraction = 1.0
                current_capacity += weight
                current_value += value
                selected_alerts.append((value, weight, pattern, tipo, nivel, fraction))

                self.steps.append({
                    'step': 3 + i,
                    'status': f'Seleccionando alerta {i + 1}',
                    'explanation': f'La alerta cabe completa. Añadimos "{pattern[:15]}..." (100%).',
                    'current_capacity': current_capacity,
                    'current_value': current_value,
                    'selected_alerts': selected_alerts.copy()
                })
            else:
                # Tomamos una fracción de la alerta
                remaining = self.max_capacity - current_capacity
                if remaining > 0:
                    fraction = remaining / weight
                    current_capacity = self.max_capacity
                    current_value += value * fraction
                    selected_alerts.append((value, weight, pattern, tipo, nivel, fraction))

                    self.steps.append({
                        'step': 3 + i,
                        'status': f'Seleccionando alerta {i + 1} (fracción)',
                        'explanation': f'La alerta no cabe completa. Añadimos "{pattern[:15]}..." ({fraction * 100:.0f}%).',
                        'current_capacity': current_capacity,
                        'current_value': current_value,
                        'selected_alerts': selected_alerts.copy()
                    })
                break

        # Paso final: Resultado
        self.steps.append({
            'step': len(self.steps) + 1,
            'status': 'Resultado final',
            'explanation': f'Hemos maximizado el valor total ({current_value:.2f}) dentro de la capacidad disponible ({self.max_capacity}).',
            'current_capacity': current_capacity,
            'current_value': current_value,
            'selected_alerts': selected_alerts
        })

        # Limitar número de pasos para la animación
        self.max_frames = len(self.steps)

        # Dibujar primer frame
        self.update_greedy_frame(0)

    def update_greedy_frame(self, frame):
        """Actualiza la visualización del algoritmo voraz para el frame actual"""
        # Limpiar todos los ejes
        for ax in self.axes:
            ax.clear()
            ax.set_facecolor('#f5f5f5')
            ax.axis('off')

        # Obtener el paso actual
        if frame < len(self.steps):
            step = self.steps[frame]
        else:
            step = self.steps[-1]

        # Paso 1: Alertas detectadas
        self.axes[0].text(0.05, 0.7, 'Alertas detectadas:', ha='left', va='center', fontsize=12, weight='bold')

        # Mostrar tabla de alertas
        headers = ["Valor", "Peso", "Patrón", "Tipo", "Severidad"]
        for i, header in enumerate(headers):
            self.axes[0].text(0.05 + i * 0.18, 0.5, header, ha='left', va='center', fontsize=10, fontweight='bold')

        for j, (value, weight, pattern, tipo, nivel) in enumerate(self.alerts):
            row_data = [str(value), str(weight), pattern[:15] + "...", tipo, nivel]
            for i, data in enumerate(row_data):
                color = 'black'
                if nivel == "Alto":
                    color = '#F44336'  # Rojo para alto
                elif nivel == "Moderado":
                    color = '#FF9800'  # Naranja para moderado
                elif nivel == "Bajo":
                    color = '#4CAF50'  # Verde para bajo

                self.axes[0].text(0.05 + i * 0.18, 0.4 - j * 0.1, data, ha='left', va='center', fontsize=9, color=color)

        # Paso 2: Alertas ordenadas por ratio valor/peso
        self.axes[1].text(0.05, 0.7, 'Alertas ordenadas por ratio valor/peso (descendente):',
                          ha='left', va='center', fontsize=12, weight='bold')

        # Mostrar tabla de alertas ordenadas
        headers = ["Valor", "Peso", "Patrón", "Tipo", "Severidad", "Ratio V/P"]
        for i, header in enumerate(headers):
            self.axes[1].text(0.05 + i * 0.15, 0.5, header, ha='left', va='center', fontsize=10, fontweight='bold')

        for j, (value, weight, pattern, tipo, nivel) in enumerate(self.sorted_alerts):
            ratio = value / weight
            row_data = [str(value), str(weight), pattern[:12] + "...", tipo, nivel, f"{ratio:.2f}"]
            for i, data in enumerate(row_data):
                color = 'black'
                if i == 5:  # Columna de ratio
                    color = '#2196F3'  # Azul para ratio

                self.axes[1].text(0.05 + i * 0.15, 0.4 - j * 0.1, data, ha='left', va='center', fontsize=9, color=color)

        # Paso 3: Estado actual
        self.axes[2].text(0.05, 0.5, f'Estado: {step["status"]} (paso {step["step"]} de {len(self.steps)})',
                          ha='left', va='center', fontsize=12, weight='bold')

        # Paso 4: Visualización de la mochila
        self.axes[3].text(0.05, 0.9, step['explanation'], ha='left', va='top', fontsize=10, wrap=True)

        # Dibujar mochila
        self.axes[3].add_patch(patches.Rectangle((0.1, 0.2), 0.8, 0.3, linewidth=2,
                                                 edgecolor='#3F51B5', facecolor='none', alpha=0.8))
        self.axes[3].text(0.5, 0.15, f'Capacidad: {self.max_capacity}', ha='center', va='center', fontsize=10)

        # Llenar la mochila con las alertas seleccionadas
        current_x = 0.1
        for value, weight, pattern, tipo, nivel, fraction in step['selected_alerts']:
            width = (weight * fraction / self.max_capacity) * 0.8

            # Color según nivel
            color = '#F44336' if nivel == "Alto" else '#FF9800' if nivel == "Moderado" else '#4CAF50'

            # Dibujar bloque en la mochila
            self.axes[3].add_patch(patches.Rectangle((current_x, 0.2), width, 0.3, linewidth=1,
                                                     edgecolor='white', facecolor=color, alpha=0.7))

            # Texto en el bloque
            if width > 0.1:
                self.axes[3].text(current_x + width / 2, 0.35, f"{pattern[:5]}...\n{fraction * 100:.0f}%",
                                  ha='center', va='center', fontsize=9, color='white')

            current_x += width

        # Información de capacidad utilizada
        self.axes[3].text(0.1, 0.1, f"Capacidad utilizada: {step['current_capacity']:.1f}/{self.max_capacity}",
                          ha='left', va='center', fontsize=10, color='#3F51B5')
        self.axes[3].text(0.5, 0.1, f"Valor total: {step['current_value']:.2f}",
                          ha='left', va='center', fontsize=10, fontweight='bold', color='#3F51B5')

    def toggle_animation(self):
        """Inicia o pausa la animación"""
        if self.timer.isActive():
            self.stop_animation()
            self.play_button.setText("▶ Reproducir")
        else:
            self.start_animation()
            self.play_button.setText("⏸ Pausar")

    def start_animation(self):
        """Inicia la animación"""
        self.timer.start(self.animation_speed)

    def stop_animation(self):
        """Detiene la animación"""
        self.timer.stop()

    def reset_animation(self):
        """Reinicia la animación"""
        self.current_frame = 0
        self.update_animation()

    def change_speed(self, value):
        """Cambia la velocidad de la animación"""
        self.animation_speed = 2000 // value  # Invertir la escala (1=lento, 10=rápido)
        if self.timer.isActive():
            self.timer.stop()
            self.timer.start(self.animation_speed)

    def update_animation(self):
        """Actualiza el frame de la animación"""
        if self.kmp_radio.isChecked():
            self.update_kmp_frame(self.current_frame)
        elif self.boyer_moore_radio.isChecked():
            self.update_boyer_moore_frame(self.current_frame)
        else:  # Algoritmo Voraz
            self.update_greedy_frame(self.current_frame)

        self.canvas.draw()

        # Avanzar al siguiente frame
        self.current_frame += 1
        if self.current_frame >= self.max_frames:
            self.current_frame = 0