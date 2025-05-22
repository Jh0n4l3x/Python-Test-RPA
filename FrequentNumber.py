from collections import Counter

def numero_mas_frecuente(lista):
    contador = Counter(lista)
    max_frecuencia = max(contador.values())
    candidatos = [num for num, freq in contador.items() if freq == max_frecuencia]
    return min(candidatos)

# Pruebas:
print("1. Numero mas frecuente: ",numero_mas_frecuente([10, 4, 4, 4, 7, 3, 2, 15,7, 7, 7, 4, 7]))
print("2. Numero mas frecuente: ",numero_mas_frecuente([4, 4, 5, 5, 5, 36, 3, 4, 2, 7, 8, 9, 6, 3, 4, 6, 6]))
