# boyer_moore.py
def bad_character_heuristic(pattern):
    """Preprocesamiento para la regla del mal carácter"""
    m = len(pattern)
    # Valor por defecto: -1 (el carácter no está en el patrón)
    bad_char = {c: -1 for c in set(pattern)}

    # Actualizar con la última ocurrencia de cada carácter
    for i in range(m):
        bad_char[pattern[i]] = i

    return bad_char


def boyer_moore_search(text, pattern):
    """Algoritmo Boyer-Moore simplificado"""
    n = len(text)
    m = len(pattern)

    if m == 0:
        return []

    # Preprocesamiento
    bad_char = bad_character_heuristic(pattern)

    results = []
    s = 0  # s es el desplazamiento del patrón con respecto al texto

    while s <= n - m:
        j = m - 1  # Empezamos desde el final del patrón

        # Coincidencia de caracteres de derecha a izquierda
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1

        # Si el patrón se encontró completamente
        if j < 0:
            results.append(s)
            # Movemos el patrón para buscar la siguiente ocurrencia
            s += 1
        else:
            # Aplicamos la regla del mal carácter
            char_in_text = text[s + j]
            if char_in_text in bad_char:
                skip = max(1, j - bad_char[char_in_text])
            else:
                skip = max(1, j + 1)
            s += skip

    return results