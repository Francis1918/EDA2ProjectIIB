import pandas as pd
import csv


class PatronesManager:
    def __init__(self, csv_path=None):
        self.patrones = []
        if csv_path:
            self.cargar_desde_csv(csv_path)

    def cargar_desde_csv(self, csv_path):
        """Carga patrones desde un archivo CSV"""
        try:
            df = pd.read_csv(csv_path)
            self.patrones = [(row['Patrón'], row['Tipo'], row['Nivel de Severidad'])
                             for _, row in df.iterrows()]
            return True
        except Exception as e:
            print(f"Error al cargar CSV: {e}")
            return False

    def guardar_a_csv(self, csv_path):
        """Guarda patrones a un archivo CSV"""
        try:
            with open(csv_path, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["Patrón", "Tipo", "Nivel de Severidad"])
                for patron in self.patrones:
                    writer.writerow(patron)
            return True
        except Exception as e:
            print(f"Error al guardar CSV: {e}")
            return False

    def agregar_patron(self, patron, tipo, nivel):
        """Agrega un nuevo patrón a la lista"""
        self.patrones.append((patron, tipo, nivel))

    def eliminar_patron(self, indice):
        """Elimina un patrón por su índice"""
        if 0 <= indice < len(self.patrones):
            del self.patrones[indice]
            return True
        return False

    def obtener_patrones(self):
        """Retorna la lista completa de patrones"""
        return self.patrones