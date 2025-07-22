# kmp.py
def compute_lps(pattern):
    """Computa la tabla de prefijos-sufijos (LPS) para KMP"""
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


def kmp_search(text, pattern):
    """Algoritmo KMP para búsqueda de patrones"""
    n = len(text)
    m = len(pattern)

    if m == 0:
        return []

    # Preprocesamiento: computar la tabla LPS
    lps = compute_lps(pattern)

    results = []
    i = 0  # índice para text
    j = 0  # índice para pattern

    while i < n:
        # Coincidencia de caracteres
        if pattern[j] == text[i]:
            i += 1
            j += 1

        # Si encontramos el patrón completo
        if j == m:
            results.append(i - j)
            j = lps[j - 1]
        # Si hay una no coincidencia
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    return results