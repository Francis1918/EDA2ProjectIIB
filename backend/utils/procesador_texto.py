from backend.algoritmos.kmp import kmp_search
from backend.algoritmos.boyer_moore import boyer_moore_search
import re


def select_search_algorithm(text, pattern):
    """Selecciona automáticamente entre KMP y Boyer-Moore basado en características del texto y patrón"""
    text_complexity = len(set(text)) / len(text)  # Complejidad como proporción de caracteres únicos

    # Si el alfabeto es grande (texto variado) y el patrón no es muy corto, Boyer-Moore es más eficiente
    if text_complexity > 0.3 and len(pattern) > 3:
        return "boyer_moore", boyer_moore_search
    # En otros casos, KMP puede ser más adecuado
    else:
        return "kmp", kmp_search


def segment_text(text, max_segment_size=1000):
    """Segmenta el texto en partes más pequeñas para procesamiento eficiente"""
    # Dividir por párrafos
    paragraphs = text.split('\n')
    segments = []

    current_segment = ""
    for paragraph in paragraphs:
        if len(current_segment) + len(paragraph) <= max_segment_size:
            current_segment += paragraph + "\n"
        else:
            segments.append(current_segment)
            current_segment = paragraph + "\n"

    if current_segment:
        segments.append(current_segment)

    return segments


def detect_patterns(text, patterns):
    """
    Detecta patrones en el texto usando el algoritmo más apropiado

    Args:
        text: texto a analizar
        patterns: lista de tuplas (patron, tipo, nivel)

    Returns:
        Lista de coincidencias con información contextual
    """
    # Segmentar texto si es muy largo
    segments = segment_text(text) if len(text) > 1000 else [text]

    results = []

    for segment in segments:
        for pattern, tipo, nivel in patterns:
            # Seleccionar algoritmo
            algorithm_name, search_function = select_search_algorithm(segment, pattern)

            # Buscar patrón
            positions = search_function(segment, pattern)

            # Procesar resultados
            for pos in positions:
                # Extraer contexto (texto alrededor del patrón)
                start = max(0, pos - 20)
                end = min(len(segment), pos + len(pattern) + 20)
                context = segment[start:end]

                # Añadir a resultados
                results.append({
                    'patron': pattern,
                    'tipo': tipo,
                    'nivel': nivel,
                    'posicion': pos,
                    'contexto': context,
                    'algoritmo': algorithm_name
                })

    return results