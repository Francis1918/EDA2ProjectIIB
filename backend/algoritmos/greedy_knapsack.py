# greedy_knapsack.py
def greedy_knapsack(alerts, max_capacity):
    """
    Implementa el algoritmo voraz de la mochila fraccionaria para priorizar alertas

    Args:
        alerts: lista de tuplas (valor_alerta, peso_alerta, info_alerta)
        max_capacity: capacidad máxima (ej. tiempo disponible para revisar alertas)

    Returns:
        Lista de alertas priorizadas hasta alcanzar la capacidad máxima
    """
    # Ordenar alertas por valor/peso (eficiencia) de forma descendente
    alerts_sorted = sorted(alerts, key=lambda x: x[0] / x[1], reverse=True)

    result = []
    total_value = 0
    total_weight = 0

    for alert in alerts_sorted:
        value, weight, info = alert

        if total_weight + weight <= max_capacity:
            # Si la alerta cabe completa, la incluimos
            result.append((value, weight, info, 1.0))  # 1.0 indica que se toma completa
            total_value += value
            total_weight += weight
        else:
            # Si no cabe completa, tomamos una fracción
            fraction = (max_capacity - total_weight) / weight
            if fraction > 0:
                result.append((value, weight, info, fraction))
                total_value += value * fraction
                total_weight = max_capacity
            break

    return result, total_value